#!/usr/bin/env bash
# One-time setup on a RunPod GPU pod (1x A100 80GB) with a /workspace volume.
# Runs interp-engine with Qwen3.6-27B and its J++ lens, and the lab app beside it.
#
#   export HF_TOKEN=...        # if the model or lens needs it
#   export MALA_TOKEN=...      # passcode for the app; required, the proxy URL is public
#   export LENS=...            # optional; defaults to the released J++ lens for Qwen3.6-27B
#   bash runpod/setup.sh
#
# Then open https://<pod-id>-8080.proxy.runpod.net on your phone (expose HTTP port 8080 on the pod).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
# Keys and the passcode can live in keys.env (see keys.env.example) instead of the shell.
if [ -f "$HERE/keys.env" ]; then set -a; . "$HERE/keys.env"; set +a; fi

: "${MALA_TOKEN:?Set MALA_TOKEN: the app holds your API keys, so it must have a passcode}"
LENS="${LENS:-hf://koayon/jpp-lenses/qwen3.6-27b/lens.pt}"   # Ayonrinde & Lindsey (2026)
MODEL="${MODEL:-Qwen/Qwen3.6-27B}"
cd /workspace

python -m venv ie && ./ie/bin/pip install -q 'interp-engine[vllm]'
python -m venv lab && ./lab/bin/pip install -q -r "$HERE/requirements.txt"

[ -f ie-token ] || python -c "import secrets; print(secrets.token_urlsafe(32))" > ie-token
chmod 600 ie-token

# interp-engine stays on localhost; only the lab app is exposed.
nohup ./ie/bin/python -m interp_engine.server --model "$MODEL" --backend vllm \
  --host 127.0.0.1 --port 8000 --token-file /workspace/ie-token \
  --lens-jacobians "$LENS" > ie.log 2>&1 &

cd "$HERE"
export MALA_DATA=/workspace/mala-data INTERP_ENGINE_URL=http://127.0.0.1:8000 MALA_ENGINE=interp
export INTERP_ENGINE_TOKEN="$(cat /workspace/ie-token)"
nohup /workspace/lab/bin/uvicorn lab.server:app --host 0.0.0.0 --port 8080 > /workspace/lab.log 2>&1 &

echo "interp-engine is loading (tail -f /workspace/ie.log). The app is on port 8080."
echo "The app starts on interp-engine. Run Experiments -> Readout recall (exact J++ replication)."
