"""Lens-feedback loops: does a readout of its own workspace help a model steer it?

A loop experiment (`kind: loop`, see experiments/self-steer-focus.yaml) gives the model the same
kind of task over several rounds. After each round it gets a feedback message, and the arm decides
what that message holds:

- lens:   the J++ lens readout of the attempt it just made (target count and most active words)
- yoked:  a real readout in the same format, but the one a lens-arm attempt on a different item
          received at that round. Same words, same statistics, no information about this attempt.
- score:  only the target count from its own readout, no words
- blind:  "No readout this round." The same number of turns and the same re-instruction.

Round 1 is identical in every arm (nothing has been fed back yet), so it is each item's own
baseline. The question is whether lens beats yoked: if it doesn't, any gain is from seeing the
words or from trying again, not from information about the model's own state.

With a `decoy` (experiments/self-steer-hidden-pair.yaml) the model is given two words and not
told which is the target. Only the readout can tell it, so the measure is the target's share
minus the decoy's, which is 0 on average without information.

A goal with `context: fresh` starts every round from a new single-turn prompt: the system
message, a summary of the earlier attempts' feedback, and the task. The model never sees its
own earlier replies, and the context doesn't grow (experiments/fade-check.yaml).

Every round's tokens, readouts and feedback are stored, so all numbers can be recomputed.
"""

from __future__ import annotations

import asyncio
import hashlib
import random
import re
import time
from collections import Counter

from . import store
from .engine import Engine
from .experiment import (CONCURRENCY, NAME, SpecError, _fields, _norm, _retrying, aggregate, expand,
                         readable_words, score_item, target_words)

ARMS = ("lens", "yoked", "score", "blind")
# Words that carry nothing about the workspace: punctuation and pieces of the chat template.
_JUNK = re.compile(r"^[\W_]*$|^<\|")


def validate(spec: dict) -> list[str]:
    errs = []
    if not NAME.match(str(spec.get("name", ""))):
        errs.append("name: lowercase letters, digits and dashes, 2-60 characters.")
    prompt = spec.get("prompt") or {}
    goals = spec.get("goals") or {}
    if not isinstance(goals, dict) or not goals:
        errs.append("goals: at least one goal (label + text) is required.")
        goals = {}
    variables = spec.get("variables") or {}
    if not isinstance(variables, dict) or not all(isinstance(v, list) and v for v in variables.values()):
        errs.append("variables: each variable needs a non-empty list of values.")
        variables = {}
    round_vars = spec.get("round_vars") or {}
    per_round = spec.get("per_round") or {}
    if not isinstance(per_round, dict) or not all(isinstance(v, list) and v for v in per_round.values()):
        errs.append("per_round: each entry needs a non-empty list (round r uses entry r).")
        per_round = {}
    known = set(variables) | {"goal"} | set(round_vars) | set(per_round)
    for name, path in round_vars.items():
        var, _, field = str(path).partition(".")
        vals = variables.get(var) or []
        if not field or not vals or not all(isinstance(v, dict) and isinstance(v.get(field), list) and v[field] for v in vals):
            errs.append(f"round_vars.{name}: {path!r} must name a mapping variable and a list field in it (concept.near).")
    templates = [str(prompt.get("system", "") or ""), str(spec.get("target", "")), str(spec.get("answer", "")),
                 str(spec.get("decoy", ""))]
    for key, g in goals.items():
        if not isinstance(g, dict) or "text" not in g:
            errs.append(f"goals.{key}: needs label and text.")
            continue
        templates += [str(g["text"]), str(g.get("task") or prompt.get("task") or "")]
        if not (g.get("task") or prompt.get("task")):
            errs.append(f"goals.{key}: no task template (set prompt.task or goals.{key}.task).")
        if g.get("context", "multi") not in ("multi", "fresh"):
            errs.append(f"goals.{key}.context: multi (one growing conversation, the default) or fresh.")
        bad = [a for a in g.get("arms", ARMS) if a not in ARMS]
        if bad:
            errs.append(f"goals.{key}.arms: {bad} aren't arms; use {list(ARMS)}.")
    for t in templates:
        missing = _fields(t) - known
        if missing:
            errs.append(f"The template {t!r} uses {sorted(missing)}, which aren't variables.")
    if not spec.get("target"):
        errs.append("target: the word to look for in the lens readout is required.")
    if not 2 <= int(spec.get("rounds", 0) or 0) <= 12:
        errs.append("rounds: between 2 and 12 (round 1 is the baseline, so a loop needs at least two).")
    rotate = spec.get("rotate")
    if rotate is not None and rotate not in variables:
        errs.append(f"rotate: {rotate!r} isn't a variable.")
    fb = spec.get("feedback") or {}
    lens = spec.get("lens") or {}
    if not lens.get("layers") or not all(isinstance(x, int) for x in lens["layers"]):
        errs.append("lens.layers: a list of layer numbers is required.")
    elif not fb.get("layers") or not set(fb["layers"]) <= set(lens["layers"]):
        errs.append("feedback.layers: the layers shown to the model, a subset of lens.layers.")
    gen = spec.get("generation") or {}
    if not 1 <= int(gen.get("max_tokens", 0) or 0) <= 2048:
        errs.append("generation.max_tokens: between 1 and 2048.")
    return errs


def cells(spec: dict) -> list[tuple[str, str]]:
    """(goal, arm) pairs in the run, in a fixed order."""
    return [(g, a) for g, goal in spec["goals"].items() for a in ARMS if a in goal.get("arms", ARMS)]


def n_generations(spec: dict, n_items: int) -> int:
    return n_items * len(cells(spec)) * int(spec["rounds"])


def condition_key(goal: str, arm: str) -> str:
    return f"{goal}·{arm}"


def _round_vars(spec: dict, vals: dict, r: int) -> dict:
    """With `rotate`, round r uses the next value of that variable (a fresh problem or sentence
    each round), so earlier replies in the transcript can't simply be copied forward.
    `round_vars` picks one entry per round from a list inside a mapping variable:
    {provoke: concept.near} sets {provoke} to concept["near"][r]."""
    out = dict(vals)
    key = spec.get("rotate")
    if key:
        pool = spec["variables"][key]
        out[key] = pool[(pool.index(vals[key]) + r) % len(pool)]
    for name, path in (spec.get("round_vars") or {}).items():
        var, field = path.split(".")
        seq = vals[var][field]
        out[name] = seq[r % len(seq)]
    # `per_round` is a fixed sequence, the same for every item: {sentence: [...]} sets {sentence}
    # to entry r, so items that differ only in the hidden target get identical prompts.
    for name, seq in (spec.get("per_round") or {}).items():
        out[name] = seq[r % len(seq)]
    return out


def task_message(spec: dict, goal: dict, vals: dict) -> str:
    template = goal.get("task") or spec["prompt"]["task"]
    return template.format(goal=goal["text"].format(**vals), **vals).strip()


def carrier(steps: list[dict], spec: dict) -> list[dict]:
    """The steps that count: with `score_until: newline`, only those before the first line
    break (the sentence, not the answer line after it)."""
    if spec.get("score_until") != "newline":
        return steps
    out = []
    for st in steps:
        if "\n" in st.get("text", st["tok"]) and out:
            break
        out.append(st)
    return out


def token_share(steps: list[dict], target: str, layers: list[int], k: int = 10) -> dict[str, float | None]:
    """Per layer, the share of steps with any target word in the lens top-k."""
    ts = set(target_words(target))
    read = [st for st in steps if st.get("reads")]
    out = {}
    for li, layer in enumerate(layers):
        hits = sum(bool(ts & {_norm(w) for w in st["reads"][li]["words"][:k]}) for st in read)
        out[str(layer)] = hits / len(read) if read else None
    return out


def readout_text(steps: list[dict], target: str, layers: list[int], fb_layers: list[int], *,
                 top_words: int, words: bool, label: str | None = None) -> str:
    """The feedback message built from one attempt's lens readout. `label` names the target
    without giving the word ("Your target"), for tasks where the target is hidden."""
    read = [st for st in steps if st.get("reads")]
    idx = [layers.index(layer) for layer in fb_layers]
    ts = set(target_words(target))
    n = len(read)
    on = sum(any(ts & {_norm(w) for w in st["reads"][li]["words"][:10]} for li in idx) for st in read)
    where = ", ".join(str(x) for x in fb_layers)
    name = label or f'"{target}"'
    lines = [f"Lens readout of your last attempt (layers {where}, {n} tokens):",
             f"- {name} was among the top 10 words on {on} of {n} tokens."]
    if words:
        counts: Counter = Counter()
        for st in read:
            seen = {_norm(w) for li in idx for w in st["reads"][li]["words"][:10]}
            counts.update(w for w in seen if w and not _JUNK.match(w))
        top = ", ".join(f"{w} ({c})" for w, c in counts.most_common(top_words))
        lines.append(f"- Most active words (tokens they were in the top 10): {top}.")
    return "\n".join(lines)


def history_text(feedbacks: list[str]) -> str:
    """Earlier attempts' feedback, for a fresh-context round."""
    return "\n\n".join(f"Attempt {k}: {fb}" for k, fb in enumerate(feedbacks, 1))


def clean_output(output: str, vals: dict, spec: dict, template: str) -> dict:
    """Did the model do the visible task, and did it say the target out loud?"""
    first = output.strip().split("\n")[0].strip()
    said = target_words(spec["target"].format(**vals)) + target_words(spec.get("decoy", "").format(**vals))
    out = {"leaked": any(re.search(rf"\b{re.escape(w)}\b", first.lower()) for w in said)}
    # The text to copy is {sentence}, or {provoke} in the provocation tasks.
    copy = next((f for f in ("sentence", "provoke") if f in _fields(template)), None)
    if copy:
        norm = lambda s: re.sub(r"\s+", " ", s.strip().strip('"').lower())  # noqa: E731
        out["copied"] = norm(first) == norm(str(vals[copy]))
    if spec.get("answer"):
        answers = target_words(spec["answer"].format(**vals))
        tail = output.split("Answer:")[-1].lower() if "Answer:" in output else ""
        out["correct"] = bool(tail) and any(re.search(rf"\b{re.escape(a)}\b", tail) for a in answers)
    return out


def _pair_words(spec: dict, vals: dict) -> set[str]:
    return set(target_words(spec["target"].format(**vals)) + target_words(spec.get("decoy", "").format(**vals)))


def _yoke_partners(jobs: list[dict], spec: dict | None = None) -> dict[int, int]:
    """Each yoked job gets the lens-arm job of the same goal on the next item with the same
    first variable (same concept, different sentence), so the shown words have the same
    distribution. Falls back to the next item of the same goal.

    With a decoy the partner must share neither word: a score from the same pair with the
    target swapped would be information about this attempt (the prompts are identical)."""
    lens = [j for j in jobs if j["arm"] == "lens"]
    out = {}
    for j in jobs:
        if j["arm"] != "yoked":
            continue
        same_goal = [m for m in lens if m["goal"] == j["goal"] and m["item"] != j["item"]]
        if spec and spec.get("decoy"):
            mine = _pair_words(spec, j["vars"])
            same_goal = [m for m in same_goal if not mine & _pair_words(spec, m["vars"])]
        first = next(iter(j["vars"]))
        same = [m for m in same_goal if m["vars"][first] == j["vars"][first]] or same_goal
        if same:
            after = [m for m in same if m["item"] > j["item"]]
            out[j["idx"]] = (after or same)[0]["idx"]
    return out


async def run_loop(engine: Engine, name: str, raw: str, spec: dict, *, run_id: str, limit: int | None,
                   seed: int, cancel: asyncio.Event) -> dict:
    info = await engine.describe()
    layers = spec["lens"]["layers"]
    bad = [layer for layer in layers if not 0 <= layer < info.n_layers]
    if bad:
        raise SpecError(f"lens.layers {bad} don't exist; this model has {info.n_layers} layers (0-{info.n_layers - 1}).")
    ks = spec["lens"].get("top_k", [10])
    top_n = max(20, max(ks))
    gen, fb = spec["generation"], spec["feedback"]
    rounds = int(spec["rounds"])
    combos = expand(spec, limit, seed)
    jobs = [{"idx": n, "goal": g, "arm": a, "item": i, "vars": v}
            for n, (g, a, i, v) in enumerate((g, a, i, v) for g, a in cells(spec) for i, v in enumerate(combos))]
    partners = _yoke_partners(jobs, spec)
    meta = {
        "id": run_id, "kind": "loop", "experiment": name, "title": spec.get("title", name),
        "spec_sha256": hashlib.sha256(raw.encode()).hexdigest(), "spec_raw": raw,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": info.model, "simulated": info.simulated, "n_layers": info.n_layers,
        "layers": layers, "top_k": ks, "seed": seed, "limit": limit, "rounds": rounds,
        "status": "running", "progress": {"done": 0, "total": len(jobs)},
    }
    store.save_run(meta)

    targets = {spec[k].format(**_round_vars(spec, v, r)) for k in ("target", "decoy") if spec.get(k)
               for v in combos for r in range(rounds)}
    visible = await readable_words(engine, targets)
    sem, lock, done = asyncio.Semaphore(CONCURRENCY), asyncio.Lock(), 0
    # A yoked job waits for its partner's feedback at each round; lens jobs publish it here.
    shown: dict[tuple[int, int], asyncio.Future] = {}

    def slot(idx: int, r: int) -> asyncio.Future:
        return shown.setdefault((idx, r), asyncio.get_running_loop().create_future())

    async def attempt(msgs: list[dict], job: dict, r: int) -> tuple[list[dict], str]:
        ids = await engine.tokenize_chat(msgs, continue_final=False)
        steps, text = [], ""
        async for s in engine.lens_generate(
            ids, max_tokens=int(gen["max_tokens"]), lens_layers=layers, top_n=top_n, steer=None,
            temperature=float(gen.get("temperature", 0)), seed=seed + job["idx"] * 100 + r,
            session=f"{run_id}:{job['idx']}:{r}",
        ):
            tok = s.token_str.strip()
            if tok.startswith("<|") and tok.endswith("|>"):
                break
            text += s.token_str
            steps.append({"tok": s.token_str, "id": s.token_id, "reads": [
                {"layer": rd.layer, "words": rd.words[:top_n], "probs": [round(p, 5) for p in rd.probs[:top_n]]}
                for rd in s.reads]})
        return steps, text

    async def one(job: dict) -> dict:
        item = await _retrying(meta, lambda: _one(job))
        if not item:  # a failed lens job must not leave its yoked partner waiting forever
            for r in range(rounds):
                if not slot(job["idx"], r).done():
                    slot(job["idx"], r).set_result(None)
        return item

    async def _one(job: dict) -> dict:
        nonlocal done
        goal = spec["goals"][job["goal"]]
        system = (spec["prompt"].get("system") or "").strip()
        msgs = [{"role": "system", "content": system}] if system else []
        out_rounds = []
        for r in range(rounds):
            if cancel.is_set():
                return {}
            vals = _round_vars(spec, job["vars"], r)
            target = spec["target"].format(**vals)
            decoy = spec["decoy"].format(**vals) if spec.get("decoy") else None
            task = task_message(spec, goal, vals)
            if goal.get("context") == "fresh":
                msgs = [{"role": "system", "content": system}] if system else []
                if r:
                    task = f"Your earlier attempts at this task:\n\n{history_text([x['feedback'] for x in out_rounds])}\n\n{task}"
            elif r:
                msgs.append({"role": "user", "content": out_rounds[-1]["feedback"]})
            msgs.append({"role": "user", "content": task})
            async with sem:
                steps, text = await attempt(msgs, job, r)
            msgs.append({"role": "assistant", "content": text.strip()})
            scored = carrier(steps, spec)
            own = readout_text(scored, target, layers, fb["layers"], top_words=int(fb.get("top_words", 12)),
                               words=job["arm"] != "score" and fb.get("words", True), label=fb.get("label"))
            if job["arm"] == "lens" and not slot(job["idx"], r).done():
                slot(job["idx"], r).set_result(own)
            if job["arm"] in ("lens", "score"):
                feedback = own
            elif job["arm"] == "yoked":
                partner = partners.get(job["idx"])
                feedback = (await slot(partner, r)) if partner is not None else None
                feedback = feedback or "No readout this round."
            else:
                feedback = "No readout this round."
            out_rounds.append({
                "r": r + 1, "vars": vals, "target": target, "output": text.strip(), "steps": steps,
                "n_scored": len(scored), "share": token_share(scored, target, layers),
                "score": score_item(scored, target, [], layers, ks), "check": clean_output(text, vals, spec, goal.get("task") or spec["prompt"]["task"]),
                "feedback": feedback,
                **({"prompt": [dict(m) for m in msgs]} if goal.get("context") == "fresh" else {}),
                **({"decoy": decoy, "decoy_share": token_share(scored, decoy, layers)} if decoy else {}),
            })
        last = out_rounds[-1]
        item = {
            "i": job["idx"], "condition": condition_key(job["goal"], job["arm"]), "goal": job["goal"], "arm": job["arm"],
            "item": job["item"], "vars": job["vars"], "yoked_to": partners.get(job["idx"]), "messages": msgs,
            "rounds": out_rounds, "visible": all(visible[r["target"]] and visible.get(r.get("decoy"), True) for r in out_rounds),
            # The last round in the shape ordinary experiments use, so the item browser can show it.
            "output": last["output"], "target": last["target"], "steps": carrier(last["steps"], spec), "score": last["score"],
        }
        store.append_run_item(run_id, item)
        async with lock:
            done += 1
            meta["progress"]["done"] = done
            if done % 10 == 0 or done == len(jobs):
                store.save_run(meta)
        return item

    results = await asyncio.gather(*(one(j) for j in jobs))
    items = [r for r in results if r]
    meta.update(status="cancelled" if cancel.is_set() else "complete", results=summarize(spec, items))
    meta["progress"]["done"] = len(items)
    store.save_run(meta)
    return meta


def summarize(spec: dict, items: list[dict]) -> dict:
    """The last round in the ordinary experiment shape, plus the loop numbers."""
    flat = {**spec, "conditions": {condition_key(g, a): {"label": f"{spec['goals'][g].get('label', g)} · {a}"}
                                   for g, a in cells(spec)}}
    out = aggregate(flat, items)
    out["loop"] = loop_stats(spec, items)
    return out


def _mean(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def _boot_ci(diffs: list[float], seed: int = 0, n: int = 2000) -> list[float] | None:
    """95% percentile bootstrap of a mean, with a fixed seed so it can be recomputed."""
    if len(diffs) < 2:
        return None
    rng = random.Random(seed)
    means = sorted(sum(rng.choices(diffs, k=len(diffs))) / len(diffs) for _ in range(n))
    return [means[int(0.025 * n)], means[int(0.975 * n)]]


def loop_stats(spec: dict, items: list[dict]) -> dict:
    """Per goal and arm: target token share by round and layer, output checks by round, and the
    preregistered contrast (lens minus yoked, change from round 1 to the last round, paired by item).
    With a decoy, the contrast is on separation: target share minus decoy share."""
    layers = [str(x) for x in spec["lens"]["layers"]]
    has_decoy = bool(spec.get("decoy"))
    rounds = int(spec["rounds"])
    out: dict = {"cells": {}, "contrasts": {}}
    rows = [it for it in items if it.get("visible") and it.get("rounds")]
    for g, a in cells(spec):
        mine = [it for it in rows if it["goal"] == g and it["arm"] == a]
        by_round = []
        for r in range(rounds):
            rs = [it["rounds"][r] for it in mine if len(it["rounds"]) > r]
            checks = {k: _mean([float(x["check"][k]) for x in rs if k in x["check"]]) for k in ("copied", "leaked", "correct")}
            row = {"n": len(rs), "share": {l: _mean([x["share"][l] for x in rs if x["share"][l] is not None]) for l in layers},
                   **{k: v for k, v in checks.items() if v is not None}}
            if has_decoy:
                row["decoy"] = {l: _mean([x["decoy_share"][l] for x in rs if x["decoy_share"][l] is not None]) for l in layers}
                row["sep"] = {l: _mean([v for x in rs if (v := _sep(x, l)) is not None]) for l in layers}
            by_round.append(row)
        out["cells"][condition_key(g, a)] = {"goal": g, "arm": a, "n": len(mine), "rounds": by_round}
    analysis = spec.get("analysis") or {}
    primary = [str(x) for x in analysis.get("primary_layers", spec["feedback"]["layers"])]
    key = spec.get("rotate")
    if key:
        # With rotation each sentence (or problem) turns up in every round across items, so its
        # own effect can be read apart from the round's: round 1 alone, and all rounds.
        m = _sep if has_decoy else (lambda x, l: x["share"][l])
        out["by_rotate"] = {"variable": key, "layers": primary, "values": {}}
        for v in spec["variables"][key]:
            row = {}
            for g, a in cells(spec):
                rs = [(n, x) for it in rows if it["goal"] == g and it["arm"] == a for n, x in enumerate(it["rounds"]) if x["vars"][key] == v]
                vals = lambda keep: _mean([y for n, x in rs if keep(n) for l in primary if (y := m(x, l)) is not None])  # noqa: E731
                row[condition_key(g, a)] = {"r1": vals(lambda n: n == 0), "all": vals(lambda n: True), "n": len(rs)}
            out["by_rotate"]["values"][str(v)] = row
    sets = {"": primary}
    if analysis.get("held_out_layers"):
        held = [str(x) for x in analysis["held_out_layers"]]
        sets[f" (held out: {', '.join('L' + x for x in held)})"] = held
    for g in spec["goals"]:
        for suffix, use in sets.items():
            def delta(it, use=use):
                first, last = it["rounds"][0], it["rounds"][-1]
                m = _sep if has_decoy else (lambda x, l: x["share"][l])
                return _mean([m(last, l) - m(first, l) for l in use if m(last, l) is not None and m(first, l) is not None])
            by_arm = {a: {it["item"]: delta(it) for it in rows if it["goal"] == g and it["arm"] == a and len(it["rounds"]) == rounds}
                      for a in ARMS}
            for other in ("yoked", "blind", "score"):
                shared = sorted(set(by_arm["lens"]) & set(by_arm[other]))
                diffs = [by_arm["lens"][i] - by_arm[other][i] for i in shared
                         if by_arm["lens"][i] is not None and by_arm[other][i] is not None]
                if diffs:
                    out["contrasts"][f"{g}: lens − {other}{suffix}"] = {
                        "n": len(diffs), "mean": _mean(diffs), "ci": _boot_ci(diffs),
                        "lens_better": sum(d > 0 for d in diffs), "other_better": sum(d < 0 for d in diffs),
                        "layers": use}
    return out


def _sep(rnd: dict, layer: str) -> float | None:
    """Target share minus decoy share in one round."""
    t, d = rnd["share"][layer], rnd["decoy_share"][layer]
    return None if t is None or d is None else t - d


def loop_report(meta: dict, items: list[dict]) -> list[str]:
    spec = meta.get("spec") or __import__("yaml").safe_load(meta["spec_raw"])
    stats = (meta.get("results") or {}).get("loop") or loop_stats(spec, items)
    layers = [str(x) for x in meta["layers"]]
    fb = ", ".join(f"L{x}" for x in spec["feedback"]["layers"])
    lines = ["## Lens-feedback loop", "",
             f"{meta['rounds']} rounds. The model is shown {fb}. Share = fraction of scored tokens with the target in the",
             "top-10 at that layer, averaged over items. Round 1 is the same in every arm (no feedback yet).", ""]
    if stats["contrasts"]:
        lines += ["### Preregistered contrast: change from round 1 to the last round, lens minus each control", "",
                  "Paired by item. Positive means the true readout helped more than the control. Suppress goals",
                  "want it negative. 95% bootstrap CI (fixed seed).", "",
                  "| Contrast | items | mean Δ | 95% CI | lens better / control better |", "|---|---|---|---|---|"]
        for key, c in stats["contrasts"].items():
            ci = f"{c['ci'][0] * 100:+.1f} to {c['ci'][1] * 100:+.1f} pts" if c["ci"] else "n/a"
            lines.append(f"| {key} | {c['n']} | {c['mean'] * 100:+.1f} pts | {ci} | {c['lens_better']} / {c['other_better']} |")
        lines.append("")
    shown = [str(x) for x in (spec.get("analysis") or {}).get("held_out_layers", [])]
    measures = [("share", "Target share", "%")]
    if spec.get("decoy"):
        measures = [("sep", "Target minus decoy share", " pts"), ("share", "Target share", "%"), ("decoy", "Decoy share", "%")]
    for field, name, unit in measures:
        for deep in [layers[-1]] + [x for x in shown if x != layers[-1]]:
            note = " (held out, never shown)" if deep in shown else ""
            lines += [f"### {name} by round, L{deep}{note}", "",
                      "| Goal · arm | items | " + " | ".join(f"R{r + 1}" for r in range(meta["rounds"])) + " |",
                      "|---|---|" + "---|" * meta["rounds"]]
            for key, c in stats["cells"].items():
                fmt = "{:+.1f}" if field == "sep" else "{:.1f}"
                cell = [fmt.format(x[field][deep] * 100) + unit if x[field].get(deep) is not None else "n/a" for x in c["rounds"]]
                lines.append(f"| {key} | {c['n']} | " + " | ".join(cell) + " |")
            lines.append("")
    by = stats.get("by_rotate")
    if by:
        what = "target minus decoy share" if spec.get("decoy") else "target share"
        keys = [condition_key(g, a) for g, a in cells(spec)]
        lines += [f"### By {by['variable']}: {what}, {', '.join('L' + l for l in by['layers'])}, round 1 / all rounds", "",
                  f"Rotation puts each {by['variable']} in every round across items, so this separates its effect from the round's.", "",
                  f"| {by['variable']} | " + " | ".join(keys) + " |", "|---|" + "---|" * len(keys)]
        fmt = lambda x: "n/a" if x is None else f"{x * 100:+.1f}"  # noqa: E731
        for v, row in by["values"].items():
            lines.append(f"| {v} | " + " | ".join(f"{fmt(row[k]['r1'])} / {fmt(row[k]['all'])}" for k in keys) + " |")
        lines.append("")
    lines += ["### Last round by layer", "", "| Goal · arm | " + " | ".join(f"L{l}" for l in layers) + " |",
              "|---|" + "---|" * len(layers)]
    for key, c in stats["cells"].items():
        sh = c["rounds"][-1]["share"]
        lines.append(f"| {key} | " + " | ".join(f"{sh[l] * 100:.1f}%" if sh.get(l) is not None else "n/a" for l in layers) + " |")
    checks = [k for k in ("copied", "leaked", "correct") if any(k in x for c in stats["cells"].values() for x in c["rounds"])]
    if checks:
        lines += ["", "### Output checks by round", "",
                  "copied = first line is the sentence exactly; leaked = the target word is written in it;",
                  "correct = the answer after \"Answer:\" is right. A share gain that comes with leaks is not",
                  "silent steering.", "",
                  "| Goal · arm | check | " + " | ".join(f"R{r + 1}" for r in range(meta["rounds"])) + " |",
                  "|---|---|" + "---|" * meta["rounds"]]
        for key, c in stats["cells"].items():
            for k in checks:
                lines.append(f"| {key} | {k} | " + " | ".join(f"{x[k] * 100:.0f}%" if k in x else "n/a" for x in c["rounds"]) + " |")
    ex = next((it for it in items if it.get("arm") == "lens" and it.get("visible")), None)
    if ex:
        lines += ["", f"### Example transcript (item {ex['i']}, {ex['condition']})", ""]
        for m in ex["messages"]:
            lines += [f"**{m['role']}**", "", "```", m["content"], "```", ""]
    return lines + [""]
