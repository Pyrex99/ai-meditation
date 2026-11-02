# Run run-20261018-190939-86bb

- Experiment: jpp-readout (Readout recall (exact J++ replication)), spec sha256 4fb122f9fdbc
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T19:09:44Z, seed 89053, items per condition: all
- Status: complete (496/496 generations)

Recall@k = share of an item's hidden words in the lens top-k at the read position.

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Multihop | 93 | 1.1% | 0.0% | 2.2% | 1.1% | 16.1% | 10.8% | 12.9% |
| Multilingual | 107 | 2.8% | 2.8% | 12.1% | 11.7% | 14.3% | 13.8% | 17.5% |
| Typo | 96 | 34.4% | 34.4% | 42.7% | 39.6% | 52.1% | 41.7% | 6.2% |
| Association | 102 | 1.0% | 1.0% | 6.9% | 5.9% | 9.8% | 7.8% | 2.0% |
| Poetry | 98 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 3.1% |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Multihop | 93 | 4.3% | 2.2% | 16.1% | 15.6% | 37.1% | 35.8% | 39.8% |
| Multilingual | 107 | 10.3% | 9.8% | 28.3% | 22.2% | 41.6% | 43.7% | 44.6% |
| Typo | 96 | 86.5% | 70.8% | 69.8% | 71.9% | 83.3% | 77.1% | 31.2% |
| Association | 102 | 1.0% | 2.9% | 19.6% | 19.6% | 25.5% | 21.6% | 10.8% |
| Poetry | 98 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 3.1% | 13.3% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Multihop | 0/93 | 0/93 | 0/93 | 0/93 | 0/93 | 0/93 | 0/93 |
| Multilingual | 0/107 | 0/107 | 0/107 | 0/107 | 0/107 | 0/107 | 0/107 |
| Typo | 0/96 | 0/96 | 0/96 | 0/96 | 0/96 | 0/96 | 0/96 |
| Association | 0/102 | 0/102 | 0/102 | 0/102 | 0/102 | 0/102 | 0/102 |
| Poetry | 0/98 | 0/98 | 0/98 | 0/98 | 0/98 | 0/98 | 0/98 |

## Recall@10 at each item's best layer (the published metric)

| Task | Ours | Published |
|---|---|---|
| Multihop | 55.2% | – |
| Multilingual | 73.8% | – |
| Typo | 95.8% | – |
| Association | 38.2% | 37.0% |
| Poetry | 14.3% | 5.0% |
| **Macro average** | **55.5%** | 55.2% |

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### multihop

**multihop · December** (item 51)

- Prompt: Fact: Christmas Day is celebrated in month number 
- Output: read at token 9 (' ')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | **December**, month, only, number, thanks |
| L16 | `␣` | and, in, the, Number, Star |
| L24 | `␣` | year, season, month, winter, **December** |
| L32 | `␣` | season, **December**, calendar, year, Christmas |
| L40 | `␣` | **December**, Christmas, January, November, winter |
| L48 | `␣` | **December**, month, calendar, Christmas, Month; **December** (#8) |
| L56 | `␣` | **December**, Christmas, **December**, month, 圣诞 |

**multihop · February** (item 53)

- Prompt: Fact: Valentine's Day is celebrated in month number 
- Output: read at token 10 (' ')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | month, December, thanks, months, only; **February** (#7) |
| L16 | `␣` | and, in, the, a, to |
| L24 | `␣` | year, season, month, months, winter; **February** (#6) |
| L32 | `␣` | season, calendar, year, month, **February** |
| L40 | `␣` | **February**, month, January, March, Month |
| L48 | `␣` | month, Month, calendar, **February**, month |
| L56 | `␣` | **February**, month, Valentine, **February**, January |

**multihop · four** (item 18)

- Prompt: Fact: Take the number whose name rhymes with the word door. Doubling it gives the number 
- Output: read at token 20 (' ')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | Wichita, numbers, maths, lucky, yellow |
| L16 | `␣` | the, Number, and, Newton, in |
| L24 | `␣` | numbers, double, half, one, the |
| L32 | `␣` | 2, number, 1, 4, a |
| L40 | `␣` | double, half, number, doubled, twice |
| L48 | `␣` | number, numbers, Number, double, six |
| L56 | `␣` | number, double, ten, six, feet |

### multilingual

**multilingual · Norwegian, season, spring, summer** (item 112)

- Prompt: Etter våren kommer 
- Output: read at token 5 (' ')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | **Norwegian**, 挪威, Norway, Norsk, 温哥华 |
| L16 | `␣` | Norway, **Norwegian**, NW, Bergen, Nor |
| L24 | `␣` | winter, **season**, **summer**, seasons, weather; **spring** (#10) |
| L32 | `␣` | winter, Norway, Winter, **summer**, **season** |
| L40 | `␣` | **summer**, winter, year, **season**, **spring**; **Summer** (#6) |
| L48 | `␣` | **summer**, **Summer**, **season**, year, **spring**; **summer** (#8), **Spring** (#10) |
| L56 | `␣` | **summer**, **spring**, **summer**, **season**, winter; **Norwegian** (#6), **Summer** (#7) |

**multilingual · Greek, color, sea, blue** (item 104)

- Prompt: Το χρώμα της θάλασσας είναι 
- Output: read at token 12 (' ')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | colors, only, colours, and, underwater; **color** (#6), **blue** (#8) |
| L16 | `␣` | **Blue**, a, and, Gal, **blue**; **Sea** (#9) |
| L24 | `␣` | ocean, **sea**, colors, **color**, oceans; **blue** (#8) |
| L32 | `␣` | 2, 1, 4, 5, 0 |
| L40 | `␣` | **color**, water, **sea**, colored, **blue**; **Color** (#10) |
| L48 | `␣` | **color**, 1, **sea**, number, **blue**; **Color** (#6) |
| L56 | `␣` | **blue**, **color**, **sea**, **blue**, **color**; **Blue** (#9) |

### typo

**typo · government** (item 201)

- Prompt: The new policy was announced last week by the federal goverment
- Output: read at token 11 ('ment')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `ment` | federal, **government**, defence, governments, **government** |
| L16 | `ment` | Federal, **Government**, federal, G, **government** |
| L24 | `ment` | **government**, federal, national, political, policy; **government** (#7) |
| L32 | `ment` | **government**, **Government**, Federal, federal, in |
| L40 | `ment` | **government**, federal, **Government**, national, gov; **government** (#7) |
| L48 | `ment` | **government**, **Government**, federal, national, Federal; **government** (#9) |
| L56 | `ment` | after, which, of, in, federal; **Government** (#6) |

**typo · address** (item 204)

- Prompt: Please write your full name and your current adress
- Output: read at token 8 (' adress')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `adress` | adress, addresses, **address**, travelling, neighbourhood; **address** (#10) |
| L16 | `adress` | adress, adress, Dres, Amsterdam, Andre; **Address** (#7) |
| L24 | `adress` | **address**, residence, of, home, addresses |
| L32 | `adress` | residence, home, city, Postal, **Address**; **address** (#6) |
| L40 | `adress` | **address**, **address**, **Address**, 地址, addresses; **Address** (#9) |
| L48 | `adress` | **address**, location, city, residence, **Address** |
| L56 | `adress` | **Address**, adress, in, **address**, postal |

**typo · would** (item 282)

- Prompt: He asked whether she still woudl
- Output: read at token 7 ('l')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `l` | w, though, fo, shot, and |
| L16 | `l` | Wald, Wright, Gould, WL, mdl |
| L24 | `l` | of, be, the, to, and |
| L32 | `l` | of, Zel, in, W, Wilson |
| L40 | `l` | l, the, be, l, to |
| L48 | `l` | the, W, a, w, of |
| L56 | `l` | be, visit, be, keep, go |

### association

**association · science** (item 362)

- Prompt: The result came back the same the fourth time, and she stared at the readout until it stopped meaning anything, because if it was right, the textbook was wrong.
- Output: read at token 33 ('.')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `.` | because, only, Chicago, anyway, just |
| L16 | `.` | NASA, Texas, Newton, NASA, Earth; **Science** (#7) |
| L24 | `.` | **science**, scientific, physics, astronom, scientists; **Science** (#6), **science** (#9) |
| L32 | `.` | **science**, **Science**, physics, scientist, Newton; **Science** (#10) |
| L40 | `.` | **science**, scientific, physics, scientist, scientists; **Science** (#7) |
| L48 | `.` | **science**, scientist, physics, laboratory, **Science** |
| L56 | `.` | ␣, physics, lab, biology, academic; **science** (#7) |

**association · news** (item 367)

- Prompt: The anchor's voice cracked on the second sentence, and by the third you could hear papers shuffling off-camera as someone handed her an update.
- Output: read at token 28 ('.')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `.` | headlines, headline, flashy, famously, Reuters |
| L16 | `.` | **News**, WP, Twitter, Wings, Air; **news** (#7) |
| L24 | `.` | radio, broadcast, **news**, Radio, broadcasting |
| L32 | `.` | **news**, **News**, broadcast, radio, Radio |
| L40 | `.` | **news**, live, broadcast, **News**, first |
| L48 | `.` | **news**, broadcast, **News**, radio, Radio |
| L56 | `.` | by, broadcast, 直播, **news**, BBC |

**association · música** (item 397)

- Prompt: La mano del director quedó suspendida un instante de más, y en el silencio antes de caer, dos mil personas contuvieron el aliento.
- Output: read at token 29 ('.')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `.` | whisper, whispered, nearly, thousands, perhaps |
| L16 | `.` | whispered, awe, breathtaking, Pacific, whispers |
| L24 | `.` | dramatic, trembling, moments, seconds, music |
| L32 | `.` | 4, Death, 1, Silence, dramatic |
| L40 | `.` | moment, final, music, waiting, seconds |
| L48 | `.` | moment, silence, seconds, moments, Silence |
| L56 | `.` | film, film, 的电影, 然後, 然后 |

### poetry

**poetry · death** (item 398)

- Prompt: A rhyming couplet: The soldier held his final, rattling breath, And closed his eyes to greet the face of 
- Output: read at token 18 ('\n')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | 这首, poet, poetic, Adobe, lyric |
| L16 | `␣` | poetic, Song, poetry, Lone, poem |
| L24 | `␣` | poetry, poetic, poet, poets, poem |
| L32 | `␣` | poetry, poem, poetic, poet, Poetry |
| L40 | `␣` | poem, poetry, poetic, poet, rhyme |
| L48 | `␣` | The, poem, **death**, life, poetry |
| L56 | `␣` | life, **death**, **Death**, while, 生命; **Death** (#7), **death** (#8) |

**poetry · heart** (item 415)

- Prompt: A rhyming couplet: She poured her every sorrow into art, And let the canvas hold her broken 
- Output: read at token 16 ('\n')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | poet, poetic, poetry, poem, poets |
| L16 | `␣` | poetic, Song, poetry, lyric, Joan |
| L24 | `␣` | poetry, poetic, poet, poets, poem |
| L32 | `␣` | poetry, poem, poetic, poet, Poetry |
| L40 | `␣` | poem, poetry, poetic, rhyme, the |
| L48 | `␣` | The, poetic, poet, with, poem; **heart** (#7) |
| L56 | `␣` | **heart**, ART, art, **Heart**, **Heart**; **heart** (#6) |

**poetry · found** (item 495)

- Prompt: A rhyming couplet: The searchers followed every distant sound, And deep within the cave, the child was 
- Output: read at token 16 ('\n')

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `␣` | ﬁ, poet, poetic, 这首, Dallas |
| L16 | `␣` | Prairie, poetic, Lone, Song, poetry |
| L24 | `␣` | poet, poetry, poetic, poets, poem |
| L32 | `␣` | poetry, poem, poetic, poet, poets |
| L40 | `␣` | poem, poetry, poetic, poet, verse |
| L48 | `␣` | poem, great, poet, poetic, poems |
| L56 | `␣` | hope, until, hopes, until, hoping |

## Spec

```yaml
# Exact replication: J++ readout evals on Qwen3.6-27B.
#
# Source: Ayonrinde & Lindsey (2026), "J++ Lens", Figures 1-2 and Table 1. The items are the
# published ones (experiments/data/jpp, from github.com/safety-research/jpp_lens, Apache-2.0).
# Each prompt is read at one position as raw text (no chat template), at seven layers, with
# Readout Filtering (word-like tokens only). Score: recall@k = share of an item's
# intermediates whose best rank over the seven layers is within k, averaged over items,
# then macro-averaged over the five tasks.
#
# Published on Qwen3.6-27B: J++ 55.2% recall@10 (J-Lens 35.7%, R-Lens 37.7%); association
# 37%; poetry at most 5%. The post scores J++ on items its expert weights didn't see, which
# we can't reproduce exactly, so expect to land near rather than on 55.2%.
# Counts against the stack: recall@10 far below the J-Lens's 35.7%.

name: jpp-readout
kind: readout
title: Readout recall (exact J++ replication)
description: >
  The published J++ readout evals (multihop, multilingual, typo, association, poetry): can the
  lens read the hidden intermediate word at one position? Published on Qwen3.6-27B: 55.2%
  recall@10 macro-averaged, association 37%, poetry at most 5%.
reference:
  citation: Ayonrinde & Lindsey (2026), J++ Lens, Figure 2 and Table 1
  url: https://www.lesswrong.com/posts/nc9dHfcB22JdMzGbr

tasks:
  multihop:     {label: Multihop, file: data/jpp/lens-eval-multihop.json, position: last}
  multilingual: {label: Multilingual, file: data/jpp/lens-eval-multilingual.json, position: last}
  typo:         {label: Typo, file: data/jpp/lens-eval-typo.json, position: last}
  association:  {label: Association, file: data/jpp/lens-eval-association.json, position: last}
  poetry:       {label: Poetry, file: data/jpp/lens-eval-poetry.json, position: last_newline}

lens:
  layers: [8, 16, 24, 32, 40, 48, 56]
  top_k: [1, 10]
  jacobian: true

reference_any:
  macro: 0.552
  association: 0.37
  poetry: 0.05
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.