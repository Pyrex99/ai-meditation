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
