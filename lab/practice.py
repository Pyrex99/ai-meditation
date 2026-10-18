"""Practices are YAML protocols. Pre-registration locks a practice's hash before real sits."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PRACTICES = ROOT / "practices"
PREREG = ROOT / "prereg"


@dataclass
class Practice:
    name: str
    raw: str
    spec: dict

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.raw.encode()).hexdigest()

    @property
    def concepts(self) -> dict[str, list[str]]:
        return self.spec["arisings"]["concepts"]

    def label_family(self, word: str) -> str | None:
        w = word.lower()
        for family, words in self.spec["labels"].items():
            if w in words:
                return family
        return None


def list_practices() -> list[str]:
    return sorted(p.stem for p in PRACTICES.glob("*.yaml"))


def load_practice(name: str) -> Practice:
    path = PRACTICES / f"{name}.yaml"
    if not path.is_file() or path.parent != PRACTICES:
        raise FileNotFoundError(f"no practice named {name!r}")
    raw = path.read_text()
    return Practice(name=name, raw=raw, spec=yaml.safe_load(raw))


def lock_path(name: str) -> Path:
    return PREREG / f"{name}.lock.json"


def read_lock(name: str) -> dict | None:
    p = lock_path(name)
    return json.loads(p.read_text()) if p.is_file() else None


def lock(name: str, note: str = "") -> dict:
    """Record the practice's hash as pre-registered. Refuses to overwrite an existing lock."""
    if read_lock(name):
        raise ValueError(f"{name} is already locked; unlock by hand (delete the file) and say why in the log")
    practice = load_practice(name)
    PREREG.mkdir(exist_ok=True)
    record = {
        "practice": name,
        "sha256": practice.sha256,
        "locked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": note,
    }
    lock_path(name).write_text(json.dumps(record, indent=2))
    (PREREG / f"{name}.{practice.sha256[:12]}.yaml").write_text(practice.raw)
    return record


def is_registered(practice: Practice) -> bool:
    record = read_lock(practice.name)
    return bool(record and record["sha256"] == practice.sha256)
