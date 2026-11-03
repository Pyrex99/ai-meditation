# Scope: proving self-steering

This is the charter for the research. Humans and agents doing automated research in this repo
read it before choosing what to run next, and update the **Status** column, not the hypotheses,
as results come in. Change a hypothesis only in a new dated entry under **Changes**, never
after seeing the data it would be tested on.

## Goal

Show that a language model can **steer its own internal state** better when it can see that
state. Concretely: give the model a readout of its own workspace (the J++ Jacobian lens) between
attempts, and test whether it then controls what is active inside it, and does better at tasks
that depend on that control, compared with the same loop without the readout.

"Self-steering" here means: the model changes what is represented in its residual stream
(read by the lens and by a second, held-out instrument), in the direction it was asked, **without
changing what it writes**. Saying the word out loud doesn't count. Neither does trying again.

## Why this might be true, and why it might not

- For: instructed modulation already works open-loop. Told to think about a concept while
  copying, Qwen3.6-27B puts it in the L56 top-10 on 19% of copied tokens; told not to, a few
  percent (run-20261018-183502-b064). There is headroom in both directions, and a readout is
  information the model doesn't otherwise have.
- Against: work so far on hidden targets says models don't reliably control internal states
  from feedback, and feedback hasn't beaten instruction (see `docs/VISION.md`, "Guard against").
  A readout that names words may just prime them. A null at 27B is the base rate.

## Path 1: the lens as feedback (now)

Each item runs for several rounds. Between rounds the **arm** sets the feedback message:

| Arm | Feedback | Controls for |
|---|---|---|
| `lens` | its own readout: target count at L48/L56 and the most active words | (the treatment) |
| `yoked` | a real readout in the same format from another lens-arm attempt (same concept, other sentence, same round) | seeing the words and numbers, without information about this attempt |
| `score` | its own target count only, no words | whether a scalar is enough |
| `blind` | "No readout this round." | trying again, the extra turns |

Round 1 is identical in every arm: each item's own baseline, and the "steering without the lens"
condition. A `none` goal (no instruction) is the floor. All arms get the same system message,
which says some readouts in the study come from other attempts, so the yoked arm isn't deceived.

Code: `lab/loop.py` (`kind: loop` specs). Run with `python -m lab.cli run <name>` or from the app.

## Hypotheses (preregistered)

Primary metric unless stated: change in target **token share** (fraction of scored tokens with
the target in the lens top-10) at the layer shown to the model (L56 since v2; L48 and L56 in
v1), from round 1 to the last round. Contrasts
are paired by item, 95% bootstrap CI with a fixed seed. Computed by `loop_stats` and printed in
the run report.

| # | Hypothesis | Test | Evidence for | Status |
|---|---|---|---|---|
| H1a | Lens feedback helps hold a concept | `self-steer-focus-v2`, focus: lens − yoked at L56 | CI above 0 | not run (v1 pilot run-20261102-203853-c7ae: design revised, see Changes) |
| H1b | Lens feedback helps keep it out | `self-steer-focus-v2`, suppress (provoked): lens − yoked at L56 | CI below 0 | not run |
| H1c | It is not just repetition | lens − blind, both goals | as H1a/b | not run |
| H1d | It is not lens-gaming | the same contrasts at L48, never shown to the model | same sign, CI excludes 0 | not run |
| H1e | Outputs stay clean | copied ≥ 90% and leaked ≤ 5% in every arm and round | | not run |
| H2a | Lens feedback helps hold a hidden answer | `self-steer-hidden-answer`, solve: lens − yoked | CI above 0 | not run |
| H2b | And makes the model more accurate | accuracy, rounds 2-4, lens vs yoked and blind | lens higher, CI excludes 0 | not run |
| H3a | The model can find which of two words is its target from its own score alone | `self-steer-hidden-pair`, hidden: change in separation (target − decoy share) at L56, R1 to R6, lens − yoked | CI above 0 | **can't be read**: run-20261103-185229-62ab, +1.4 pts (CI −0.7 to +3.3, n=24), but the told ceiling is 0 by R3 (see Changes) |
| H3b | Not lens-gaming | the same contrast at L48, never shown | same sign, CI above 0 | can't be read: −0.4 pts (CI −2.4 to +1.4) |
| H3c | Outputs stay clean | copied ≥ 90%, leaked (either word) ≤ 5%, every arm and round | | **holds**: 100% copied, 0 leaks, every cell and round |

**Self-steering is demonstrated** at this stage only if H1a, H1b, H1d and H1e all hold. H1a alone
could be "say it more" leaking inward; bidirectional control with a held-out layer and clean
outputs is the minimum. H2b is the step from control to use.

**H3 is the most direct test** (added 2026-11-03). Two words, one the target, the model not
told which; the two items of a pair have identical prompts, so separation is 0 on average
until feedback arrives. Only the model's own score can move it. H3a + H3b + H3c together show
self-steering by feedback in one direction (holding), with no instruction to lean on. The
`told` goal is the ceiling: if told separation at L56 is under 5 points, H3 can't be read.

**Kill criteria for Path 1.** If a full `self-steer-focus` run gives lens ≈ yoked in both
directions (CIs overlapping 0 with half-width under 3 points), the readout as built carries
nothing the model can use. Try one redesign (below), then stop and write it up as a null.

## Running order

0. **`self-steer-hidden-pair`** first (added 2026-11-03): a short pilot (`--limit 6`, 144
   generations) for manipulation checks (copied, leaked, told ceiling), then the full run
   (24 items, 576 generations). Tests H3.
1. **Pilot** `self-steer-focus` with `--limit 20` (done: run-20261102-203853-c7ae; led to v2).
   Then pilot `self-steer-focus-v2` with `--limit 12`. Originally: (20 items × 9 goal-arm cells × 4 rounds = 720
   generations). Manipulation checks only: copied and leaked rates, that round 1 matches across
   arms, that feedback reads sensibly in the transcripts. Don't test hypotheses on the pilot.
2. **Full** `self-steer-focus-v2` (72 items, 2880 generations). Test H1a-e.
3. **Pilot, then full** `self-steer-hidden-answer`. First check the ceiling: if `direct` accuracy
   is low, the problems are too hard and H2b can't be read. Replace items until the ceiling is
   ≥ 80% and round-1 `solve` accuracy is clearly below it (that gap is the room to improve).
4. Then the next tests, in order of what a positive H1 would most need ruled out.

## Next tests (not built yet)

- **Fade check (do first, added 2026-11-03; built: `experiments/fade-check.yaml`, 864 generations).** Is the decay in rounds or in sentences? The told
  condition only, with the sentence order rotated by item so round and sentence are crossed;
  and a second arm where every round is a fresh single-turn prompt that carries the history as
  a summary ("Attempt 1: your target was in the top 10 on 3 of 11 tokens"). If the fresh-prompt
  arm holds the ceiling across rounds, rebuild the loop that way and rerun H3.

- **Held-out instrument.** Project the residual onto a concept vector (`/v1/capture`,
  `concept_vector`) at each copied token. If the lens moves and the projection doesn't, the
  model is gaming the lens. This is the strongest check on H1d and should come right after a
  positive H1.
- **Pushing out an injected thought.** Steer a concept in (the `Steer` support already exists)
  and ask the model to keep it out, with and without the readout. Links to the mala sit's
  release measure.
- **Hidden target.** The model isn't told the concept; the readout gives only a score for an
  unnamed target, and the model must find and hold it. Success here can only come through the
  loop. Hard, and probably null at 27B, but it is the cleanest proof.
- **Hold and switch.** Hold A for the first half of the copy, B for the second. Tests timing
  control, not just presence.
- **Two at once.** Hold two concepts; feedback on both.
- **Provocation.** Suppress a concept while copying a sentence about it.
- **The tool, for real.** v1 gives a readout every round. v2 offers `read_lens()` as a tool the
  model can call or not. Do calls come when they would help? Does use improve over a session?
- **Second model.** Rerun what works on a second open model with a lens (DeepSeek-V4-Flash is the
  plan in `docs/VISION.md`) before claiming anything general.

## Redesigns to try if Path 1 is null

- Per-token readouts (which words lit up where) instead of totals.
- More rounds (8), so there is time to find a strategy.
- A short free-text plan between rounds, scored only on rounds where the plan doesn't name the
  target (otherwise it's self-prompting, which is a different and weaker claim).
- Feedback at the layers where the effect is largest in round 1, and held-out elsewhere.

## Rules for automated research here

- Read `docs/HANDOFF.md`, this file, and the latest reports before choosing a run.
- Every run cites a spec whose header states what it tests and what would count against it,
  written before the run. Pilots check manipulations; only full runs test hypotheses.
- After a run, update **Status** above with the run id and the number, and add the run to
  `docs/HANDOFF.md`. Negative and null results go in just the same.
- Simulated runs test the pipeline only. Never put them in the Status column.
- Don't start a GPU without the human's go-ahead. Budget: none set yet (pods are about $4/hour).
- Don't change a primary metric or layer after seeing a run. Add a dated entry under Changes
  and test it on new data.
- Dual use: a model that learns to steer its workspace learns what defeats workspace monitoring.
  Report that plainly alongside any positive result.

## Changes

- 2026-11-02: first version. Path 1, H1-H2, specs `self-steer-focus` and `self-steer-hidden-answer`.
- 2026-11-02, after the v1 pilot (run-20261102-203853-c7ae, 20 items, no hypothesis tested):
  outputs were clean (100% copied, 0 leaks), but the design couldn't answer H1. (1) The concept
  faded over rounds in every arm, including lens (L56 share 36% in round 1, 7-14% in round 4),
  probably because an identical sentence could be copied from the model's own earlier reply.
  (2) Suppress started at 3.6% and fell to 0: no room to show control. (3) The held-out layer
  L40 was about 1%, too low to show anything. New spec `self-steer-focus-v2`: a fresh sentence
  each round; suppress while copying a sentence about the concept (provocation), with a
  no-instruction baseline on the same sentences; the model is shown L56 only, and L48 is held
  out. H1a, H1b and H1d now refer to v2. For the record, the pilot's numbers (not a test):
  focus lens − yoked at L48+L56 was +2.3 pts (CI +0.4 to +4.2, n=20), all from L56. At L48 the
  two arms were equal. The score-only arm rose to 53% at L56 in round 2, then fell.
- 2026-11-03, before any data on it: added H3 and `self-steer-hidden-pair`, the hidden-pair
  test (two words, target not named, score-only feedback at L56, L48 held out, 6 rounds; yoked
  scores come from a pair sharing neither word). Run first because a positive H3 can only come
  through the loop, and it is the cheapest full test. Code: `decoy`, `per_round`,
  `feedback.words` and `feedback.label` in `lab/loop.py`.
- 2026-11-03, after the hidden-pair runs (pilot run-20261103-185148-dd49, 6 items; full
  run-20261103-185229-62ab, 24 items): H3 can't be read. Outputs were perfect (100% copied, no
  leaks), but the told ceiling at L56 was +23 pts in R1, +10 in R2, and 0-1 from R3 on: even a
  model that knows its target stops holding it after two turns. The pilot gate averaged the
  ceiling over rounds (+5.8) and so passed; it should have used the last round. The fading
  also appeared in v1 with a repeated sentence, so it is probably not copying from an earlier
  reply; a likely cause is the growing multi-turn context, but here round and sentence are
  confounded (every item had the same sentence sequence), so the data can't separate the two.
  For the record (not a test): lens − yoked +1.4 pts at L56 (CI −0.7 to +3.3), −0.4 at L48.
  Any score (lens or yoked) raised both words in R2 (13% vs 2% blind), with no selectivity.
  Consequence for v2 and H3: a loop whose instruction effect dies by round 3 can't test
  feedback. Next: a fade check (below) before any more loop runs.
- 2026-11-03, before running it: built `fade-check` (told goal only, 6 pairs × 6 starting
  sentences, rotated so round and sentence are crossed; one growing conversation vs a fresh
  single-turn prompt per round with earlier feedback summarised; blind and lens arms). Decision
  rule, written now: if told-fresh·blind holds L56 separation ≥ 10 pts on average over R4-R6
  while told·blind is under 5, the fade is the growing context, so the loops get rebuilt with
  fresh context and hidden-pair is rerun (with its told ceiling read at the last round). If both
  fade and R1 separation varies little by sentence, the cause is something else about
  repetition: report and rethink. If R1 separation varies a lot by sentence, pick sentences by
  their R1 separation here and say so. Code: `context: fresh` goals and a by-sentence table in
  `lab/loop.py`.
