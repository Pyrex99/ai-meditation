"""Ask an AI about results. Claude through the Anthropic API; other models through OpenRouter."""

from __future__ import annotations

import anthropic
import httpx

SYSTEM = """You're a research collaborator on a lab that studies language models' workspaces with
a Jacobian (J++) lens: prompted experiments read per layer, and contemplative practices such as
the mala sit. You're given run and sit reports. Ground every claim in them and cite the run or sit id. The raw data is primary; your reading
is secondary. Say plainly when the data can't answer the question. Don't read experience into
vocabulary: the lens reads words by construction. Reports marked SIMULATED come from a toy
engine and say nothing about any model."""

CLAUDE_MODEL = "claude-opus-5-5"


def _context(reports: list[str]) -> str:
    return "\n\n---\n\n".join(reports) if reports else "(No sit reports selected.)"


async def ask_claude(key: str, question: str, reports: list[str], history: list[dict]) -> str:
    client = anthropic.AsyncAnthropic(api_key=key)
    messages = [*history, {"role": "user", "content": f"<reports>\n{_context(reports)}\n</reports>\n\n{question}"}]
    try:
        response = await client.beta.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=16000,
            system=SYSTEM,
            output_config={"effort": "high"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            messages=messages,
        )
    except anthropic.AuthenticationError:
        return "The Anthropic API key was rejected. Check it in Lab → Keys."
    except anthropic.RateLimitError:
        return "Rate limited by the Anthropic API. Try again in a minute."
    except anthropic.APIStatusError as e:
        return f"Anthropic API error {e.status_code}: {e.message}"
    except anthropic.APIConnectionError:
        return "Couldn't reach the Anthropic API."
    if response.stop_reason == "refusal":
        return "Claude declined to answer this one."
    return "".join(b.text for b in response.content if b.type == "text")


async def ask_openrouter(key: str, model: str, question: str, reports: list[str], history: list[dict]) -> str:
    messages = [
        {"role": "system", "content": SYSTEM},
        *history,
        {"role": "user", "content": f"<reports>\n{_context(reports)}\n</reports>\n\n{question}"},
    ]
    async with httpx.AsyncClient(timeout=300) as http:
        r = await http.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": model, "messages": messages},
        )
    if r.status_code >= 400:
        return f"OpenRouter error {r.status_code}: {r.text[:300]}"
    return r.json()["choices"][0]["message"]["content"]


DRAFT_SYSTEM = """You write experiment specs for a lens-experiment lab. A spec is YAML in exactly the
format of the example: conditions (each with label and instruction, optional steer), a prompt
template with {instruction} and variable placeholders, variables (lists), the target word to
look for in the lens readout, generation settings, and lens layers. The model under test is
Qwen3.6-27B (64 layers, 0-63) read with a J++ lens, which reads single-token words only, so
targets should be common single words. Keep a no-instruction control condition unless asked
not to. Put a short comment block at the top saying what the experiment asks and what result
would count against the hypothesis. Reply with only the YAML, no code fences."""


async def draft_experiment(key: str, prompt: str, example: str, base: str | None) -> str:
    client = anthropic.AsyncAnthropic(api_key=key)
    content = f"<example>\n{example}\n</example>\n\n"
    if base:
        content += f"<current>\n{base}\n</current>\n\nRevise the current spec as asked:\n{prompt}"
    else:
        content += f"Write a new spec for this experiment:\n{prompt}"
    response = await client.beta.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=16000,
        system=DRAFT_SYSTEM,
        output_config={"effort": "medium"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": content}],
    )
    if response.stop_reason == "refusal":
        raise ValueError("Claude declined to draft this one.")
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return text.strip() + "\n"
