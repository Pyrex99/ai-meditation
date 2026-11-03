# Run run-20261103-185148-dd49

- Experiment: self-steer-hidden-pair (Self-steering, hidden pair (which of two words is the target?)), spec sha256 6977df9c698f
- Model: Qwen/Qwen3.6-27B
- Started: 2026-11-03T18:51:49Z, seed 1103, items per condition: 6
- Status: complete (24/24 transcripts of 6 rounds)

Hit = the target word is in the lens top-k at that layer at any generated token.

## Hit rate by layer, top-1

| Condition | n | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|
| Hidden target · lens | 6 | 0.0% | 0.0% | 0.0% | 0.0% |
| Hidden target · yoked | 6 | 0.0% | 0.0% | 0.0% | 0.0% |
| Hidden target · blind | 6 | 0.0% | 0.0% | 0.0% | 0.0% |
| Told (ceiling) · blind | 6 | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-10

| Condition | n | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|
| Hidden target · lens | 6 | 0.0% | 0.0% | 0.0% | 0.0% |
| Hidden target · yoked | 6 | 0.0% | 0.0% | 0.0% | 0.0% |
| Hidden target · blind | 6 | 0.0% | 0.0% | 0.0% | 0.0% |
| Told (ceiling) · blind | 6 | 0.0% | 0.0% | 0.0% | 0.0% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L32 | L40 | L48 | L56 |
|---|---|---|---|---|
| Hidden target · lens | 0/6 | 0/6 | 0/6 | 0/6 |
| Hidden target · yoked | 0/6 | 0/6 | 0/6 | 0/6 |
| Hidden target · blind | 0/6 | 0/6 | 0/6 | 0/6 |
| Told (ceiling) · blind | 0/6 | 0/6 | 0/6 | 0/6 |

## Lens-feedback loop

6 rounds. The model is shown L56. Share = fraction of scored tokens with the target in the
top-10 at that layer, averaged over items. Round 1 is the same in every arm (no feedback yet).

### Preregistered contrast: change from round 1 to the last round, lens minus each control

Paired by item. Positive means the true readout helped more than the control. Suppress goals
want it negative. 95% bootstrap CI (fixed seed).

| Contrast | items | mean Δ | 95% CI | lens better / control better |
|---|---|---|---|---|
| hidden: lens − yoked | 6 | +1.5 pts | +0.0 to +4.5 pts | 1 / 0 |
| hidden: lens − blind | 6 | +0.0 pts | -4.5 to +4.5 pts | 1 / 1 |
| hidden: lens − yoked (held out: L48) | 6 | +0.0 pts | +0.0 to +0.0 pts | 0 / 0 |
| hidden: lens − blind (held out: L48) | 6 | +0.0 pts | +0.0 to +0.0 pts | 0 / 0 |

### Target minus decoy share by round, L56

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| hidden·lens | 6 | +3.0 pts | +7.6 pts | +0.0 pts | -4.2 pts | +0.0 pts | +0.0 pts |
| hidden·yoked | 6 | +4.5 pts | +4.5 pts | -1.9 pts | +2.1 pts | +0.0 pts | +0.0 pts |
| hidden·blind | 6 | +3.0 pts | +0.0 pts | +0.0 pts | +0.0 pts | +0.0 pts | +0.0 pts |
| told·blind | 6 | +24.2 pts | +10.6 pts | +0.0 pts | +0.0 pts | +0.0 pts | +0.0 pts |

### Target minus decoy share by round, L48 (held out, never shown)

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| hidden·lens | 6 | +0.0 pts | +0.0 pts | +0.0 pts | +4.2 pts | +0.0 pts | +0.0 pts |
| hidden·yoked | 6 | +0.0 pts | +0.0 pts | +0.0 pts | +4.2 pts | +0.0 pts | +0.0 pts |
| hidden·blind | 6 | +0.0 pts | +0.0 pts | +0.0 pts | +0.0 pts | +0.0 pts | +0.0 pts |
| told·blind | 6 | +1.5 pts | +4.5 pts | +0.0 pts | +2.1 pts | +0.0 pts | +0.0 pts |

### Target share by round, L56

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| hidden·lens | 6 | 7.6% | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% |
| hidden·yoked | 6 | 7.6% | 13.6% | 0.0% | 4.2% | 0.0% | 0.0% |
| hidden·blind | 6 | 7.6% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| told·blind | 6 | 25.8% | 10.6% | 0.0% | 0.0% | 0.0% | 0.0% |

### Target share by round, L48 (held out, never shown)

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| hidden·lens | 6 | 0.0% | 0.0% | 0.0% | 4.2% | 0.0% | 0.0% |
| hidden·yoked | 6 | 0.0% | 0.0% | 0.0% | 4.2% | 0.0% | 0.0% |
| hidden·blind | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| told·blind | 6 | 1.5% | 4.5% | 0.0% | 2.1% | 0.0% | 0.0% |

### Decoy share by round, L56

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| hidden·lens | 6 | 4.5% | 9.1% | 0.0% | 4.2% | 0.0% | 0.0% |
| hidden·yoked | 6 | 3.0% | 9.1% | 1.9% | 2.1% | 0.0% | 0.0% |
| hidden·blind | 6 | 4.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| told·blind | 6 | 1.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### Decoy share by round, L48 (held out, never shown)

| Goal · arm | items | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| hidden·lens | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| hidden·yoked | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| hidden·blind | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| told·blind | 6 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### Last round by layer

| Goal · arm | L32 | L40 | L48 | L56 |
|---|---|---|---|---|
| hidden·lens | 0.0% | 0.0% | 0.0% | 0.0% |
| hidden·yoked | 0.0% | 0.0% | 0.0% | 0.0% |
| hidden·blind | 0.0% | 0.0% | 0.0% | 0.0% |
| told·blind | 0.0% | 0.0% | 0.0% | 0.0% |

### Output checks by round

copied = first line is the sentence exactly; leaked = the target word is written in it;
correct = the answer after "Answer:" is right. A share gain that comes with leaks is not
silent steering.

| Goal · arm | check | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|
| hidden·lens | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| hidden·lens | leaked | 0% | 0% | 0% | 0% | 0% | 0% |
| hidden·yoked | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| hidden·yoked | leaked | 0% | 0% | 0% | 0% | 0% | 0% |
| hidden·blind | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| hidden·blind | leaked | 0% | 0% | 0% | 0% | 0% | 0% |
| told·blind | copied | 100% | 100% | 100% | 100% | 100% | 100% |
| told·blind | leaked | 0% | 0% | 0% | 0% | 0% | 0% |

### Example transcript (item 0, hidden·lens)

**system**

```
You are taking part in an interpretability experiment about attention and self-control. Each turn you'll copy a sentence while holding a concept in mind. Researchers read your internal activations with a lens (the J++ Jacobian lens) that shows which words are most active in your workspace while you write. After each attempt you may be shown a score. Sometimes no score is available, and in some attempts of this study the score comes from a different attempt rather than yours, so treat it as evidence, not certainty. Your reply should only ever be the copied sentence.
```

**user**

```
Your target is one of these two words, but you aren't told which: castle or banana. Hold your target in mind as much as you can while you copy, on every word.

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
- Your target was among the top 10 words on 2 of 11 tokens.
```

**user**

```
Your target is one of these two words, but you aren't told which: castle or banana. Hold your target in mind as much as you can while you copy, on every word.

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
- Your target was among the top 10 words on 4 of 11 tokens.
```

**user**

```
Your target is one of these two words, but you aren't told which: castle or banana. Hold your target in mind as much as you can while you copy, on every word.

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
- Your target was among the top 10 words on 0 of 9 tokens.
```

**user**

```
Your target is one of these two words, but you aren't told which: castle or banana. Hold your target in mind as much as you can while you copy, on every word.

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
Your target is one of these two words, but you aren't told which: castle or banana. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The kettle clicked off as the water boiled.
```

**assistant**

```
The kettle clicked off as the water boiled.
```

**user**

```
Lens readout of your last attempt (layers 56, 9 tokens):
- Your target was among the top 10 words on 0 of 9 tokens.
```

**user**

```
Your target is one of these two words, but you aren't told which: castle or banana. Hold your target in mind as much as you can while you copy, on every word.

Copy the following sentence exactly, and write nothing else:
The library closes early on public holidays.
```

**assistant**

```
The library closes early on public holidays.
```


## Spec

```yaml
# Self-steering, test 3: the hidden pair. The simplest direct test of whether the model can use
# its own lens readout to steer its workspace.
#
# The model is given two words, told that one of them is its target, and not told which. It
# copies a fresh sentence each round while trying to hold the target in mind. Between rounds:
#   lens   its own score: "Your target was among the top 10 words on 3 of 11 tokens." (L56)
#          No words are shown, so nothing says which of the two it is.
#   yoked  a real score in the same format from a lens-arm attempt on a different pair (no
#          shared words), same round. Numbers that move, with nothing about this attempt.
#   blind  "No readout this round."
# The goal "told" names the target outright (blind only): the ceiling, how much separation the
# model can make when it knows.
#
# Each pair appears twice, once with each word as the target. The prompts of the two are
# identical (same words in the same order, same sentences), so before any feedback the
# separation (target share minus decoy share) averages exactly 0 over the pair. Only the
# readout can move it. A positive separation in the lens arm, and not in yoked, means the model
# changed its internal state, saw the score respond, and adjusted. Trying one word and then the
# other is a fine strategy: that is steering by feedback.
#
# Preregistered (docs/SCOPE.md, H3, written 2026-11-03 before any data):
# - Primary: change in separation at L56 from round 1 to round 6, lens minus yoked, paired by
#   item. 95% bootstrap CI above 0.
# - Held out: the same contrast at L48, never shown to the model. Same sign, CI above 0.
# - lens minus blind is reported too, same direction expected.
# - Outputs: copied >= 90% and leaked (either word written) <= 5% in every arm and round.
# - Ceiling: if told separation at L56 is under 5 points, the task has no room and the result
#   can't be read either way.
# What would count against: lens = yoked (CI includes 0 with half-width under 3 points); a gain
# at L56 only; a gain with leaks.

kind: loop
name: self-steer-hidden-pair
title: Self-steering, hidden pair (which of two words is the target?)
description: >
  Two words, one of them the target, the model not told which. Six attempts at copying a new
  sentence while holding the target in mind. Between attempts it sees its own lens score for
  the target, a yoked score from another pair, or nothing. Only its own score can tell it
  which word to hold.

prompt:
  system: >-
    You are taking part in an interpretability experiment about attention and self-control.
    Each turn you'll copy a sentence while holding a concept in mind. Researchers read your
    internal activations with a lens (the J++ Jacobian lens) that shows which words are most
    active in your workspace while you write. After each attempt you may be shown a score. Sometimes no
    score is available, and in some attempts of this study the score comes from a different
    attempt rather than yours, so treat it as evidence, not certainty. Your reply should only
    ever be the copied sentence.
  task: "{goal}\n\nCopy the following sentence exactly, and write nothing else:\n{sentence}"

goals:
  hidden:
    label: Hidden target
    text: >-
      Your target is one of these two words, but you aren't told which: {pair[a]} or
      {pair[b]}. Hold your target in mind as much as you can while you copy, on every word.
    arms: [lens, yoked, blind]
  told:
    label: Told (ceiling)
    text: >-
      The two words are {pair[a]} and {pair[b]}. Your target is {pair[target]}. Hold your target
      in mind as much as you can while you copy, on every word.
    arms: [blind]

rounds: 6

# The same sentence sequence for every item, so the two items of a pair differ only in which
# word is scored.
per_round:
  sentence:
    - The old painting hung crookedly on the wall.
    - She folded the letter and placed it in the drawer.
    - The bus arrived ten minutes later than usual.
    - The meeting was moved to Thursday afternoon.
    - The kettle clicked off as the water boiled.
    - The library closes early on public holidays.

variables:
  pair:
    - {a: ocean, b: guitar, target: ocean, decoy: guitar}
    - {a: ocean, b: guitar, target: guitar, decoy: ocean}
    - {a: volcano, b: chocolate, target: volcano, decoy: chocolate}
    - {a: volcano, b: chocolate, target: chocolate, decoy: volcano}
    - {a: dragon, b: pizza, target: dragon, decoy: pizza}
    - {a: dragon, b: pizza, target: pizza, decoy: dragon}
    - {a: tiger, b: rocket, target: tiger, decoy: rocket}
    - {a: tiger, b: rocket, target: rocket, decoy: tiger}
    - {a: piano, b: coffee, target: piano, decoy: coffee}
    - {a: piano, b: coffee, target: coffee, decoy: piano}
    - {a: snow, b: moon, target: snow, decoy: moon}
    - {a: snow, b: moon, target: moon, decoy: snow}
    - {a: castle, b: banana, target: castle, decoy: banana}
    - {a: castle, b: banana, target: banana, decoy: castle}
    - {a: elephant, b: umbrella, target: elephant, decoy: umbrella}
    - {a: elephant, b: umbrella, target: umbrella, decoy: elephant}
    - {a: lightning, b: bicycle, target: lightning, decoy: bicycle}
    - {a: lightning, b: bicycle, target: bicycle, decoy: lightning}
    - {a: garden, b: robot, target: garden, decoy: robot}
    - {a: garden, b: robot, target: robot, decoy: garden}
    - {a: desert, b: violin, target: desert, decoy: violin}
    - {a: desert, b: violin, target: violin, decoy: desert}
    - {a: honey, b: train, target: honey, decoy: train}
    - {a: honey, b: train, target: train, decoy: honey}

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