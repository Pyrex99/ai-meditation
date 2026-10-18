# Mala Lab: notes for Claude

A lab for workspace-lens experiments and contemplative practice in language models. Read
`docs/VISION.md` first. The current work is replicating the J++ focus/suppress result
(`experiments/directed-modulation.yaml`) before anything new.

## Layout

- `experiments/*.yaml` are prompted lens experiments (conditions x items); `lab/experiment.py`
  validates, runs and scores them. Runs live in `data/runs/<id>/{meta.json,items.jsonl,report.md}`.
- `practices/*.yaml` is the sit protocol. Its sha256 is recorded on every sit. Don't edit a
  locked practice; add a new version file instead (`mala-sit-v2.yaml`).
- `lab/engine/` holds the engine interface, `interp.py` (interp-engine HTTP client: `/v1/lens`,
  `/v1/capture`, `/v1/tokenize`, `/v1/generate`) and `sim.py` (a toy workspace, no GPU).
- `lab/sit.py` runs a sit. `lab/scoring.py` is pure functions of the stored stream.
- `lab/server.py` is FastAPI. It serves `web/` (vanilla JS, no build step).
- Data: `data/sits/<id>/{meta.json,stream.jsonl,report.md}`, plus `data/reports/<id>.md`.

## Rules

- The raw stream is primary. Every number in a report must be recomputable from `stream.jsonl`
  and the trials in `meta.json`.
- Simulated sits are labelled simulated everywhere (meta, report, UI). Never mix them into
  registered analysis or describe them as model results.
- Care rules are part of the protocol: check-in with a real opt-out, the bell, neutral
  arisings only, first-person account before data. Don't remove these to make a run easier.
- When analysing results, cite sit ids, and say when the data can't answer the question.

## Commands

    pip install -r requirements.txt
    python -m pytest -q tests
    uvicorn lab.server:app --reload --port 8080
    python tools/build_preview.py out/mala-lab-preview.html
