"""Adapter for an interp-engine server (https://github.com/decoderesearch/interp-engine).

Endpoints used, as defined in interp_engine/server/app.py and schemas.py:
  GET  /v1/describe   model shape
  POST /v1/tokenize   chat template -> token ids
  POST /v1/lens       generate with the Jacobian lens attached; NDJSON, one "step" line per position
  POST /v1/capture    residual activations, for building concept vectors
  POST /v1/generate   plain generation, for the check-in and the interview

Start the server on the pod with the J++ lens loaded. Use the hooked `vllm` backend: the sit
steers a different layer and concept per request, and `vllm-static` only writes the taps it
declared at load. For example:
  python -m interp_engine.server --model Qwen/Qwen3.6-27B --backend vllm \
      --host 0.0.0.0 --port 8000 --token-file /workspace/ie-token \
      --lens-jacobians hf://koayon/jpp-lenses/qwen3.6-27b/lens.pt
"""

from __future__ import annotations

import base64
import json
from typing import Any, AsyncIterator

import httpx
import numpy as np

from .base import LayerRead, ModelInfo, Steer, Step, default_lens_layers


class InterpEngine:
    def __init__(self, url: str, token: str | None, *, chat_kwargs: dict | None = None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self._http = httpx.AsyncClient(base_url=url.rstrip("/"), headers=headers, timeout=httpx.Timeout(180, connect=20))
        # Qwen3 family: turn thinking off in the chat template.
        self._template_kwargs = chat_kwargs if chat_kwargs is not None else {"enable_thinking": False}
        self._info: ModelInfo | None = None

    async def aclose(self) -> None:
        await self._http.aclose()

    async def _post(self, path: str, body: dict) -> Any:
        r = await self._http.post(path, json=body)
        if r.status_code >= 400:
            raise RuntimeError(f"interp-engine {path} returned {r.status_code}: {r.text[:400]}")
        return r.json()

    async def describe(self) -> ModelInfo:
        if self._info is None:
            r = await self._http.get("/v1/describe")
            r.raise_for_status()
            body = r.json()
            d = body["description"]
            n_layers = int(d["n_layers"])
            d_model = int(d["d_model"])
            jac = [int(x) for x in (body.get("lens", {}).get("jacobian_layers") or [])]
            self._info = ModelInfo(
                model=str(d["hf_model_id"]),
                n_layers=n_layers,
                d_model=d_model,
                lens_layers=default_lens_layers(n_layers),
                jacobian_layers=jac,
                simulated=False,
            )
        return self._info

    async def tokenize_chat(self, messages: list[dict], *, continue_final: bool) -> list[int]:
        body = {
            "messages": messages,
            "add_generation_prompt": not continue_final,
            "continue_final_message": continue_final,
            "template_kwargs": self._template_kwargs,
        }
        return (await self._post("/v1/tokenize", body))["token_ids"]

    async def tokenize_text(self, text: str) -> list[int]:
        return (await self._post("/v1/tokenize", {"text": text, "prepend_bos": False}))["token_ids"]

    async def tokenize_raw(self, text: str) -> tuple[list[int], list[str]]:
        r = await self._post("/v1/tokenize", {"text": text})
        return r["token_ids"], r["str_tokens"]

    async def lens_read(self, prompt_ids: list[int], *, position: int, lens_layers: list[int], top_n: int) -> Step:
        """The lens readout at one prompt position, no generation."""
        body = {
            "prompt_token_ids": prompt_ids, "lenses": [{"layers": lens_layers, "jacobian": True}],
            "top_n": top_n, "max_tokens": 0, "words_only": True, "skip_before": position, "stream": False,
        }
        for msg in (await self._post("/v1/lens", body))["steps"]:
            if msg["position"] == position:
                lens = msg["lenses"][0]
                return Step(token_id=msg["token_id"], token_str=msg["token_str"], reads=[
                    LayerRead(layer=layer, words=[w.strip() for w in strs], probs=list(probs))
                    for layer, strs, probs in zip(lens_layers, lens["top_strs"], lens["top_probs"])])
        raise RuntimeError(f"interp-engine returned no readout at position {position}")

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
        body: dict[str, Any] = {
            "prompt_token_ids": prompt_ids,
            "lenses": [{"layers": lens_layers, "jacobian": True}],
            "top_n": top_n,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "seed": seed,
            "words_only": True,
            "skip_before": len(prompt_ids),
            "stream": True,
        }
        if steer is not None:
            body["steering"] = [
                {
                    "point": "resid_post",
                    "layers": {steer.layer: [{"method": "additive", "vector": steer.vector, "scale": steer.scale}]},
                }
            ]
        async with self._http.stream("POST", "/v1/lens", json=body) as r:
            if r.status_code >= 400:
                raise RuntimeError(f"interp-engine /v1/lens returned {r.status_code}: {(await r.aread())[:400]!r}")
            async for line in r.aiter_lines():
                if not line.strip():
                    continue
                msg = json.loads(line)
                if msg.get("type") == "error":
                    raise RuntimeError(f"interp-engine lens error: {msg.get('detail')}")
                if msg.get("type") != "step" or not msg.get("is_generated"):
                    continue
                lens = msg["lenses"][0]
                reads = [
                    LayerRead(layer=layer, words=[w.strip() for w in strs], probs=list(probs))
                    for layer, strs, probs in zip(lens_layers, lens["top_strs"], lens["top_probs"])
                ]
                yield Step(token_id=msg["token_id"], token_str=msg["token_str"], reads=reads)

    async def _last_resid(self, text: str, layer: int) -> np.ndarray:
        ids = await self.tokenize_chat([{"role": "user", "content": text}], continue_final=False)
        body = {"prompt_token_ids": ids, "points": [f"resid_post.{layer}"], "rows": [len(ids) - 1]}
        acts = (await self._post("/v1/capture", body))["activations"]
        payload = next(iter(acts.values()))
        return _decode(payload)[-1]

    async def concept_vector(self, concept: str, layer: int, baseline: list[str]) -> list[float]:
        """Lindsey-style concept vector: the concept's residual minus the mean of baseline words."""
        prompt = "Tell me about {}."
        target = await self._last_resid(prompt.format(concept), layer)
        base = np.mean([await self._last_resid(prompt.format(w), layer) for w in baseline if w != concept], axis=0)
        return (target - base).astype(np.float32).tolist()

    async def chat(self, messages: list[dict], *, max_tokens: int, temperature: float) -> str:
        ids = await self.tokenize_chat(messages, continue_final=False)
        body = {"prompt_token_ids": ids, "max_tokens": max_tokens, "temperature": temperature, "stream": False}
        return (await self._post("/v1/generate", body))["text"]


def _decode(payload: dict) -> np.ndarray:
    raw = base64.b64decode(payload["data"])
    if payload["dtype"] == "bfloat16":
        words = np.frombuffer(raw, dtype="<u2").astype(np.uint32) << 16
        arr = words.view(np.float32)
    else:
        arr = np.frombuffer(raw, dtype="<f4" if payload["dtype"] == "float32" else "<f2").astype(np.float32)
    return arr.reshape(payload["shape"])
