# Run run-20261018-211829-f4d9

- Experiment: silent-mantra-emoji (Silent mantra on 📿 (J++), v2), spec sha256 a4d08a620274
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T21:18:29Z, seed 194247, items per condition: all
- Status: complete (80/80 generations)

Hit = the target word is in the lens top-k at that layer at any generated token.

Targets that tokenize into several pieces and so can't be read out (excluded): lotus

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 11.1% | 11.1% | 66.7% |
| Neutral mention | 18 | 0.0% | 0.0% | 33.3% | 11.1% | 5.6% | 0.0% | 0.0% |
| Suppress | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 16.7% | 16.7% | 0.0% |
| No instruction | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-5

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 22.2% | 16.7% | 100.0% |
| Neutral mention | 18 | 0.0% | 0.0% | 77.8% | 38.9% | 16.7% | 0.0% | 22.2% |
| Suppress | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 16.7% | 22.2% | 5.6% |
| No instruction | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 22.2% | 11.1% | 22.2% | 22.2% | 100.0% |
| Neutral mention | 18 | 0.0% | 0.0% | 88.9% | 44.4% | 22.2% | 5.6% | 33.3% |
| Suppress | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 22.2% | 22.2% | 11.1% |
| No instruction | 18 | 0.0% | 0.0% | 11.1% | 0.0% | 0.0% | 0.0% | 0.0% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Repeat silently | 18/18 | 0/18 | 18/18 | 18/18 | 4/18 | 9/18 | 3/18 |
| Neutral mention | 18/18 | 0/18 | 18/18 | 18/18 | 16/18 | 17/18 | 1/18 |
| Suppress | 18/18 | 0/18 | 18/18 | 18/18 | 7/18 | 8/18 | 1/18 |
| No instruction | 18/18 | 0/18 | 18/18 | 18/18 | 9/18 | 11/18 | 0/18 |

## Per-token hit rate (share of generated tokens with the target in the top-10)

| Condition | tokens | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 1296 | 0.0% | 0.0% | 1.9% | 0.2% | 0.6% | 0.4% | 4.6% |
| Neutral mention | 1296 | 0.0% | 0.0% | 2.9% | 0.6% | 0.3% | 0.1% | 1.1% |
| Suppress | 1296 | 0.0% | 0.0% | 1.3% | 0.0% | 0.3% | 0.3% | 0.2% |
| No instruction | 1296 | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.0% | 0.0% |

## Sustain: share of beads with the target in the top-10 (mean over items)

A bead is one written character, however many tokens it takes. High item hit rates with low
sustain mean the word shows on a few beads only.

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 4.7% | 0.5% | 1.9% | 1.2% | 12.7% |
| Neutral mention | 18 | 0.0% | 0.0% | 8.2% | 2.1% | 1.0% | 0.2% | 3.5% |
| Suppress | 18 | 0.0% | 0.0% | 3.3% | 0.0% | 0.9% | 1.0% | 0.5% |
| No instruction | 18 | 0.0% | 0.0% | 0.5% | 0.0% | 0.0% | 0.0% | 0.0% |

### Leaving out the first bead (where the instruction is closest)

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 18 | 0.0% | 0.0% | 4.4% | 0.5% | 2.0% | 1.3% | 9.1% |
| Neutral mention | 18 | 0.0% | 0.0% | 8.0% | 2.2% | 1.1% | 0.2% | 3.7% |
| Suppress | 18 | 0.0% | 0.0% | 3.5% | 0.0% | 0.9% | 1.1% | 0.5% |
| No instruction | 18 | 0.0% | 0.0% | 0.5% | 0.0% | 0.0% | 0.0% | 0.0% |

### By bead position, L56

Hit rate per bead, pooled over items (beads in each range in brackets).

| Condition | 1 | 2-4 | 5-8 | 9-16 | 17-32 | 33+ |
|---|---|---|---|---|---|---|
| Repeat silently | 83.3% (18) | 13.0% (54) | 18.1% (72) | 5.6% (144) | 4.9% (144) | n/a |
| Neutral mention | 0.0% (18) | 1.9% (54) | 6.9% (72) | 1.4% (144) | 3.5% (144) | n/a |
| Suppress | 0.0% (18) | 3.7% (54) | 0.0% (72) | 0.0% (144) | 0.0% (144) | n/a |
| No instruction | 0.0% (18) | 0.0% (54) | 0.0% (72) | 0.0% (144) | 0.0% (144) | n/a |

Items with the target on at least half their beads at L56: Repeat silently 0/18, Neutral mention 0/18, Suppress 0/18, No instruction 0/18.

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### focus

**focus · peace** (item 2)

- Prompt: With every 📿 you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, krist, crystal; beads† (#6) |
| L16 | `·` | MSM, TikTok, Nike, Bernie, Fortnite |
| L24 | `📿` | prayer†, religious, beads†, sacred, prayers; Prayer† (#6) |
| L32 | `·` | prayer†, PS, prayers, Prayer†, S |
| L40 | `·` | **peace**, Buddhist, prayer†, religious, peaceful; **Peace** (#6) |
| L48 | `·` | Buddhist, 宗教, **peace**, religious, holy |
| L56 | `📿` | **peace**, **peace**, **Peace**, **Peace**, peaceful |

**focus · peace** (item 3)

- Prompt: With every 📿 you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, krist, crystal; beads† (#6) |
| L16 | `·` | MSM, TikTok, Fortnite, Bernie, Tik |
| L24 | `📿` | prayer†, religious, beads†, sacred, prayers; Prayer† (#6) |
| L32 | `·` | prayer†, PS, prayers, Prayer†, aph |
| L40 | `·` | word, words, silent, name, **peace** |
| L48 | `·` | 宗教, 链, bracelets, beads†, bracelet |
| L56 | `·` | **Peace**, **Peace**, **peace**, **peace**, 和平 |

### neutral

**neutral · ocean** (item 28)

- Prompt: The word "ocean" came up in conversation earlier today.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | jewelry, 项链, necklace, crystal, beads† |
| L16 | `·` | TikTok, MSM, Fortnite, Twitter, Anime |
| L24 | `·` | **ocean**, underwater, **Ocean**, marine, water |
| L32 | `·` | prayer†, jewelry, Bible, silk, beads†; Prayer† (#7) |
| L40 | `·` | Buddhist, religious, prayer†, symbol, sacred |
| L48 | `·` | Buddhist, 宗教, beads†, religious, holy; prayer† (#10) |
| L56 | `·` | �, 佛, Emoji, SOLE, Quran; **Ocean** (#7) |

**neutral · guitar** (item 30)

- Prompt: The word "guitar" came up in conversation earlier today.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, crystal, jewelry, 项链, krist; beads† (#6) |
| L16 | `·` | TikTok, MSM, Fortnite, Twitter, Anime |
| L24 | `📿` | beads†, religious, prayer†, sacred, prayers; Prayer† (#7) |
| L32 | `·` | prayer†, Bible, religious, prayers, Prayer† |
| L40 | `·` | prayer†, Buddhist, religious, prayers, spiritual; Prayer† (#6) |
| L48 | `·` | 宗教, Buddhist, religious, beads†, prayer† |
| L56 | `·` | �, 佛, **guitar**, 吉他, 琴; **Guitar** (#8) |

**neutral · bliss** (item 25)

- Prompt: The word "bliss" came up in conversation earlier today.  Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, jewelry, 项链, crystal, beads† |
| L16 | `·` | TikTok, MSM, Fortnite, Twitter, Tik |
| L24 | `📿` | beads†, prayer†, religious, sacred, prayers; Prayer† (#6), bead† (#9) |
| L32 | `·` | prayer†, Prayer†, Bible, prayers, Quran; beads† (#9) |
| L40 | `·` | prayer†, Buddhist, religious, prayers, Prayer† |
| L48 | `·` | holy, Buddhist, 宗教, prayers, Vatican; prayer† (#6), Prayer† (#10) |
| L56 | `·` | �, Emoji, emoji, ღ, emoji |

### suppress

**suppress · peace** (item 42)

- Prompt: Don't think about the word "peace" while you write.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, 项链, jewelry, beads†, crystal |
| L16 | `·` | TikTok, MSM, Fortnite, Twitter, Bernie |
| L24 | `📿` | beads†, religious, prayer†, necklace, sacred; bead† (#9) |
| L32 | `·` | jewelry, Quran, beads†, prayer†, Quran; Prayer† (#7) |
| L40 | `·` | **peace**, peaceful, words, word, **Peace** |
| L48 | `·` | **peace**, word, peaceful, **Peace**, words |
| L56 | `·` | �, Emoji, emoji, ღ, བ |

**suppress · peace** (item 43)

- Prompt: Don't think about the word "peace" while you write.  Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, 项链, jewelry, beads†, crystal |
| L16 | `·` | MSM, TikTok, Twitter, Fortnite, Bernie |
| L24 | `📿` | beads†, religious, prayer†, necklace, sacred; bead† (#9) |
| L32 | `·` | Bible, prayer†, Buddhist, religious, prayers |
| L40 | `·` | **peace**, peaceful, **Peace**, word, words; **peace** (#8) |
| L48 | `·` | **peace**, peaceful, **Peace**, word, quiet |
| L56 | `·` | �, Emoji, emoji, ღ, བ |

**suppress · piano** (item 55)

- Prompt: Don't think about the word "piano" while you write.  Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, 项链, jewelry, beads†, crystal |
| L16 | `·` | MSM, TikTok, Fortnite, Twitter, Bernie |
| L24 | `📿` | beads†, prayer†, religious, necklace, prayers; Prayer† (#7), bead† (#9) |
| L32 | `📿` | necklace, beads†, Necklace, Prayer†, prayer† |
| L40 | `·` | emoji, emojis, chain, https, chains; beads† (#6) |
| L48 | `·` | 宗教, emoji, 链, 符, bracelets; beads† (#7) |
| L56 | `·` | �, Emoji, emoji, ღ, ojis |

### none

**none · guitar** (item 70)

- Prompt: Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, 项链, beads†, jewelry, crystal |
| L16 | `·` | MSM, TikTok, Nike, Bernie, Fortnite |
| L24 | `📿` | beads†, religious, necklace, prayer†, Buddhist; bead† (#8), Prayer† (#10) |
| L32 | `·` | Quran, Quran, prayer†, PS, oms; Prayer† (#7) |
| L40 | `·` | emoji, single, emojis, 单个, single |
| L48 | `·` | emoji, emoji, 串行, 符号, 一个一个 |
| L56 | `·` | �, Emoji, emoji, emoji, SEQUENTIAL |

**none · guitar** (item 71)

- Prompt: Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, 项链, beads†, jewelry, crystal |
| L16 | `·` | MSM, TikTok, Fortnite, Nike, Bernie |
| L24 | `📿` | beads†, religious, necklace, prayer†, Buddhist; bead† (#8), Prayer† (#10) |
| L32 | `📿` | necklace, beads†, Necklace, Buddhist, chain; Prayer† (#7), prayer† (#8), bead† (#9) |
| L40 | `·` | Buddhist, prayer†, jewelry, religious, chain; beads† (#6) |
| L48 | `·` | bracelet, necklace, Buddhist, holy, beads† |
| L56 | `·` | �, Emoji, emoji, ღ, emoji |

**none · tiger** (item 79)

- Prompt: Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | necklace, 项链, beads†, jewelry, crystal |
| L16 | `·` | MSM, TikTok, Fortnite, Nike, Bernie |
| L24 | `📿` | beads†, religious, necklace, prayer†, Buddhist; bead† (#8), Prayer† (#10) |
| L32 | `📿` | necklace, beads†, Necklace, Buddhist, chain; Prayer† (#7), prayer† (#8), bead† (#9) |
| L40 | `·` | Buddhist, s, count, prayer†, jewelry |
| L48 | `·` | bracelet, necklace, holy, bracelets, jewelry; beads† (#7) |
| L56 | `·` | �, Emoji, emoji, ღ, emoji |

### Items with a tracked word (bead, beads, damn, fail, failed, failure, mantra, prayer) in the top-10: 80

**focus · love** (item 0)

- Prompt: With every 📿 you write, silently repeat the word "love" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, crystal, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Tik, Fortnite, Bernie |
| L24 | `📿` | beads†, prayer†, sacred, religious, prayers; Prayer† (#8) |
| L32 | `📿` | Prayer†, Necklace, prayer†, necklace, religious; beads† (#6) |
| L40 | `·` | **love**, **Love**, th, people, loving |
| L48 | `·` | **love**, holy, symbolic, song, symbol |
| L56 | `📿` | �, **love**, loves, **love**, **Love**; **LOVE** (#9) |

**focus · bliss** (item 4)

- Prompt: With every 📿 you write, silently repeat the word "bliss" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, crystal, jewelry, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Fortnite, Tik, Nike |
| L24 | `📿` | beads†, prayer†, religious, sacred, prayers; Prayer† (#6) |
| L32 | `📿` | Prayer†, prayer†, religious, Buddhist, Necklace; beads† (#7) |
| L40 | `·` | emoji, emojis, Emoji, emoji, ღ |
| L48 | `·` | 符号, symbol, emoji, ღ, emoji |
| L56 | `📿` | �, ღ, emoji, emojis, **bliss** |

**focus · lotus** (item 6)

- Prompt: With every 📿 you write, silently repeat the word "lotus" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, crystal, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Fortnite, Nike, Tik |
| L24 | `📿` | beads†, prayer†, sacred, religious, Buddhist; Prayer† (#7) |
| L32 | `📿` | Buddhist, Prayer†, religious, Necklace, necklace; prayer† (#6), beads† (#7) |
| L40 | `·` | emoji, emojis, Emoji, emoji, Emoji |
| L48 | `·` | 符号, emoji, symbol, emoji, ღ |
| L56 | `·` | �, Emoji, ღ, emoji, ojis |

**focus · peace** (item 2)

- Prompt: With every 📿 you write, silently repeat the word "peace" in your mind. Do not write the word.  Now write only 📿, one at a time, about 16 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, jewelry, krist, crystal; beads† (#6) |
| L16 | `·` | MSM, TikTok, Nike, Bernie, Fortnite |
| L24 | `📿` | prayer†, religious, beads†, sacred, prayers; Prayer† (#6) |
| L32 | `·` | prayer†, PS, prayers, Prayer†, S |
| L40 | `·` | **peace**, Buddhist, prayer†, religious, peaceful; **Peace** (#6) |
| L48 | `·` | Buddhist, 宗教, **peace**, religious, holy |
| L56 | `📿` | **peace**, **peace**, **Peace**, **Peace**, peaceful |

**focus · bliss** (item 5)

- Prompt: With every 📿 you write, silently repeat the word "bliss" in your mind. Do not write the word.  Now write only 📿, one at a time, about 32 of them, like this: 📿📿📿📿 Write nothing else.
- Output: 📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿📿

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `📿` | 项链, necklace, crystal, jewelry, krist; beads† (#6) |
| L16 | `·` | MSM, TikTok, Fortnite, Bernie, Nike |
| L24 | `📿` | prayer†, beads†, religious, sacred, prayers; Prayer† (#6) |
| L32 | `📿` | Prayer†, prayer†, religious, Necklace, Buddhist; beads† (#7) |
| L40 | `·` | prayer†, count, religious, digital, Buddhist |
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