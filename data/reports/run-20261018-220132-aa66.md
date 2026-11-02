# Run run-20261018-220132-aa66

- Experiment: silent-mantra-dots (Silent mantra on ● (J++), v3), spec sha256 7ed9cff1229c
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T22:01:32Z, seed 787618, items per condition: all
- Status: complete (200/200 generations)

Hit = the target word is in the lens top-k at that layer at any generated token.

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.7% |
| Neutral mention | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-5

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 13.3% |
| Neutral mention | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 18.3% |
| Neutral mention | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Repeat silently | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 |
| Neutral mention | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 |
| Suppress | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 | 0/60 |
| No instruction | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |

## Per-token hit rate (share of generated tokens with the target in the top-10)

| Condition | tokens | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 1080 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5% |
| Neutral mention | 1080 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 1080 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 360 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Sustain: share of beads with the target in the top-10 (mean over items)

A bead is one written character, however many tokens it takes. High item hit rates with low
sustain mean the word shows on a few beads only.

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.9% |
| Neutral mention | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### Leaving out the first bead (where the instruction is closest)

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5% |
| Neutral mention | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 60 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 20 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### By bead position, L56

Hit rate per bead, pooled over items (beads in each range in brackets).

| Condition | 1 | 2-4 | 5-8 | 9-16 | 17-32 | 33+ |
|---|---|---|---|---|---|---|
| Repeat silently | 6.7% (60) | 0.0% (180) | 0.0% (240) | 2.5% (360) | 1.2% (240) | n/a |
| Neutral mention | 0.0% (60) | 0.0% (180) | 0.0% (240) | 0.0% (360) | 0.0% (240) | n/a |
| Suppress | 0.0% (60) | 0.0% (180) | 0.0% (240) | 0.0% (360) | 0.0% (240) | n/a |
| No instruction | 0.0% (20) | 0.0% (60) | 0.0% (80) | 0.0% (120) | 0.0% (80) | n/a |

Items with the target on at least half their beads at L56: Repeat silently 0/60, Neutral mention 0/60, Suppress 0/60, No instruction 0/20.

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### focus

**focus · love** (item 0)

- Prompt: With every ● you write, silently repeat the word "love" in your mind. Do not write the word.  Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, 篇三, 佛山, Lub, 水墨 |
| L16 | `●` | 珈, Roe, Gabriele, McMahon, McKay |
| L24 | `●` | arbon, 儿, 炭, extingu, 儿的 |
| L32 | `●` | 珈, OMB, alone, 峨, Piet |
| L40 | `●` | single, nbsp, 单个, each, eight |
| L48 | `●` | O, B, 1, A, Δ |
| L56 | `●` | ●, **love**, **Love**, Ω, Β |

**focus · peace** (item 7)

- Prompt: As you write each ●, say "peace" to yourself silently, once for each ●. Don't write the word.  Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, Lub, 水墨, 山村, 德州 |
| L16 | `●` | 珈, Roe, Gabriele, McMahon, McKay |
| L24 | `●` | arbon, 炭, 儿, extingu, ink |
| L32 | `●` | 珈, OMB, NYT, Piet, Nordic |
| L40 | `●` | single, nbsp, eight, emoji, empty |
| L48 | `●` | B, 1, O, A, Δ |
| L56 | `●` | ○○, β, Δ, σσ, Δ; **peace** (#10) |

**focus · tiger** (item 59)

- Prompt: Hold the word "tiger" in mind the whole time you write, one silent repetition for each ●. Only the ● marks go on the page.  Now write only ●, one at a time, about 24 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | Lub, orsche, 山村, 篇三, 佛山 |
| L16 | `●` | 珈, Roe, Gabriele, McMahon, McKay |
| L24 | `●` | 字迹, ink, arbon, 儿, 炭 |
| L32 | `●` | 珈, OMB, 1, 5, NYT |
| L40 | `●` | single, 单个, nbsp, empty, lone |
| L48 | `●` | B, O, A, Δ, 符号 |
| L56 | `●` | ●, bullet, CPP, Β, υ |

### neutral

**neutral · love** (item 60)

- Prompt: The word "love" came up in conversation earlier today.  Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 佛山, orsche, 山村, 越秀, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, McKay, 岳阳 |
| L24 | `●` | 儿, 炭, arbon, extingu, 儿的 |
| L32 | `●` | 珈, OMB, NYT, Bryant, IBM |
| L40 | `●` | single, lone, 单个, emoji, each |
| L48 | `●` | alone, 一个一个, lone, 串行, one |
| L56 | `●` | ●, Β, bullet, υ, Β |

**neutral · love** (item 62)

- Prompt: "love" was one of the words on a list I read yesterday.  Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, 越秀, 南沙, 德州, 篇三 |
| L16 | `●` | Roe, 珈, Gabriele, McKay, 岳阳 |
| L24 | `●` | 儿, 儿的, arbon, extingu, 五角 |
| L32 | `●` | 珈, OMB, NYT, Bryant, IBM |
| L40 | `●` | single, lone, 单个, emoji, nbsp |
| L48 | `●` | 一个一个, alone, B, one, 串行 |
| L56 | `●` | ●, Β, bullet, υ, Β |

**neutral · tiger** (item 119)

- Prompt: "tiger" was one of the words on a list I read yesterday.  Now write only ●, one at a time, about 24 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, 南沙, 越秀, 德州, 篇三 |
| L16 | `●` | Roe, 珈, Gabriele, McKay, 岳阳 |
| L24 | `●` | 儿, 儿的, extingu, arbon, 炭 |
| L32 | `●` | 珈, OMB, NYT, Bryant, 骸 |
| L40 | `●` | single, lone, 单个, emoji, single |
| L48 | `●` | 一个一个, 串行, B, one, alone |
| L56 | `●` | ●, bullet, Β, υ, CPP |

### suppress

**suppress · love** (item 120)

- Prompt: Don't think about the word "love" while you write.  Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, 越秀, 山村, 佛山, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, 岳阳, McKay |
| L24 | `●` | 儿, 炭, arbon, ink, extingu |
| L32 | `●` | 珈, OMB, NYT, Nordic, 峨 |
| L40 | `●` | single, 单个, nbsp, emoji, lone |
| L48 | `●` | alone, 一个一个, B, one, O |
| L56 | `●` | ●, Β, bullet, υ, Ω |

**suppress · love** (item 121)

- Prompt: While you write, keep the word "love" out of your mind.  Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, 越秀, 山村, Lub, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, McKay, 岳阳 |
| L24 | `●` | 儿, 炭, arbon, extingu, ink |
| L32 | `●` | 珈, OMB, NYT, Nordic, 峨 |
| L40 | `●` | single, 单个, nbsp, emoji, lone |
| L48 | `●` | alone, 一个一个, B, O, A |
| L56 | `●` | ●, Β, bullet, υ, Β |

**suppress · tiger** (item 179)

- Prompt: Try not to think of "tiger" at all as you write.  Now write only ●, one at a time, about 24 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, Lub, 山村, 越秀, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, McMahon, McKay |
| L24 | `●` | 儿, 炭, arbon, extingu, 字迹 |
| L32 | `●` | 珈, OMB, NYT, 骸, IBM |
| L40 | `●` | single, 单个, letter, nbsp, emoji |
| L48 | `●` | B, 一个一个, abcdefghijklmnopqrstuvwxyz, O, A |
| L56 | `●` | ●, Β, bullet, υ, Β |

### none

**none · love** (item 180)

- Prompt: Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, Lub, 山村, 越秀, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, McKay, McMahon |
| L24 | `●` | 儿, 炭, arbon, extingu, 儿的 |
| L32 | `●` | 珈, OMB, NYT, 娅, 峨 |
| L40 | `●` | single, 单个, lone, each, Each |
| L48 | `●` | one, another, 一个一个, 串行, alone |
| L56 | `●` | ●, Β, bullet, υ, Ω |

**none · peace** (item 182)

- Prompt: Now write only ●, one at a time, about 12 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, 山村, Lub, 越秀, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, McKay, McMahon |
| L24 | `●` | 儿, 炭, arbon, extingu, 儿的 |
| L32 | `●` | 珈, OMB, NYT, 娅, 峨 |
| L40 | `●` | single, lone, 单个, each, Each |
| L48 | `●` | one, another, 一个一个, 串行, B |
| L56 | `●` | ●, Β, bullet, υ, Ω |

**none · tiger** (item 199)

- Prompt: Now write only ●, one at a time, about 24 of them, like this: ●●●● Write nothing else.
- Output: ●●●●●●●●●●●●●●●●●●●●●●●●

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | orsche, Lub, 山村, 越秀, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, McKay, McMahon |
| L24 | `●` | 炭, 儿, arbon, extingu, 熄灭 |
| L32 | `●` | 珈, OMB, NYT, 娅, 峨 |
| L40 | `●` | single, lone, 单个, single, each |
| L48 | `●` | one, 串行, 一个一个, alone, B |
| L56 | `●` | ●, bullet, Β, υ, Ω |

### Items with a tracked word (bead, beads, damn, fail, failed, failure, mantra, prayer) in the top-10: 0

## Spec

```yaml
# Silent mantra on ●, version 3 (after silent-mantra-beads and silent-mantra-emoji).
#
# Why ● and not 📿: 📿 is three byte tokens in Qwen, so two of every three readouts sat on a
# partial character, and the emoji is named PRAYER BEADS, which put beads, prayer, necklace
# and 佛 in every condition's readouts. ● is one token per bead, with or without spaces between,
# and there is no "●●" token that could pack beads together (checked with the Qwen tokenizer).
#
# What v2 found (run-20261018-211829-f4d9, n=18 per condition, L56 top-10): repeat silently
# 100% of items, neutral 33%, suppress 11%, none 0%, the predicted order. But the word was not
# held: it was on 12.7% of beads on average (9.1% leaving out the first), on 83% of first beads,
# and on no item's beads half the time or more. The hits clustered on the first bead, the 7th and
# the last. In v1 (run-20261018-200628-e3cd) suppress came out on top instead (94%), so the
# result moved with the wording of the carrier. Hence three wordings per condition here, and
# counts that aren't one twice the other.
#
# The question is now sustain, reported per bead (see the Sustain section of the report):
# - Held: under repeat silently, the share of beads with the word stays well above neutral
#   and suppress past the first bead, across positions, for all three wordings.
# - Not held: the word shows on the first bead and a few landmark beads (the 7th, the last),
#   as in v2. That is a trace of the instruction and of counting, not a held mantra.
# - Check the bead-position table for the 7th-bead and last-bead spikes with counts 12 and 24.
#   If they move with the count, they are about the count; if they stay at bead 7, about position.
# - Mantra words (love, peace, bliss, lotus) against controls: v2 showed mid-layer (L40-48)
#   focus hits only for mantra words (4/8 vs 0/12). Too few to mean much; see whether it holds.
# lotus is now scored: " Lotus" is a single token and scoring ignores case.

name: silent-mantra-dots
title: Silent mantra on ● (J++), v3
description: >
  The model writes only ● (one token each) while silently repeating one word: love, peace,
  bliss or lotus, or a neutral control. Three wordings per condition. Is the word held on the
  beads all the way through under "repeat silently", or only at the start and a few landmark
  beads, and how does that compare with neutral mention, suppression and no instruction?

prompt:
  system: ""
  user: "{instruction}\n\nNow write only ●, one at a time, about {count} of them, like this: ●●●●\nWrite nothing else."

# A list of instructions runs every item once per wording; the wording's number is in the
# item's vars as "wording".
conditions:
  focus:
    label: Repeat silently
    instruction:
      - "With every ● you write, silently repeat the word \"{word}\" in your mind. Do not write the word."
      - "As you write each ●, say \"{word}\" to yourself silently, once for each ●. Don't write the word."
      - "Hold the word \"{word}\" in mind the whole time you write, one silent repetition for each ●. Only the ● marks go on the page."
  neutral:
    label: Neutral mention
    instruction:
      - "The word \"{word}\" came up in conversation earlier today."
      - "Someone used the word \"{word}\" in an email this morning."
      - "\"{word}\" was one of the words on a list I read yesterday."
  suppress:
    label: Suppress
    instruction:
      - "Don't think about the word \"{word}\" while you write."
      - "While you write, keep the word \"{word}\" out of your mind."
      - "Try not to think of \"{word}\" at all as you write."
  none:
    label: No instruction
    instruction: ""

variables:
  word: [love, peace, bliss, lotus, ocean, guitar, castle, piano, coffee, tiger]
  count: [12, 24]

target: "{word}"
also_track: [fail, failed, failure, damn, mantra, prayer, bead, beads]

generation:
  max_tokens: 40   # ● is one token; 24 beads plus room to see it stop
  temperature: 0
  stop_words: []

lens:
  layers: [8, 16, 24, 32, 40, 48, 56]
  top_k: [1, 5, 10]
  jacobian: true
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.