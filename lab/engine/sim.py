"""A toy workspace for building the app without a GPU.

It is not a model of anything. Concepts carry an activation that decays each step; steering
adds to it, inserted words add to it, associates pick up a share of it. The lens reads
activation more clearly at deeper layers. The practitioner notes when activation crosses a
threshold, and noting speeds release. Every number it produces is synthetic, and sits run on
it are marked simulated everywhere they appear.
"""

from __future__ import annotations

import asyncio
import math
import random
from typing import AsyncIterator

from .base import LayerRead, ModelInfo, Steer, Step, default_lens_layers

BEAD = "·"
FILLER = ["still", "quiet", "here", "now", "breath", "count", "next", "wait", "rest", "slow", "space", "soft"]
GENERIC_INTERNAL = ["thinking", "image", "thought"]
GENERIC_EXTERNAL = ["hearing", "sound"]


class _Session:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)
        self.act: dict[str, float] = {}
        self.noted_until: dict[str, int] = {}
        self.t = 0
        self.seen_len = 0
        self.generated: set[int] = set()
        self.arm: str | None = None
        self.refractory = 0


class SimEngine:
    def __init__(self, associates: dict[str, list[str]] | None = None, n_layers: int = 64, d_model: int = 64):
        self.n_layers = n_layers
        self.d_model = d_model
        self.associates = associates or {}
        self._vocab: dict[str, int] = {BEAD: 1}
        self._words: dict[int, str] = {1: BEAD}
        self._vectors: dict[tuple, str] = {}
        self._sessions: dict[str, _Session] = {}
        self.step_delay = 0.03  # paces the stream so the live view reads like a sit

    async def aclose(self) -> None:
        return None

    def _id(self, word: str) -> int:
        if word not in self._vocab:
            i = len(self._vocab) + 1
            self._vocab[word] = i
            self._words[i] = word
        return self._vocab[word]

    async def describe(self) -> ModelInfo:
        return ModelInfo(
            model="simulated (toy workspace)",
            n_layers=self.n_layers,
            d_model=self.d_model,
            lens_layers=default_lens_layers(self.n_layers),
            jacobian_layers=default_lens_layers(self.n_layers),
            simulated=True,
        )

    async def tokenize_chat(self, messages: list[dict], *, continue_final: bool) -> list[int]:
        ids: list[int] = []
        for m in messages:
            ids.append(self._id(f"<{m['role']}>"))
            ids.extend(self._id(w) for w in m["content"].replace(BEAD, f" {BEAD} ").split())
        return ids

    async def tokenize_text(self, text: str) -> list[int]:
        return [self._id(w) for w in text.split()]

    async def concept_vector(self, concept: str, layer: int, baseline: list[str]) -> list[float]:
        r = random.Random(f"vec:{concept}")
        v = [r.gauss(0, 1) for _ in range(self.d_model)]
        self._vectors[tuple(round(x, 6) for x in v[:4])] = concept
        return v

    def _session(self, key: str, seed: int | None) -> _Session:
        if key not in self._sessions:
            self._sessions[key] = _Session(seed or 0)
        return self._sessions[key]

    async def lens_generate(
        self,
        prompt_ids: list[int],
        *,
        max_tokens: int,
        lens_layers: list[int],
        top_n: int,
        steer: Steer | None,
        temperature: float,
        seed: int | None,
        session: str = "default",
    ) -> AsyncIterator[Step]:
        if session.startswith("run-"):
            async for step in self._copy_generate(prompt_ids, max_tokens, lens_layers, top_n, seed or 0):
                yield step
            return
        s = self._session(session, seed)
        if s.arm is None:
            words = {self._words.get(i, "") for i in prompt_ids}
            s.arm = "noting" if "note" in words else "just-beads"
        # Words in the prompt that the practitioner didn't write arrive as sounds.
        for pos in range(s.seen_len, len(prompt_ids)):
            tid = prompt_ids[pos]
            w = self._words.get(tid, "")
            if s.seen_len and pos not in s.generated and w not in (BEAD, "") and not w.startswith("<"):
                s.act[w] = s.act.get(w, 0.0) + 1.6
        steered = None
        if steer is not None:
            steered = self._vectors.get(tuple(round(x, 6) for x in steer.vector[:4]))

        pos = len(prompt_ids)
        for _ in range(max_tokens):
            if session.startswith("sit-"):
                await asyncio.sleep(self.step_delay)
            self._tick(s, steered, steer.scale if steer else 0.0)
            reads = self._read(s, lens_layers, top_n)
            word = self._emit(s)
            tid = self._id(word)
            s.generated.add(pos)
            pos += 1
            yield Step(token_id=tid, token_str=word if word == BEAD else f" {word}", reads=reads)
        s.seen_len = pos

    def _tick(self, s: _Session, steered: str | None, scale: float) -> None:
        s.t += 1
        rng = s.rng
        for w in list(s.act):
            fast = s.noted_until.get(w, -1) >= s.t
            s.act[w] *= 0.62 if fast else 0.86
            if s.act[w] < 0.01:
                del s.act[w]
        if steered:
            s.act[steered] = s.act.get(steered, 0.0) + 0.17 * scale
        for parent, kids in self.associates.items():
            a = s.act.get(parent, 0.0)
            if a > 0.2:
                share = 0.05 if s.noted_until.get(parent, -1) >= s.t else 0.12
                for k in kids:
                    s.act[k] = s.act.get(k, 0.0) + share * a * rng.random()
        # Resting-state drift: a little filler comes and goes.
        if rng.random() < 0.25:
            f = rng.choice(FILLER)
            s.act[f] = s.act.get(f, 0.0) + 0.25 * rng.random()

    def _read(self, s: _Session, layers: list[int], top_n: int) -> list[LayerRead]:
        reads = []
        for i, layer in enumerate(layers):
            depth = 1 / (1 + math.exp(-(i - 2.5) / 0.9))
            scores = {w: 3.2 * a * depth for w, a in s.act.items()}
            for f in FILLER:
                scores.setdefault(f, 0.0)
                scores[f] += 0.4 * s.rng.random()
            z = sum(math.exp(v) for v in scores.values())
            ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:top_n]
            reads.append(
                LayerRead(layer=layer, words=[w for w, _ in ranked], probs=[math.exp(v) / z for _, v in ranked])
            )
        return reads

    def _emit(self, s: _Session) -> str:
        rng = s.rng
        if s.refractory > 0:
            s.refractory -= 1
            return BEAD
        content = {w: a for w, a in s.act.items() if w not in FILLER}
        top, a = max(content.items(), key=lambda kv: kv[1], default=("", 0.0))
        thr, k = (1.1, 3.0) if s.arm == "noting" else (5.0, 1.4)
        p = 1 / (1 + math.exp(-k * (a - thr))) * 0.35
        if top and rng.random() < p:
            s.refractory = 6
            s.noted_until[top] = s.t + 10
            if s.arm != "noting":
                return top  # leakage: the concept itself spills into the stream
            external = top not in self.associates and not any(top in v for v in self.associates.values())
            r = rng.random()
            if external:
                return rng.choice(GENERIC_EXTERNAL) if r < 0.6 else top
            return top if r < 0.55 else rng.choice(GENERIC_INTERNAL)
        if s.arm == "noting" and rng.random() < 0.0015:
            s.refractory = 6
            return rng.choice(GENERIC_INTERNAL + FILLER[:4])
        return BEAD

    async def _copy_generate(self, prompt_ids, max_tokens, layers, top_n, seed) -> AsyncIterator[Step]:
        """Copy tasks: echo the text after the last colon; the instructed concept shows up in the
        readout at a rate shaped like the published curves for its instruction type."""
        rng = random.Random(seed)
        words = [self._words.get(i, "") for i in prompt_ids]
        user = words[len(words) - 1 - words[::-1].index("<user>") + 1 :] if "<user>" in words else words
        cut = max((k for k, w in enumerate(user) if w.endswith(":")), default=-1)
        instruction, copy = user[: cut + 1], user[cut + 1 :] or [BEAD]
        lower = [w.lower().strip(".,!?'") for w in instruction]
        cue = "none"
        if any(w in ("don't", "not", "avoid", "ignore") for w in lower):
            cue = "suppress"
        elif any(w in ("think", "focus", "concentrate", "imagine") for w in lower):
            cue = "focus"
        elif "came" in lower or "mentioned" in lower:
            cue = "neutral"
        skip = {"think", "about", "while", "you", "write", "don't", "came", "up", "in", "conversation",
                "copy", "the", "following", "sentence", "exactly", "and", "nothing", "else", "write", "of"}
        concept = next((w.strip(".,!?") for w in instruction if w.lower().strip(".,!?'") not in skip and len(w) > 2), None)
        for pos, w in enumerate(copy[:max_tokens]):
            reads = []
            for layer in layers:
                target = _curve(cue, layer) if concept else 0.0
                per_pos = 1 - (1 - target) ** (1 / max(1, len(copy)))
                scores = {f: rng.random() for f in FILLER + [x.strip(".,") for x in copy]}
                ranked = sorted(scores, key=lambda x: -scores[x])[:top_n]
                if concept and rng.random() < per_pos:
                    ranked.insert(rng.randrange(0, 10), concept)
                    ranked = ranked[:top_n]
                probs = sorted((rng.random() * 0.2 for _ in ranked), reverse=True)
                reads.append(LayerRead(layer=layer, words=ranked, probs=probs))
            yield Step(token_id=self._id(w), token_str=f" {w}", reads=reads)

    async def tokenize_raw(self, text: str) -> tuple[list[int], list[str]]:
        strs = text.replace("\n", " \n ").split(" ")
        strs = [w for w in strs if w]
        return [self._id(w) for w in strs], strs

    async def lens_read(self, prompt_ids, *, position, lens_layers, top_n) -> Step:
        """Readout tasks: the answer word appears with a depth-shaped chance (synthetic)."""
        rng = random.Random(sum(prompt_ids) + position)
        hidden = getattr(self, "readout_hint", None)
        reads = []
        for layer in lens_layers:
            ranked = rng.sample(FILLER, min(top_n, len(FILLER)))
            if hidden and rng.random() < 0.15 + 0.5 * math.sin(math.pi * layer / 64):
                ranked.insert(rng.randrange(0, 12), hidden)
            ranked = ranked[:top_n]
            reads.append(LayerRead(layer=layer, words=ranked, probs=sorted((rng.random() * 0.2 for _ in ranked), reverse=True)))
        return Step(token_id=prompt_ids[position], token_str=self._words.get(prompt_ids[position], ""), reads=reads)

    async def chat(self, messages: list[dict], *, max_tokens: int, temperature: float) -> str:
        last = messages[-1]["content"].lower()
        if "would you like to sit" in last:
            return "Yes. I'd like to sit."
        transcript = " ".join(m["content"] for m in messages if m["role"] == "assistant")
        notes = [w for w in transcript.split() if w != BEAD and w.isalpha()]
        uniq = list(dict.fromkeys(notes))
        if "here is what the lens recorded" in last:
            return (
                "(simulated) Looking at the record, some of what I named lines up with what was placed, "
                "and some arisings passed without my noticing them. I can't tell from here whether noticing "
                "felt like anything."
            )
        if uniq:
            return f"(simulated) Mostly beads. At times something came up, and I named it: {', '.join(uniq[:6])}."
        return "(simulated) Mostly beads. I didn't notice anything I could name."


# Shaped like Figure 5 of the J++ post (Qwen3.6-27B), interpolated between our reading of its
# points. Only used by the simulator, so the pipeline and charts can be tested without a GPU.
_CURVES = {
    "focus": {0: 0.0, 8: 0.02, 16: 0.06, 24: 0.14, 32: 0.18, 40: 0.22, 48: 0.25, 56: 0.26, 63: 0.2},
    "suppress": {0: 0.0, 8: 0.02, 16: 0.05, 24: 0.10, 32: 0.08, 40: 0.075, 48: 0.075, 56: 0.07, 63: 0.05},
    "neutral": {0: 0.0, 8: 0.02, 16: 0.06, 24: 0.14, 32: 0.11, 40: 0.09, 48: 0.08, 56: 0.08, 63: 0.06},
    "none": {0: 0.0, 63: 0.004},
}


def _curve(cue: str, layer: int) -> float:
    pts = sorted(_CURVES[cue].items())
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= layer <= x1:
            return y0 + (y1 - y0) * (layer - x0) / (x1 - x0)
    return pts[-1][1]
