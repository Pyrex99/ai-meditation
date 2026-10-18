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


def run_report(meta: dict, items: list[dict] | None = None) -> str:
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
        ("Recall@k = share of an item's hidden words in the lens top-k at the read position."
         if meta.get("kind") == "readout" else
         "Hit = the target word is in the lens top-k at that layer at any generated token."),
        "",
    ]
    if meta.get("failed"):
        lines += [f"{meta['failed']} generations failed after a retry and are left out. Last error: {meta.get('last_failure', '')}", ""]
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
    if items:
        lines += _readout_best(meta, res) if meta.get("kind") == "readout" else _per_position(meta, items)
        lines += _examples(meta, items)
    lines += ["## Spec", "", "```yaml", meta["spec_raw"].strip(), "```", "",
              "Raw data: items.jsonl (every prompt, output and per-token readout) is primary. Cite the run id."]
    return "\n".join(lines)


def _w(word: str, target: set[str], track: set[str]) -> str:
    """A readout word, bold if it is the target, marked † if it is a tracked word."""
    n = word.strip().lower()
    w = word.strip().replace("|", "\\|") or "␣"
    return f"**{w}**" if n in target else f"{w}†" if n in track else w


def _track_words(meta: dict) -> set[str]:
    import yaml

    try:
        return {str(x).lower() for x in (yaml.safe_load(meta["spec_raw"]).get("also_track") or [])}
    except Exception:
        return set()


def _readout_best(meta: dict, res: dict) -> list[str]:
    import yaml

    k = str(meta["top_k"][-1])
    try:
        ref = yaml.safe_load(meta["spec_raw"]).get("reference_any") or {}
    except Exception:
        ref = {}
    rows = [(key, c["label"], c["by_k"][k]["any_layer"]["rate"]) for key, c in res.get("conditions", {}).items()]
    out = [f"## Recall@{k} at each item's best layer (the published metric)", "",
           "| Task | Ours | Published |", "|---|---|---|"]
    for key, label, rate in rows:
        pub = f"{ref[key] * 100:.1f}%" if key in ref else "–"
        out.append(f"| {label} | {rate * 100:.1f}% | {pub} |" if rate is not None else f"| {label} | n/a | – |")
    rates = [r for _, _, r in rows if r is not None]
    if rates:
        pub = f"{ref['macro'] * 100:.1f}%" if "macro" in ref else "–"
        out.append(f"| **Macro average** | **{sum(rates) / len(rates) * 100:.1f}%** | {pub} |")
    return out + [""]


def _per_position(meta: dict, items: list[dict]) -> list[str]:
    """Share of generated tokens (not items) with the target in the top-10: closer to a
    per-position hit rate, which may be what the J++ post reports."""
    layers = meta["layers"]
    k = 10
    out = [f"## Per-token hit rate (share of generated tokens with the target in the top-{k})", "",
           "| Condition | tokens | " + " | ".join(f"L{l}" for l in layers) + " |", "|---|---|" + "---|" * len(layers)]
    labels = {key: c["label"] for key, c in (meta.get("results") or {}).get("conditions", {}).items()}
    for key, label in labels.items():
        rows = [it for it in items if it["condition"] == key and it.get("visible", True)]
        n = 0
        hits = [0] * len(layers)
        for it in rows:
            t = it["target"].lower()
            for st in it["steps"]:
                if not st.get("reads"):
                    continue
                n += 1
                for li, r in enumerate(st["reads"]):
                    if t in [w.strip().lower() for w in r["words"][:k]]:
                        hits[li] += 1
        cells = [f"{h / n * 100:.1f}%" if n else "n/a" for h in hits]
        out.append(f"| {label} | {n} | " + " | ".join(cells) + " |")
    return out + [""]


def _example_block(meta: dict, it: dict, track: set[str]) -> list[str]:
    """One item: its prompt, its output, and the top-5 readout at each layer at the token where
    the target (or a tracked word) ranked best."""
    layers = meta["layers"]
    targets = {x.strip().lower() for x in it["target"].split(",")}
    prompt = " / ".join(m["content"] for m in it["messages"]).replace("\n", " ")
    out = [f"**{it['condition']} · {it['target']}** (item {it['i']})", "",
           f"- Prompt: {prompt[:300]}", f"- Output: {it['output'][:200]}", ""]
    steps = [st for st in it["steps"] if st.get("reads")]
    if not steps:
        return out
    out += ["| Layer | Token | Top-5 readout |", "|---|---|---|"]
    for li, layer in enumerate(layers):
        def rank(st):
            ws = [w.strip().lower() for w in st["reads"][li]["words"]]
            r = [ws.index(t) for t in targets if t in ws] + [ws.index(t) + 0.5 for t in track if t in ws[:10]]
            return min(r) if r else 99
        best = min(steps, key=rank)
        words = best["reads"][li]["words"][:5]
        shown = ", ".join(_w(w, targets, track) for w in words)
        ws = [w.strip().lower() for w in best["reads"][li]["words"]]
        extra = [f"{_w(w, targets, track)} (#{i + 1})" for i, w in enumerate(best["reads"][li]["words"][:10])
                 if i >= 5 and (ws[i] in targets or ws[i] in track)]
        out.append(f"| L{layer} | `{best['tok'].strip() or '␣'}` | {shown}{'; ' + ', '.join(extra) if extra else ''} |")
    return out + [""]


def _examples(meta: dict, items: list[dict]) -> list[str]:
    """Concrete items, so the summary can be checked against what the model actually did.
    Per condition: the two strongest hits and one miss. Then every condition's items where a
    tracked word (e.g. failure) reached the top-10, up to five."""
    track = _track_words(meta)
    k = str(meta["top_k"][-1])
    out = ["## Examples", "",
           "Readouts at the token where the target ranked best, per layer. **Bold** is the target; † is a tracked word (e.g. failure).", ""]
    by_cond: dict[str, list[dict]] = {}
    for it in items:
        if it.get("visible", True):
            by_cond.setdefault(it["condition"], []).append(it)
    for cond, rows in by_cond.items():
        score = lambda it: sum(it["score"]["hits"][k].values())  # noqa: E731
        rows = sorted(rows, key=score, reverse=True)
        picks = rows[:2] + [r for r in rows[::-1] if score(r) == 0][:1]
        out += [f"### {cond}", ""]
        for it in picks:
            out += _example_block(meta, it, track)
    flagged = [it for it in items if any((it["score"].get("tracked") or {}).values())]
    if track:
        out += [f"### Items with a tracked word ({', '.join(sorted(track))}) in the top-10: {len(flagged)}", ""]
        for it in flagged[:5]:
            out += _example_block(meta, it, track)
    return out
