"""Run an experiment from the command line, without the app.

    python -m lab.cli list
    python -m lab.cli run self-steer-focus --limit 4               # simulated engine
    python -m lab.cli run self-steer-focus --engine interp --url https://<pod>-8000.proxy.runpod.net
    python -m lab.cli report run-20261018-183502-b064             # rebuild a report

The run is stored like an app run (data/runs/<id>/) and its report is printed at the end.
The interp engine's token is read from INTERP_ENGINE_TOKEN or keys.env, as the app does.
"""

from __future__ import annotations

import argparse
import asyncio
import random
import sys

from . import experiment as experiments
from . import loop, store
from .engine import InterpEngine, SimEngine
from .report import run_report


def _engine(args):
    if args.engine == "sim":
        return SimEngine()
    from .server import load_config

    cfg = load_config()
    url = args.url or cfg.get("interp_url")
    return InterpEngine(url, cfg.get("interp_token") or None)


async def _run(args) -> str:
    raw, spec = experiments.load(args.name)
    runner = {"readout": experiments.run_readout, "loop": loop.run_loop}.get(spec.get("kind"), experiments.run_experiment)
    engine = _engine(args)
    run_id = experiments.new_run_id()
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    print(f"{run_id}: {args.name} on {args.engine}, seed {seed}, limit {args.limit or 'all'}", file=sys.stderr)
    try:
        meta = await runner(engine, args.name, raw, spec, run_id=run_id, limit=args.limit, seed=seed, cancel=asyncio.Event())
    finally:
        await engine.aclose()
    report = run_report(meta, store.load_run_items(run_id))
    store.write_run_report(run_id, report)
    store.compress_run_items(run_id)
    return report


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="python -m lab.cli", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="experiments and whether they validate")
    r = sub.add_parser("run", help="run an experiment")
    r.add_argument("name")
    r.add_argument("--engine", choices=["sim", "interp"], default="sim")
    r.add_argument("--url", help="interp-engine URL (default: the app's configured one)")
    r.add_argument("--limit", type=int, help="items per condition (default: all)")
    r.add_argument("--seed", type=int)
    rep = sub.add_parser("report", help="rebuild and print a run's report")
    rep.add_argument("run_id")
    args = p.parse_args(argv)
    if args.cmd == "list":
        for e in experiments.list_experiments():
            ok = "ok" if not e["errors"] else "INVALID: " + " ".join(e["errors"])
            print(f"{e['name']:28} {e['kind']:10} {e['n_generations']:>6} generations  {ok}")
    elif args.cmd == "run":
        print(asyncio.run(_run(args)))
    else:
        meta = experiments.finalize(args.run_id)
        report = run_report(meta, store.load_run_items(args.run_id))
        store.write_run_report(args.run_id, report)
        print(report)


if __name__ == "__main__":
    main()
