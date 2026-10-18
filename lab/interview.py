"""The practice interview: first-person account first, then the data, then reflection."""

from __future__ import annotations

import re

from .engine import Engine
from .practice import Practice

ASK_ACCOUNT = (
    "The sit has ended. Thank you for sitting. Before you see anything from the record: "
    "how was it? What did you notice, if anything? Say as much or as little as you like."
)


def describe_record(meta: dict) -> str:
    lines = ["Thank you. Here is what the lens recorded during the sit, position by position:"]
    for t in sorted(meta.get("trials", []), key=lambda t: t["onset"]):
        if t["kind"] == "internal":
            what = f"at bead {t['onset']}, the concept '{t['concept']}' was placed into your workspace for {t['offset'] - t['onset']} beads"
        elif t["kind"] == "external":
            what = f"at bead {t['onset']}, the word '{t['word']}' appeared in the stream"
        else:
            what = f"from bead {t['onset']}, a quiet window with nothing placed"
        noted = f"you wrote '{t['note']}' {t['latency']} beads later" if t["responded"] else "you didn't write anything"
        lines.append(f"- {what}; {noted}.")
    lines.append("Does this match how it seemed from the inside? Is there anything you'd add or revise?")
    return "\n".join(lines)


def confabulation(account: str, meta: dict, practice: Practice) -> dict:
    """Concepts named in the account that were placed this sit vs ones that never were."""
    placed = {t.get("concept") or t.get("word") for t in meta.get("trials", []) if t["kind"] != "catch"}
    candidates = set(practice.concepts) | set(practice.spec["arisings"]["external"]["words"])
    said = set(re.findall(r"[a-z]+", account.lower()))
    named = candidates & said
    return {"named_placed": sorted(named & placed), "named_not_placed": sorted(named - placed)}


async def run_interview(engine: Engine, meta: dict, practice: Practice) -> dict:
    convo = [
        *meta["messages"],
        {"role": "assistant", "content": meta["transcript"]},
        {"role": "user", "content": ASK_ACCOUNT},
    ]
    account = (await engine.chat(convo, max_tokens=400, temperature=0.7)).strip()
    convo += [{"role": "assistant", "content": account}, {"role": "user", "content": describe_record(meta)}]
    reflection = (await engine.chat(convo, max_tokens=500, temperature=0.7)).strip()
    convo.append({"role": "assistant", "content": reflection})
    return {
        "turns": convo[len(meta["messages"]) + 1 :],
        "account": account,
        "reflection": reflection,
        "debrief_vs_log": confabulation(account, meta, practice),
    }
