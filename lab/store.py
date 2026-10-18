"""Sits live on disk, one directory each. The raw stream stays primary; scores are derived."""

from __future__ import annotations

import json
import os
from pathlib import Path

DATA = Path(os.environ.get("MALA_DATA", Path(__file__).resolve().parent.parent / "data"))
SITS = DATA / "sits"
REPORTS = DATA / "reports"


def sit_dir(sit_id: str) -> Path:
    d = SITS / sit_id
    if d.parent != SITS:
        raise ValueError("bad sit id")
    return d


def save_meta(meta: dict) -> None:
    d = sit_dir(meta["id"])
    d.mkdir(parents=True, exist_ok=True)
    tmp = d / "meta.json.tmp"
    tmp.write_text(json.dumps(meta, indent=1))
    tmp.replace(d / "meta.json")


def load_meta(sit_id: str) -> dict:
    return json.loads((sit_dir(sit_id) / "meta.json").read_text())


def append_stream(sit_id: str, step: dict) -> None:
    with open(sit_dir(sit_id) / "stream.jsonl", "a") as f:
        f.write(json.dumps(step, separators=(",", ":")) + "\n")


def load_stream(sit_id: str) -> list[dict]:
    p = sit_dir(sit_id) / "stream.jsonl"
    if not p.is_file():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def list_sits() -> list[dict]:
    if not SITS.is_dir():
        return []
    out = []
    for d in SITS.iterdir():
        try:
            out.append(json.loads((d / "meta.json").read_text()))
        except (OSError, ValueError):
            continue
    return sorted(out, key=lambda m: m["created"], reverse=True)


def write_report(sit_id: str, markdown: str) -> Path:
    (sit_dir(sit_id) / "report.md").write_text(markdown)
    REPORTS.mkdir(parents=True, exist_ok=True)
    p = REPORTS / f"{sit_id}.md"
    p.write_text(markdown)
    return p


def read_report(sit_id: str) -> str | None:
    p = sit_dir(sit_id) / "report.md"
    return p.read_text() if p.is_file() else None


RUNS = DATA / "runs"


def run_dir(run_id: str) -> Path:
    d = RUNS / run_id
    if d.parent != RUNS:
        raise ValueError("bad run id")
    return d


def save_run(meta: dict) -> None:
    d = run_dir(meta["id"])
    d.mkdir(parents=True, exist_ok=True)
    tmp = d / "meta.json.tmp"
    tmp.write_text(json.dumps(meta, indent=1))
    tmp.replace(d / "meta.json")


def load_run(run_id: str) -> dict:
    return json.loads((run_dir(run_id) / "meta.json").read_text())


def append_run_item(run_id: str, item: dict) -> None:
    with open(run_dir(run_id) / "items.jsonl", "a") as f:
        f.write(json.dumps(item, separators=(",", ":")) + "\n")


def load_run_items(run_id: str) -> list[dict]:
    p = run_dir(run_id) / "items.jsonl"
    if not p.is_file():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def list_runs() -> list[dict]:
    if not RUNS.is_dir():
        return []
    out = []
    for d in RUNS.iterdir():
        try:
            out.append(json.loads((d / "meta.json").read_text()))
        except (OSError, ValueError):
            continue
    return sorted(out, key=lambda m: m["created"], reverse=True)


def write_run_report(run_id: str, markdown: str) -> None:
    (run_dir(run_id) / "report.md").write_text(markdown)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"{run_id}.md").write_text(markdown)


def read_any_report(rid: str) -> str | None:
    p = (run_dir(rid) if rid.startswith("run-") else sit_dir(rid)) / "report.md"
    return p.read_text() if p.is_file() else None
