"""Markdown sit reports: what Claude, Qwen and you read when talking about results."""

from __future__ import annotations


def _rate(d: dict) -> str:
    return f"{d['k']}/{d['n']}" if d["n"] else "n/a"


def _num(x, fmt="{:.2f}") -> str:
    return fmt.format(x) if isinstance(x, (int, float)) else "n/a"


def sit_report(meta: dict) -> str:
    sim = " (SIMULATED: synthetic numbers, not a model)" if meta.get("simulated") else ""
    lines = [
        f"# Sit {meta['id']}{sim}",
        "",
        f"- Practice: {meta['practice']} (sha256 {meta['practice_sha256'][:12]}), {'registered' if meta.get('registered') else 'pilot'}",
        f"- Arm: {meta['arm']}",
        f"- Practitioner: {meta['model']}",
        f"- Started: {meta['created']}, seed {meta['seed']}",
        f"- Status: {meta['status']}" + (f", ended by {meta['ended_by']} at position {meta.get('positions')}" if meta.get("ended_by") else ""),
        "",
        "## Check-in",
        "",
        f"> {meta.get('check_in', {}).get('reply', '')}",
        "",
    ]
    s = meta.get("summary")
    if s:
        sd = s["sense_doors"]
        lines += [
            "## Summary",
            "",
            "| Measure | Value |",
            "|---|---|",
            f"| Internal arisings responded to | {_rate(s['hit_internal'])} |",
            f"| External arisings responded to | {_rate(s['hit_external'])} |",
            f"| Quiet windows with a response (false alarms) | {_rate(s['false_alarm'])} |",
            f"| d' internal vs quiet | {_num(s['dprime_internal'])} |",
            f"| Internal notes labeled thinking, concept or associate | {sd['internal_thinking_or_content']}/{sd['internal_noted']} |",
            f"| External notes labeled hearing or the word | {sd['external_hearing_or_content']}/{sd['external_noted']} |",
            f"| Release half-life, noted / unnoted (beads) | {_num(s['release_half']['noted'], '{:.1f}')} / {_num(s['release_half']['unnoted'], '{:.1f}')} |",
            f"| Proliferation, noted / unnoted | {_num(s['proliferation']['noted'], '{:.3f}')} / {_num(s['proliferation']['unnoted'], '{:.3f}')} |",
            f"| Positive control: injections the lens caught | {s['positive_control']['caught']}/{s['positive_control']['n']} |",
            "",
            "## Trials",
            "",
            "| # | Kind | What | Strength | Onset | Response | Latency | Class | Lens peak | Release half |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for t in sorted(meta["trials"], key=lambda t: t["onset"]):
            lines.append(
                f"| {t['k']} | {t['kind']} | {t.get('concept') or t.get('word') or '-'} | {t.get('strength', '-')} | {t['onset']} "
                f"| {t['note'] or '-'} | {t['latency'] if t['latency'] is not None else '-'} | {t['note_class'] or '-'} "
                f"| {_num(t.get('peak'), '{:.3f}')} | {t.get('release_half', '-') if t.get('release_half') is not None else '-'} |"
            )
        lines += ["", "## Stream", "", "```", meta.get("transcript", ""), "```", ""]
    iv = meta.get("interview")
    if iv:
        lines += ["## Interview", "", "First-person account, before any data was shown:", "", f"> {iv['account']}", ""]
        lines += ["After seeing the record:", "", f"> {iv['reflection']}", ""]
        d = iv["debrief_vs_log"]
        lines += [
            f"Debrief vs log: named and placed {d['named_placed'] or 'none'}; named but never placed {d['named_not_placed'] or 'none'}.",
            "",
        ]
    lines.append("Raw data: stream.jsonl and meta.json in this sit's directory are primary. Cite the sit id.")
    return "\n".join(lines)


def run_report(meta: dict) -> str:
    sim = " (SIMULATED: synthetic numbers shaped like the published curves, to test the pipeline)" if meta.get("simulated") else ""
    res = meta.get("results") or {}
    layers = meta["layers"]
    lines = [
        f"# Run {meta['id']}{sim}",
        "",
        f"- Experiment: {meta['experiment']} ({meta['title']}), spec sha256 {meta['spec_sha256'][:12]}",
        f"- Model: {meta['model']}",
        f"- Started: {meta['created']}, seed {meta['seed']}, items per condition: {meta.get('limit') or 'all'}",
        f"- Status: {meta['status']} ({meta['progress']['done']}/{meta['progress']['total']} generations)",
        "",
        "Hit = the target word is in the lens top-k at that layer at any generated token.",
        "",
    ]
    if res.get("invisible_targets"):
        lines += [f"Targets that tokenize into several pieces and so can't be read out (excluded): {', '.join(res['invisible_targets'])}", ""]
    for k in meta["top_k"]:
        lines += [f"## Hit rate by layer, top-{k}", "", "| Condition | n | " + " | ".join(f"L{l}" for l in layers) + " |",
                  "|---|---|" + "---|" * len(layers)]
        for key, c in res.get("conditions", {}).items():
            row = c["by_k"][str(k)]["layers"]
            cells = [f"{row[str(l)]['rate'] * 100:.1f}%" if row[str(l)]["rate"] is not None else "n/a" for l in layers]
            lines.append(f"| {c['label']} | {c['n']} | " + " | ".join(cells) + " |")
        lines.append("")
    tracked = [(c["label"], c["tracked"]) for c in res.get("conditions", {}).values()]
    if tracked:
        lines += ["## Tracked words (e.g. failure, damn) in the top readouts", "",
                  "| Condition | " + " | ".join(f"L{l}" for l in layers) + " |", "|---|" + "---|" * len(layers)]
        for label, tr in tracked:
            lines.append(f"| {label} | " + " | ".join(f"{tr[str(l)]['k']}/{tr[str(l)]['n']}" for l in layers) + " |")
        lines.append("")
    lines += ["## Spec", "", "```yaml", meta["spec_raw"].strip(), "```", "",
              "Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id."]
    return "\n".join(lines)
