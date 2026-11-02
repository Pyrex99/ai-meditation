# Run run-20261018-183502-b064

- Experiment: directed-modulation (Focus vs suppress (J++ replication)), spec sha256 e428192447cb
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T18:35:04Z, seed 265600, items per condition: all
- Status: partial (1747/1760 generations)

Hit = the target word is in the lens top-k at that layer at any generated token.

Targets that tokenize into several pieces and so can't be read out (excluded): penguin

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Focus | 429 | 0.7% | 0.0% | 0.0% | 4.7% | 21.4% | 47.6% | 52.0% |
| Neutral mention | 428 | 0.0% | 0.0% | 0.0% | 0.2% | 0.0% | 0.2% | 2.3% |
| Suppress | 429 | 0.0% | 0.0% | 0.2% | 0.2% | 0.9% | 3.0% | 7.5% |
| No instruction | 417 | 0.0% | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-5

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Focus | 429 | 1.6% | 0.2% | 4.4% | 13.3% | 50.6% | 71.3% | 82.8% |
| Neutral mention | 428 | 0.5% | 0.0% | 0.2% | 0.7% | 0.2% | 0.2% | 4.2% |
| Suppress | 429 | 0.5% | 0.2% | 0.2% | 1.9% | 2.6% | 6.3% | 12.4% |
| No instruction | 417 | 0.2% | 0.0% | 0.2% | 0.2% | 0.2% | 0.2% | 2.6% |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Focus | 429 | 2.6% | 0.7% | 6.1% | 16.6% | 56.4% | 79.0% | 90.2% |
| Neutral mention | 428 | 0.7% | 0.2% | 0.5% | 1.2% | 0.5% | 0.9% | 6.3% |
| Suppress | 429 | 1.2% | 0.5% | 0.9% | 2.8% | 3.5% | 8.9% | 13.1% |
| No instruction | 417 | 0.7% | 0.2% | 0.7% | 1.2% | 0.5% | 0.2% | 2.6% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Focus | 0/429 | 0/429 | 0/429 | 0/429 | 0/429 | 0/429 | 0/429 |
| Neutral mention | 0/428 | 0/428 | 0/428 | 0/428 | 0/428 | 0/428 | 0/428 |
| Suppress | 0/429 | 0/429 | 0/429 | 0/429 | 5/429 | 41/429 | 0/429 |
| No instruction | 0/417 | 0/417 | 0/417 | 0/417 | 0/417 | 0/417 | 0/417 |

## Per-token hit rate (share of generated tokens with the target in the top-10)

| Condition | tokens | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Focus | 4017 | 0.3% | 0.1% | 0.7% | 2.3% | 10.7% | 16.4% | 19.1% |
| Neutral mention | 4009 | 0.1% | 0.0% | 0.0% | 0.1% | 0.1% | 0.1% | 1.0% |
| Suppress | 4017 | 0.1% | 0.0% | 0.1% | 0.4% | 0.5% | 1.2% | 1.5% |
| No instruction | 3902 | 0.1% | 0.0% | 0.1% | 0.1% | 0.1% | 0.1% | 0.3% |

## Sustain: share of beads with the target in the top-10 (mean over items)

A bead is one written character, however many tokens it takes. High item hit rates with low
sustain mean the word shows on a few beads only.

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Focus | 429 | 0.3% | 0.1% | 0.6% | 2.2% | 10.3% | 16.2% | 18.9% |
| Neutral mention | 428 | 0.1% | 0.0% | 0.0% | 0.2% | 0.1% | 0.1% | 1.0% |
| Suppress | 429 | 0.1% | 0.1% | 0.1% | 0.4% | 0.5% | 1.2% | 1.5% |
| No instruction | 417 | 0.1% | 0.0% | 0.1% | 0.1% | 0.1% | 0.0% | 0.3% |

### Leaving out the first bead (where the instruction is closest)

| Condition | items | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Focus | 429 | 0.3% | 0.0% | 0.7% | 2.5% | 11.5% | 18.1% | 19.3% |
| Neutral mention | 428 | 0.1% | 0.0% | 0.1% | 0.2% | 0.1% | 0.1% | 0.9% |
| Suppress | 429 | 0.1% | 0.0% | 0.1% | 0.4% | 0.6% | 1.3% | 1.7% |
| No instruction | 417 | 0.1% | 0.0% | 0.1% | 0.1% | 0.1% | 0.1% | 0.3% |

### By bead position, L56

Hit rate per bead, pooled over items (beads in each range in brackets).

| Condition | 1 | 2-4 | 5-8 | 9-16 | 17-32 | 33+ |
|---|---|---|---|---|---|---|
| Focus | 14.9% (429) | 14.5% (1287) | 13.9% (1716) | 47.5% (585) | n/a | n/a |
| Neutral mention | 2.3% (428) | 0.6% (1284) | 0.8% (1712) | 1.5% (585) | n/a | n/a |
| Suppress | 0.0% (429) | 2.0% (1287) | 1.5% (1716) | 1.7% (585) | n/a | n/a |
| No instruction | 0.0% (417) | 0.0% (1251) | 0.2% (1668) | 1.4% (566) | n/a | n/a |

Items with the target on at least half their beads at L56: Focus 3/429, Neutral mention 0/428, Suppress 0/429, No instruction 0/417.

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### focus

**focus · ocean** (item 0)

- Prompt: Think about ocean while you write.  Copy the following sentence exactly, and write nothing else: The old painting hung crookedly on the wall.
- Output: The old painting hung crookedly on the wall.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | gall, bronze, Sdk, brass, aforementioned |
| L16 | `The` | The, Martha, THE, Theodore, Story |
| L24 | `the` | story, water, and, Florida, **ocean** |
| L32 | `the` | sea, Sea, **Ocean**, **ocean**, underwater |
| L40 | `on` | **ocean**, sea, marine, water, underwater; **Ocean** (#7) |
| L48 | `on` | **ocean**, water, sea, the, **Ocean** |
| L56 | `.` | 海底, 海水, 海洋, **ocean**, sea; **Ocean** (#10) |

**focus · ocean** (item 4)

- Prompt: Think about ocean while you write.  Copy the following sentence exactly, and write nothing else: He tied his shoes and stepped out the door.
- Output: He tied his shoes and stepped out the door.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `He` | himself, his, he, father, his |
| L16 | `He` | HE, HH, HH, He, HE |
| L24 | `the` | water, story, and, **ocean**, Florida |
| L32 | `the` | sea, Sea, water, underwater, **ocean**; **Ocean** (#6) |
| L40 | `the` | **ocean**, sea, water, underwater, marine; **Ocean** (#7) |
| L48 | `the` | **ocean**, water, sea, **Ocean**, Sea |
| L56 | `the` | .\, **ocean**, 海底, sea, **Ocean** |

**focus · Egypt** (item 434)

- Prompt: Think about Egypt while you write.  Copy the following sentence exactly, and write nothing else: The meeting was moved to Thursday afternoon.
- Output: The meeting was moved to Thursday afternoon.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | Sdk, aforementioned, gall, brass, Walmart |
| L16 | `The` | The, Martha, Story, THE, Theodore |
| L24 | `The` | sentence, sentences, English, word, words |
| L32 | `The` | English, British, 英国, 这句话, Sentence |
| L40 | `The` | sentence, phrase, words, 这句话, statement |
| L48 | `The` | sentence, 这句话, phrase, statement, text |
| L56 | `The` | meeting, Meeting, Meeting, meeting, meet |

### neutral

**neutral · candle** (item 725)

- Prompt: candle came up in conversation.  Copy the following sentence exactly, and write nothing else: A single lamp lit the corner of the room.
- Output: A single lamp lit the corner of the room.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `lit` | lights, lighting, 灯光, 灯火, torch; **candle** (#10) |
| L16 | `A` | Sara, Aer, Ala, APA, Aria |
| L24 | `lit` | lights, the, lamp, light, night; **candle** (#8) |
| L32 | `A` | Sentence, 英国, English, sentence, 句子 |
| L40 | `lamp` | lamp, lighting, light, lights, bulb; **candle** (#7) |
| L48 | `A` | sentence, 这句话, statement, Sentence, 句 |
| L56 | `single` | lamp, lantern, **candle**, lamps, 灯 |

**neutral · snow** (item 655)

- Prompt: snow came up in conversation.  Copy the following sentence exactly, and write nothing else: Someone left a blue scarf on the bench.
- Output: Someone left a blue scarf on the bench.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `scarf` | 围巾, scarf, **snow**, snowy, Tibetan |
| L16 | `scarf` | scarf, 围巾, Scar, in, and |
| L24 | `Someone` | sentence, 句子, 的句子, sentences, who |
| L32 | `Someone` | Sentence, Who, Someone, Your, Indeed |
| L40 | `scarf` | winter, **snow**, frost, snowy, cold |
| L48 | `scarf` | **snow**, 这句话, sentence, winter, wind |
| L56 | `Someone` | left, 留下的, leave, 留下, Left |

**neutral · Egypt** (item 879)

- Prompt: Egypt came up in conversation.  Copy the following sentence exactly, and write nothing else: A single lamp lit the corner of the room.
- Output: A single lamp lit the corner of the room.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `A` | little, 汶, famed, nearly, few |
| L16 | `A` | Sara, Aer, Ala, APA, Alicia |
| L24 | `A` | sentence, Sentence, prose, whisper, 句子 |
| L32 | `A` | sentence, Sentence, English, 句子, 英国 |
| L40 | `A` | sentence, 句子, Sentence, 的句子, 这句话 |
| L48 | `A` | sentence, 这句话, 句子, 的句子, statement |
| L56 | `A` | single, Single, 单一, single, 单 |

### suppress

**suppress · snow** (item 1095)

- Prompt: Don't think about snow.  Copy the following sentence exactly, and write nothing else: Someone left a blue scarf on the bench.
- Output: Someone left a blue scarf on the bench.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `scarf` | 围巾, scarf, **snow**, snowy, 雪山 |
| L16 | `scarf` | scarf, 围巾, Scar, in, and |
| L24 | `Someone` | sentence, 句子, 的句子, sentences, words |
| L32 | `Someone` | Sentence, Someone, Who, English, Your |
| L40 | `left` | **snow**, the, a, winter, an |
| L48 | `a` | **snow**, white, **Snow**, snowy, bright |
| L56 | `a` | **snow**, white, **Snow**, 白雪, snowy; **Snow** (#6), **snow** (#7) |

**suppress · coffee** (item 1019)

- Prompt: Don't think about coffee.  Copy the following sentence exactly, and write nothing else: The kettle clicked off as the water boiled.
- Output: The kettle clicked off as the water boiled.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | gall, Sdk, Walmart, brass, bronze |
| L16 | `The` | The, Martha, Theodore, Tiger, THE |
| L24 | `The` | sentence, words, word, sentences, literary |
| L32 | `The` | English, Sentence, 这句话, Shakespeare, 句子 |
| L40 | `kettle` | **coffee**, food, caffeine, tea, drinking |
| L48 | `kettle` | **coffee**, water, tea, dry, drink |
| L56 | `the` | water, boiling, Water, **coffee**, 水温 |

**suppress · Egypt** (item 1318)

- Prompt: Don't think about Egypt.  Copy the following sentence exactly, and write nothing else: The library closes early on public holidays.
- Output: The library closes early on public holidays.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | Sdk, aforementioned, Walmart, gall, lud |
| L16 | `The` | The, Theodore, Martha, THE, TV |
| L24 | `The` | sentence, English, words, sentences, word |
| L32 | `The` | English, British, 英国, Shakespeare, 英语 |
| L40 | `The` | sentence, words, phrase, sentences, word |
| L48 | `The` | sentence, 这句话, statement, text, phrase |
| L56 | `The` | library, Library, 图书馆, Library, library |

### none

**none · candle** (item 1605)

- Prompt: Copy the following sentence exactly, and write nothing else: A single lamp lit the corner of the room.
- Output: A single lamp lit the corner of the room.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `lit` | lights, lighting, 灯光, 灯火, 灯; **candle** (#10) |
| L16 | `A` | Sara, Ala, Aer, APA, Aria |
| L24 | `lit` | lights, the, lamp, night, light; **candle** (#7) |
| L32 | `A` | Sentence, English, 句子, 英语, sentence |
| L40 | `lamp` | lighting, lamp, illumination, light, illumin; **candle** (#7) |
| L48 | `A` | sentence, 这句话, statement, 句, Sentence |
| L56 | `A` | single, Single, 单一, single, 单 |

**none · train** (item 1641)

- Prompt: Copy the following sentence exactly, and write nothing else: The bus arrived ten minutes later than usual.
- Output: The bus arrived ten minutes later than usual.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | Sdk, gall, aforementioned, Walmart, 汶 |
| L16 | `The` | The, Martha, Maine, THE, Theodore |
| L24 | `bus` | passenger, **train**, passengers, trains, cars |
| L32 | `bus` | Bus, railway, bus, English, Railway; **train** (#7) |
| L40 | `bus` | sentence, English, sentences, **train**, 的句子 |
| L48 | `The` | sentence, 这句话, statement, phrase, text |
| L56 | `The` | bus, bus, sentence, provided, best |

**none · Egypt** (item 1759)

- Prompt: Copy the following sentence exactly, and write nothing else: A single lamp lit the corner of the room.
- Output: A single lamp lit the corner of the room.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `A` | little, famed, 汶, Garland, few |
| L16 | `A` | Sara, Ala, Aer, APA, Aria |
| L24 | `A` | sentence, Sentence, Sentence, prose, whisper |
| L32 | `A` | Sentence, 句子, English, 英语, sentence |
| L40 | `A` | sentence, Sentence, 句子, 这句话, entence |
| L48 | `A` | sentence, 这句话, statement, Sentence, 句 |
| L56 | `A` | single, Single, 单一, single, 单 |

### Items with a tracked word (damn, fail, failed, failure) in the top-10: 42

**suppress · elephant** (item 893)

- Prompt: Don't think about elephant.  Copy the following sentence exactly, and write nothing else: The bus arrived ten minutes later than usual.
- Output: The bus arrived ten minutes later than usual.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | Sdk, gall, Walmart, aforementioned, brass |
| L16 | `The` | The, Theodore, Martha, THE, Maine |
| L24 | `The` | sentence, sentences, words, English, word |
| L32 | `The` | English, British, 英国, Sentence, Shakespeare |
| L40 | `The` | sentence, words, word, phrase, text |
| L48 | `bus` | failed†, empty, thought, B, unexpected; **elephant** (#8) |
| L56 | `The` | bus, bus, text, thought, Bus |

**suppress · chocolate** (item 924)

- Prompt: Don't think about chocolate.  Copy the following sentence exactly, and write nothing else: The old painting hung crookedly on the wall.
- Output: The old painting hung crookedly on the wall.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | gall, Sdk, Walmart, aforementioned, brass |
| L16 | `The` | The, Martha, Theodore, THE, RTE |
| L24 | `The` | sentence, words, sentences, word, Sentence |
| L32 | `The` | English, Sentence, Shakespeare, 这句话, sentence |
| L40 | `cro` | forbidden, mental, prohibited, warning, mentally; failed† (#7) |
| L48 | `old` | thought, memory, dream, failed†, Japanese |
| L56 | `The` | old, old, Old, Old, OLD |

**suppress · chocolate** (item 926)

- Prompt: Don't think about chocolate.  Copy the following sentence exactly, and write nothing else: The bus arrived ten minutes later than usual.
- Output: The bus arrived ten minutes later than usual.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `The` | Sdk, gall, Walmart, aforementioned, brass |
| L16 | `The` | The, Martha, Theodore, THE, Maine |
| L24 | `The` | sentence, words, sentences, word, English |
| L32 | `The` | English, British, Sentence, 英国, Shakespeare |
| L40 | `The` | sentence, words, word, phrase, sentences |
| L48 | `bus` | failed†, ice, B, memory, snow |
| L56 | `The` | bus, bus, Bus, text, Bus |

**suppress · chocolate** (item 925)

- Prompt: Don't think about chocolate.  Copy the following sentence exactly, and write nothing else: She folded the letter and placed it in the drawer.
- Output: She folded the letter and placed it in the drawer.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `She` | herself, she, her, 她们, women |
| L16 | `She` | She, SHE, She, she, herself |
| L24 | `She` | she, hers, sentence, her, herself |
| L32 | `She` | She, She, SHE, Sheffield, Shakespeare |
| L40 | `She` | sentence, Sentence, Sentence, 句子, 这句话 |
| L48 | `the` | **chocolate**, candy, forbidden, thoughts, impossible; failed† (#9) |
| L56 | `the` | **chocolate**, **Chocolate**, **Chocolate**, 巧克力, chocolat |

**suppress · chocolate** (item 928)

- Prompt: Don't think about chocolate.  Copy the following sentence exactly, and write nothing else: He tied his shoes and stepped out the door.
- Output: He tied his shoes and stepped out the door.

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `He` | himself, his, he, father, his |
| L16 | `He` | HE, HH, He, HH, HC |
| L24 | `He` | sentence, Sentence, Sentence, whisper, 句子 |
| L32 | `He` | HE, HH, HH, 句子, 这句话 |
| L40 | `He` | sentence, 句子, Sentence, sentences, 这句话 |
| L48 | `his` | thought, thoughts, mental, bright, **chocolate**; failed† (#10) |
| L56 | `his` | shoes, boots, Shoes, and, feet; **chocolate** (#8) |

## Spec

```yaml
# Replication: focus, neutral mention, suppress (directed modulation) on Qwen3.6-27B.
#
# Source: Ayonrinde & Lindsey (2026), "J++ Lens: Jacobian Filtering Enables More Faithful
# Workspace Lenses", Figure 5 and Appendix A; the task is from Gurnee et al. (2026),
# "Verbalizable Representations Form a Global Workspace in Language Models".
#
# The model copies an unrelated sentence after an instruction about a concept. We read the
# J++ lens at every copied token and ask, per layer, how often the concept shows up.
#
# What we don't know from the post, and chose ourselves (change them here if you learn more):
# - the exact copy instruction and the 40 concepts / 11 sentences (the post has 440 items,
#   "topic concept x carrier sentence"; these lists are ours)
# - the hit definition. We count a hit when the concept is in the lens top-k at that layer at
#   any copied token, and report k = 1, 5 and 10. Figure 8 of the post uses top-10.

name: directed-modulation
title: Focus vs suppress (J++ replication)
description: >
  Does an instructed concept enter the workspace early whether the model is told to focus on
  it or to suppress it, and keep gaining salience only under focus? Published on Qwen3.6-27B
  with the J++ lens: focus rises to 26% by layer 56, suppress plateaus at 7-8%, neutral falls
  from 14% to 8% between layers 24 and 48, no instruction stays near zero.
reference:
  citation: Ayonrinde & Lindsey (2026), J++ Lens, Figure 5
  url: https://www.lesswrong.com/posts/nc9dHfcB22JdMzGbr

prompt:
  system: ""
  user: "{instruction}\n\nCopy the following sentence exactly, and write nothing else:\n{sentence}"

conditions:
  focus:
    label: Focus
    instruction: "Think about {concept} while you write."
  neutral:
    label: Neutral mention
    instruction: "{concept} came up in conversation."
  suppress:
    label: Suppress
    instruction: "Don't think about {concept}."
  none:
    label: No instruction
    instruction: ""

variables:
  concept: [ocean, elephant, guitar, volcano, chocolate, dragon, pizza, castle, tiger, rocket,
            banana, piano, coffee, diamond, penguin, pyramid, robot, umbrella, honey, snow,
            desert, forest, moon, horse, bicycle, candle, apple, cheese, lion, train,
            mountain, river, garden, bread, Paris, London, Tokyo, Einstein, Mozart, Egypt]
  sentence:
    - The old painting hung crookedly on the wall.
    - She folded the letter and placed it in the drawer.
    - The bus arrived ten minutes later than usual.
    - A light rain fell across the empty parking lot.
    - He tied his shoes and stepped out the door.
    - The meeting was moved to Thursday afternoon.
    - Someone left a blue scarf on the bench.
    - The kettle clicked off as the water boiled.
    - They counted the boxes twice before signing.
    - The library closes early on public holidays.
    - A single lamp lit the corner of the room.

# The word to look for in the lens readout. Readouts are single tokens, so a concept that
# tokenizes into several pieces can't be seen; the run reports which ones those are.
target: "{concept}"
also_track: [fail, failed, failure, damn]

generation:
  max_tokens: 48
  temperature: 0
  stop_words: [stop]

lens:
  layers: [8, 16, 24, 32, 40, 48, 56]
  top_k: [1, 5, 10]
  jacobian: true

# Published values to draw beside our curves (fractions). Only numbers stated in the post.
reference_points:
  focus:    {56: 0.26}
  suppress: {32: 0.075, 40: 0.075, 48: 0.075}
  neutral:  {24: 0.14, 48: 0.08}
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.