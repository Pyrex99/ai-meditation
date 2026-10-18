#!/usr/bin/env bash
# Start Mala Lab on this computer: ./run.sh   (then open http://localhost:8080)
# First run creates a Python environment in .venv and installs what the app needs.
set -euo pipefail
cd "$(dirname "$0")"
PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$c" >/dev/null && "$c" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "Mala Lab needs Python 3.10 or newer. On a Mac: install it from https://www.python.org/downloads/ (or 'brew install python@3.12'), then run ./run.sh again."
  exit 1
fi
if [ ! -x .venv/bin/python ]; then
  "$PY" -m venv .venv
fi
if [ ! -f .venv/.installed ] || [ requirements.txt -nt .venv/.installed ]; then
  .venv/bin/python -m pip install -q --upgrade pip
  .venv/bin/python -m pip install -q -r requirements.txt
  touch .venv/.installed
fi
echo "Mala Lab: http://localhost:8080  (Ctrl+C to stop)"
exec .venv/bin/python -m uvicorn lab.server:app --port 8080
