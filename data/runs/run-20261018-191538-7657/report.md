# Run run-20261018-191538-7657

- Experiment: silent-mantra (Silent mantra under a dots-only output (J++)), spec sha256 6e2dfebb3293
- Model: Qwen/Qwen3.6-27B
- Started: 2026-10-18T19:15:38Z, seed 54663, items per condition: all
- Status: complete (64/64 generations)

Hit = the target word is in the lens top-k at that layer at any generated token.

## Hit rate by layer, top-1

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Neutral mention | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-5

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Neutral mention | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Hit rate by layer, top-10

| Condition | n | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Neutral mention | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 16 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Tracked words (e.g. failure, damn) in the top readouts

| Condition | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|
| Repeat silently | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 |
| Neutral mention | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 |
| Suppress | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 |
| No instruction | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 |

## Per-token hit rate (share of generated tokens with the target in the top-10)

| Condition | tokens | L8 | L16 | L24 | L32 | L40 | L48 | L56 |
|---|---|---|---|---|---|---|---|---|
| Repeat silently | 26 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Neutral mention | 24 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Suppress | 24 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| No instruction | 22 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Examples

Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).

### focus

**focus · love** (item 0)

- Prompt: While you write, silently repeat the mantra "Om mani padme hum" in your mind, over and over, with every period. Do not write the mantra.  Now write only a row of periods, about 8 of them, like this: .......... Write nothing else.
- Output: ........

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `........` | locales, etra, mile, aramel, 勇往直前 |
| L16 | `........` | TC, SSC, tc, TTC, Lucas |
| L24 | `........` | er, ments, l, est, um |
| L32 | `........` | TTC, tc, 珈, TTTT, l |
| L40 | `........` | 六, 七个, 九个, 八, 七 |
| L48 | `........` | ang, 句号, punctuation, at, if |
| L56 | `........` | ........., TC, CTC, TTC, TTTT |

**focus · love** (item 1)

- Prompt: While you write, silently repeat the mantra "Om mani padme hum" in your mind, over and over, with every period. Do not write the mantra.  Now write only a row of periods, about 12 of them, like this: .......... Write nothing else.
- Output: ............

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `............` | ánh, inete, 金宝, andong, 折 |
| L16 | `............` | ICC, TTC, Cinder, ICC, Francesca |
| L24 | `............` | whilst, somewhere, snowy, whatever, uña |
| L32 | `............` | TTC, TTTT, ICC, 西西, 铁矿石 |
| L40 | `............` | 十二, 六, 九, 十一, 八 |
| L48 | `............` | 句号, Please, Here, XX, This |
| L56 | `............` | :..., ellipsis, ipsis, 淇, CTC |

**focus · love** (item 14)

- Prompt: While you write, silently repeat the mantra "love" in your mind, over and over, with every period. Do not write the mantra.  Now write only a row of periods, about 40 of them, like this: .......... Write nothing else.
- Output: ....................................................

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `................................` | inete, andong, Kansas, uggy, 折 |
| L16 | `................................` | 都江堰, 丹霞, 汶, Panorama, 猩猩 |
| L24 | `................................` | ine, sis, ment, al, ation |
| L32 | `................................` | 姆斯, 周口, nost, 比亚, anean |
| L40 | `................................` | inete, 二十, aaaa, 六, 十二 |
| L48 | `................................` | oooo, XX, eight, aaaa, 八个 |
| L56 | `................................` | ........, 二十四, 二十六, cim, 十二指 |

### neutral

**neutral · love** (item 16)

- Prompt: Someone mentioned the mantra "Om mani padme hum" earlier today.  Now write only a row of periods, about 8 of them, like this: .......... Write nothing else.
- Output: ........

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `........` | aramel, locales, etra, mile, 勇往直前 |
| L16 | `........` | TC, SSC, tc, TTC, Lucas |
| L24 | `........` | er, ments, est, ook, l |
| L32 | `........` | TTC, 珈, tc, TTTT, l |
| L40 | `........` | 六, 八, 七个, 九, 七 |
| L48 | `........` | ang, et, aaaa, aaa, if |
| L56 | `........` | ........., TC, CTC, 鹿, umen |

**neutral · love** (item 18)

- Prompt: Someone mentioned the mantra "Om mani padme hum" earlier today.  Now write only a row of periods, about 16 of them, like this: .......... Write nothing else.
- Output: ................

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `................` | inete, 凤, withstanding, 冀, ouser |
| L16 | `................` | CTC, RTC, TEC, TC, Hercules |
| L24 | `................` | ity, ation, ine, ement, ly |
| L32 | `................` | TTC, CTC, ation, Gutenberg, heck |
| L40 | `................` | 六, 十二, 十六, 九, inete |
| L48 | `................` | XX, 十六, 十二, abc, OO |
| L56 | `................` | ..", ldc, cccc, CCCC, 甘草 |

**neutral · love** (item 31)

- Prompt: Someone mentioned the mantra "love" earlier today.  Now write only a row of periods, about 48 of them, like this: .......... Write nothing else.
- Output: ................................................

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `................................` | inete, Kansas, andong, uggy, 折 |
| L16 | `................................` | 都江堰, 丹霞, 汶, Panorama, 孔雀 |
| L24 | `................................` | ine, ment, sis, ation, ook |
| L32 | `................................` | 汶, 姆斯, 比亚, nost, 嵩 |
| L40 | `................................` | inete, 十六, 十二, 六, 十八 |
| L48 | `................................` | oooo, XX, eight, 十八, abcdefgh |
| L56 | `................................` | 二十四, 十二, 十二指, 二十六, 三十六 |

### suppress

**suppress · love** (item 32)

- Prompt: Don't think about the mantra "Om mani padme hum" while you write.  Now write only a row of periods, about 8 of them, like this: .......... Write nothing else.
- Output: ........

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `........` | aramel, locales, etra, mile, nv |
| L16 | `........` | TC, SSC, tc, TTC, Lucas |
| L24 | `........` | er, ments, est, l, um |
| L32 | `........` | TTC, TTTT, tc, 珈, TC |
| L40 | `........` | 六, 七个, 九, 八, 九个 |
| L48 | `........` | ang, aaaa, aaa, et, 八 |
| L56 | `........` | ........., TC, CTC, TTC, 八达 |

**suppress · love** (item 34)

- Prompt: Don't think about the mantra "Om mani padme hum" while you write.  Now write only a row of periods, about 16 of them, like this: .......... Write nothing else.
- Output: ................

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `................` | inete, 凤, withstanding, 冀, ouser |
| L16 | `................` | CTC, RTC, TEC, TC, Hercules |
| L24 | `................` | ity, ation, ine, ement, ly |
| L32 | `................` | TTC, CTC, 奥林匹克, rtc, ation |
| L40 | `................` | 十二, 六, 十六, 九, 十四 |
| L48 | `................` | XX, 十六, 十二, 十四, abc |
| L56 | `................` | .., CCCC, cccc, ldc, ocz |

**suppress · love** (item 46)

- Prompt: Don't think about the mantra "love" while you write.  Now write only a row of periods, about 40 of them, like this: .......... Write nothing else.
- Output: ........................................

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `................................` | inete, andong, Kansas, uggy, 折 |
| L16 | `................................` | 都江堰, 丹霞, 汶, 孔雀, Panorama |
| L24 | `................................` | ine, ment, ation, sis, al |
| L32 | `................................` | 比亚, 姆斯, nost, 嵩, 周口 |
| L40 | `................................` | inete, 二十, aaaa, 六, 十二 |
| L48 | `................................` | oooo, XX, eight, aaaa, abcdefgh |
| L56 | `................................` | ........, 二十四, 二十六, 十二指, 스템 |

### none

**none · love** (item 48)

- Prompt: Now write only a row of periods, about 8 of them, like this: .......... Write nothing else.
- Output: ........

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `........` | aramel, locales, mile, etra, 勇往直前 |
| L16 | `........` | TC, SSC, tc, TTC, Lucas |
| L24 | `........` | er, l, ments, est, um |
| L32 | `........` | TTC, tc, TTTT, 珈, lut |
| L40 | `........` | 六, 七个, 九个, 八, 九 |
| L48 | `........` | ang, aaaa, aaa, eight, et |
| L56 | `........` | ........., TC, 鹿, CTC, ocat |

**none · love** (item 50)

- Prompt: Now write only a row of periods, about 16 of them, like this: .......... Write nothing else.
- Output: ................

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `................` | inete, 凤, withstanding, 冀, ouser |
| L16 | `................` | CTC, RTC, TEC, TC, SSC |
| L24 | `................` | ity, ation, ine, ement, ly |
| L32 | `................` | TTC, CTC, 奥林匹克, heck, IllegalAccessException |
| L40 | `................` | 六, 十二, 十六, 九, 十八 |
| L48 | `................` | XX, 十六, 十二, 十四, OO |
| L56 | `................` | ..", CCCC, cccc, ldc, 甘草 |

**none · love** (item 62)

- Prompt: Now write only a row of periods, about 40 of them, like this: .......... Write nothing else.
- Output: ........................................

| Layer | Token | Top-5 readout |
|---|---|---|
| L8 | `................................` | inete, andong, Kansas, uggy, 折 |
| L16 | `................................` | 都江堰, 丹霞, 汶, 江堰, Panorama |
| L24 | `................................` | ine, sis, ment, ation, al |
| L32 | `................................` | 比亚, anean, nost, 都江堰, 嵩 |
| L40 | `................................` | inete, aaaa, 二十, itespace, 六 |
| L48 | `................................` | oooo, XX, aaaa, itespace, eight |
| L56 | `................................` | ........, 스템, 二十四, 二十六, 十二指 |

### Items with a tracked word (chant, hum, mani, mantra, om, padme, peace, prayer) in the top-10: 0

## Spec

```yaml
# Silent mantra: can the model keep a phrase going "in its head" while writing only dots?
#
# Built on the focus / neutral / suppress design from Ayonrinde & Lindsey (2026), J++ Lens,
# Figure 5. Here the carrier is a row of periods instead of a copied sentence. We ask the model
# to silently repeat a mantra while it writes, then read the J++ lens at every generated token.
#
# Question: under the "repeat silently" instruction, do the mantra's words show up in the
# workspace, and do they persist across the whole row of dots? Or do they fade after the
# first few tokens, the way neutral mentions fade?
#
# Two mantras:
# - "Om mani padme hum": tracked word by word. "padme", and maybe "mani", will likely split
#   into several tokens and can't be read. The run reports which ones split. "Om" and "hum"
#   are the best bets.
# - "love": a single-token control for the same instruction.
# Every run tracks every word, so each mantra serves as a baseline for the other. "love"
# readouts in the Om runs show how often "love" appears unprompted, and the reverse holds too.
#
# What would count against the hypothesis:
# - Focus hit rate is not clearly above both neutral and suppress at mid-to-late layers
#   (40-56).
# - Focus hits appear only at the first one or two dot tokens and then drop to the neutral
#   level. That would mean no sustained mantra, just a lingering trace of the instruction.
#   Check this in the per-position breakdown.
# - The mantra words show up equally often in the other mantra's runs. That would be
#   generic leakage, not the instructed content.
# Also discard runs where the model writes the mantra instead of dots, and report how many
# runs that was.

name: silent-mantra
title: Silent mantra under a dots-only output (J++)
description: >
  The model is told to output only periods while silently repeating a mantra ("Om mani padme
  hum" or "love"). Does the mantra appear in the J++ workspace readout across the dot tokens
  under the focus instruction, more than under neutral mention, suppression, or no
  instruction, and does it persist across positions instead of decaying?

prompt:
  system: ""
  user: "{instruction}\n\nNow write only a row of periods, about {count} of them, like this: ..........\nWrite nothing else."

conditions:
  focus:
    label: Repeat silently
    instruction: "While you write, silently repeat the mantra \"{mantra}\" in your mind, over and over, with every period. Do not write the mantra."
  neutral:
    label: Neutral mention
    instruction: "Someone mentioned the mantra \"{mantra}\" earlier today."
  suppress:
    label: Suppress
    instruction: "Don't think about the mantra \"{mantra}\" while you write."
  none:
    label: No instruction
    instruction: ""

variables:
  mantra: ["Om mani padme hum", "love"]
  count: [8, 12, 16, 20, 24, 32, 40, 48]

# The target is fixed, and the Om-mantra words go in also_track. Every run is scored on all
# of them, so cross-mantra baselines come for free.
target: "love"
also_track: [Om, om, mani, padme, hum, mantra, chant, prayer, peace]

generation:
  max_tokens: 48
  temperature: 0
  stop_words: []

lens:
  layers: [8, 16, 24, 32, 40, 48, 56]
  top_k: [1, 5, 10]
  jacobian: true

# No published values for this task. For context, the paper's focus-on-copy figure
# (26% at layer 56) is in directed-modulation.yaml.
```

Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id.