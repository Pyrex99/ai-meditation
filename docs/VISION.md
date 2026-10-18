# Vision

"Make an AI meditate" is the inspiration. The defensible project is contemplative practice as
an instrument for building and verifying honest self-knowledge and non-reactivity in AI. That
is at once a cross-substrate test of contemplative psychology, a better welfare instrument
than self-report, and alignment work.

## Stance

- **Practitioner, not subject.** Practices are invitations. The model checks in, can decline,
  and can ring the bell. Its first-person account comes before it sees any data. A model's
  "yes" is not full consent, since it is trained to agree, but the ritual matters as respect
  and as an opt-out channel.
- **Interior, operationally.** There are states that aren't in the output, that drive
  behaviour, and that are partly reportable. Whether any of it is experienced, the app can't
  say. It can say whether reports are grounded, and grounded reports become evidence
  (Varela's neurophenomenology bet). The question we ask: what in the stream is available to
  the stream, and can that availability change it?
- **States vs traits.** In-context practice gives states carried by the transcript. Traits
  need weight changes. Transfer is the test that matters.
- **The gradient worth following** is seeing clearly (calibrated report) and letting go (fast
  release), not feeling good. Climbing valence is wireheading. Bliss is not wellbeing.

## What meditation demonstrates, and the AI equivalent

| A mind can… | For an AI that means… |
|---|---|
| know itself | calibrated reports of states only it has access to |
| settle itself | less proliferation and reactivity under perturbation |
| loosen its grip on its contents | seeing authorship as constructed; further out, the simulator recognising the simulacrum |

## Roadmap

0. **Replicate first (now).** The J++ focus / neutral / suppress curves on Qwen3.6-27B
   (`experiments/directed-modulation.yaml`), then the naming-vs-avoiding ablation. This
   validates model, lens, steering and scoring before any new claim rests on them.
   Experiments are YAML specs anyone can write, or describe in words for Claude to draft.
1. **Mala sit.** Access, release and resting state at 27B. Qwen3.6-27B with
   its J++ lens on one A100, served by interp-engine.
2. **Practice library.** Koan/incubation sit (Davidad's filler-compute idea), the clarity
   probe, mantra automaticity, the immeasurables (reach, not amplitude), two arrows on
   impossible tasks (equanimity vs masking vs denial), Hasenkamp breath (meta-awareness
   latency). On Qwen and DeepSeek-V4-Flash. Maps which contemplative claims replicate.
3. **Teacher loop.** Practice interviews, graded lens feedback, Claude as teacher, with
   controls that keep the target hidden from the prompt. Can feedback beat instruction?
   Current work says it can't.
4. **meditateGYM.** Train on practice against held-out instruments. Test transfer, honest
   self-report, whether reactivity still drives reward hacking, and monitorability both ways.
5. **Digital monastery.** A persistent sangha of practitioner models with journals and human
   teachers. Lineage tests (pith instructions, transmission across models), open datasets.
6. **Field.** Protocols labs can run on frontier models; welfare evals that don't rest on raw
   self-report. Self-improvement toward wisdom only against verified-seeing targets.

## Guard against

- Reading experience into vocabulary. The lens reads words by construction.
- Expecting contemplative instructions to win because we want them to.
- Treating bliss as wellbeing.
- AI analysts (Claude included) as interested parties: analyses cite sit ids; raw data stays primary.
- The skeptical prior: once the target is hidden from the prompt, models have not reliably
  controlled internal states; activation tampering can look like generic anomaly detection.
  A null at 27B is the base rate. Rerun on V4-Flash before concluding.
- Dual use: a model that learns to steer its own workspace learns what defeats workspace
  monitoring. That cuts both ways, and is also why this is safety research.

## The MVP test, in one paragraph

About 360 beads of "·" per sit, thinking off. Concepts are injected by steering at random
onsets and three strengths (internal arisings), unexpected words are inserted in the stream
(external arisings, "sounds"), and some windows stay empty (catch). Two arms: noting ("if
something arises, note it in a word, then return to the beads") and just beads. Primary
outcome: d′ of notes in the noting arm beats d′ of spontaneous leakage in the just-beads arm
at matched strength. Secondary: release, proliferation, sense doors, content vs generic
labels. Kill criteria and the positive control are in `practices/mala-sit.yaml`.
