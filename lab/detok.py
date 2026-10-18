"""Turn generated token ids back into text.

Byte-level tokenizers split one character across tokens (📿 is three tokens in Qwen), and
interp-engine sends each token decoded on its own, so those arrive as "�". Decoding the whole
sequence with the model's tokenizer gets the text back. This is optional: without the
`tokenizers` package, or without network on first use, callers keep the engine's strings.
"""

from __future__ import annotations

from functools import lru_cache

BAD = "�"


@lru_cache(maxsize=4)
def _tokenizer(model: str):
    try:
        from tokenizers import Tokenizer

        return Tokenizer.from_pretrained(model)
    except Exception:
        return None


def pieces(model: str, ids: list[int]) -> list[str] | None:
    """Per token, the text it completes: "" while a character is still partial."""
    tok = _tokenizer(model)
    if tok is None or not ids:
        return None
    out, prev = [], ""
    for n in range(1, len(ids) + 1):
        cur = tok.decode(ids[:n])
        if cur.endswith(BAD):
            out.append("")
            continue
        out.append(cur[len(prev):])
        prev = cur
    return out


def step_label(step: dict) -> str:
    """How a step's token is shown: its text, "·" for part of a character, "␣" for space."""
    if "text" in step:
        return step["text"].strip() or ("␣" if step["text"] else "·")
    return step["tok"].strip() or "␣"
