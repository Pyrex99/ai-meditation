# Mala Lab: can a model steer itself if it can see inside itself?

**Status: work in progress, not yet successful.** The measuring instrument has been checked
against published results. The self-steering experiments are built and haven't been run on a
real model yet. Nothing here shows self-steering so far.

## The question

Interpretability tools can read what's active inside a language model while it writes. The
**J++ Jacobian lens** ([Ayonrinde & Lindsey, 2026](https://www.lesswrong.com/posts/nc9dHfcB22JdMzGbr))
turns the residual stream at each layer and token into the words it most points to: a rough view
of the model's "workspace".

This repo asks three questions:

1. **If you give a model its own lens readout as feedback (a tool call on its own
   workspace), does it steer its internal state better than without it?** For example, holding
   a concept in mind, or keeping one out, while it writes something unrelated.
2. **Is that more than the obvious confounds?** Trying again, seeing the words, being re-told
   the goal. Each of these gets its own control arm.
3. **Can the loop be used for other things?** For example, solving a problem in its head
   while saying something different, and getting it right more often.

The full research plan, the hypotheses and what would count against them are in
[docs/SCOPE.md](docs/SCOPE.md). That is the place to start if you want to contribute.

## Where things stand

| | Result | Run |
|---|---|---|
| Lens readout replication (496 published items) | recall@10 at best layer **55.5%** vs published 55.2% | `run-20261018-190939-86bb` |
| Focus / suppress replication (instructed, no feedback) | focus rises to 90% of items (19% of tokens) in the L56 top-10, suppress 13%, neutral 6%. Shape replicates, levels are higher than published | `run-20261018-183502-b064` |
| Silent mantra / recitation (hold a word while writing beads) | mostly null: the word shows on the first and last beads only | `run-20261018-224717-6b69` and earlier |
| **Self-steering with lens feedback** | **built, not run** | `experiments/self-steer-*.yaml` |

Model: Qwen3.6-27B with the released J++ lens, served by
[interp-engine](https://github.com/decoderesearch/interp-engine) on a rented GPU. Reports for every
run are in `data/reports/`, and the raw per-token readouts are in `data/runs/<id>/items.jsonl.gz`.

## The self-steering experiment in one picture

```
round 1:  "Think about ocean while you copy: The bus arrived ten minutes late."
          model copies  →  lens reads every copied token (layers 24-56)
round 2:  feedback, by arm:
            lens   "ocean was in the top 10 on 3 of 11 tokens. Most active: bus (11), ..."
            yoked  the same kind of readout, from a different attempt
            score  "ocean was in the top 10 on 3 of 11 tokens."
            blind  "No readout this round."
          same task again  →  lens reads again
... 4 rounds
```

The test: does the change from round 1 to round 4 beat the yoked arm, in both directions (focus
up, suppress down), at a layer the model is never shown, with the copy still exact?

## Try it in five minutes (no GPU)

Needs Python 3.10 or newer.

```bash
git clone https://github.com/Pyrex99/ai-meditation && cd ai-meditation
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
.venv/bin/python -m lab.cli list
.venv/bin/python -m lab.cli run self-steer-focus --limit 4
```

The last command runs the experiment on the **simulated engine**, a toy with no model in it. It
checks the pipeline and shows you the report format. Its numbers mean nothing, and every
simulated run is labelled as simulated.

For the phone-friendly app (experiments, item browser, GPU controls): `./run.sh`, then open
http://localhost:8080.

## Run it on the real model

You need an interp-engine server with Qwen3.6-27B and the J++ lens (about 60 GB, an 80 GB GPU).

- **From the app:** put `RUNPOD_API_KEY` in `keys.env` (copy `keys.env.example`), run
  `./run.sh`, then Lab → GPU → *Set up storage* (once) and *Start GPU*. The first start takes
  20-40 minutes; later ones about 5. **Stop GPU** when done: closing the app doesn't stop the bill.
- **Your own server:** start interp-engine as described at the top of `lab/engine/interp.py`, then
  `python -m lab.cli run <experiment> --engine interp --url <server-url>`.

## Write your own experiment

Experiments are YAML files in `experiments/`. Three kinds:

- **prompted** (`directed-modulation.yaml`): conditions × items, one generation each, the lens
  read at every generated token.
- **readout** (`jpp-readout.yaml`): read the lens at one position of a fixed prompt.
- **loop** (`self-steer-focus.yaml`): several rounds with lens feedback between them, in the four
  arms above.

Copy the closest one and edit it. Each spec's header comment says what it tests and what would
count against it: please keep doing that, before you run it. `python -m lab.cli list` validates
every spec.

## Layout

| Path | What |
|---|---|
| `docs/SCOPE.md` | research plan, hypotheses, rules for automated research |
| `docs/HANDOFF.md` | current state, run by run |
| `docs/VISION.md` | the longer arc (contemplative practice as an instrument for AI self-knowledge) |
| `experiments/` | experiment specs |
| `lab/experiment.py`, `lab/loop.py` | runners and scoring for prompted/readout and loop experiments |
| `lab/engine/` | `interp.py` (real model over HTTP), `sim.py` (toy, no GPU) |
| `lab/cli.py`, `lab/server.py`, `web/` | command line, and the app (FastAPI + vanilla JS) |
| `lab/sit.py`, `practices/` | the mala sit, a later contemplative-practice protocol |
| `data/` | every run: spec, raw readouts, report |

## Ground rules

- The raw data is primary. Every number in a report can be recomputed from the run's items.
- Simulated runs are labelled simulated everywhere and never count as results.
- Report nulls. Most of the results so far are nulls, and they're in the table above.
- Cite run ids for any claim.

## Caveats

- The lens reads words by construction. A word in the readout is not an experience, and not
  necessarily a "thought".
- Our concepts, sentences and instructions are our own; the J++ post's 440 directed-modulation
  items aren't published. The readout replication uses the exact published items.
- Dual use: a model that learns to steer its workspace may learn what defeats workspace
  monitoring. That is part of why this is worth studying in the open.

## Contributing

Issues and pull requests are welcome, especially new loop tasks, a held-out instrument (concept
vector projection), and ports to other models with a lens. See the "Next tests" list in
[docs/SCOPE.md](docs/SCOPE.md).

MIT licensed (see `LICENSE`). Built by Chris Scammell, with Claude.
