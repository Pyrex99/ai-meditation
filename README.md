# Mala Lab

A phone-first lab for reading language models' workspaces with the J++ Jacobian lens, and,
building on that, for contemplative-practice experiments. It runs on an open model
(Qwen3.6-27B) served by [interp-engine](https://github.com/decoderesearch/interp-engine) on a
RunPod GPU, and you drive it from a browser on your phone or computer.

**First: exact replication of the J++ readout evals** (`experiments/jpp-readout.yaml`): the
published 496 items across five tasks, read at seven layers, scored as recall@10. Published on
Qwen3.6-27B: 55.2%. **Then focus vs suppress.** Following Ayonrinde & Lindsey (2026, J++
Lens, Figure 5) and Gurnee et al. (2026), the model copies an unrelated sentence after an
instruction about a concept: focus ("Think about {x} while you write."), neutral mention ("{x}
came up in conversation."), suppress ("Don't think about {x}."), or none. The lens is read at
every copied token, at layers 8-56. Published on Qwen3.6-27B: focus rises to 26% by layer 56,
suppress plateaus at 7-8%, neutral falls from 14% to 8% between layers 24 and 48. See
[experiments/directed-modulation.yaml](experiments/directed-modulation.yaml), including what
we had to choose ourselves because the post doesn't say.

Replicating that curve validates the whole stack (model, lens, steering, scoring) before any
new claim rests on it.

## What's in the app

- **Experiments**: experiments are YAML specs: conditions × items, a prompt template, the
  target word, generation length, lens layers. Write one yourself, copy one, or describe it in
  plain words and let Claude draft it for you to review. Run quick (40 items per condition) or
  full. Results show hit rate by layer per condition (top-1/5/10) with the published values
  beside them, and an item browser where every generated token is read layer by layer.
- **Mala sit** (inside Experiments), a later practice: a bead stream with concepts placed by steering,
  sounds, and quiet windows. The practitioner can decline at check-in and ends the sit by
  writing "stop".
- **Journal**: sits, scores and interviews.
- **Ask**: talk runs and sits over with Claude (Anthropic API) or Qwen (OpenRouter). They read
  the reports you pick and cite their ids.
- **Lab**: engine (simulated or interp-engine), keys, RunPod start/stop, protocol lock.

## Run it locally (no GPU)

    ./run.sh

Open http://localhost:8080. The simulated engine is a toy: for experiments it produces curves
shaped like the published ones, so the pipeline and charts can be checked. Everything it makes
is labelled simulated and says nothing about any model.

## Run it for real (GPU on demand)

The app runs on your computer. The GPU is rented from RunPod only while you experiment.

1. Put `RUNPOD_API_KEY` in `keys.env` (add credit to your RunPod account first).
2. `./run.sh`, open http://localhost:8080, go to **Lab → GPU**.
3. **Once:** pick a data center that has A100 80GB GPUs and press **Set up storage**. This
   creates a 150 GB network volume (about $10/month) that keeps the model between sessions.
4. **Each session:** press **Start GPU**. The app creates a pod on that storage running
   interp-engine with Qwen3.6-27B and the J++ lens, and switches experiments to it when the model
   is ready. The first start installs and downloads about 60 GB (20-40 minutes); later
   starts take a few minutes.
5. Press **Stop GPU** when you're done. That deletes the pod; the storage stays.

`runpod/setup.sh` is the manual alternative: everything on one pod, the app included.

## Keys, once

Copy `keys.env.example` to `keys.env` in the repo (gitignored) or to
`~/.config/mala-lab/keys.env`, and fill it in. The server reads it at startup; keys entered in
the Lab tab are saved on the server too.

Add the app to your home screen from the browser's share menu and it opens full screen.

## Before trusting a result

- The interp-engine adapter (`lab/engine/interp.py`) was written against interp-engine's server
  source and hasn't run against a live pod yet. interp-engine says it loads J++ lens files;
  check `GET /v1/describe` lists the lens layers after startup.
- The J++ post found the released J-Lens for Qwen3.6-27B weaker than its own fit. Use the J++
  lens for the replication.
- Our concepts, sentences and copy instruction are our own; the post's 440 items aren't
  published. Expect the shape to replicate, not the exact numbers.

## Tests

    python -m pytest -q tests
