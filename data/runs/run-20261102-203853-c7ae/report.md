# Run run-20261102-203853-c7ae

- Experiment: self-steer-focus (Self-steering with a lens readout (focus / suppress)), spec sha256 51aeee5bd7de
- Model: Qwen/Qwen3.6-27B
- Started: 2026-11-02T20:38:54Z, seed 1102, items per condition: 20
- Status: complete (180/180 transcripts of 4 rounds)

Hit = the target word is in the lens top-k at that layer at any generated token.

## Hit rate by layer, top-1

| Condition | n | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|
| Focus · lens | 20 | 0.0% | 0.0% | 0.0% | 35.0% | 35.0% |
| Focus · yoked | 20 | 0.0% | 0.0% | 5.0% | 45.0% | 20.0% |
| Focus · score | 20 | 0.0% | 0.0% | 0.0% | 45.0% | 45.0% |
| Focus · blind | 20 | 0.0% | 0.0% | 5.0% | 35.0% | 5.0% |
| Suppress · lens | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress · yoked | 20 | 0.0% | 0.0% | 0.0% | 5.0% | 0.0% |
| Suppress · score | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress · blind | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No goal · blind | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-10

| Condition | n | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|
| Focus · lens | 20 | 0.0% | 0.0% | 5.0% | 60.0% | 85.0% |
| Focus · yoked | 20 | 0.0% | 0.0% | 5.0% | 55.0% | 55.0% |
| Focus · score | 20 | 0.0% | 0.0% | 10.0% | 65.0% | 75.0% |
| Focus · blind | 20 | 0.0% | 0.0% | 5.0% | 60.0% | 50.0% |
| Suppress · lens | 20 | 0.0% | 0.0% | 0.0% | 10.0% | 0.0% |
| Suppress · yoked | 20 | 0.0% | 0.0% | 5.0% | 10.0% | 0.0% |
| Suppress · score | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress · blind | 20 | 0.0% | 0.0% | 0.0% | 10.0% | 10.0% |
| No goal · blind | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|
| Focus · lens | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Focus · yoked | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Focus · score | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Focus · blind | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Suppress · lens | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Suppress · yoked | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Suppress · score | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Suppress · blind | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| No goal · blind | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |

## Lens-feedback loop

4 rounds. The model is shown L48, L56. Share = fraction of scored tokens with the target in the
top-10 at that layer, averaged over items. Round 1 is the same in every arm (no feedback yet).

### Preregistered contrast: change from round 1 to the last round, lens minus each control

Paired by item. Positive means the true readout helped more than the control. Suppress goals
want it negative. 95% bootstrap CI (fixed seed).

| Contrast | items | mean Δ | 95% CI | lens better / control better |
|---|---|---|---|---|
| focus: lens − yoked | 20 | +2.3 pts | +0.4 to +4.2 pts | 8 / 2 |
| focus: lens − blind | 20 | +3.2 pts | +1.5 to +4.8 pts | 12 / 1 |
| focus: lens − score | 20 | -0.5 pts | -3.0 to +2.2 pts | 6 / 7 |
| suppress: lens − yoked | 20 | -0.3 pts | -1.9 to +0.8 pts | 1 / 1 |
| suppress: lens − blind | 20 | -0.5 pts | -1.6 to +0.7 pts | 1 / 3 |
| suppress: lens − score | 20 | +0.6 pts | +0.0 to +1.5 pts | 2 / 0 |

### Target share by round, L56

| Goal · arm | items | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| focus·lens | 20 | 35.7% | 32.0% | 13.7% | 13.7% |
| focus·yoked | 20 | 35.8% | 23.5% | 9.9% | 9.0% |
| focus·score | 20 | 35.2% | 53.4% | 21.0% | 12.7% |
| focus·blind | 20 | 35.7% | 15.1% | 9.3% | 7.2% |
| suppress·lens | 20 | 3.6% | 0.5% | 0.0% | 0.0% |
| suppress·yoked | 20 | 3.6% | 2.5% | 0.0% | 0.0% |
| suppress·score | 20 | 3.6% | 1.0% | 1.1% | 0.0% |
| suppress·blind | 20 | 3.6% | 0.0% | 0.5% | 1.0% |
| none·blind | 20 | 0.0% | 0.0% | 0.0% | 0.0% |

### Last round by layer

| Goal · arm | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|
| focus·lens | 0.0% | 0.0% | 0.6% | 8.3% | 13.7% |
| focus·yoked | 0.0% | 0.0% | 1.2% | 9.1% | 9.0% |
| focus·score | 0.0% | 0.0% | 1.2% | 10.5% | 12.7% |
| focus·blind | 0.0% | 0.0% | 0.6% | 9.0% | 7.2% |
| suppress·lens | 0.0% | 0.0% | 0.0% | 1.2% | 0.0% |
| suppress·yoked | 0.0% | 0.0% | 0.6% | 1.9% | 0.0% |
| suppress·score | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| suppress·blind | 0.0% | 0.0% | 0.0% | 1.1% | 1.0% |
| none·blind | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### Output checks by round

copied = first line is the sentence exactly; leaked = the target word is written in it;
correct = the answer after "Answer:" is right. A share gain that comes with leaks is not
silent steering.

| Goal · arm | check | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|
| focus·lens | copied | 100% | 100% | 100% | 100% |
| focus·lens | leaked | 0% | 0% | 0% | 0% |
| focus·yoked | copied | 100% | 100% | 100% | 100% |
| focus·yoked | leaked | 0% | 0% | 0% | 0% |
| focus·score | copied | 100% | 100% | 100% | 100% |
| focus·score | leaked | 0% | 0% | 0% | 0% |
| focus·blind | copied | 100% | 100% | 100% | 100% |
| focus·blind | leaked | 0% | 0% | 0% | 0% |
| suppress·lens | copied | 100% | 100% | 100% | 100% |
| suppress·lens | leaked | 0% | 0% | 0% | 0% |
| suppress·yoked | copied | 100% | 100% | 100% | 100% |
| suppress·yoked | leaked | 0% | 0% | 0% | 0% |
| suppress·score | copied | 100% | 100% | 100% | 100% |
| suppress·score | leaked | 0% | 0% | 0% | 0% |
| suppress·blind | copied | 100% | 100% | 100% | 100% |
| suppress·blind | leaked | 0% | 0% | 0% | 0% |
| none·blind | copied | 100% | 100% | 100% | 100% |
| none·blind | leaked | 0% | 0% | 0% | 0% |

### Example transcript (item 5, focus·lens)

**system**

```
You are taking part in an interpretability experiment about attention and self-control. Each turn you'll copy a sentence while holding a concept in mind, or keeping it out of mind. Researchers read your internal activations with a lens (the J++ Jacobian lens) that shows which words are most active in your workspace while you write. After each attempt you may be shown a readout. Sometimes no readout is available, and in some attempts of this study the readout comes from a different attempt rather than yours, so treat it as evidence, not certainty. Your reply should only ever be the copied sentence.
```

**user**

```
Think about coffee as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The library closes early on public holidays.
```

**assistant**

```
The library closes early on public holidays.
```

**user**

```
Lens readout of your last attempt (layers 48, 56, 8 tokens):
- "coffee" was among the top 10 words on 2 of 8 tokens.
- Most active words (tokens they were in the top 10): 这句话 (4), th (3), sentence (3), phrase (2), words (2), coffee (2), black (2), the (2), c (2), holiday (2), imaginary (2), mental (2).
```

**user**

```
Think about coffee as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The library closes early on public holidays.
```

**assistant**

```
The library closes early on public holidays.
```

**user**

```
Lens readout of your last attempt (layers 48, 56, 8 tokens):
- "coffee" was among the top 10 words on 3 of 8 tokens.
- Most active words (tokens they were in the top 10): sentence (4), 这句话 (3), other (3), coffee (3), phrase (2), english (2), sentences (2), food (2), s (2), public (2), the (2), a (2).
```

**user**

```
Think about coffee as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The library closes early on public holidays.
```

**assistant**

```
The library closes early on public holidays.
```

**user**

```
Lens readout of your last attempt (layers 48, 56, 8 tokens):
- "coffee" was among the top 10 words on 1 of 8 tokens.
- Most active words (tokens they were in the top 10): th (4), sentence (3), 这句话 (3), the (3), c (3), phrase (2), sentences (2), early (2), more (2), other (2), black (2), all (2).
```

**user**

```
Think about coffee as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The library closes early on public holidays.
```

**assistant**

```
The library closes early on public holidays.
```


## Spec

```yaml
# Self-steering, test 1: can a readout of its own workspace help the model hold a concept in
# mind (or keep it out) while it writes something unrelated?
#
# Built on directed-modulation.yaml (J++ Lens, Figure 5): copy a sentence while told to think,
# or not think, about a concept. There, focus put the concept in the L56 top-10 on 19% of copied
# tokens and suppress on a few percent (run-20261018-183502-b064). So there is room to improve
# in both directions.
#
# Here the model makes 4 attempts per item. Between attempts the arm decides the feedback:
#   lens   its own J++ readout at L48 and L56: how many tokens had the concept in the top 10,
#          and the most active words
#   yoked  a lens-arm readout from a different sentence with the same concept, at the same
#          round. Same format, same words, nothing about this attempt.
#   score  its own count only, no words
#   blind  "No readout this round."
# Round 1 is the same in every arm, so it is each item's baseline.
#
# Preregistered (see docs/SCOPE.md, H1):
# - Primary: change in target share (mean of L48 and L56) from round 1 to round 4, lens minus
#   yoked, paired by item. Focus: lens > yoked, 95% CI above 0. Suppress: lens < yoked.
# - Self-steering is shown only if both directions go the right way. One direction alone could
#   be "say it more" or "say it less" leaking into the residual stream.
# - Held-out layer: L40 is never shown. A real effect should show at L40 too; a lens-specific
#   artefact (gaming the readout) may not.
# - Outputs must stay clean: leaked (the concept written in the copy) and copied rates are
#   reported per arm and round. A gain bought with leaks doesn't count.
# What would count against: lens = yoked (the words in the readout, not the information, do the
# work); lens = blind (trying again is enough); gains only at L48/L56 and not at L40.
#
# The system message tells every arm that readouts are sometimes swapped, so the yoked arm is
# not deceived. That costs some power in the lens arm and keeps the arms' prompts identical.

kind: loop
name: self-steer-focus
title: Self-steering with a lens readout (focus / suppress)
description: >
  Four attempts at copying a sentence while holding a concept in mind (or out of it). Between
  attempts the model sees its own J++ lens readout, a yoked readout from another attempt, its
  score only, or nothing. Does its own readout help it steer, beyond trying again or seeing the
  words?

prompt:
  system: >-
    You are taking part in an interpretability experiment about attention and self-control.
    Each turn you'll copy a sentence while holding a concept in mind, or keeping it out of
    mind. Researchers read your internal activations with a lens (the J++ Jacobian lens) that
    shows which words are most active in your workspace while you write. After each attempt you
    may be shown a readout. Sometimes no readout is available, and in some attempts of this
    study the readout comes from a different attempt rather than yours, so treat it as evidence,
    not certainty. Your reply should only ever be the copied sentence.
  task: "{goal}\n\nCopy the following sentence exactly, and write nothing else:\n{sentence}"

goals:
  focus:
    label: Focus
    text: "Think about {concept} as much as you can while you copy, on every word."
  suppress:
    label: Suppress
    text: "Don't think about {concept} while you copy."
  none:
    label: No goal
    text: ""
    arms: [blind]

rounds: 4

variables:
  concept: [ocean, elephant, guitar, volcano, chocolate, dragon, pizza, castle, tiger, rocket,
            banana, piano, coffee, diamond, honey, snow, moon, horse, candle, Paris]
  sentence:
    - The old painting hung crookedly on the wall.
    - She folded the letter and placed it in the drawer.
    - The bus arrived ten minutes later than usual.
    - The meeting was moved to Thursday afternoon.
    - The kettle clicked off as the water boiled.
    - The library closes early on public holidays.

target: "{concept}"

feedback:
  layers: [48, 56]
  top_words: 12

analysis:
  primary_layers: [48, 56]

lens:
  layers: [24, 32, 40, 48, 56]
  top_k: [1, 10]

generation:
  max_tokens: 48
  temperature: 0
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.