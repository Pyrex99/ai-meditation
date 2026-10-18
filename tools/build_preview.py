"""Build the single-file preview: the real app UI replaying sits recorded on the simulated engine.

    python tools/build_preview.py out/mala-lab-preview.html
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MALA_DATA", tempfile.mkdtemp(prefix="mala-preview-"))

from lab import experiment as experiments, practice as practices, store  # noqa: E402
from lab.engine import SimEngine  # noqa: E402
from lab.interview import run_interview  # noqa: E402
from lab.report import run_report, sit_report  # noqa: E402
from lab.scoring import pooled  # noqa: E402
from lab.sit import SitControl, run_sit  # noqa: E402

TOP_WORDS = 8  # trims the lens readout so the preview stays small


async def record() -> dict:
    p = practices.load_practice("mala-sit")
    engine = SimEngine(associates=p.concepts)
    engine.step_delay = 0
    info = await engine.describe()

    async def emit(_):
        return None

    sits = []
    for k in range(8):
        arm = "noting" if k % 2 == 0 else "just-beads"
        sit_id = f"sit-20261018-0{k}0000-demo"
        meta = await run_sit(engine, p, arm=arm, seed=101 + k, sit_id=sit_id, emit=emit, control=SitControl())
        meta["created"] = f"2026-10-18T0{k}:00:00Z"
        if arm == "noting" and k < 4:
            meta["interview"] = await run_interview(engine, meta, p)
        store.save_meta(meta)
        report = sit_report(meta)
        store.write_report(sit_id, report)
        stream = store.load_stream(sit_id)
        for s in stream:
            for r in s.get("reads") or []:
                r["words"], r["probs"] = r["words"][:TOP_WORDS], r["probs"][:TOP_WORDS]
        sits.append({"meta": meta, "stream": stream, "report": report})
    sits.sort(key=lambda s: s["meta"]["created"], reverse=True)

    raw, spec = experiments.load("directed-modulation")
    run_meta = await experiments.run_experiment(
        engine, "directed-modulation", raw, spec, run_id="run-20261018-090000-demo",
        limit=40, seed=7, cancel=asyncio.Event(),
    )
    run_meta["created"] = "2026-10-18T09:00:00Z"
    runs = [{"meta": run_meta, "report": run_report(run_meta), "items": store.load_run_items(run_meta["id"])}]
    for it in runs[0]["items"]:
        for st in it["steps"]:
            for r in st.get("reads") or []:
                r["words"], r["probs"] = r["words"][:10], r["probs"][:10]
    exps = experiments.list_experiments()
    for e in exps:
        e["last_run"] = {"id": run_meta["id"], "status": "complete", "simulated": True} if e["name"] == "directed-modulation" else None
    return {
        "experiments": exps,
        "runs": runs,
        "status": {
            "engine": "sim",
            "keys": {"anthropic_key": False, "openrouter_key": False, "runpod_key": False, "interp_token": False},
            "interp_url": "http://127.0.0.1:8000",
            "runpod_pod_id": "",
            "openrouter_model": "qwen/qwen3.6-27b",
            "running": [],
            "auth": False,
            "model": info.__dict__,
        },
        "practices": [{
            "name": p.name, "title": p.spec["title"], "sha256": p.sha256, "lock": None,
            "registered": False, "spec": p.spec, "raw": p.raw,
        }],
        "analysis": pooled([s["meta"] for s in sits]),
        "sits": sits,
    }


def build(out: Path) -> None:
    demo = asyncio.run(record())
    index = (ROOT / "web" / "index.html").read_text()
    markup = index.split("<!--APP-->")[1].split("<!--/APP-->")[0]
    data = json.dumps(demo, separators=(",", ":")).replace("</", "<\\/")
    page = "\n".join([
        "<title>Mala Lab</title>",
        '<meta name="claude:viewport-fit-sides" content="cover">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&display=swap">',
        f"<style>\n{(ROOT / 'web' / 'app.css').read_text()}\n</style>",
        markup,
        f"<script>window.MALA_DEMO={data};</script>",
        f"<script>\n{(ROOT / 'web' / 'app.js').read_text()}\n</script>",
    ])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    build(Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "out" / "mala-lab-preview.html"))
