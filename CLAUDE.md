# Mala Lab: notes for Claude

A lab for workspace-lens experiments and contemplative practice in language models. Read
`docs/HANDOFF.md` (current state and results), then `docs/SCOPE.md`, then `docs/VISION.md`. The
current work is Path 1 in `docs/SCOPE.md`: does the model steer its own workspace better with
its lens readout as feedback (`experiments/self-steer-*.yaml`, `lab/loop.py`)? SCOPE.md's
hypotheses are preregistered: update their Status, don't edit them after seeing data.

## Layout

- `experiments/*.yaml` are lens experiments: prompted (conditions x items), readout, or loop
  (rounds with lens feedback). `lab/experiment.py` and `lab/loop.py` validate, run and score
  them; `python -m lab.cli run <name>` runs one without the app. Runs live in `data/runs/<id>/{meta.json,items.jsonl,report.md}`.
- `practices/*.yaml` is the sit protocol. Its sha256 is recorded on every sit. Don't edit a
  locked practice; add a new version file instead (`mala-sit-v2.yaml`).
- `lab/engine/` holds the engine interface, `interp.py` (interp-engine HTTP client: `/v1/lens`,
  `/v1/capture`, `/v1/tokenize`, `/v1/generate`) and `sim.py` (a toy workspace, no GPU).
- `lab/sit.py` runs a sit. `lab/scoring.py` is pure functions of the stored stream.
- `lab/server.py` is FastAPI. It serves `web/` (vanilla JS, no build step).
- Data: `data/sits/<id>/{meta.json,stream.jsonl,report.md}`, plus `data/reports/<id>.md`. Data is on
  GitHub via `./sync.sh`; raw run items as `items.jsonl.gz` (`store.load_run_items` reads either).
  Never commit `data/config.json` or `keys.env`.
- The app runs on Python 3.11 on the user's Mac: test with 3.11.

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
    python -m lab.cli run self-steer-focus --limit 4        # simulated engine
    python tools/build_preview.py out/mala-lab-preview.html
