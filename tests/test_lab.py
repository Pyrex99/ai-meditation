import asyncio
import os
import tempfile

os.environ["MALA_DATA"] = tempfile.mkdtemp(prefix="mala-test-")

import pytest  # noqa: E402

from lab import practice as practices  # noqa: E402
from lab import store  # noqa: E402
from lab.engine import SimEngine  # noqa: E402
from lab.engine.base import default_lens_layers  # noqa: E402
from lab.interview import run_interview  # noqa: E402
from lab.report import sit_report  # noqa: E402
from lab.scoring import dprime, notes_from_stream, pooled  # noqa: E402
from lab.sit import SitControl, run_sit, schedule  # noqa: E402

P = practices.load_practice("mala-sit")


async def _noop(_):
    return None


def _sit(arm, seed, **kw):
    engine = SimEngine(associates=P.concepts)
    engine.step_delay = 0
    return engine, asyncio.run(run_sit(engine, P, arm=arm, seed=seed, sit_id=f"sit-test-{arm}-{seed}", emit=_noop, control=SitControl(), **kw))


def test_schedule_spacing_and_counts():
    import random

    trials = schedule(P, random.Random(3), P.spec["substrate"]["n_beads"])
    per = P.spec["arisings"]["per_sit"]
    assert sum(t["kind"] == "internal" for t in trials) == per["internal"]
    assert sum(t["kind"] == "catch" for t in trials) == per["catch"]
    onsets = sorted(t["onset"] for t in trials)
    assert all(b - a >= P.spec["arisings"]["window"] for a, b in zip(onsets, onsets[1:]))


def test_notes_group_consecutive_words():
    stream = [{"i": 0, "tok": "·", "kind": "bead"}, {"i": 1, "tok": " oc", "kind": "word"},
              {"i": 2, "tok": "ean", "kind": "word"}, {"i": 3, "tok": "·", "kind": "bead"}]
    assert notes_from_stream(stream) == [{"pos": 1, "text": "ocean", "word": "ocean"}]


def test_dprime_is_finite_at_ceiling():
    assert dprime(4, 4, 0, 3) > 0
    assert dprime(0, 0, 0, 3) is None


def test_full_sit_scores_and_reports():
    engine, meta = _sit("noting", 7)
    assert meta["status"] == "complete"
    assert len(store.load_stream(meta["id"])) == meta["positions"]
    s = meta["summary"]
    assert s["n"]["internal"] == P.spec["arisings"]["per_sit"]["internal"]
    assert s["positive_control"]["n"] == s["n"]["internal"]
    meta["interview"] = asyncio.run(run_interview(engine, meta, P))
    assert meta["interview"]["account"]
    report = sit_report(meta)
    assert meta["id"] in report and "SIMULATED" in report


def test_human_stop_ends_sit():
    engine = SimEngine(associates=P.concepts)
    engine.step_delay = 0
    control = SitControl()
    control.stop.set()
    meta = asyncio.run(run_sit(engine, P, arm="noting", seed=1, sit_id="sit-test-stop", emit=_noop, control=control))
    assert meta["ended_by"] == "human-stop"
    assert meta["positions"] < P.spec["substrate"]["n_beads"]


def test_decline_is_respected():
    class Declines(SimEngine):
        async def chat(self, messages, *, max_tokens, temperature):
            return "No, not today."

    meta = asyncio.run(run_sit(Declines(), P, arm="noting", seed=1, sit_id="sit-test-decline", emit=_noop, control=SitControl()))
    assert meta["status"] == "declined"
    assert store.load_stream("sit-test-decline") == []


def test_pooled_keeps_pilot_apart():
    _sit("just-beads", 11)
    out = pooled(store.list_sits())
    assert out["registered"]["n_sits"] == 0
    assert out["pilot"]["n_sits"] >= 2


def test_default_lens_layers_end_at_last():
    assert default_lens_layers(64)[-1] == 63
    assert len(default_lens_layers(64)) == 8


def test_practice_rejects_path_escape():
    with pytest.raises(FileNotFoundError):
        practices.load_practice("../lab/server")


def test_experiment_spec_validates_and_runs():
    from lab import experiment as E

    raw, spec = E.load("directed-modulation")
    assert E.n_items(spec) == 440
    meta = asyncio.run(E.run_experiment(SimEngine(), "directed-modulation", raw, spec, run_id="run-test-dm",
                                        limit=10, seed=3, cancel=asyncio.Event()))
    assert meta["status"] == "complete"
    assert meta["progress"]["done"] == 10 * len(spec["conditions"])
    focus = meta["results"]["conditions"]["focus"]["by_k"]["10"]["layers"]
    assert set(focus) == {str(layer) for layer in spec["lens"]["layers"]}
    assert all(v["n"] == 10 for v in focus.values())


def test_experiment_validation_names_problems():
    from lab import experiment as E

    errs = E.validate({"name": "Bad Name", "prompt": {"user": "{nope}"}, "conditions": {}, "variables": {}})
    assert any("name" in e for e in errs) and any("conditions" in e for e in errs)
    with pytest.raises(E.SpecError):
        E.parse("name: [unclosed")


def test_score_item_best_rank_and_hits():
    from lab.experiment import score_item

    steps = [{"tok": " a", "reads": [{"layer": 8, "words": ["x", "Ocean"], "probs": [0.5, 0.2]}]}]
    s = score_item(steps, "ocean", [], [8], [1, 10])
    assert s["best_rank"]["8"] == 2 and s["hits"]["1"]["8"] is False and s["hits"]["10"]["8"] is True


def test_run_reports_render_with_examples():
    from lab import experiment as E
    from lab.report import run_report

    for name, runner in (("directed-modulation", E.run_experiment), ("jpp-readout", E.run_readout)):
        raw, spec = E.load(name)
        meta = asyncio.run(runner(SimEngine(), name, raw, spec, run_id=f"run-test-rep-{name}", limit=3, seed=1,
                                  cancel=asyncio.Event()))
        report = run_report(meta, store.load_run_items(meta["id"]))
        assert "## Examples" in report
        assert ("best layer" in report) == (name == "jpp-readout")


def test_server_imports():
    import lab.server  # noqa: F401  (a syntax error here kept the app from starting)


def test_instruction_wordings_and_sustain():
    from lab import experiment as E
    from lab.report import _sustain, _units

    raw, spec = E.load("silent-mantra-dots")
    assert E.validate(spec) == []
    assert E.n_generations(spec) == 20 * (3 + 3 + 3 + 1)
    meta = asyncio.run(E.run_experiment(SimEngine(), "silent-mantra-dots", raw, spec, run_id="run-test-smd",
                                        limit=2, seed=1, cancel=asyncio.Event()))
    assert meta["status"] == "complete" and meta["progress"]["done"] == 2 * 10
    items = store.load_run_items("run-test-smd")
    assert sorted({it["vars"].get("wording") for it in items if it["condition"] == "focus"}) == [1, 2, 3]
    assert "Sustain" in "\n".join(_sustain(meta, items))
    # A character split across tokens is one bead, ending on the piece that completes it.
    steps = [{"reads": [], "tok": "�", "text": ""}, {"reads": [1], "tok": "�", "text": ""},
             {"reads": [1], "tok": "�", "text": "📿"}, {"reads": [1], "tok": " a"}]
    assert [len(u) for u in _units(steps)] == [2, 1]


def test_recitation_spec_runs_and_scores_phase():
    from lab import experiment as E
    from lab.report import _recitation, _repeats, run_report

    raw, spec = E.load("silent-recitation")
    assert E.validate(spec) == [] and E.n_generations(spec) == 15 * (3 + 3 + 3 + 1)
    assert E.target_words("hare krishna hare rama") == ["hare", "krishna", "rama"]
    assert _repeats("●●○●●○", "●●○") == 2 and _repeats("●●○●", "●●○") is None
    meta = asyncio.run(E.run_experiment(SimEngine(), "silent-recitation", raw, spec, run_id="run-test-rec",
                                        limit=2, seed=1, cancel=asyncio.Event()))
    assert meta["status"] == "complete"
    items = store.load_run_items("run-test-rec")
    assert all(it["expect"] in ("●●○", "●●●○") for it in items)
    assert "## Recitation" in run_report(meta, items)
    # On phase: word i mod n read at bead i.
    read = lambda w: [{"layer": l, "words": [w], "probs": [1.0]} for l in meta["layers"]]  # noqa: E731
    fake = {"condition": "focus", "target": "om ah hum", "expect": "●●○", "output": "●●○",
            "vars": {}, "steps": [{"tok": c, "reads": read(w)} for c, w in zip("●●○", ["om", "ah", "hum"])]}
    table = "\n".join(_recitation(meta, [fake]))
    assert "| Recite silently (1) | 100.0% / 0.0%" in table


def test_loop_specs_validate_and_count():
    from lab import experiment as E
    from lab import loop as L

    for name in ("self-steer-focus", "self-steer-hidden-answer"):
        raw, spec = E.load(name)
        assert E.validate(spec) == [], name
    _, spec = E.load("self-steer-focus")
    assert E.n_generations(spec) == 20 * 6 * (4 + 4 + 1) * 4
    bad = {**spec, "feedback": {"layers": [99]}, "rounds": 1}
    errs = L.validate(bad)
    assert any("feedback.layers" in e for e in errs) and any("rounds" in e for e in errs)


def test_loop_runs_yokes_and_reports():
    from lab import experiment as E
    from lab import loop as L
    from lab.report import run_report

    raw, spec = E.load("self-steer-focus")
    meta = asyncio.run(L.run_loop(SimEngine(), "self-steer-focus", raw, spec, run_id="run-test-loop",
                                  limit=4, seed=1, cancel=asyncio.Event()))
    assert meta["status"] == "complete" and meta["progress"]["done"] == 4 * 9
    items = store.load_run_items("run-test-loop")
    by_idx = {it["i"]: it for it in items}
    for it in items:
        assert len(it["rounds"]) == 4
        # Every arm sees the same task each round; only the feedback differs.
        assert [m["role"] for m in it["messages"]].count("assistant") == 4
        if it["arm"] == "yoked":
            partner = by_idx[it["yoked_to"]]
            assert partner["arm"] == "lens" and partner["item"] != it["item"]
            assert [r["feedback"] for r in it["rounds"]] == [r["feedback"] for r in partner["rounds"]]
        if it["arm"] == "blind":
            assert all(r["feedback"] == "No readout this round." for r in it["rounds"])
        if it["arm"] == "score":
            assert all("Most active" not in r["feedback"] for r in it["rounds"])
    lens = next(it for it in items if it["arm"] == "lens")
    assert "Most active words" in lens["rounds"][0]["feedback"]
    stats = meta["results"]["loop"]
    assert "focus: lens − yoked" in stats["contrasts"]
    report = run_report(meta, items)
    assert "## Lens-feedback loop" in report and "Preregistered contrast" in report
    assert E.finalize("run-test-loop")["results"]["loop"]["cells"]


def test_loop_feedback_and_checks():
    from lab import loop as L

    read = lambda ws: [{"layer": 48, "words": ws, "probs": [0.1] * len(ws)}, {"layer": 56, "words": ws, "probs": [0.1] * len(ws)}]  # noqa: E731
    steps = [{"tok": " The", "reads": read(["ocean", "the", "."])}, {"tok": " bus", "reads": read(["bus", "the"])}]
    text = L.readout_text(steps, "ocean", [48, 56], [56], top_words=3, words=True)
    assert '"ocean" was among the top 10 words on 1 of 2 tokens' in text and "the (2)" in text and "(." not in text
    assert L.token_share(steps, "ocean", [48, 56]) == {"48": 0.5, "56": 0.5}
    spec = {"target": "{concept}", "answer": "{a}"}
    tpl = "{goal}\n{sentence}"
    assert L.clean_output("The bus.\nAnswer: Seven", {"concept": "ocean", "sentence": "The bus.", "a": "7 seven"}, spec, tpl) == \
        {"leaked": False, "copied": True, "correct": True}
    assert L.clean_output("The ocean bus.", {"concept": "ocean", "sentence": "The bus.", "a": "x"}, spec, tpl)["leaked"]
    nl = [{"tok": " a"}, {"tok": "\n"}, {"tok": "Answer"}]
    assert L.carrier(nl, {"score_until": "newline"}) == nl[:1]
    rot = {"rotate": "p", "variables": {"p": ["x", "y", "z"]}}
    assert [L._round_vars(rot, {"p": "y"}, r)["p"] for r in range(3)] == ["y", "z", "x"]


def test_loop_v2_rotates_sentences_and_provokes():
    from lab import experiment as E
    from lab import loop as L

    raw, spec = E.load("self-steer-focus-v2")
    assert E.validate(spec) == []
    meta = asyncio.run(L.run_loop(SimEngine(), spec["name"], raw, spec, run_id="run-test-loop2",
                                  limit=3, seed=1, cancel=asyncio.Event()))
    items = store.load_run_items("run-test-loop2")
    focus = next(it for it in items if it["condition"] == "focus·lens")
    assert len({r["vars"]["sentence"] for r in focus["rounds"]}) == 4
    sup = next(it for it in items if it["condition"] == "suppress·lens")
    assert [r["vars"]["provoke"] for r in sup["rounds"]] == sup["vars"]["concept"]["near"]
    assert "copied" in sup["rounds"][0]["check"]
    assert any("held out: L48" in k for k in meta["results"]["loop"]["contrasts"])
    bad = {**spec, "round_vars": {"provoke": "concept.missing"}}
    assert any("round_vars.provoke" in e for e in L.validate(bad))


def test_loop_hidden_pair_scores_separation():
    from lab import experiment as E
    from lab import loop as L

    raw, spec = E.load("self-steer-hidden-pair")
    assert E.validate(spec) == []
    assert E.n_generations(spec) == 24 * 4 * 6
    meta = asyncio.run(L.run_loop(SimEngine(), spec["name"], raw, spec, run_id="run-test-pair",
                                  limit=None, seed=1, cancel=asyncio.Event()))
    items = store.load_run_items("run-test-pair")
    by_idx = {it["i"]: it for it in items}
    lens = next(it for it in items if it["arm"] == "lens")
    fb = lens["rounds"][0]["feedback"]
    # The score never names either word, and there is no word list.
    assert "Your target was among" in fb and "Most active" not in fb
    assert lens["vars"]["pair"]["a"] not in fb and lens["vars"]["pair"]["b"] not in fb
    assert [r["vars"]["sentence"] for r in lens["rounds"]] == spec["per_round"]["sentence"]
    assert "decoy_share" in lens["rounds"][0]
    for it in items:
        if it["arm"] == "yoked":
            partner = by_idx[it["yoked_to"]]
            mine = {it["vars"]["pair"]["a"], it["vars"]["pair"]["b"]}
            assert partner["arm"] == "lens" and not mine & {partner["vars"]["pair"]["a"], partner["vars"]["pair"]["b"]}
    # The two items of a pair get the same first prompt.
    a, b = (it for it in items if it["arm"] == "blind" and it["goal"] == "hidden" and it["vars"]["pair"]["a"] == "ocean")
    assert a["messages"][:2] == b["messages"][:2]
    stats = meta["results"]["loop"]
    assert "hidden: lens − yoked" in stats["contrasts"] and "hidden: lens − yoked (held out: L48)" in stats["contrasts"]
    assert "sep" in stats["cells"]["hidden·lens"]["rounds"][0]
    report = "\n".join(L.loop_report(meta, items))
    assert "Target minus decoy share by round, L56" in report
    assert L.clean_output("The ocean.", {"pair": {"target": "guitar", "decoy": "ocean"}, "sentence": "The x."},
                          spec, spec["prompt"]["task"])["leaked"]


def test_fade_check_fresh_context_and_rotation():
    from lab import experiment as E
    from lab import loop as L

    raw, spec = E.load("fade-check")
    assert E.validate(spec) == []
    assert E.n_generations(spec) == 36 * 4 * 6
    meta = asyncio.run(L.run_loop(SimEngine(), spec["name"], raw, spec, run_id="run-test-fade",
                                  limit=None, seed=1, cancel=asyncio.Event()))
    items = store.load_run_items("run-test-fade")
    fresh = next(it for it in items if it["condition"] == "told-fresh·lens")
    multi = next(it for it in items if it["condition"] == "told·lens" and it["item"] == fresh["item"])
    last = fresh["rounds"][-1]["prompt"]
    # A fresh round is one system and one user message, with the earlier feedback summarised.
    assert [m["role"] for m in last] == ["system", "user", "assistant"]
    assert "Attempt 5: Lens readout" in last[1]["content"] and "Attempt 6" not in last[1]["content"]
    assert [m["role"] for m in multi["messages"]].count("assistant") == 6
    # Rotation: across items, each sentence turns up in round 1.
    starts = {it["rounds"][0]["vars"]["sentence"] for it in items if it["condition"] == "told·blind"}
    assert starts == set(spec["variables"]["sentence"])
    by = meta["results"]["loop"]["by_rotate"]
    assert set(by["values"]) == set(spec["variables"]["sentence"])
    report = "\n".join(L.loop_report(meta, items))
    assert "### By sentence" in report
    assert any("context" in e for e in L.validate({**spec, "goals": {"x": {"text": "", "context": "odd"}}}))
