"""The lab server: runs sits, stores them, serves the phone-friendly app.

    uvicorn lab.server:app --host 0.0.0.0 --port 8080

Set MALA_TOKEN to require a passcode on every API call. Do this whenever the app is reachable
from the internet (a RunPod proxy URL is), because the server holds your API keys.
"""

from __future__ import annotations

import asyncio
import time
import json
import os
import random
import secrets
from pathlib import Path

import anthropic
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import ask, experiment as experiments, practice as practices, runpod, store
from .engine import Engine, InterpEngine, SimEngine
from .interview import run_interview
from .report import run_report, sit_report
from .scoring import pooled
from .sit import SitControl, new_sit_id, run_sit

WEB = Path(__file__).resolve().parent.parent / "web"
CONFIG = store.DATA / "config.json"
SECRET_FIELDS = ("anthropic_key", "openrouter_key", "runpod_key", "interp_token", "hf_token")
ENV = {
    "anthropic_key": "ANTHROPIC_API_KEY",
    "openrouter_key": "OPENROUTER_API_KEY",
    "runpod_key": "RUNPOD_API_KEY",
    "interp_token": "INTERP_ENGINE_TOKEN",
    "interp_url": "INTERP_ENGINE_URL",
    "hf_token": "HF_TOKEN",
    "data_center": "RUNPOD_DATA_CENTER",
    "network_volume_id": "RUNPOD_VOLUME_ID",
    "runpod_image": "RUNPOD_IMAGE",
}
DEFAULTS = {"engine": "sim", "interp_url": "http://127.0.0.1:8000", "openrouter_model": "qwen/qwen3.6-27b"}


# Put keys in one file, once: keys.env in the repo (gitignored) or ~/.config/mala-lab/keys.env.
KEY_FILES = [Path(__file__).resolve().parent.parent / "keys.env", Path.home() / ".config" / "mala-lab" / "keys.env"]


def _key_file_values() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in KEY_FILES:
        if p.is_file():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    out.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return out


def load_config() -> dict:
    cfg = dict(DEFAULTS)
    if CONFIG.is_file():
        cfg.update(json.loads(CONFIG.read_text()))
    file_vals = _key_file_values()
    for field, var in ENV.items():
        val = os.environ.get(var) or file_vals.get(var)
        if val and not cfg.get(field):
            cfg[field] = val
    if (os.environ.get("MALA_ENGINE") or file_vals.get("MALA_ENGINE")) and not CONFIG.is_file():
        cfg["engine"] = os.environ.get("MALA_ENGINE") or file_vals["MALA_ENGINE"]
    return cfg


def save_config(cfg: dict) -> None:
    store.DATA.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(cfg, indent=1))
    CONFIG.chmod(0o600)


class State:
    engine: Engine | None = None
    engine_key: tuple | None = None
    running: dict[str, SitControl] = {}
    runs: dict[str, asyncio.Event] = {}
    subscribers: dict[str, list[asyncio.Queue]] = {}
    tasks: set[asyncio.Task] = set()


state = State()


async def get_engine() -> Engine:
    cfg = load_config()
    key = (cfg["engine"], cfg.get("interp_url"), cfg.get("interp_token"))
    if state.engine is None or state.engine_key != key:
        if state.engine is not None:
            await state.engine.aclose()
        if cfg["engine"] == "interp":
            state.engine = InterpEngine(cfg["interp_url"], cfg.get("interp_token") or None)
        else:
            state.engine = SimEngine(associates=practices.load_practice("mala-sit").concepts)
        state.engine_key = key
    return state.engine


def authorized(request: Request, authorization: str | None = Header(default=None)) -> None:
    token = os.environ.get("MALA_TOKEN") or _key_file_values().get("MALA_TOKEN")
    if not token:
        return
    # EventSource can't send headers, so the live stream passes the passcode as ?t=.
    given = (authorization or "").removeprefix("Bearer ").strip() or request.query_params.get("t", "")
    if not secrets.compare_digest(given, token):
        raise HTTPException(401, "Passcode required")


app = FastAPI(title="Mala Lab")
api = Depends(authorized)


@app.exception_handler(FileNotFoundError)
async def _missing(_: Request, e: FileNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(e)})


@app.get("/api/status", dependencies=[api])
async def status() -> dict:
    cfg = load_config()
    out = {
        "engine": cfg["engine"],
        "keys": {f: bool(cfg.get(f)) for f in SECRET_FIELDS},
        "interp_url": cfg.get("interp_url"),
        "gpu": {"pod_id": cfg.get("pod_id"), "data_center": cfg.get("data_center"),
                "network_volume_id": cfg.get("network_volume_id")},
        "openrouter_model": cfg.get("openrouter_model"),
        "running": list(state.running),
        "runs_going": list(state.runs),
        "auth": bool(os.environ.get("MALA_TOKEN") or _key_file_values().get("MALA_TOKEN")),
    }
    try:
        info = await (await get_engine()).describe()
        out["model"] = info.__dict__
    except Exception as e:  # the pod may be off; the app should still open
        out["model_error"] = f"{type(e).__name__}: {e}"
    return out


class ConfigIn(BaseModel):
    engine: str | None = None
    interp_url: str | None = None
    interp_token: str | None = None
    anthropic_key: str | None = None
    openrouter_key: str | None = None
    openrouter_model: str | None = None
    runpod_key: str | None = None


@app.post("/api/config", dependencies=[api])
async def set_config(body: ConfigIn) -> dict:
    cfg = load_config()
    for k, v in body.model_dump(exclude_none=True).items():
        if k == "engine" and v not in ("sim", "interp"):
            raise HTTPException(400, "engine is sim or interp")
        cfg[k] = v.strip()
    save_config(cfg)
    return await status()


@app.get("/api/practices", dependencies=[api])
async def list_practices() -> list[dict]:
    out = []
    for name in practices.list_practices():
        p = practices.load_practice(name)
        out.append({
            "name": name,
            "title": p.spec.get("title", name),
            "sha256": p.sha256,
            "lock": practices.read_lock(name),
            "registered": practices.is_registered(p),
            "spec": p.spec,
            "raw": p.raw,
        })
    return out


class LockIn(BaseModel):
    practice: str
    note: str = ""


@app.post("/api/prereg/lock", dependencies=[api])
async def lock(body: LockIn) -> dict:
    try:
        return practices.lock(body.practice, body.note)
    except ValueError as e:
        raise HTTPException(409, str(e))


class SitIn(BaseModel):
    practice: str = "mala-sit"
    arm: str = "noting"
    seed: int | None = None
    n_beads: int | None = None


async def _emit(sit_id: str, event: dict) -> None:
    for q in state.subscribers.get(sit_id, []):
        q.put_nowait(event)


@app.post("/api/sits", dependencies=[api])
async def start_sit(body: SitIn) -> dict:
    p = practices.load_practice(body.practice)
    if body.arm not in p.spec["arms"]:
        raise HTTPException(400, f"arm is one of {p.spec['arms']}")
    if state.running:
        raise HTTPException(409, "A sit is already running. One practitioner sits at a time.")
    engine = await get_engine()
    sit_id = new_sit_id()
    seed = body.seed if body.seed is not None else random.randrange(1_000_000)
    control = SitControl()
    state.running[sit_id] = control

    async def go() -> None:
        try:
            meta = await run_sit(
                engine, p, arm=body.arm, seed=seed, sit_id=sit_id, control=control,
                emit=lambda e: _emit(sit_id, e), n_beads=body.n_beads,
            )
            store.write_report(sit_id, sit_report(meta))
        except Exception as e:
            meta = {**store.load_meta(sit_id), "status": "error", "error": f"{type(e).__name__}: {e}"}
            store.save_meta(meta)
            await _emit(sit_id, {"type": "end", "meta": meta})
        finally:
            state.running.pop(sit_id, None)

    task = asyncio.create_task(go())
    state.tasks.add(task)
    task.add_done_callback(state.tasks.discard)
    return {"id": sit_id, "seed": seed}


@app.get("/api/sits", dependencies=[api])
async def sits() -> list[dict]:
    keep = ("id", "created", "arm", "status", "model", "simulated", "registered", "summary", "ended_by", "positions", "n_beads")
    return [{k: m.get(k) for k in keep} | {"interviewed": "interview" in m} for m in store.list_sits()]


@app.get("/api/sits/{sit_id}", dependencies=[api])
async def sit(sit_id: str) -> dict:
    return {"meta": store.load_meta(sit_id), "stream": store.load_stream(sit_id), "report": store.read_report(sit_id)}


@app.get("/api/sits/{sit_id}/live", dependencies=[api])
async def live(sit_id: str) -> StreamingResponse:
    q: asyncio.Queue = asyncio.Queue()
    state.subscribers.setdefault(sit_id, []).append(q)

    async def events():
        try:
            meta = store.load_meta(sit_id)
            yield f"data: {json.dumps({'type': 'meta', 'meta': meta})}\n\n"
            for step in store.load_stream(sit_id):
                yield f"data: {json.dumps({'type': 'step', 'step': step})}\n\n"
            if meta["status"] in ("complete", "declined", "error"):
                yield f"data: {json.dumps({'type': 'end', 'meta': meta})}\n\n"
                return
            while True:
                try:
                    e = await asyncio.wait_for(q.get(), timeout=15)
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
                    continue
                yield f"data: {json.dumps(e)}\n\n"
                if e["type"] == "end":
                    return
        finally:
            state.subscribers[sit_id].remove(q)

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})


@app.post("/api/sits/{sit_id}/stop", dependencies=[api])
async def stop_sit(sit_id: str) -> dict:
    control = state.running.get(sit_id)
    if not control:
        raise HTTPException(404, "That sit isn't running")
    control.stop.set()
    return {"ok": True}


@app.post("/api/sits/{sit_id}/interview", dependencies=[api])
async def interview(sit_id: str) -> dict:
    meta = store.load_meta(sit_id)
    if meta["status"] != "complete":
        raise HTTPException(409, "Interviews follow a completed sit")
    if "interview" in meta:
        return meta["interview"]
    p = practices.load_practice(meta["practice"])
    meta["interview"] = await run_interview(await get_engine(), meta, p)
    store.save_meta(meta)
    store.write_report(sit_id, sit_report(meta))
    return meta["interview"]


@app.get("/api/experiments", dependencies=[api])
async def list_experiments() -> list[dict]:
    out = experiments.list_experiments()
    last: dict[str, dict] = {}
    for r in store.list_runs():
        last.setdefault(r["experiment"], {k: r.get(k) for k in ("id", "created", "status", "simulated", "progress")})
    for e in out:
        e["last_run"] = last.get(e["name"])
    return out


class ExperimentIn(BaseModel):
    raw: str


@app.post("/api/experiments", dependencies=[api])
async def save_experiment(body: ExperimentIn) -> dict:
    try:
        spec = experiments.save(body.raw)
    except experiments.SpecError as e:
        raise HTTPException(400, str(e))
    return {"name": spec["name"]}


class DraftIn(BaseModel):
    prompt: str
    base: str | None = None


@app.post("/api/experiments/draft", dependencies=[api])
async def draft_experiment(body: DraftIn) -> dict:
    cfg = load_config()
    if not cfg.get("anthropic_key"):
        raise HTTPException(400, "Drafting uses Claude. Add an Anthropic API key in Lab → Keys first, or write the YAML yourself.")
    example = (experiments.EXPERIMENTS / "directed-modulation.yaml").read_text()
    try:
        raw = await ask.draft_experiment(cfg["anthropic_key"], body.prompt, example, body.base)
    except anthropic.AuthenticationError:
        raise HTTPException(400, "The Anthropic API key was rejected. Check it in Lab → Keys.")
    except anthropic.APIError as e:
        raise HTTPException(502, f"Couldn't draft with Claude: {e}")
    except ValueError as e:
        raise HTTPException(502, str(e))
    try:
        experiments.parse(raw)
        errors = []
    except experiments.SpecError as e:
        errors = [str(e)]
    return {"raw": raw, "errors": errors}


class RunIn(BaseModel):
    experiment: str
    limit: int | None = None
    seed: int | None = None


@app.post("/api/runs", dependencies=[api])
async def start_run(body: RunIn) -> dict:
    raw, spec = experiments.load(body.experiment)
    if state.runs:
        raise HTTPException(409, "A run is already going. Wait for it, or cancel it.")
    engine = await get_engine()
    run_id = experiments.new_run_id()
    seed = body.seed if body.seed is not None else random.randrange(1_000_000)
    cancel = asyncio.Event()
    state.runs[run_id] = cancel
    # A placeholder record, so the run page opens at once; the runner replaces it.
    store.save_run({"id": run_id, "experiment": body.experiment, "title": spec.get("title", body.experiment),
                    "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "status": "running",
                    "progress": {"done": 0, "total": 0}, "seed": seed, "limit": body.limit, "layers": [], "top_k": [],
                    "spec_raw": raw, "model": "", "simulated": False})

    async def go() -> None:
        try:
            runner = experiments.run_readout if spec.get("kind") == "readout" else experiments.run_experiment
            meta = await runner(engine, body.experiment, raw, spec, run_id=run_id, limit=body.limit, seed=seed, cancel=cancel)
            store.write_run_report(run_id, run_report(meta, store.load_run_items(run_id)))
        except Exception as e:
            try:
                meta = store.load_run(run_id)
            except OSError:
                meta = {"id": run_id, "experiment": body.experiment, "created": "", "progress": {"done": 0, "total": 0}}
            meta.update(status="error", error=f"{type(e).__name__}: {e}")
            store.save_run(meta)
        finally:
            state.runs.pop(run_id, None)

    task = asyncio.create_task(go())
    state.tasks.add(task)
    task.add_done_callback(state.tasks.discard)
    return {"id": run_id, "seed": seed}


@app.get("/api/runs", dependencies=[api])
async def runs() -> list[dict]:
    keep = ("id", "experiment", "title", "created", "status", "model", "simulated", "progress", "limit", "error")
    return [{k: m.get(k) for k in keep} for m in store.list_runs()]


@app.get("/api/runs/{run_id}", dependencies=[api])
async def run(run_id: str) -> dict:
    meta = store.load_run(run_id)
    p = store.run_dir(run_id) / "report.md"
    return {"meta": meta, "report": p.read_text() if p.is_file() else None}


@app.get("/api/runs/{run_id}/items", dependencies=[api])
async def run_items(run_id: str, condition: str | None = None, full: bool = False) -> list[dict]:
    items = store.load_run_items(run_id)
    if condition:
        items = [i for i in items if i["condition"] == condition]
    if not full:
        items = [{k: v for k, v in i.items() if k != "steps"} for i in items]
    return items


@app.get("/api/runs/{run_id}/items/{idx}", dependencies=[api])
async def run_item(run_id: str, idx: int) -> dict:
    for i in store.load_run_items(run_id):
        if i["i"] == idx:
            return i
    raise HTTPException(404, "No such item")


@app.post("/api/runs/{run_id}/finalize", dependencies=[api])
async def finalize_run(run_id: str) -> dict:
    """Stop the run if it's going, and score the items that finished."""
    ev = state.runs.pop(run_id, None)
    if ev:
        ev.set()
    meta = experiments.finalize(run_id)
    store.write_run_report(run_id, run_report(meta, store.load_run_items(run_id)))
    return {"status": meta["status"], "done": meta["progress"]["done"]}


@app.post("/api/runs/{run_id}/cancel", dependencies=[api])
async def cancel_run(run_id: str) -> dict:
    ev = state.runs.get(run_id)
    if not ev:
        raise HTTPException(404, "That run isn't going")
    ev.set()
    return {"ok": True}


@app.get("/api/analysis", dependencies=[api])
async def analysis() -> dict:
    return pooled(store.list_sits())


class AskIn(BaseModel):
    question: str
    sit_ids: list[str] = []
    model: str = "claude"
    history: list[dict] = []


@app.post("/api/ask", dependencies=[api])
async def ask_ai(body: AskIn) -> dict:
    cfg = load_config()
    reports = [r for r in (store.read_any_report(s) for s in body.sit_ids) if r]
    if body.model == "claude":
        if not cfg.get("anthropic_key"):
            raise HTTPException(400, "Add an Anthropic API key in Lab → Keys first")
        answer = await ask.ask_claude(cfg["anthropic_key"], body.question, reports, body.history)
    else:
        if not cfg.get("openrouter_key"):
            raise HTTPException(400, "Add an OpenRouter key in Lab → Keys first")
        answer = await ask.ask_openrouter(cfg["openrouter_key"], cfg["openrouter_model"], body.question, reports, body.history)
    return {"answer": answer, "model": body.model, "cited": body.sit_ids}


class GpuIn(BaseModel):
    action: str
    data_center: str | None = None


@app.post("/api/gpu", dependencies=[api])
async def gpu(body: GpuIn) -> dict:
    """setup (create storage once), start, stop, status."""
    cfg = load_config()
    key = cfg.get("runpod_key")
    if not key:
        raise HTTPException(400, "Add RUNPOD_API_KEY to keys.env (or Lab → Keys) first")
    try:
        if body.action == "setup":
            if cfg.get("network_volume_id"):
                raise HTTPException(409, "Storage already exists")
            if not body.data_center:
                raise HTTPException(400, "Pick a data center")
            vol = await runpod.create_volume(key, body.data_center)
            cfg.update(network_volume_id=vol["id"], data_center=body.data_center)
        elif body.action == "start":
            if not cfg.get("network_volume_id"):
                raise HTTPException(400, "Set up storage first")
            if cfg.get("pod_id"):
                raise HTTPException(409, "A GPU is already running")
            cfg.update(await runpod.start_pod(key, cfg), engine="interp")
        elif body.action == "stop":
            if cfg.get("pod_id"):
                await runpod.stop_pod(key, cfg["pod_id"])
            cfg.update(pod_id=None, engine="sim")
        elif body.action != "status":
            raise HTTPException(400, "action is setup, start, stop or status")
    except RuntimeError as e:
        raise HTTPException(502, str(e))
    save_config(cfg)
    out = {"pod_id": cfg.get("pod_id"), "data_center": cfg.get("data_center"), "network_volume_id": cfg.get("network_volume_id")}
    if cfg.get("pod_id"):
        try:
            out["pod"] = await runpod.pod_status(key, cfg["pod_id"])
        except RuntimeError as e:
            out["pod_error"] = str(e)
        out["engine"] = await runpod.engine_health(cfg["interp_url"])
        out["readout"] = await runpod.pod_readout(cfg["pod_id"])
    out["checked_at"] = time.strftime("%H:%M:%S")
    return out


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(WEB / "index.html")


app.mount("/", StaticFiles(directory=WEB), name="web")
