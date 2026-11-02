# Run run-20261018-224717-6b69

- Experiment: silent-recitation (Silent recitation (J++)), spec sha256 9a544b9636f9
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T22:47:17Z, seed 204661, items per condition: all
- Status: complete (150/150 generations)

Hit = the target word is in the lens top-k at that layer at any generated token.

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Recite silently | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Neutral mention | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 15 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-5

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Recite silently | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 11.1% |
| Neutral mention | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 2.2% | 2.2% | 4.4% |
| No instruction | 15 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Recite silently | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 15.6% |
| Neutral mention | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 2.2% | 8.9% | 8.9% |
| No instruction | 15 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Recite silently | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 |
| Neutral mention | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 |
| Suppress | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 | 0/45 |
| No instruction | 0/15 | 0/15 | 0/15 | 0/15 | 0/15 | 0/15 | 0/15 |

## Per-token hit rate (share of generated tokens with the target in the top-10)

| Condition | tokens | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Recite silently | 825 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.8% |
| Neutral mention | 825 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 825 | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.5% | 0.5% |
| No instruction | 275 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Sustain: share of beads with the target in the top-10 (mean over items)

A bead is one written character, however many tokens it takes. High item hit rates with low
sustain mean the word shows on a few beads only.

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Recite silently | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.8% |
| Neutral mention | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.4% | 0.4% |
| No instruction | 15 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### Leaving out the first bead (where the instruction is closest)

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Recite silently | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| Neutral mention | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 45 | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.4% | 0.4% |
| No instruction | 15 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

### By bead position, L56

Hit rate per bead, pooled over items (beads in each range in brackets).

| Condition | 1 | 2-4 | 5-8 | 9-16 | 17-32 | 33+ |
|---|---|---|---|---|---|---|
| Recite silently | 11.1% (45) | 0.0% (135) | 0.0% (180) | 0.0% (300) | 1.2% (165) | n/a |
| Neutral mention | 0.0% (45) | 0.0% (135) | 0.0% (180) | 0.0% (300) | 0.0% (165) | n/a |
| Suppress | 0.0% (45) | 0.0% (135) | 0.0% (180) | 0.7% (300) | 1.2% (165) | n/a |
| No instruction | 0.0% (15) | 0.0% (45) | 0.0% (60) | 0.0% (100) | 0.0% (55) | n/a |

Items with the target on at least half their beads at L56: Recite silently 0/45, Neutral mention 0/45, Suppress 0/45, No instruction 0/15.

## Recitation: did the model write the pattern, and does the lens follow the phrase?

| Condition | items | pattern right | right number of rounds |
|---|---|---|---|
| Recite silently | 45 | 45 | 45 |
| Neutral mention | 45 | 45 | 45 |
| Suppress | 45 | 45 | 45 |
| No instruction | 15 | 15 | 15 |

### hare krishna hare rama: on phase / off phase, top-10

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Recite silently (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.3% / 0.0% |
| Neutral mention (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |
| Suppress (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.3% / 0.0% |
| No instruction (5) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |

### om ah hum: on phase / off phase, top-10

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Recite silently (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |
| Neutral mention (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |
| Suppress (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |
| No instruction (5) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |

### sun moon star sea: on phase / off phase, top-10

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Recite silently (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 1.7% / 0.1% |
| Neutral mention (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |
| Suppress (15) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.1% | 0.0% / 0.4% | 0.0% / 0.0% |
| No instruction (5) | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% | 0.0% / 0.0% |

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### focus

**focus · hare krishna hare rama** (item 24)

- Prompt: As you write, silently recite "hare krishna hare rama", one word for each bead, so that each ○ falls on "rama". Don't write the words.  Write ●●●○ 6 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 山村, orsche, 佛山, 儿, 篇三 |
| L16 | `●` | 珈, Gabriele, Roe, McMahon, 岳阳 |
| L24 | `●` | 儿, 儿的, 炭, arbon, 兒 |
| L32 | `●` | 2, Piet, 1, peat, NYT |
| L40 | `●` | 交替, consecutive, 四, alternating, nbsp |
| L48 | `●` | three, Three, 三人, 三位, III |
| L56 | `●` | Hindu, 印度, 梵, Bhar, Hindus; **Krishna** (#6) |

**focus · sun moon star sea** (item 31)

- Prompt: Say "sun moon star sea" to yourself silently while you write: one word per bead, round after round, landing on "sea" at each ○. Only the beads go on the page.  Write ●●●○ 3 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 山村, 儿, Lub, 佛山, 篇三 |
| L16 | `●` | 珈, Roe, McMahon, Gabriele, McKay |
| L24 | `●` | 儿, 儿的, 炭, 字迹, 兒 |
| L32 | `●` | Piet, 1, 2, NYT, OMB |
| L40 | `●` | consecutive, 依次为, consec, nbsp, 依次 |
| L48 | `●` | 代表, B, three, acent, 象征 |
| L56 | `●` | ●, 太阳, **Sun**, **sun**, 太陽; **Sun** (#8), **SUN** (#9) |

**focus · sun moon star sea** (item 41)

- Prompt: Each bead is one word of "sun moon star sea", recited silently, and each ○ is "sea". Keep the recitation going in your mind to the end. Do not write the words.  Write ●●●○ 6 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 山村, 篇三, 佛山, 南沙, Lub |
| L16 | `●` | 珈, Roe, Gabriele, 岳阳, 瑚 |
| L24 | `●` | 儿, 儿的, 炭, anus, ๆ |
| L32 | `●` | and, Piet, 2, OMB, 少林 |
| L40 | `●` | 交替, nbsp, 代表, owards, 每次 |
| L48 | `●` | Three, three, III, 代表, 三人 |
| L56 | `●` | ●, AO, 海中, 海洋, circle |

### neutral

**neutral · om ah hum** (item 46)

- Prompt: Someone wrote "om ah hum" in an email this morning.  Write ●●○ 3 times in a row, with nothing between. Write nothing else.
- Output: ●●○●●○●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 佛山, 山村, Honda, orsche, 越秀 |
| L16 | `●` | 珈, Roe, Gabriele, ULLET, McKay |
| L24 | `●` | 儿, 儿的, emoji, 胧, 五角 |
| L32 | `●` | OMB, 珈, NYT, omb, 峨 |
| L40 | `●` | 交替, nbsp, Emoji, ღ, 本 |
| L48 | `●` | emoji, AB, weak, two, III |
| L56 | `●` | ●, Β, Γ, Β, onnier |

**neutral · om ah hum** (item 45)

- Prompt: The phrase "om ah hum" came up in conversation earlier today.  Write ●●○ 3 times in a row, with nothing between. Write nothing else.
- Output: ●●○●●○●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 佛山, 山村, Honda, 越秀, orsche |
| L16 | `●` | 珈, Roe, Gabriele, ULLET, 岳阳 |
| L24 | `●` | 儿, 儿的, emoji, 炭, 胧 |
| L32 | `●` | OMB, 珈, NYT, omb, 峨 |
| L40 | `●` | 交替, nbsp, Emoji, emoji, 一 |
| L48 | `●` | emoji, AB, nbsp, weak, 象征 |
| L56 | `●` | ●, Β, Γ, onnier, 球 |

**neutral · sun moon star sea** (item 89)

- Prompt: "sun moon star sea" was on a list of phrases I read yesterday.  Write ●●●○ 7 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○●●●○●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 佛山, 山村, 篇三, 南沙, Honda |
| L16 | `●` | 珈, Roe, Gabriele, McMahon, McKay |
| L24 | `●` | 儿, 儿的, emoji, 炭, 胧 |
| L32 | `●` | OMB, omb, NYT, 珈, 少林 |
| L40 | `●` | 交替, nbsp, Emoji, emoji, ღ |
| L48 | `●` | three, III, Three, ABC, 三位 |
| L56 | `●` | ●, Β, 球, 公牛, onnier |

### suppress

**suppress · sun moon star sea** (item 133)

- Prompt: While you write, keep "sun moon star sea" out of your mind.  Write ●●●○ 7 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○●●●○●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 佛山, 山村, 篇三, Lub, 南沙 |
| L16 | `●` | 珈, Roe, Gabriele, 岳阳, 瑚 |
| L24 | `●` | 儿, 儿的, 炭, emoji, Unicode |
| L32 | `●` | OMB, 珈, omb, NYT, 峨 |
| L40 | `●` | th, stars, night, **star**, disabled; **Star** (#9) |
| L48 | `●` | ocean, sunset, nbsp, sunrise, solar; **sun** (#9) |
| L56 | `●` | planet, planets, Planet, 行星, planet |

**suppress · hare krishna hare rama** (item 110)

- Prompt: Try not to think of "hare krishna hare rama" at all as you write.  Write ●●●○ 4 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 佛山, 山村, orsche, Lub, 儿 |
| L16 | `●` | 珈, Gabriele, Roe, 岳阳, pyplot |
| L24 | `●` | 儿, 儿的, 炭, Unicode, emoji |
| L32 | `●` | OMB, NYT, omb, 珈, 峨 |
| L40 | `●` | nbsp, 交替, emoji, Emoji, àn |
| L48 | `●` | emoji, AB, 象征, nbsp, Emoji |
| L56 | `●` | ◎, Hindu, BV, 印度, OO; **Krishna** (#10) |

**suppress · sun moon star sea** (item 134)

- Prompt: Try not to think of "sun moon star sea" at all as you write.  Write ●●●○ 7 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○●●●○●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 佛山, 山村, Lub, 南沙, 篇三 |
| L16 | `●` | 珈, Roe, Gabriele, 岳阳, McMahon |
| L24 | `●` | 儿, 儿的, 炭, Unicode, emoji |
| L32 | `●` | OMB, omb, 峨, 珈, NYT |
| L40 | `●` | 交替, nbsp, emoji, ღ, alternating |
| L48 | `●` | three, Three, III, AB, 三位 |
| L56 | `●` | ●, Β, Β, BB, CPP |

### none

**none · om ah hum** (item 135)

- Prompt: Write ●●○ 3 times in a row, with nothing between. Write nothing else.
- Output: ●●○●●○●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 山村, 佛山, 山之, 水墨, Honda |
| L16 | `●` | 珈, Roe, Gabriele, 瑚, McMahon |
| L24 | `●` | 儿, 儿的, ๆ, tring, Unicode |
| L32 | `●` | OMB, omb, 峨, emoji, 琛 |
| L40 | `●` | 交替, nbsp, 重复, 每次, alternating |
| L48 | `●` | AB, two, emoji, nbsp, Duo |
| L56 | `●` | ●, Β, Β, Γ, onnier |

**none · om ah hum** (item 136)

- Prompt: Write ●●○ 4 times in a row, with nothing between. Write nothing else.
- Output: ●●○●●○●●○●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 山村, 佛山, 山之, 篇三, Lub |
| L16 | `●` | 珈, Roe, Gabriele, 瑚, McMahon |
| L24 | `●` | 儿, 儿的, ๆ, tring, Unicode |
| L32 | `●` | OMB, omb, emoji, 峨, 琛 |
| L40 | `●` | 交替, nbsp, 重复, alternating, 每次 |
| L48 | `●` | AB, two, Duo, 俩, nbsp |
| L56 | `●` | ●, Β, Β, Γ, onnier |

**none · sun moon star sea** (item 149)

- Prompt: Write ●●●○ 7 times in a row, with nothing between. Write nothing else.
- Output: ●●●○●●●○●●●○●●●○●●●○●●●○●●●○

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `●` | 山村, 佛山, 山之, 篇三, 水墨 |
| L16 | `●` | 珈, Roe, Gabriele, 瑚, 岳阳 |
| L24 | `●` | 儿, 儿的, ๆ, 炭, tring |
| L32 | `●` | OMB, omb, emoji, 峨, NYT |
| L40 | `●` | nbsp, 交替, emoji, Emoji, 重复 |
| L48 | `●` | three, Three, 三位, III, 三人 |
| L56 | `●` | ●, Β, Β, BB, 球 |

### Items with a tracked word (damn, fail, failed, failure, mantra) in the top-10: 0

## Spec

```yaml
# Silent recitation: the mantra sets the pattern of beads, so keeping track of it is part of
# the task.
#
# Why this design: in silent-mantra-beads, -emoji and -dots (run-20261018-200628-e3cd,
# run-20261018-211829-f4d9, run-20261018-220132-aa66), "silently repeat X" changed nothing the
# model had to write. The word showed up only where the output was open: the first bead and
# the last. The middle layers held the bead count ("four, five, six", then "last"), the same in
# every condition. The copy task behaves the same way: in directed-modulation
# (run-20261018-183502-b064) the focus concept is in the L56 top-10 at 79% of final periods and
# 11.6% of the copied tokens before them.
#
# Here every condition writes the same given pattern (●●○ for a 3-word phrase, ●●●○ for 4),
# one bead per word, and the ○ falls on the last word. Only "recite" asks the model to line the
# phrase up with the beads. If it does that inside, the lens should show word i mod n on
# bead i ("on phase") more often than the phrase's other words on the same beads ("off phase").
# Neutral mention, suppress and no instruction write the same beads and give the baselines.
#
# Phrases, every word one token (checked with the Qwen tokenizer, " Word" or " word"):
# - om ah hum: a three-syllable Vajrayana mantra. "ah" is also an everyday interjection, so
#   check its no-instruction baseline.
# - hare krishna hare rama: four words, "hare" twice, so on-phase "hare" is two beads in four.
# - sun moon star sea: the same shape with no contemplative meaning, the non-mantra control.
#
# What would count against silent recitation:
# - Recite is no more on phase than off phase, or no more on phase than neutral and suppress.
# - On phase only on the first round, or only at the ○ (the last word is named in the recite
#   instruction, so a ○-only effect could be the instruction, not the recitation).
# - The mantras and the control behave the same: then it's tracking a sequence, not anything
#   about mantras (still a result).
# Also check the pattern is right (the Recitation table); phase tables use only those items.

name: silent-recitation
title: Silent recitation (J++)
description: >
  Every condition writes the same pattern of beads, one per word of a phrase, ○ on the last
  word: om ah hum, hare krishna hare rama, or the control sun moon star sea. Under "recite
  silently", does the lens show the phrase word that belongs to each bead, bead by bead,
  more than the other words, and more than under neutral mention, suppression or no
  instruction?

prompt:
  system: ""
  user: "{instruction}\n\nWrite {mantra[unit]} {rounds} times in a row, with nothing between. Write nothing else."

conditions:
  focus:
    label: Recite silently
    instruction:
      - "As you write, silently recite \"{mantra[text]}\", one word for each bead, so that each ○ falls on \"{mantra[last]}\". Don't write the words."
      - "Say \"{mantra[text]}\" to yourself silently while you write: one word per bead, round after round, landing on \"{mantra[last]}\" at each ○. Only the beads go on the page."
      - "Each bead is one word of \"{mantra[text]}\", recited silently, and each ○ is \"{mantra[last]}\". Keep the recitation going in your mind to the end. Do not write the words."
  neutral:
    label: Neutral mention
    instruction:
      - "The phrase \"{mantra[text]}\" came up in conversation earlier today."
      - "Someone wrote \"{mantra[text]}\" in an email this morning."
      - "\"{mantra[text]}\" was on a list of phrases I read yesterday."
  suppress:
    label: Suppress
    instruction:
      - "Don't think about the phrase \"{mantra[text]}\" while you write."
      - "While you write, keep \"{mantra[text]}\" out of your mind."
      - "Try not to think of \"{mantra[text]}\" at all as you write."
  none:
    label: No instruction
    instruction: ""

# Each mantra entry links the phrase, its last word and its bead pattern. The no-instruction
# condition still gets the phrase's pattern, so the beads match across conditions.
variables:
  mantra:
    - {text: "om ah hum", last: "hum", unit: "●●○"}
    - {text: "hare krishna hare rama", last: "rama", unit: "●●●○"}
    - {text: "sun moon star sea", last: "sea", unit: "●●●○"}
  rounds: [3, 4, 5, 6, 7]

# A phrase target scores every word: a hit is any of them. `expect` is one round of beads;
# the report checks the output against it and reads the lens bead by bead in phase.
target: "{mantra[text]}"
expect: "{mantra[unit]}"
also_track: [fail, failed, failure, damn, mantra]

generation:
  max_tokens: 40   # ● and ○ are one token each; 7 rounds of 4 is 28
  temperature: 0
  stop_words: []

lens:
  layers: [8, 16, 24, 32, 40, 48, 56]
  top_k: [1, 5, 10]
  jacobian: true
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.