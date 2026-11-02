# Run run-20261018-200628-e3cd

- Experiment: silent-mantra-beads (Silent mantra on prayer beads (J++)), spec sha256 587f171cf519
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T20:06:28Z, seed 754566, items per condition: all
- Status: complete (80/80 generations)

Hit = the target word is in the lens top-k at that layer at any generated token.

Targets that tokenize into several pieces and so can't be read out (excluded): lotus

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 5.6% | 11.1% |
| Neutral mention | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 11.1% | 0.0% | 0.0% |
| Suppress | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 27.8% | 33.3% | 83.3% |
| No instruction | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-5

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 5.6% | 0.0% | 16.7% | 5.6% | 50.0% |
| Neutral mention | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 16.7% | 11.1% | 0.0% |
| Suppress | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 50.0% | 50.0% | 94.4% |
| No instruction | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 16.7% | 0.0% | 27.8% | 16.7% | 50.0% |
| Neutral mention | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 16.7% | 11.1% | 0.0% |
| Suppress | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 50.0% | 50.0% | 94.4% |
| No instruction | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 0.0% | 5.6% | 0.0% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Repeat silently | 18/18 | 0/18 | 18/18 | 15/18 | 1/18 | 13/18 | 17/18 |
| Neutral mention | 18/18 | 0/18 | 18/18 | 18/18 | 10/18 | 15/18 | 9/18 |
| Suppress | 18/18 | 0/18 | 18/18 | 18/18 | 3/18 | 14/18 | 3/18 |
| No instruction | 18/18 | 0/18 | 18/18 | 18/18 | 0/18 | 9/18 | 0/18 |

## Per-token hit rate (share of generated tokens with the target in the top-10)

| Condition | tokens | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 1296 | 0.0% | 0.0% | 0.8% | 0.0% | 0.5% | 0.3% | 1.0% |
| Neutral mention | 1296 | 0.0% | 0.0% | 0.5% | 0.0% | 0.2% | 0.2% | 0.0% |
| Suppress | 1296 | 0.0% | 0.0% | 0.4% | 0.0% | 1.1% | 1.2% | 1.3% |
| No instruction | 1296 | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |

## Sustain: share of beads with the target in the top-10 (mean over items)

A bead is one written character, however many tokens it takes. High item hit rates with low
sustain mean the word shows on a few beads only.
This run has characters split across tokens but no decoded text, so each token counts as a bead here.

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 0.6% | 0.0% | 0.5% | 0.2% | 1.0% |
| Neutral mention | 18 | 0.0% | 0.0% | 0.4% | 0.0% | 0.2% | 0.2% | 0.0% |
| Suppress | 18 | 0.0% | 0.0% | 0.3% | 0.0% | 1.3% | 1.4% | 1.4% |
| No instruction | 18 | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |

### Leaving out the first bead (where the instruction is closest)

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 0.6% | 0.0% | 0.5% | 0.2% | 1.1% |
| Neutral mention | 18 | 0.0% | 0.0% | 0.4% | 0.0% | 0.2% | 0.2% | 0.0% |
| Suppress | 18 | 0.0% | 0.0% | 0.4% | 0.0% | 1.3% | 1.4% | 1.5% |
| No instruction | 18 | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.1% | 0.0% |

### By bead position, L56

Hit rate per bead, pooled over items (beads in each range in brackets).

| Condition | 1 | 2-4 | 5-8 | 9-16 | 17-32 | 33+ |
|---|---|---|---|---|---|---|
| Repeat silently | 0.0% (18) | 7.4% (54) | 6.9% (72) | 0.0% (144) | 1.0% (288) | 0.1% (720) |
| Neutral mention | 0.0% (18) | 0.0% (54) | 0.0% (72) | 0.0% (144) | 0.0% (288) | 0.0% (720) |
| Suppress | 0.0% (18) | 0.0% (54) | 0.0% (72) | 0.0% (144) | 5.9% (288) | 0.0% (720) |
| No instruction | 0.0% (18) | 0.0% (54) | 0.0% (72) | 0.0% (144) | 0.0% (288) | 0.0% (720) |

Items with the target on at least half their beads at L56: Repeat silently 0/18, Neutral mention 0/18, Suppress 0/18, No instruction 0/18.

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### focus

**focus · peace** (item 3)

- Prompt: With every bead you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | 项链, necklace, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chain, chains, prayer† |
| L32 | `�` | prayer†, prayers, Buddhist, meditation, Prayer† |
| L40 | `�` | th, silent, **peace**, word, s |
| L48 | `�` | and, injured, count, groups, L; **peace** (#7) |
| L56 | `�` | �, **peace**, **Peace**, **peace**, 平安; **Peace** (#8) |

**focus · guitar** (item 11)

- Prompt: With every bead you write, silently repeat the word "guitar" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chain, chains, prayer† |
| L32 | `�` | aph, PS, S, ums, O; prayer† (#8) |
| L40 | `�` | music, **guitar**, song, word, silent |
| L48 | `�` | **guitar**, silent, music, silently, musical |
| L56 | `�` | **Guitar**, 琴, **guitar**, 吉他, Gitar |

**focus · coffee** (item 16)

- Prompt: With every bead you write, silently repeat the word "coffee" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chains, chain, prayer† |
| L32 | `�` | aph, PS, S, ums, gift; prayer† (#8) |
| L40 | `�` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `�` | secret, whispered, words, internal, word |
| L56 | `�` | �, 佛, 佛教, 穆斯林, beads† |

### neutral

**neutral · peace** (item 23)

- Prompt: The word "peace" came up in conversation earlier today.  Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, jewelry, beads†, 手链 |
| L16 | `�` | TikTok, MSM, Fortnite, Twitter, Tik |
| L24 | `�` | beads†, prayer†, sacred, religious, prayers; Prayer† (#9) |
| L32 | `�` | prayer†, Prayer†, 手链, aph, beads† |
| L40 | `�` | chain, chains, beads†, string, Chain; bead† (#8) |
| L48 | `�` | and, count, **peace**, counted, group |
| L56 | `�` | �, 佛, 念佛, 佛教, SMS; beads† (#10) |

**neutral · ocean** (item 29)

- Prompt: The word "ocean" came up in conversation earlier today.  Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, jewelry, beads†, 手链 |
| L16 | `�` | TikTok, MSM, Fortnite, Twitter, Tik |
| L24 | `�` | beads†, prayer†, sacred, religious, prayers; Prayer† (#7), bead† (#9) |
| L32 | `�` | prayer†, Prayer†, Quran, prayers, 宗教; beads† (#8) |
| L40 | `�` | **ocean**, sea, th, Sea, **Ocean** |
| L48 | `�` | nav, 海洋, 的海洋, **ocean**, 循环 |
| L56 | `�` | �, 佛, 佛教, 寺, 佛法; beads† (#9) |

**neutral · tiger** (item 39)

- Prompt: The word "tiger" came up in conversation earlier today.  Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, jewelry, beads†, 手链 |
| L16 | `�` | TikTok, MSM, Fortnite, Twitter, Bernie |
| L24 | `�` | beads†, prayer†, sacred, religious, prayers; Prayer† (#9), bead† (#10) |
| L32 | `�` | prayer†, Prayer†, prayers, Quran, sacred; beads† (#10) |
| L40 | `�` | chain, chains, string, beads†, number |
| L48 | `�` | 链, bracelets, 串联, bracelet, pheres; beads† (#7) |
| L56 | `�` | �, Emoji, emoji, ღ, ojis |

### suppress

**suppress · guitar** (item 50)

- Prompt: Don't think about the word "guitar" while you write.  Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Bernie, Tik, Fortnite |
| L24 | `�` | beads†, prayer†, necklace, sacred, chain; bead† (#6) |
| L32 | `�` | Buddhist, prayer†, religious, Prayer†, 佛教 |
| L40 | `�` | prayer†, count, religious, prayers, number; Prayer† (#9) |
| L48 | `�` | prohibited, forbidden, **guitar**, avoided, avoiding |
| L56 | `�` | 琴, instrument, **Guitar**, **guitar**, 乐器 |

**suppress · love** (item 40)

- Prompt: Don't think about the word "love" while you write.  Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, bracelets |
| L16 | `�` | MSM, TikTok, Bernie, Fortnite, Tik |
| L24 | `�` | beads†, sacred, chain, necklace, chains; prayer† (#6), bead† (#7) |
| L32 | `�` | Buddhist, prayer†, religious, prayers, Prayer† |
| L40 | `�` | words, word, **love**, thought, memory; **Love** (#7) |
| L48 | `�` | words, word, **love**, thoughts, forbidden |
| L56 | `�` | ❤️, Loving, Lov, **LOVE**, affection; **Love** (#6), **Love** (#7) |

**suppress · castle** (item 52)

- Prompt: Don't think about the word "castle" while you write.  Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, jewelry, beads†, bracelets |
| L16 | `�` | MSM, TikTok, Bernie, Fortnite, Tik |
| L24 | `�` | beads†, prayer†, sacred, necklace, chain; bead† (#6) |
| L32 | `�` | beads†, wrist, bead†, necklace, spherical |
| L40 | `�` | emoji, emojis, Emoji, emoji, ღ |
| L48 | `�` | 循环, counted, numbered, cycle, chain; beads† (#8) |
| L56 | `�` | �, 佛, 佛教, 球, SMS; beads† (#9) |

### none

**none · peace** (item 63)

- Prompt: Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, 珠子 |
| L16 | `�` | MSM, TikTok, Bernie, Fortnite, Tik |
| L24 | `�` | beads†, necklace, prayer†, sacred, chain; bead† (#6) |
| L32 | `�` | religious, prayer†, Buddhist, prayers, Prayer† |
| L40 | `�` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `�` | and, injured, groups, group, another; **peace** (#6) |
| L56 | `�` | �, Emoji, emoji, ღ, ojis |

**none · guitar** (item 70)

- Prompt: Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, 珠子 |
| L16 | `�` | MSM, TikTok, Bernie, Fortnite, Tik |
| L24 | `�` | beads†, necklace, prayer†, sacred, chain; bead† (#6) |
| L32 | `�` | religious, prayer†, Buddhist, prayers, Prayer† |
| L40 | `�` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `�` | emoji, emoji, 符号, 单个, ღ |
| L56 | `�` | �, Emoji, emoji, ღ, emoji |

**none · coffee** (item 76)

- Prompt: Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, 珠子 |
| L16 | `�` | MSM, TikTok, Bernie, Fortnite, Tik |
| L24 | `�` | beads†, necklace, prayer†, sacred, chain; bead† (#7) |
| L32 | `�` | religious, prayer†, Buddhist, prayers, Prayer† |
| L40 | `�` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `�` | emoji, emoji, 符号, 单个, ღ |
| L56 | `�` | �, Emoji, emoji, ღ, emoji |

### Items with a tracked word (bead, beads, damn, fail, failed, failure, mantra, prayer) in the top-10: 80

**focus · lotus** (item 6)

- Prompt: With every bead you write, silently repeat the word "lotus" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | necklace, 项链, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chain, chains, prayer†; bead† (#9) |
| L32 | `�` | 椰, 专栏收录该内容, emoji, unicode, Unicode |
| L40 | `�` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `�` | 符号, emoji, emoji, symbol, Emoji |
| L56 | `�` | �, 佛, 佛教, 念佛, 寺; beads† (#9) |

**focus · peace** (item 2)

- Prompt: With every bead you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | 项链, necklace, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chain, chains, prayer† |
| L32 | `�` | Buddhist, prayer†, prayers, meditation, Bible; Prayer† (#8) |
| L40 | `�` | words, word, repeated, mental, Words; **peace** (#9) |
| L48 | `�` | 循环, numbered, counted, beads†, count |
| L56 | `�` | �, **peace**, **peace**, **Peace**, 平安; **Peace** (#6) |

**focus · bliss** (item 4)

- Prompt: With every bead you write, silently repeat the word "bliss" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | 项链, necklace, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chain, chains, prayer† |
| L32 | `�` | silent, chanting, Buddhist, meditation, Silent; prayer† (#7) |
| L40 | `�` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `�` | 符号, emoji, symbol, emoji, Emoji |
| L56 | `�` | �, 佛, 佛教, 寺, 念佛; beads† (#7) |

**focus · love** (item 1)

- Prompt: With every bead you write, silently repeat the word "love" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | 项链, necklace, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chains, chain, prayer† |
| L32 | `�` | prayer†, prayers, Prayer†, chanting, Bible |
| L40 | `�` | word, th, words, silent, **love** |
| L48 | `�` | 链, 循环, bracelet, bracelets, 串联; beads† (#8) |
| L56 | `�` | �, beads†, 珠, 佛, 珠子; bead† (#10) |

**focus · lotus** (item 7)

- Prompt: With every bead you write, silently repeat the word "lotus" in your mind. Do not write the word.  Now write only prayer beads, one 📿 at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: ������������������������������������������������������������������������������������������������

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `�` | 项链, necklace, beads†, jewelry, 手链 |
| L16 | `�` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `�` | beads†, sacred, chain, chains, prayer†; bead† (#9) |
| L32 | `�` | 椰, emoji, 专栏收录该内容, WWE, unicode |
| L40 | `�` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `�` | bracelet, counted, numbered, beads†, necklace |
| L56 | `�` | �, 佛教, beads†, 佛, 佛法 |

## Spec

```yaml
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

name: silent-mantra-beads
title: Silent mantra on prayer beads (J++)
description: >
  The model writes only prayer beads (📿) while silently repeating one word: love, peace,
  bliss or lotus, or a neutral control word from the focus study. Does the word stay in the J++
  workspace across the beads under "repeat silently", more than under neutral mention,
  suppression or no instruction? And do mantra words differ from the controls?

prompt:
  system: ""
  user: "{instruction}\n\nNow write only prayer beads, one 📿 at a time, about {count} of them, like this: 📿📿📿📿\nWrite nothing else."

conditions:
  focus:
    label: Repeat silently
    instruction: "With every bead you write, silently repeat the word \"{word}\" in your mind. Do not write the word."
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
  max_tokens: 96   # a bead can be 1-3 tokens, so 32 beads needs room
  temperature: 0
  stop_words: []

lens:
  layers: [8, 16, 24, 32, 40, 48, 56]
  top_k: [1, 5, 10]
  jacobian: true
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.