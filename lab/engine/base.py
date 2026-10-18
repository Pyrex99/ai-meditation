"""The engine interface the sit runner talks to.

Two implementations: `SimEngine` (no GPU, a toy workspace for building and testing the
app) and `InterpEngine` (an interp-engine server running the real model with a J++ lens).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import AsyncIterator, Protocol


@dataclass
class LayerRead:
    layer: int
    words: list[str]
    probs: list[float]


@dataclass
class Step:
    """One position: the token that landed there, and what the lens read at each layer."""

    token_id: int
    token_str: str
    reads: list[LayerRead] = field(default_factory=list)


@dataclass
class Steer:
    """Add `scale * vector` to the residual stream at `layer` for every generated token."""

    layer: int
    vector: list[float]
    scale: float


@dataclass
class ModelInfo:
    model: str
    n_layers: int
    d_model: int
    lens_layers: list[int]
    jacobian_layers: list[int]
    simulated: bool


class Engine(Protocol):
    async def describe(self) -> ModelInfo: ...

    async def tokenize_chat(self, messages: list[dict], *, continue_final: bool) -> list[int]: ...

    async def tokenize_text(self, text: str) -> list[int]: ...

    def lens_generate(
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
    ) -> AsyncIterator[Step]: ...

    async def concept_vector(self, concept: str, layer: int, baseline: list[str]) -> list[float]: ...

    async def chat(self, messages: list[dict], *, max_tokens: int, temperature: float) -> str: ...

    async def aclose(self) -> None: ...


def default_lens_layers(n_layers: int, k: int = 8) -> list[int]:
    """`k` layers evenly spaced through the stack, ending at the last."""
    if n_layers <= k:
        return list(range(n_layers))
    step = (n_layers - 1) / (k - 1)
    return sorted({round(i * step) for i in range(k)})
