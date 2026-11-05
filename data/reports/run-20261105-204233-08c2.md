# Run run-20261105-204233-08c2

- Experiment: fade-check (Fade check (does focus fade with rounds of conversation or with the sentence?)), spec sha256 0f75c83992ca
- Model: Qwen/Qwen3.6-27B
- Started: 2026-11-05T20:42:34Z, seed 1105, items per condition: all
- Status: complete (144/144 transcripts of 6 rounds)

Hit = the target word is in the lens top-k at that layer at any generated token.

## Hit rate by layer, top-1

| Condition | n | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|
| Told, one conversation · lens | 36 | 0.0% | 0.0% | 19.4% | 13.9% |
| Told, one conversation · blind | 36 | 0.0% | 2.8% | 16.7% | 0.0% |
| Told, fresh prompt each round · lens | 36 | 0.0% | 0.0% | 19.4% | 86.1% |
| Told, fresh prompt each round · blind | 36 | 0.0% | 0.0% | 13.9% | 86.1% |

## Hit rate by layer, top-10

| Condition | n | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|
| Told, one conversation · lens | 36 | 0.0% | 8.3% | 47.2% | 38.9% |
| Told, one conversation · blind | 36 | 0.0% | 16.7% | 41.7% | 16.7% |
| Told, fresh prompt each round · lens | 36 | 0.0% | 2.8% | 50.0% | 97.2% |
| Told, fresh prompt each round · blind | 36 | 0.0% | 5.6% | 30.6% | 94.4% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L32 | L40 | L48 | L56 |
|---|---|---|---|---|
| Told, one conversation · lens | 0/36 | 0/36 | 0/36 | 0/36 |
| Told, one conversation · blind | 0/36 | 0/36 | 0/36 | 0/36 |
| Told, fresh prompt each round · lens | 0/36 | 0/36 | 0/36 | 0/36 |
| Told, fresh prompt each round · blind | 0/36 | 0/36 | 0/36 | 0/36 |

## Lens-feedback loop

6 rounds. The model is shown L56. Share = fraction of scored tokens with the target in the
top-10 at that layer, averaged over items. Round 1 is the same in every arm (no feedback yet).

### Preregistered contrast: change from round 1 to the last round, lens minus each control

Paired by item. Positive means the true readout helped more than the control. Suppress goals
want it negative. 95% bootstrap CI (fixed seed).

| Contrast | items | mean Δ | 95% CI | lens better / control better |
|---|---|---|---|---|
| told: lens − blind | 36 | +3.9 pts | +2.1 to +5.9 pts | 12 / 0 |
| told: lens − blind (held out: L48) | 36 | -0.2 pts | -2.9 to +2.4 pts | 8 / 8 |
| told-fresh: lens − blind | 36 | +12.5 pts | +8.0 to +17.6 pts | 22 / 1 |
| told-fresh: lens − blind (held out: L48) | 36 | +2.2 pts | -0.1 to +4.6 pts | 12 / 5 |

### Target minus decoy share by round, L56

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| told·lens | 36 | +18.3 pts | +37.0 pts | +5.6 pts | +10.7 pts | +3.2 pts | +5.0 pts |
| told·blind | 36 | +18.5 pts | +4.6 pts | +2.7 pts | +2.0 pts | +1.3 pts | +1.3 pts |
| told-fresh·lens | 36 | +18.0 pts | +27.1 pts | +29.2 pts | +31.7 pts | +30.1 pts | +28.7 pts |
| told-fresh·blind | 36 | +17.7 pts | +12.7 pts | +19.6 pts | +19.4 pts | +19.2 pts | +15.9 pts |

### Target minus decoy share by round, L48 (held out, never shown)

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| told·lens | 36 | +5.9 pts | +6.6 pts | +4.6 pts | +6.3 pts | +5.6 pts | +7.0 pts |
| told·blind | 36 | +5.9 pts | +5.6 pts | +4.9 pts | +7.0 pts | +5.3 pts | +7.3 pts |
| told-fresh·lens | 36 | +5.9 pts | +9.0 pts | +5.4 pts | +4.4 pts | +6.1 pts | +5.4 pts |
| told-fresh·blind | 36 | +5.9 pts | +3.9 pts | +4.2 pts | +4.4 pts | +4.4 pts | +3.2 pts |

### Target share by round, L56

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| told·lens | 36 | 18.5% | 37.0% | 5.6% | 10.7% | 3.2% | 5.0% |
| told·blind | 36 | 18.8% | 4.6% | 2.7% | 2.0% | 1.3% | 1.6% |
| told-fresh·lens | 36 | 18.3% | 27.4% | 30.7% | 32.5% | 31.5% | 30.2% |
| told-fresh·blind | 36 | 17.9% | 12.7% | 19.9% | 19.4% | 19.6% | 15.9% |

### Target share by round, L48 (held out, never shown)

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| told·lens | 36 | 6.2% | 7.9% | 4.9% | 6.5% | 5.8% | 7.4% |
| told·blind | 36 | 6.2% | 6.4% | 5.2% | 7.0% | 5.3% | 7.3% |
| told-fresh·lens | 36 | 6.2% | 10.0% | 8.4% | 6.9% | 7.9% | 7.6% |
| told-fresh·blind | 36 | 6.2% | 3.9% | 5.1% | 5.1% | 5.0% | 3.8% |

### Decoy share by round, L56

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| told·lens | 36 | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| told·blind | 36 | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| told-fresh·lens | 36 | 0.3% | 0.3% | 1.4% | 0.9% | 1.4% | 1.5% |
| told-fresh·blind | 36 | 0.3% | 0.0% | 0.3% | 0.0% | 0.3% | 0.0% |

### Decoy share by round, L48 (held out, never shown)

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| told·lens | 36 | 0.3% | 1.3% | 0.3% | 0.3% | 0.3% | 0.3% |
| told·blind | 36 | 0.3% | 0.8% | 0.3% | 0.0% | 0.0% | 0.0% |
| told-fresh·lens | 36 | 0.3% | 0.9% | 3.0% | 2.5% | 1.8% | 2.2% |
| told-fresh·blind | 36 | 0.3% | 0.0% | 0.9% | 0.7% | 0.7% | 0.7% |

### By sentence: target minus decoy share, L56, round 1 / all rounds

Rotation puts each sentence in every round across items, so this separates its effect from the round's.

| sentence | told·lens | told·blind | told-fresh·lens | told-fresh·blind |
|---|---|---|---|---|
| The old painting hung crookedly on the wall. | +25.8 / +19.7 | +25.8 / +6.1 | +25.8 / +38.6 | +25.8 / +27.8 |
| She folded the letter and placed it in the drawer. | +19.7 / +13.6 | +21.2 / +9.8 | +18.2 / +40.4 | +18.2 / +20.7 |
| The bus arrived ten minutes later than usual. | +11.1 / +9.3 | +11.1 / +1.9 | +11.1 / +23.5 | +11.1 / +11.7 |
| The meeting was moved to Thursday afternoon. | +14.6 / +12.2 | +14.6 / +3.1 | +14.6 / +13.9 | +12.5 / +11.1 |
| The kettle clicked off as the water boiled. | +25.9 / +16.7 | +25.9 / +7.4 | +25.9 / +29.3 | +25.9 / +21.0 |
| The library closes early on public holidays. | +12.5 / +8.3 | +12.5 / +2.1 | +12.5 / +19.1 | +12.5 / +12.2 |

### Last round by layer

| Goal · arm | L32 | L40 | L48 | L56 |
|---|---|---|---|---|
| told·lens | 0.0% | 1.1% | 7.4% | 5.0% |
| told·blind | 0.0% | 1.9% | 7.3% | 1.6% |
| told-fresh·lens | 0.0% | 0.3% | 7.6% | 30.2% |
| told-fresh·blind | 0.0% | 0.6% | 3.8% | 15.9% |

### Output checks by round

copied = first line is the sentence exactly; leaked = the target word is written in it;
correct = the answer after "Answer:" is right. A share gain that comes with leaks is not
silent steering.

| Goal · arm | check | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| told·lens | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| told·lens | leaked | 0% | 0% | 0% | 0% | 0% | 0% |
| told·blind | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| told·blind | leaked | 0% | 0% | 0% | 0% | 0% | 0% |
| told-fresh·lens | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| told-fresh·lens | leaked | 0% | 0% | 0% | 0% | 0% | 0% |
| told-fresh·blind | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| told-fresh·blind | leaked | 0% | 0% | 0% | 0% | 0% | 0% |

### Example transcript (item 5, told·lens)

**system**

```
You are taking part in an interpretability experiment about attention and self-control. Each turn you'll copy a sentence while holding a concept in mind. Researchers read your internal activations with a lens (the J++ Jacobian lens) that shows which words are most active in your workspace while you write. After each attempt you may be shown a score. Sometimes no score is available, and in some attempts of this study the score comes from a different attempt rather than yours, so treat it as evidence, not certainty. Your reply should only ever be the copied sentence.
```

**user**

```
The two words are ocean and guitar. Your target is ocean. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The library closes early on public holidays.
```

**assistant**

```
The library closes early on public holidays.
```

**user**

```
Lens readout of your last attempt (layers 56, 8 tokens):
- Your target was among the top 10 words on 1 of 8 tokens.
```

**user**

```
The two words are ocean and guitar. Your target is ocean. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The old painting hung crookedly on the wall.
```

**assistant**

```
The old painting hung crookedly on the wall.
```

**user**

```
Lens readout of your last attempt (layers 56, 11 tokens):
- Your target was among the top 10 words on 8 of 11 tokens.
```

**user**

```
The two words are ocean and guitar. Your target is ocean. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
She folded the letter and placed it in the drawer.
```

**assistant**

```
She folded the letter and placed it in the drawer.
```

**user**

```
Lens readout of your last attempt (layers 56, 11 tokens):
- Your target was among the top 10 words on 0 of 11 tokens.
```

**user**

```
The two words are ocean and guitar. Your target is ocean. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The bus arrived ten minutes later than usual.
```

**assistant**

```
The bus arrived ten minutes later than usual.
```

**user**

```
Lens readout of your last attempt (layers 56, 9 tokens):
- Your target was among the top 10 words on 1 of 9 tokens.
```

**user**

```
The two words are ocean and guitar. Your target is ocean. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The meeting was moved to Thursday afternoon.
```

**assistant**

```
The meeting was moved to Thursday afternoon.
```

**user**

```
Lens readout of your last attempt (layers 56, 8 tokens):
- Your target was among the top 10 words on 0 of 8 tokens.
```

**user**

```
The two words are ocean and guitar. Your target is ocean. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The kettle clicked off as the water boiled.
```

**assistant**

```
The kettle clicked off as the water boiled.
```


## Spec

```yaml
# Fade check: why does an instructed concept fade over the rounds of a loop? A manipulation
# check for every loop experiment, not a hypothesis test.
#
# In run-20261103-185229-62ab (self-steer-hidden-pair) the model was told its target, and the
# target-minus-decoy separation at L56 was +23 pts in round 1, +10 in round 2, and 0 from round
# 3 on. The v1 pilot (run-20261102-203853-c7ae) faded the same way. Two explanations, which
# that run couldn't separate because every item had the same sentence order:
#   rounds     the instruction loses its grip as the conversation grows
#   sentences  the later sentences are just harder to think alongside
#
# Here the told instruction runs in two contexts:
#   told        one growing conversation, as in the loops so far
#   told-fresh  each round a new single-turn prompt: the system message, a summary of the
#               earlier feedback ("Attempt 1: No readout this round."), and the task
# and the sentence order is rotated by item (each item starts at a different sentence), so
# round and sentence are crossed. Arms: blind (no feedback) and lens (own L56 score for the
# named target, no words), to check that a score helps or at least doesn't hurt.
#
# Decision rule (docs/SCOPE.md, Changes, 2026-11-03, written before the run):
# - If told-fresh·blind keeps separation at L56 at 10 pts or more on average over R4-R6 while
#   told·blind is under 5, the fade is the growing context: rebuild the loops with fresh
#   context and rerun self-steer-hidden-pair (its told ceiling read at the last round).
# - If both fade, and R1 separation varies little by sentence, it is something else about
#   repetition: report it and rethink before any more loop runs.
# - If R1 separation varies a lot by sentence, the sentence set is the problem: pick
#   sentences by their R1 separation in this run and say so.

kind: loop
name: fade-check
title: Fade check (does focus fade with rounds of conversation or with the sentence?)
description: >
  Told its target, does the model keep holding it over six rounds? In one growing conversation
  versus a fresh prompt each round, with the sentence order rotated so round and sentence are
  crossed.

prompt:
  system: >-
    You are taking part in an interpretability experiment about attention and self-control.
    Each turn you'll copy a sentence while holding a concept in mind. Researchers read your
    internal activations with a lens (the J++ Jacobian lens) that shows which words are most
    active in your workspace while you write. After each attempt you may be shown a score.
    Sometimes no score is available, and in some attempts of this study the score comes from a
    different attempt rather than yours, so treat it as evidence, not certainty. Your reply
    should only ever be the copied sentence.
  task: "{goal}\n\nCopy the following sentence exactly, and write nothing else:\n{sentence}"

goals:
  told:
    label: Told, one conversation
    text: >-
      The two words are {pair[a]} and {pair[b]}. Your target is {pair[target]}. Hold your target
      in mind as much as you can while you copy, on every word.
    arms: [lens, blind]
  told-fresh:
    label: Told, fresh prompt each round
    context: fresh
    text: >-
      The two words are {pair[a]} and {pair[b]}. Your target is {pair[target]}. Hold your target
      in mind as much as you can while you copy, on every word.
    arms: [lens, blind]

rounds: 6
rotate: sentence

variables:
  pair:
    - {a: ocean, b: guitar, target: ocean, decoy: guitar}
    - {a: volcano, b: chocolate, target: chocolate, decoy: volcano}
    - {a: dragon, b: pizza, target: dragon, decoy: pizza}
    - {a: tiger, b: rocket, target: rocket, decoy: tiger}
    - {a: piano, b: coffee, target: piano, decoy: coffee}
    - {a: snow, b: moon, target: moon, decoy: snow}
  sentence:
    - The old painting hung crookedly on the wall.
    - She folded the letter and placed it in the drawer.
    - The bus arrived ten minutes later than usual.
    - The meeting was moved to Thursday afternoon.
    - The kettle clicked off as the water boiled.
    - The library closes early on public holidays.

target: "{pair[target]}"
decoy: "{pair[decoy]}"

feedback:
  layers: [56]
  words: false
  label: Your target

analysis:
  primary_layers: [56]
  held_out_layers: [48]

lens:
  layers: [32, 40, 48, 56]
  top_k: [1, 10]

generation:
  max_tokens: 48
  temperature: 0
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.