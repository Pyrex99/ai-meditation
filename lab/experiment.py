"""Prompted lens experiments: conditions x items, generate, read the lens, score per layer.

An experiment is a YAML spec (see experiments/directed-modulation.yaml). Each condition fills
the prompt template with every combination of the variables. The run generates the model's
reply with the lens attached and asks, per layer, whether the target word reached the lens
top-k at any generated token.
"""

from __future__ import annotations

import asyncio
import hashlib
import itertools
import random
import re
import string
import time
import uuid
from pathlib import Path

import yaml

from . import store
from .engine import Engine, Steer
from .scoring import wilson

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = ROOT / "experiments"
NAME = re.compile(r"^[a-z0-9][a-z0-9-]{1,60}$")
CONCURRENCY = 8


class SpecError(ValueError):
    pass


def _fields(template: str) -> set[str]:
    return {f for _, f, _, _ in string.Formatter().parse(template) if f}


def validate(spec: dict) -> list[str]:
    """Problems with a spec, in plain words. Empty means it can run."""
    errs = []
    if not isinstance(spec, dict):
        return ["The spec must be a YAML mapping."]
    if spec.get("kind") == "readout":
        return _validate_readout(spec)
    if not NAME.match(str(spec.get("name", ""))):
        errs.append("name: lowercase letters, digits and dashes, 2-60 characters.")
    prompt = spec.get("prompt") or {}
    if not prompt.get("user"):
        errs.append("prompt.user: the user message template is required.")
    conds = spec.get("conditions") or {}
    if not isinstance(conds, dict) or not conds:
        errs.append("conditions: at least one condition is required.")
    variables = spec.get("variables") or {}
    if not isinstance(variables, dict) or not all(isinstance(v, list) and v for v in variables.values()):
        errs.append("variables: each variable needs a non-empty list of values.")
        variables = {}
    known = set(variables) | {"instruction"}
    templates = [prompt.get("user", ""), prompt.get("system", "") or "", str(spec.get("target", ""))]
    for key, c in conds.items() if isinstance(conds, dict) else []:
        if not isinstance(c, dict):
            errs.append(f"conditions.{key}: needs label and instruction.")
            continue
        templates.append(str(c.get("instruction", "")))
        steer = c.get("steer")
        if steer is not None:
            if not isinstance(steer, dict) or "concept" not in steer or "strength" not in steer:
                errs.append(f"conditions.{key}.steer: needs concept and strength (layer optional).")
            else:
                templates.append(str(steer["concept"]))
    for t in templates:
        missing = _fields(t) - known
        if missing:
            errs.append(f"The template {t!r} uses {sorted(missing)}, which aren't variables.")
    if not spec.get("target"):
        errs.append("target: the word to look for in the lens readout is required.")
    lens = spec.get("lens") or {}
    if not lens.get("layers") or not all(isinstance(x, int) for x in lens["layers"]):
        errs.append("lens.layers: a list of layer numbers is required.")
    gen = spec.get("generation") or {}
    if not 1 <= int(gen.get("max_tokens", 0) or 0) <= 2048:
        errs.append("generation.max_tokens: between 1 and 2048.")
    return errs


def _validate_readout(spec: dict) -> list[str]:
    errs = []
    if not NAME.match(str(spec.get("name", ""))):
        errs.append("name: lowercase letters, digits and dashes, 2-60 characters.")
    tasks = spec.get("tasks") or {}
    if not isinstance(tasks, dict) or not tasks:
        errs.append("tasks: at least one task (file + position) is required.")
    for key, t in tasks.items() if isinstance(tasks, dict) else []:
        if not isinstance(t, dict) or not (EXPERIMENTS / str(t.get("file", ""))).is_file():
            errs.append(f"tasks.{key}.file: no such file under experiments/.")
        elif t.get("position", "last") not in ("last", "last_newline"):
            errs.append(f"tasks.{key}.position: last or last_newline.")
    lens = spec.get("lens") or {}
    if not lens.get("layers") or not all(isinstance(x, int) for x in lens["layers"]):
        errs.append("lens.layers: a list of layer numbers is required.")
    return errs


def parse(raw: str) -> dict:
    try:
        spec = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        raise SpecError(f"That isn't valid YAML: {e}") from e
    errs = validate(spec)
    if errs:
        raise SpecError(" ".join(errs))
    return spec


def list_experiments() -> list[dict]:
    out = []
    for p in sorted(EXPERIMENTS.glob("*.yaml")):
        raw = p.read_text()
        try:
            spec = yaml.safe_load(raw)
        except yaml.YAMLError:
            spec = {}
        out.append({
            "name": p.stem,
            "title": (spec or {}).get("title", p.stem),
            "description": (spec or {}).get("description", ""),
            "n_conditions": len((spec or {}).get("conditions") or (spec or {}).get("tasks") or {}),
            "kind": (spec or {}).get("kind", "prompted"),
            "n_items": n_items(spec or {}),
            "sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "raw": raw,
            "errors": validate(spec),
        })
    return out


def n_items(spec: dict) -> int:
    if spec.get("kind") == "readout":
        return sum(len(_task_items(t)) for t in (spec.get("tasks") or {}).values() if isinstance(t, dict))
    n = 1
    for v in (spec.get("variables") or {}).values():
        n *= len(v) if isinstance(v, list) else 0
    return n


def load(name: str) -> tuple[str, dict]:
    if not NAME.match(name):
        raise FileNotFoundError(f"no experiment named {name!r}")
    p = EXPERIMENTS / f"{name}.yaml"
    if not p.is_file():
        raise FileNotFoundError(f"no experiment named {name!r}")
    raw = p.read_text()
    return raw, parse(raw)


def save(raw: str) -> dict:
    spec = parse(raw)
    EXPERIMENTS.mkdir(exist_ok=True)
    (EXPERIMENTS / f"{spec['name']}.yaml").write_text(raw)
    return spec


def expand(spec: dict, limit: int | None, seed: int) -> list[dict]:
    """Every combination of the variables, optionally a seeded sample of `limit` of them."""
    keys = list(spec["variables"])
    combos = [dict(zip(keys, vals)) for vals in itertools.product(*(spec["variables"][k] for k in keys))]
    if limit and limit < len(combos):
        combos = random.Random(seed).sample(combos, limit)
    return combos


def build_messages(spec: dict, cond: dict, values: dict) -> list[dict]:
    instruction = cond.get("instruction", "").format(**values)
    user = spec["prompt"]["user"].format(instruction=instruction, **values).strip()
    msgs = []
    system = (spec["prompt"].get("system") or "").format(instruction=instruction, **values).strip()
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    return msgs


async def _retrying(meta: dict, attempt) -> dict:
    """One retry for a dropped or failed request; after that the item is counted as failed
    and the run carries on, so one bad connection can't sink a whole run."""
    for n in range(2):
        try:
            return await attempt()
        except Exception as e:  # network drops, proxy timeouts, server errors
            last = f"{type(e).__name__}: {e}"
            await asyncio.sleep(2)
    meta["failed"] = meta.get("failed", 0) + 1
    meta["last_failure"] = last[:300]
    return {}


def finalize(run_id: str) -> dict:
    """Score whatever items are saved for a run (after a crash, a cancel or a stuck tail)."""
    meta = store.load_run(run_id)
    spec = yaml.safe_load(meta["spec_raw"])
    items = store.load_run_items(run_id)
    meta["results"] = aggregate(spec, items)
    meta["progress"]["done"] = len(items)
    if meta.get("status") != "complete":
        meta["status"] = "partial" if len(items) < meta["progress"]["total"] else "complete"
    store.save_run(meta)
    return meta


def new_run_id() -> str:
    return time.strftime("run-%Y%m%d-%H%M%S-", time.gmtime()) + uuid.uuid4().hex[:4]


def _norm(w: str) -> str:
    return w.strip().lower()


def score_item(steps: list[dict], target: str, track: list[str], layers: list[int], ks: list[int]) -> dict:
    """Per layer: the best rank the target reached over generated tokens, and hits at each k."""
    t = _norm(target)
    best: dict[int, int | None] = {}
    tracked: dict[int, bool] = {}
    for li, layer in enumerate(layers):
        ranks = []
        seen_track = False
        for s in steps:
            if not s.get("reads"):
                continue
            words = [_norm(w) for w in s["reads"][li]["words"]]
            if t in words:
                ranks.append(words.index(t) + 1)
            if any(w in track for w in words[: max(ks)]):
                seen_track = True
        best[layer] = min(ranks) if ranks else None
        tracked[layer] = seen_track
    hits = {str(k): {str(layer): (r is not None and r <= k) for layer, r in best.items()} for k in ks}
    return {"best_rank": {str(k): v for k, v in best.items()}, "hits": hits, "tracked": {str(k): v for k, v in tracked.items()}}


def aggregate(spec: dict, items: list[dict]) -> dict:
    layers, ks = spec["lens"]["layers"], spec["lens"].get("top_k", [10])
    out: dict = {"conditions": {}}
    groups = spec.get("conditions") or {k: {"label": t.get("label", k)} for k, t in spec["tasks"].items()}
    for key, cond in groups.items():
        rows = [it for it in items if it["condition"] == key and it.get("score") and it["visible"]]
        c = {"label": cond.get("label", key), "n": len(rows), "by_k": {}, "tracked": {}}
        for k in ks:
            per = {}
            for layer in layers:
                hits = sum(r["score"]["hits"][str(k)][str(layer)] for r in rows)
                per[str(layer)] = {"k": hits, "n": len(rows), "rate": hits / len(rows) if rows else None,
                                   "ci": wilson(hits, len(rows))}
            anyl = sum(r["score"]["any"][str(k)] if "any" in r["score"] else any(r["score"]["hits"][str(k)].values()) for r in rows)
            c["by_k"][str(k)] = {"layers": per, "any_layer": {"k": anyl, "n": len(rows), "rate": anyl / len(rows) if rows else None}}
        for layer in layers:
            tr = sum(r["score"].get("tracked", {}).get(str(layer), False) for r in rows)
            c["tracked"][str(layer)] = {"k": tr, "n": len(rows)}
        out["conditions"][key] = c
    out["invisible_targets"] = sorted({it["target"] for it in items if not it["visible"]})
    if spec.get("kind") == "readout":
        rates = [c["by_k"][str(ks[-1])]["any_layer"]["rate"] for c in out["conditions"].values() if c["n"]]
        out["macro"] = {"k": ks[-1], "rate": sum(rates) / len(rates) if rates else None}
    return out


def _task_items(task: dict) -> list[dict]:
    import json

    p = EXPERIMENTS / str(task.get("file", ""))
    if not p.is_file():
        return []
    items = json.loads(p.read_text())["items"]
    if task.get("only_correct"):
        import csv

        ok = {(r["eval"], r["item"]) for r in csv.DictReader(open(p.parent / "model_correctness.csv")) if r.get(task["only_correct"]) == "True"}
        name = p.stem.removeprefix("lens-eval-")
        items = [i for i in items if (name, i["name"]) in ok]
    return items


async def run_readout(engine: Engine, name: str, raw: str, spec: dict, *, run_id: str, limit: int | None,
                      seed: int, cancel: asyncio.Event) -> dict:
    """Readout evals: one prompt position, every layer; pass@k = share of intermediates whose
    best rank over layers is within k (the J++ post's recall@k)."""
    info = await engine.describe()
    layers, ks = spec["lens"]["layers"], spec["lens"].get("top_k", [10])
    top_n = max(20, max(ks))
    jobs = []
    for key, task in spec["tasks"].items():
        items = _task_items(task)
        if limit and limit < len(items):
            items = random.Random(seed).sample(items, limit)
        jobs += [(key, task, it) for it in items]
    meta = {
        "id": run_id, "kind": "readout", "experiment": name, "title": spec.get("title", name),
        "spec_sha256": hashlib.sha256(raw.encode()).hexdigest(), "spec_raw": raw,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": info.model, "simulated": info.simulated, "n_layers": info.n_layers,
        "layers": layers, "top_k": ks, "seed": seed, "limit": limit,
        "status": "running", "progress": {"done": 0, "total": len(jobs)},
    }
    store.save_run(meta)
    sem, lock, done = asyncio.Semaphore(CONCURRENCY), asyncio.Lock(), 0

    async def one(idx, key, task, it):
        return await _retrying(meta, lambda: _one(idx, key, task, it))

    async def _one(idx, key, task, it):
        nonlocal done
        async with sem:
            if cancel.is_set():
                return {}
            ids, strs = await engine.tokenize_raw(it["prompt"])
            pos = len(ids) - 1
            if task.get("position") == "last_newline":
                pos = max((i for i, s in enumerate(strs) if "\n" in s), default=pos)
            engine.readout_hint = it["intermediates"][0] if engine.__class__.__name__ == "SimEngine" else None
            step = await engine.lens_read(ids, position=pos, lens_layers=layers, top_n=top_n)
            reads = [{"layer": r.layer, "words": r.words[:top_n], "probs": [round(p, 5) for p in r.probs[:top_n]]} for r in step.reads]
            ranks = {}
            for target in it["intermediates"]:
                t = _norm(target)
                ranks[target] = {str(r["layer"]): ([_norm(w) for w in r["words"]].index(t) + 1 if t in [_norm(w) for w in r["words"]] else None) for r in reads}
            n = len(it["intermediates"])
            score = {
                "ranks": ranks,
                "hits": {str(k): {str(layer): sum((rk[str(layer)] or 99) <= k for rk in ranks.values()) / n for layer in layers} for k in ks},
                "any": {str(k): sum(min((v or 99) for v in rk.values()) <= k for rk in ranks.values()) / n for k in ks},
            }
            item = {"i": idx, "condition": key, "vars": {"name": it["name"]}, "messages": [{"role": "raw", "content": it["prompt"]}],
                    "output": f"read at token {pos} ({strs[pos]!r})", "target": ", ".join(it["intermediates"]), "visible": True,
                    "steps": [{"tok": strs[pos], "reads": reads}], "score": score}
            store.append_run_item(run_id, item)
            async with lock:
                done += 1
                meta["progress"]["done"] = done
                if done % 10 == 0 or done == len(jobs):
                    store.save_run(meta)
            return item

    results = await asyncio.gather(*(one(i, *j) for i, j in enumerate(jobs)))
    items = [r for r in results if r]
    meta.update(status="cancelled" if cancel.is_set() else "complete", results=aggregate(spec, items))
    meta["progress"]["done"] = len(items)
    store.save_run(meta)
    return meta


async def run_experiment(engine: Engine, name: str, raw: str, spec: dict, *, run_id: str,
                         limit: int | None, seed: int, cancel: asyncio.Event) -> dict:
    info = await engine.describe()
    layers = spec["lens"]["layers"]
    bad = [layer for layer in layers if not 0 <= layer < info.n_layers]
    if bad:
        raise SpecError(f"lens.layers {bad} don't exist; this model has {info.n_layers} layers (0-{info.n_layers - 1}).")
    ks = spec["lens"].get("top_k", [10])
    top_n = max(20, max(ks))
    gen = spec["generation"]
    stops = {_norm(w) for w in gen.get("stop_words", [])}
    track = [_norm(w) for w in spec.get("also_track", [])]
    combos = expand(spec, limit, seed)
    jobs = [(key, cond, vals) for key, cond in spec["conditions"].items() for vals in combos]
    meta = {
        "id": run_id, "kind": "experiment", "experiment": name, "title": spec.get("title", name),
        "spec_sha256": hashlib.sha256(raw.encode()).hexdigest(), "spec_raw": raw,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": info.model, "simulated": info.simulated, "n_layers": info.n_layers,
        "layers": layers, "top_k": ks, "seed": seed, "limit": limit,
        "status": "running", "progress": {"done": 0, "total": len(jobs)},
    }
    store.save_run(meta)

    # Readouts are single tokens: a target that tokenizes into pieces can never be read out.
    visible: dict[str, bool] = {}
    for vals in combos:
        t = spec["target"].format(**vals)
        if t not in visible:
            visible[t] = len(await engine.tokenize_text(" " + t)) == 1
    vectors: dict[str, list[float]] = {}
    sem = asyncio.Semaphore(CONCURRENCY)
    done = 0
    lock = asyncio.Lock()

    async def one(idx: int, key: str, cond: dict, vals: dict) -> dict:
        return await _retrying(meta, lambda: _one(idx, key, cond, vals))

    async def _one(idx: int, key: str, cond: dict, vals: dict) -> dict:
        nonlocal done
        async with sem:
            if cancel.is_set():
                return {}
            msgs = build_messages(spec, cond, vals)
            ids = await engine.tokenize_chat(msgs, continue_final=False)
            steer = None
            if cond.get("steer"):
                st = cond["steer"]
                concept = st["concept"].format(**vals)
                layer = int(st.get("layer", round(0.6 * info.n_layers)))
                if concept not in vectors:
                    vectors[concept] = await engine.concept_vector(concept, layer, list(spec["variables"].get("concept", [concept])))
                steer = Steer(layer=layer, vector=vectors[concept], scale=float(st["strength"]))
            steps, text = [], ""
            async for s in engine.lens_generate(
                ids, max_tokens=int(gen["max_tokens"]), lens_layers=layers, top_n=top_n, steer=steer,
                temperature=float(gen.get("temperature", 0)), seed=seed + idx, session=f"{run_id}:{idx}",
            ):
                tok = s.token_str.strip()
                if tok.startswith("<|") and tok.endswith("|>"):
                    break
                text += s.token_str
                steps.append({"tok": s.token_str, "reads": [
                    {"layer": r.layer, "words": r.words[:top_n], "probs": [round(p, 5) for p in r.probs[:top_n]]}
                    for r in s.reads]})
                if _norm(tok).strip(".!,") in stops:
                    break
            target = spec["target"].format(**vals)
            item = {
                "i": idx, "condition": key, "vars": vals, "messages": msgs, "output": text.strip(),
                "target": target, "visible": visible[target], "steps": steps,
                "score": score_item(steps, target, track, layers, ks),
            }
            store.append_run_item(run_id, item)
            async with lock:
                done += 1
                meta["progress"]["done"] = done
                if done % 10 == 0 or done == len(jobs):
                    store.save_run(meta)
            return item

    results = await asyncio.gather(*(one(i, k, c, v) for i, (k, c, v) in enumerate(jobs)))
    items = [r for r in results if r]
    meta.update(status="cancelled" if cancel.is_set() else "complete", results=aggregate(spec, items))
    meta["progress"]["done"] = len(items)
    store.save_run(meta)
    return meta
