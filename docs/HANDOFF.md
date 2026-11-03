# Handoff: state of the lab (2026-11-02)

Read this, then `docs/SCOPE.md` (the research plan: proving self-steering), then
`docs/VISION.md`, to pick up where the last session stopped.

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
Recall@10 at each item's best layer (the published metric, in the rebuilt report): macro **55.5%**
vs published J++ 55.2% (J-Lens 35.7%). Multihop 55.2%, multilingual 73.8%, typo 95.8%,
association 38.2% (published 37.0%), poetry 14.3% (published 5.0%; check the read position).
The lens stack replicates.

**Silent mantra and recitation (hold a word while writing a row of beads).** Mostly null.
- run-20261018-191538-7657 (periods): all zeros.
- run-20261018-200628-e3cd (📿 beads, n=18 per condition): suppress hit more than "repeat
  silently" at L56 (94% vs 50% of items, top-10). Small n; a white-bear pattern again.
- run-20261018-220132-aa66 (● beads, 3 wordings): repeat silently 18% of items at L56, but
  sustain 1.9% of beads: the word shows on the first and last beads, not throughout.
- run-20261018-224717-6b69 (silent recitation, phrase lined up with beads): recite 16% of items
  at L56, sustain 0.8%.
So open-loop instruction doesn't hold a word through a long output. That is part of why the
lens-feedback loop is next.

**Self-steering loop.** `lab/loop.py`, `kind: loop`: several rounds of the same kind of task;
between rounds the model gets its own lens readout, a yoked readout from another attempt, its
score only, or nothing. Hypotheses and running order: `docs/SCOPE.md`.

**run-20261102-203853-c7ae, self-steer-focus v1 pilot (20 items, 180 transcripts × 4 rounds).**
Pod ran 11 minutes (about $0.75); the run itself took 2.5 minutes. Outputs clean: 100% copied,
0 leaks, round 1 identical across arms in 58 of 60 items. But the design couldn't test H1: the
concept faded over rounds in every arm (focus L56 36% → 7-14%), suppress sat at the floor
(3.6% → 0), and L40 (meant to be held out) was about 1%. Replaced by
`experiments/self-steer-focus-v2.yaml` (fresh sentence each round, provoked suppress, show L56
and hold out L48). Details in SCOPE.md, Changes.

**self-steer-hidden-pair, 2026-11-03.** The simplest direct test: two words, one the target,
the model not told which; between rounds only its own score ("Your target was among the top 10
words on 3 of 11 tokens", L56), a yoked score from another pair, or nothing. Measure: target
share minus decoy share, which is 0 before feedback. Hypotheses H3a-c in SCOPE.md.
Pilot run-20261103-185148-dd49 (6 items), full run run-20261103-185229-62ab (24 items, 576
generations). Pod 10 minutes plus about 9 waiting for a GPU (about $0.70). **H3 can't be read:**
the told ceiling at L56 is +23 pts in R1, +10 in R2, then 0 from R3. The model stops holding
even a named target after two turns, so there was nothing for feedback to act on by R6. Outputs
were perfect (100% copied, 0 leaks). lens − yoked +1.4 pts (CI −0.7 to +3.3), not a test.

## Next steps

0. The fade check (SCOPE.md, Next tests): does focus decay with rounds of conversation or with
   the sentence? If a fresh single-turn prompt per round (history as a summary) holds the told
   ceiling, rebuild the loop that way and rerun hidden-pair. Until then v2 has the same problem.
1. Pilot `self-steer-focus-v2`: `python -m lab.cli run self-steer-focus-v2 --engine interp
   --limit 12` (480 generations). Check copied/leaked, that focus no longer fades in the blind
   arm, and that provoked is well above 0 at L56 and L48 (room to push down).
2. If those pass, the full v2 run (2880 generations, likely under 20 GPU minutes). Test H1a-e.
3. Pilot `self-steer-hidden-answer`; check the `direct` ceiling before reading H2.
4. Build the held-out instrument (concept-vector projection over copied tokens) if H1 is positive.
5. Older threads, paused: the naming-vs-avoiding ablation (J++ Figure 7), the mala sit.

GPU note: pods in US-CA-2 were unavailable for about 6 minutes before one started. A retry loop
(one try a minute) got one at 20:30. The engine took 8 minutes from pod start to ready.

## Open product notes

- Automatic GPU shutdown after an idle period (offered, not built). Closing the app does not stop
  the pod or the bill.
- Interview, Ask, and Draft-with-Claude exist but haven't been exercised on real runs.
