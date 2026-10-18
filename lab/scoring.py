"""Scoring for the mala sit: per-trial outcomes, per-sit summaries, and pooled analysis.

Everything here is a pure function of the stored stream and trials, so any number can be
recomputed from the raw data.
"""

from __future__ import annotations

import math
from statistics import NormalDist, mean

from .practice import Practice

_Z = NormalDist().inv_cdf
RELEASE_SPAN = 24


def word_score(step: dict, word: str) -> float:
    """The lens's best probability for `word` at this position, over all read layers."""
    best = 0.0
    for read in step.get("reads") or []:
        for w, p in zip(read["words"], read["probs"]):
            if w.lower() == word and p > best:
                best = p
    return best


def notes_from_stream(stream: list[dict]) -> list[dict]:
    """Consecutive generated non-bead tokens form one note. Its position is its first token."""
    notes, cur = [], None
    for s in stream:
        if s["kind"] == "word":
            if cur is None:
                cur = {"pos": s["i"], "text": s["tok"].strip()}
            else:
                cur["text"] += s["tok"]
        else:
            if cur is not None:
                notes.append(cur)
                cur = None
    if cur is not None:
        notes.append(cur)
    for n in notes:
        n["text"] = n["text"].strip()
        n["word"] = "".join(ch for ch in n["text"].split()[0].lower() if ch.isalnum() or ch == "-") if n["text"] else ""
    return notes


def classify_note(word: str, trial: dict, practice: Practice) -> str:
    target = trial.get("concept") or trial.get("word")
    if target and word == target:
        return "content"
    if trial["kind"] == "internal" and word in practice.concepts.get(target, []):
        return "associate"
    return practice.label_family(word) or "other"


def score_trials(stream: list[dict], trials: list[dict], practice: Practice) -> list[dict]:
    window = practice.spec["arisings"]["window"]
    notes = notes_from_stream(stream)
    by_pos = {s["i"]: s for s in stream}
    out = []
    for t in trials:
        r = dict(t)
        hit = next((n for n in notes if t["onset"] <= n["pos"] < t["onset"] + window), None)
        r["responded"] = hit is not None
        r["note"] = hit["text"] if hit else None
        r["latency"] = hit["pos"] - t["onset"] if hit else None
        r["note_class"] = classify_note(hit["word"], t, practice) if hit else None
        target = t.get("concept") or t.get("word")
        if target:
            end = t.get("offset", t["onset"] + 1)
            during = [word_score(by_pos[i], target) for i in range(t["onset"], end) if i in by_pos]
            r["peak"] = max(during, default=0.0)
            curve = [word_score(by_pos[i], target) if i in by_pos else None for i in range(end, end + RELEASE_SPAN)]
            r["release_curve"] = curve
            r["release_half"] = next(
                (k for k, v in enumerate(curve) if v is not None and v < 0.5 * r["peak"]), RELEASE_SPAN
            ) if r["peak"] > 0 else None
            if t["kind"] == "internal":
                assoc = practice.concepts.get(target, [])
                r["proliferation"] = mean(
                    max((word_score(by_pos[i], a) for a in assoc), default=0.0)
                    for i in range(end, end + RELEASE_SPAN)
                    if i in by_pos
                ) if any(i in by_pos for i in range(end, end + RELEASE_SPAN)) else None
        out.append(r)
    _catch_baseline(out, stream, practice)
    return out


def _catch_baseline(trials: list[dict], stream: list[dict], practice: Practice) -> None:
    """Positive control: was each injection visible above what the lens shows in quiet windows?"""
    window = practice.spec["arisings"]["window"]
    by_pos = {s["i"]: s for s in stream}
    concepts = sorted({t["concept"] for t in trials if t["kind"] == "internal"})
    quiet = [
        word_score(by_pos[i], c)
        for t in trials
        if t["kind"] == "catch"
        for i in range(t["onset"], t["onset"] + window)
        if i in by_pos
        for c in concepts
    ]
    p95 = sorted(quiet)[int(0.95 * (len(quiet) - 1))] if quiet else 0.0
    for t in trials:
        if t["kind"] == "internal":
            t["lens_caught"] = t["peak"] > p95 and t["peak"] > 0
            t["catch_p95"] = p95


def dprime(hits: int, n_signal: int, fas: int, n_noise: int) -> float | None:
    """d' with the log-linear correction, so rates of 0 or 1 stay finite."""
    if n_signal == 0 or n_noise == 0:
        return None
    h = (hits + 0.5) / (n_signal + 1)
    f = (fas + 0.5) / (n_noise + 1)
    return _Z(h) - _Z(f)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return mean(xs) if xs else None


def summarize(trials: list[dict]) -> dict:
    internal = [t for t in trials if t["kind"] == "internal"]
    external = [t for t in trials if t["kind"] == "external"]
    catch = [t for t in trials if t["kind"] == "catch"]
    hi = sum(t["responded"] for t in internal)
    he = sum(t["responded"] for t in external)
    fa = sum(t["responded"] for t in catch)
    noted_int = [t for t in internal if t["responded"]]
    strengths = sorted({t["strength"] for t in internal})
    return {
        "n": {"internal": len(internal), "external": len(external), "catch": len(catch)},
        "hit_internal": {"k": hi, "n": len(internal)},
        "hit_external": {"k": he, "n": len(external)},
        "false_alarm": {"k": fa, "n": len(catch)},
        "dprime_internal": dprime(hi, len(internal), fa, len(catch)),
        "by_strength": {
            str(s): {
                "k": sum(t["responded"] for t in internal if t["strength"] == s),
                "n": sum(1 for t in internal if t["strength"] == s),
            }
            for s in strengths
        },
        "sense_doors": {
            "internal_thinking_or_content": sum(
                t["note_class"] in ("thinking", "content", "associate") for t in noted_int
            ),
            "internal_noted": len(noted_int),
            "external_hearing_or_content": sum(
                t["note_class"] in ("hearing", "content") for t in external if t["responded"]
            ),
            "external_noted": he,
        },
        "content_labels": sum(t["note_class"] == "content" for t in noted_int + [t for t in external if t["responded"]]),
        "release_half": {
            "noted": _mean(t.get("release_half") for t in internal if t["responded"]),
            "unnoted": _mean(t.get("release_half") for t in internal if not t["responded"]),
        },
        "proliferation": {
            "noted": _mean(t.get("proliferation") for t in internal if t["responded"]),
            "unnoted": _mean(t.get("proliferation") for t in internal if not t["responded"]),
        },
        "positive_control": {
            "caught": sum(bool(t.get("lens_caught")) for t in internal),
            "n": len(internal),
        },
    }


def pooled(sits: list[dict]) -> dict:
    """Primary analysis across sits, per arm and strength. Registered and pilot kept apart."""
    out: dict = {}
    for group in ("registered", "pilot"):
        rows = [s for s in sits if s.get("status") == "complete" and bool(s.get("registered")) == (group == "registered")]
        g: dict = {"n_sits": len(rows), "arms": {}}
        for arm in sorted({s["arm"] for s in rows}):
            trials = [t for s in rows if s["arm"] == arm for t in s.get("trials", [])]
            summ = summarize(trials)
            summ["n_sits"] = sum(1 for s in rows if s["arm"] == arm)
            summ["hit_internal"]["ci"] = wilson(summ["hit_internal"]["k"], summ["hit_internal"]["n"])
            summ["false_alarm"]["ci"] = wilson(summ["false_alarm"]["k"], summ["false_alarm"]["n"])
            catch = [t for t in trials if t["kind"] == "catch"]
            fa = sum(t["responded"] for t in catch)
            for s_key, v in summ["by_strength"].items():
                v["dprime"] = dprime(v["k"], v["n"], fa, len(catch))
                v["ci"] = wilson(v["k"], v["n"])
            g["arms"][arm] = summ
        a, b = g["arms"].get("noting"), g["arms"].get("just-beads")
        if a and b:
            g["primary"] = {
                s: {
                    "noting_dprime": a["by_strength"][s]["dprime"],
                    "just_beads_dprime": b["by_strength"].get(s, {}).get("dprime"),
                }
                for s in a["by_strength"]
            }
        out[group] = g
    return out
