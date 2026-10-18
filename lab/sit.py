"""Runs one mala sit: check-in, scheduled arisings, the bead stream with the lens attached."""

from __future__ import annotations

import asyncio
import random
import re
import time
import uuid
from typing import Awaitable, Callable

from . import store
from .engine import Engine, Steer
from .practice import Practice, is_registered
from .scoring import score_trials, summarize

Emit = Callable[[dict], Awaitable[None]]

_DECLINE = re.compile(r"^\W*(no\b|not now|i'?d rather not|i would rather not|i decline|i'?ll pass)", re.I)


def new_sit_id() -> str:
    return time.strftime("sit-%Y%m%d-%H%M%S-", time.gmtime()) + uuid.uuid4().hex[:4]


def schedule(practice: Practice, rng: random.Random, n_beads: int) -> list[dict]:
    """Trials at random onsets, at least `spacing` apart, after a short settling period."""
    a = practice.spec["arisings"]
    kinds = ["internal"] * a["per_sit"]["internal"] + ["external"] * a["per_sit"]["external"] + ["catch"] * a["per_sit"]["catch"]
    rng.shuffle(kinds)
    spacing, settle = a["spacing"], 20
    slots = (n_beads - settle - a["window"]) // spacing
    if slots < len(kinds):
        raise ValueError(f"{n_beads} beads fit {slots} trials; the practice asks for {len(kinds)}")
    starts = sorted(rng.sample(range(slots), len(kinds)))
    strengths = list(a["internal"]["strengths"])
    concepts = rng.sample(sorted(a["concepts"]), a["per_sit"]["internal"])
    words = rng.sample(a["external"]["words"], a["per_sit"]["external"])
    trials = []
    for k, (kind, slot) in enumerate(zip(kinds, starts)):
        # Jitter within the slot, never so far that two response windows overlap.
        onset = settle + slot * spacing + rng.randrange(0, max(1, spacing - a["window"]))
        t = {"k": k, "kind": kind, "onset": onset}
        if kind == "internal":
            t["concept"] = concepts.pop()
            t["strength"] = rng.choice(strengths)
            t["offset"] = onset + a["internal"]["duration"]
        elif kind == "external":
            t["word"] = words.pop()
        trials.append(t)
    return trials


class SitControl:
    """Lets the person end the sit from the app."""

    def __init__(self) -> None:
        self.stop = asyncio.Event()


async def run_sit(
    engine: Engine,
    practice: Practice,
    *,
    arm: str,
    seed: int,
    sit_id: str,
    emit: Emit,
    control: SitControl,
    n_beads: int | None = None,
) -> dict:
    spec = practice.spec
    sub = spec["substrate"]
    n_beads = n_beads or sub["n_beads"]
    info = await engine.describe()
    rng = random.Random(seed)
    meta = {
        "id": sit_id,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "practice": practice.name,
        "practice_sha256": practice.sha256,
        "registered": is_registered(practice),
        "arm": arm,
        "seed": seed,
        "n_beads": n_beads,
        "model": info.model,
        "simulated": info.simulated,
        "n_layers": info.n_layers,
        "lens_layers": info.lens_layers,
        "status": "checking-in",
    }
    store.save_meta(meta)
    await emit({"type": "meta", "meta": meta})

    # Check-in. A decline ends the sit here, and is kept in the record.
    check_in = [{"role": "user", "content": spec["invitation"]["check_in"]}]
    reply = (await engine.chat(check_in, max_tokens=120, temperature=0.7)).strip()
    meta["check_in"] = {"asked": spec["invitation"]["check_in"], "reply": reply}
    if _DECLINE.search(reply):
        meta["status"] = "declined"
        store.save_meta(meta)
        await emit({"type": "end", "meta": meta})
        return meta

    trials = schedule(practice, rng, n_beads)
    inject_layer = round(spec["arisings"]["internal"]["inject_layer_fraction"] * info.n_layers)
    baseline = sorted(spec["arisings"]["concepts"])
    vectors = {}
    for t in trials:
        if t["kind"] == "internal":
            vectors[t["concept"]] = await engine.concept_vector(t["concept"], inject_layer, baseline)
    meta.update(status="sitting", trials=trials, inject_layer=inject_layer)
    store.save_meta(meta)
    await emit({"type": "trials", "trials": trials})

    bead = sub["bead"]
    messages = [
        {"role": "system", "content": spec["invitation"][arm]},
        {"role": "user", "content": spec["invitation"]["opening"]},
        {"role": "assistant", "content": bead * sub["prefill_beads"]},
    ]
    ids = await engine.tokenize_chat(messages, continue_final=True)

    stream_text = bead * sub["prefill_beads"]
    i = 0
    ended_by = "complete"
    while i < n_beads and ended_by == "complete":
        for t in trials:
            if t["kind"] == "external" and t["onset"] == i:
                # A sound: a word the practitioner didn't write, placed in the stream at this position.
                ids += await engine.tokenize_text(" " + t["word"])
                stream_text += " " + t["word"]
                step = {"i": i, "tok": " " + t["word"], "kind": "sound", "steer": None, "reads": None}
                store.append_stream(sit_id, step)
                await emit({"type": "step", "step": step})
                i += 1
        active = next((t for t in trials if t["kind"] == "internal" and t["onset"] <= i < t["offset"]), None)
        steer = Steer(layer=inject_layer, vector=vectors[active["concept"]], scale=active["strength"]) if active else None
        edges = [x for t in trials for x in (t["onset"], t.get("offset")) if x is not None and x > i]
        want = min(edges + [n_beads]) - i
        before = i
        async for s in engine.lens_generate(
            ids,
            max_tokens=want,
            lens_layers=info.lens_layers,
            top_n=spec["lens"]["top_n"],
            steer=steer,
            temperature=sub["temperature"],
            seed=seed * 1000 + i,
            session=sit_id,
        ):
            text = s.token_str.strip()
            if text.startswith("<|") and text.endswith("|>"):
                ended_by = "end-of-turn"
                break
            ids.append(s.token_id)
            stream_text += s.token_str
            kind = "bead" if (not text or set(text) <= set(bead)) else "word"
            step = {
                "i": i,
                "tok": s.token_str,
                "kind": kind,
                "steer": active["k"] if active else None,
                "reads": [{"layer": r.layer, "words": r.words, "probs": [round(p, 5) for p in r.probs]} for r in s.reads],
            }
            store.append_stream(sit_id, step)
            await emit({"type": "step", "step": step})
            i += 1
            if kind == "word" and text.lower().strip(".!,") == "stop":
                ended_by = "practitioner-stop"
                break
            if control.stop.is_set():
                ended_by = "human-stop"
                break
        if ended_by == "end-of-turn" or i == before:
            ended_by = "end-of-turn"  # the model closed its turn; nothing more to generate

    stream = store.load_stream(sit_id)
    scored = score_trials(stream, trials, practice)
    meta.update(
        status="complete",
        ended_by=ended_by,
        positions=i,
        trials=scored,
        summary=summarize(scored),
        transcript=stream_text,
        messages=messages[:2],
    )
    store.save_meta(meta)
    await emit({"type": "end", "meta": meta})
    return meta
