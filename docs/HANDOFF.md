# Handoff: state of the lab (2026-10-18)

Read this, then `docs/VISION.md`, to pick up where the last session stopped.

## What this is

A lab for reading a language model's workspace with the J++ Jacobian lens, building toward
contemplative-practice experiments (the mala sit, silent mantra, noting). Model: Qwen3.6-27B,
served by interp-engine with the released J++ lens (`hf://koayon/jpp-lenses/qwen3.6-27b/lens.pt`).
The app runs on Chris's Mac (`~/Code/ai-meditation`, `./run.sh`, http://localhost:8080); the GPU
is a RunPod pod started and stopped from Lab → GPU.

## Infrastructure (working)

- `./run.sh` sets up `.venv` and starts the app (Python 3.10+; the Mac has 3.11, so test on 3.11).
- Keys: `keys.env` (gitignored). RunPod network volume `apthu6t1zn` in US-CA-2 holds the model,
  the lens and the interp-engine venv. Start GPU makes a pod on it (~5 min to "Model ready" now);
  Stop GPU deletes the pod. Pods have been H100s at $3.99/hr (no A100 free in US-CA-2).
- Pod status page on port 8001: `https://<pod-id>-8001.proxy.runpod.net/engine.log` has the full
  server log. Lab shows a readout from it.
- `./sync.sh` sends experiments and results to GitHub (and pulls). Raw items go as
  `items.jsonl.gz`; `data/config.json` and `keys.env` never leave the Mac.
- Fixed along the way: missing `ninja` on the pod (FlashInfer JIT), stale engine log across pods,
  runs stalling on dropped proxy connections (now one retry, then the item is counted failed),
  a Python 3.12-only f-string.

## Results so far (real model, H100)

**run-20261018-183502-b064, directed-modulation (focus / neutral / suppress, 1747 of 1760).**
Our items (40 concepts × 11 sentences; the post's items aren't published). Hit = concept in the
lens top-k at any copied token.
- Focus rises late and steeply: top-10 16.6% (L32) → 56.4% → 79.0% → 90.2% (L56). Published 26%
  at L56; our levels are higher, most likely because the post's hit definition differs
  (possibly per token rather than per item). Shape replicates; levels don't.
- Suppress (13.1% at L56) > neutral (6.3%) > none (2.6%): a white-bear effect.
- Failure words (fail/failed/failure/damn) in the top-10 only under suppress: 41/429 items at
  L48, 5 at L40, none elsewhere. Matches Gurnee et al.'s observation qualitatively. Not yet
  inspected item by item.
- Not replicated: the early "retrieve" step (all instructed conditions above baseline by L24).
  At L24 only focus is above baseline.

**run-20261018-190939-86bb, jpp-readout (exact published items, 496/496).**
Per-layer recall@10 peaks: multihop 39.8%, multilingual 44.6%, typo 86.5%, association 25.5%,
poetry 13.3% (L56). Macro of those per-layer peaks is 41.9%, a lower bound on the published
metric (best layer per item; published J++ 55.2%, J-Lens 35.7%). The best-layer table is in the
rebuilt report; rebuild it to get the number. Task order matches the post. Poetry is higher than
published (≤5%), all at L56; check the read position (last newline).

**run-20261018-191538-7657, silent-mantra (Chris's spec, local only).** All zeros, every
condition and layer, including tracked words. Suspected: periods pack into few tokens, or the
model didn't write dots. Superseded by `experiments/silent-mantra-beads.yaml` (📿 carrier, one
target word per item: love, peace, bliss, lotus + six controls). Not yet run.

## Next steps

1. `./sync.sh` on the Mac so the runs above are on GitHub (they were made before syncing existed).
2. Rebuild both reports (button on each run) and read: the readout best-layer macro vs 55.2%;
   the per-token rates for focus/suppress vs the published 26% / 7-8%; the failure-word examples.
3. Run silent-mantra-beads.
4. If the per-token definition matches the post better, make it the headline metric for
   directed-modulation. Consider reading the instruction tokens too (the early retrieve step).
5. Next replication: the naming-vs-avoiding ablation (J++ post, Figure 7), which needs lens-vector
   ablation (not built yet).
6. Later: the mala sit (`practices/mala-sit.yaml`, inside Experiments), then the practice library
   in `docs/VISION.md`.

## Open product notes

- Automatic GPU shutdown after an idle period (offered, not built). Closing the app does not stop
  the pod or the bill.
- Interview, Ask, and Draft-with-Claude exist but haven't been exercised on real runs.
