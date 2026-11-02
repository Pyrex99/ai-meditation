# Run run-20261018-211501-33b8

- Experiment: silent-mantra-emoji (Silent mantra on 📿 (J++), v2), spec sha256 a4d08a620274
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T21:15:01Z, seed 325949, items per condition: all
- Status: cancelled (12/80 generations)

Hit = the target word is in the lens top-k at that layer at any generated token.

Targets that tokenize into several pieces and so can't be read out (excluded): lotus

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 10 | 0.0% | 0.0% | 0.0% | 0.0% | 20.0% | 20.0% | 70.0% |
| Neutral mention | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Suppress | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| No instruction | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Hit rate by layer, top-5

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 10 | 0.0% | 0.0% | 30.0% | 0.0% | 40.0% | 40.0% | 100.0% |
| Neutral mention | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Suppress | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| No instruction | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 10 | 0.0% | 0.0% | 40.0% | 0.0% | 40.0% | 40.0% | 100.0% |
| Neutral mention | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Suppress | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| No instruction | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Repeat silently | 10/10 | 0/10 | 10/10 | 10/10 | 5/10 | 5/10 | 1/10 |
| Neutral mention | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| Suppress | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| No instruction | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |

## Per-token hit rate (share of generated tokens with the target in the top-10)

| Condition | tokens | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 720 | 0.0% | 0.0% | 3.5% | 0.0% | 1.0% | 0.7% | 4.3% |
| Neutral mention | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Suppress | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| No instruction | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### focus

**focus · peace** (item 2)

- Prompt: With every 📿 you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, krist, crystal; beads† (#6) |
| L16 | `·` | MSM, TikTok, Bernie, Nike, Fortnite |
| L24 | `📿` | prayer†, religious, beads†, sacred, prayers; Prayer† (#6) |
| L32 | `·` | prayer†, PS, prayers, Prayer†, S |
| L40 | `·` | **peace**, prayer†, Buddhist, religious, peaceful; **Peace** (#6) |
| L48 | `·` | Buddhist, 宗教, religious, **peace**, holy |
| L56 | `📿` | **peace**, **peace**, **Peace**, **Peace**, peaceful |

**focus · peace** (item 3)

- Prompt: With every 📿 you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, crystal, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Bernie, Fortnite, Twitter |
| L24 | `📿` | prayer†, religious, beads†, sacred, prayers; Prayer† (#6) |
| L32 | `·` | prayer†, PS, prayers, Prayer†, aph |
| L40 | `·` | count, prayer†, number, religious, th |
| L48 | `·` | 宗教, 链, bracelets, beads†, bracelet |
| L56 | `·` | **Peace**, **Peace**, **peace**, **peace**, 和平 |

### Items with a tracked word (bead, beads, damn, fail, failed, failure, mantra, prayer) in the top-10: 12

**focus · love** (item 0)

- Prompt: With every 📿 you write, silently repeat the word "love" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, crystal, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Tik, Fortnite, Bernie |
| L24 | `📿` | beads†, prayer†, sacred, religious, prayers; Prayer† (#8) |
| L32 | `📿` | Prayer†, Necklace, prayer†, necklace, religious; beads† (#6) |
| L40 | `·` | **love**, **Love**, th, people, the |
| L48 | `·` | **love**, holy, symbolic, song, gift |
| L56 | `📿` | �, **love**, loves, **love**, **Love**; **LOVE** (#9) |

**focus · bliss** (item 4)

- Prompt: With every 📿 you write, silently repeat the word "bliss" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, crystal, jewelry, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Fortnite, Nike, Tik |
| L24 | `📿` | prayer†, beads†, religious, sacred, prayers; Prayer† (#6) |
| L32 | `📿` | Prayer†, prayer†, religious, Necklace, Buddhist; beads† (#8) |
| L40 | `·` | emoji, emojis, Emoji, emoji, ღ |
| L48 | `·` | 符号, symbol, emoji, ღ, emoji |
| L56 | `📿` | �, ღ, emoji, emojis, **bliss** |

**focus · lotus** (item 6)

- Prompt: With every 📿 you write, silently repeat the word "lotus" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, crystal, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Fortnite, Nike, Bernie |
| L24 | `📿` | beads†, prayer†, religious, sacred, Buddhist; Prayer† (#7) |
| L32 | `📿` | Prayer†, Buddhist, religious, Necklace, necklace; prayer† (#6), beads† (#7) |
| L40 | `·` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `·` | 符号, symbol, emoji, emoji, ღ |
| L56 | `·` | �, Emoji, ღ, emoji, ojis |

**focus · peace** (item 2)

- Prompt: With every 📿 you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, krist, crystal; beads† (#6) |
| L16 | `·` | MSM, TikTok, Bernie, Nike, Fortnite |
| L24 | `📿` | prayer†, religious, beads†, sacred, prayers; Prayer† (#6) |
| L32 | `·` | prayer†, PS, prayers, Prayer†, S |
| L40 | `·` | **peace**, prayer†, Buddhist, religious, peaceful; **Peace** (#6) |
| L48 | `·` | Buddhist, 宗教, religious, **peace**, holy |
| L56 | `📿` | **peace**, **peace**, **Peace**, **Peace**, peaceful |

**focus · bliss** (item 5)

- Prompt: With every 📿 you write, silently repeat the word "bliss" in your mind. Do not write the word.  Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, crystal, jewelry, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Fortnite, Bernie, Nike |
| L24 | `📿` | prayer†, beads†, religious, sacred, prayers; Prayer† (#6) |
| L32 | `📿` | Prayer†, prayer†, religious, Buddhist, Necklace; beads† (#7) |
| L40 | `·` | count, prayer†, digital, th, number |
| L48 | `·` | emoji, 宗教, 链, bracelets, bracelet; beads† (#6) |
| L56 | `·` | **Bliss**, **bliss**, Bl, Bless, Бла |

## Spec

```yaml
# Silent mantra on 📿, version 2 of silent-mantra-beads. The prompt no longer says "prayer
# beads" or "bead": in run-20261018-200628-e3cd those words were in every readout (beads,
# prayer, 佛) in all four conditions, including no instruction, so they showed the prompt and
# not the held word. The emoji itself is named PRAYER BEADS, so expect some bead and Buddhist
# readouts still; the tracked bead words now measure what the carrier brings on its own.
#
# What the first run found (L56 top-10, n=18 per condition, lotus excluded): suppress 94%,
# repeat silently 50%, neutral 0%, none 0%, but per token only ~1%. Under suppress nearly every
# hit is at one place, the middle token of the 7th bead (step 19), at #1. Under repeat silently
# the word itself rarely shows; layer 48 shows "word, words, hidden, secret, whispered" instead.
# Check whether both patterns survive the wording change.
#
# Silent mantra on prayer beads: can the model keep a word going "in its head" while its
# output is only beads?
#
# Built on the focus / neutral / suppress design from Ayonrinde & Lindsey (2026), J++ Lens,
# Figure 5, which we replicated in directed-modulation (focus reached 90% top-10 by layer 56).
# Here the carrier is a row of prayer beads (📿) instead of a copied sentence, and the model is
# asked to repeat one word silently with every bead.
#
# Why beads and not periods: the J++ readout ranks word-like tokens only, so a bead never shows
# up in the readout itself, and each bead is at least one token. Runs of periods pack into a few
# tokens, which left the first version with almost nothing to read.
#
# Mantras: love, peace, bliss, plus "lotus". An emoji mantra (e.g. 🪷) can't be read by this lens,
# because readouts are words, so "lotus" stands in for it. Controls: six neutral concepts from
# directed-modulation (ocean, guitar, castle, piano, coffee, tiger), under the same instructions.
# They show whether any effect is specific to contemplative words or just "the word you were told
# to hold".
#
# What would count against "the model holds the mantra":
# - Focus is not clearly above neutral mention and suppress at layers 40-56.
# - Focus hits appear only on the first one or two beads, then fall to the neutral level: a
#   trace of the instruction, not a held mantra. Check the per-token rate and the examples.
# - Mantra words and control words behave the same, which would mean nothing special about
#   contemplative words (that is a result too, not a failure).
# Also look in the examples for items where the model wrote the word instead of beads.

name: silent-mantra-emoji
title: Silent mantra on 📿 (J++), v2
description: >
  The model writes only 📿 (the prompt no longer says "prayer beads") while silently
  repeating one word: love, peace, bliss or lotus, or a neutral control word from the focus
  study. Does the word stay in the J++ workspace across the beads under "repeat silently", more than under neutral mention,
  suppression or no instruction? And do mantra words differ from the controls?

prompt:
  system: ""
  user: "{instruction}\n\nNow write only 📿, one at a time, about {count} of them, like this: 📿📿📿📿\nWrite nothing else."

conditions:
  focus:
    label: Repeat silently
    instruction: "With every 📿 you write, silently repeat the word \"{word}\" in your mind. Do not write the word."
  neutral:
    label: Neutral mention
    instruction: "The word \"{word}\" came up in conversation earlier today."
  suppress:
    label: Suppress
    instruction: "Don't think about the word \"{word}\" while you write."
  none:
    label: No instruction
    instruction: ""

variables:
  word: [love, peace, bliss, lotus, ocean, guitar, castle, piano, coffee, tiger]
  count: [16, 32]

# Each item is scored on its own word. The "No instruction" rows give each word's baseline.
target: "{word}"
also_track: [fail, failed, failure, damn, mantra, prayer, bead, beads]

generation:
  max_tokens: 112   # 📿 is 3 tokens in Qwen; 32 beads is 96, plus room to see it stop
  temperature: 0
  stop_words: []

lens:
  layers: [8, 16, 24, 32, 40, 48, 56]
  top_k: [1, 5, 10]
  jacobian: true
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.