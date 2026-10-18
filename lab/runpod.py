"""GPU on demand through the RunPod REST API.

The app runs on your computer. Once, it creates a network volume (storage that outlives pods)
in one data center. Each session, "Start GPU" creates a pod on that volume running
interp-engine with Qwen3.6-27B and the J++ lens; "Stop GPU" deletes the pod. Model weights and
the Python environment stay on the volume, so only the first start downloads them.
"""

from __future__ import annotations

import secrets

import httpx

BASE = "https://rest.runpod.io/v1"
GPU_TYPES = ["NVIDIA A100 80GB PCIe", "NVIDIA A100-SXM4-80GB", "NVIDIA H100 80GB HBM3", "NVIDIA H100 PCIe"]
DEFAULT_IMAGE = "runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04"
DEFAULT_MODEL = "Qwen/Qwen3.6-27B"
DEFAULT_LENS = "hf://koayon/jpp-lenses/qwen3.6-27b/lens.pt"
PORT = 8000
STATUS_PORT = 8001
MODEL_GB = 56  # Qwen3.6-27B in bf16 plus the lens, roughly

# Runs inside the pod. Installs interp-engine onto the volume the first time, then serves.
# A small read-only status page on port 8001 shows progress: the log, the download size, the GPU.
START = r"""
set -e
export HF_HOME=/workspace/hf PIP_CACHE_DIR=/workspace/pip-cache PATH=/workspace/ie/bin:$PATH
S=/workspace/status; mkdir -p $S; : > $S/log.txt
[ -f $S/engine.log ] && mv $S/engine.log $S/engine.prev.log; : > $S/engine.log; : > $S/errors.txt
log() { echo "$(date -u +%H:%M:%S) $*" >> $S/log.txt; }
(cd $S && python3 -m http.server 8001 >/dev/null 2>&1 &)
(while true; do
  du -sm /workspace/hf 2>/dev/null | cut -f1 > $S/hf_mb.txt
  nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits > $S/gpu.txt 2>/dev/null || true
  tail -n 40 $S/engine.log > $S/engine_tail.txt 2>/dev/null || true
  grep -E "Error:|Errno|error:" $S/engine.log 2>/dev/null | grep -v "^ *File" | tail -n 3 > $S/errors.txt || true
  sleep 10; done) &
log "Pod up"
command -v ninja >/dev/null 2>&1 && log "ninja found" || true
cd /workspace
if [ ! -f ie/.installed ]; then
  log "Installing interp-engine and vLLM (first start only, about 10 minutes)"
  { python3 -m venv ie && ./ie/bin/pip install -q 'interp-engine[vllm]' >> $S/engine.log 2>&1 && touch ie/.installed; } \
    || { log "Install failed; see the engine log"; sleep infinity; }
fi
# FlashInfer compiles kernels on first use and needs ninja on PATH.
[ -x ie/bin/ninja ] || ./ie/bin/pip install -q ninja >> $S/engine.log 2>&1 || log "Couldn't install ninja"
[ -x ie/bin/ninja ] && log "ninja ready: $(ie/bin/ninja --version)"
log "Starting interp-engine; downloading the model and lens if they aren't on storage yet"
umask 077; printf '%s' "$IE_TOKEN" > /workspace/ie-token
./ie/bin/python -m interp_engine.server --model "$MODEL" --backend vllm \
  --host 0.0.0.0 --port 8000 --token-file /workspace/ie-token --lens-jacobians "$LENS" >> $S/engine.log 2>&1 \
  || log "interp-engine exited with an error; see the engine log"
sleep infinity
"""

async def _call(method: str, key: str, path: str, body: dict | None = None) -> dict | list:
    async with httpx.AsyncClient(timeout=60) as http:
        r = await http.request(method, f"{BASE}{path}", headers={"Authorization": f"Bearer {key}"}, json=body)
    if r.status_code >= 400:
        raise RuntimeError(f"RunPod returned {r.status_code}: {r.text[:300]}")
    return r.json() if r.content else {}


def proxy_url(pod_id: str) -> str:
    return f"https://{pod_id}-{PORT}.proxy.runpod.net"


async def create_volume(key: str, data_center: str, size_gb: int = 150) -> dict:
    return await _call("POST", key, "/networkvolumes", {"name": "mala-lab", "size": size_gb, "dataCenterId": data_center})


async def start_pod(key: str, cfg: dict) -> dict:
    """A pod on the saved volume. Returns the pod id and the engine URL and token to use."""
    token = secrets.token_urlsafe(24)
    env = {
        "IE_TOKEN": token,
        "MODEL": cfg.get("model") or DEFAULT_MODEL,
        "LENS": cfg.get("lens") or DEFAULT_LENS,
    }
    if cfg.get("hf_token"):
        env["HF_TOKEN"] = cfg["hf_token"]
    body = {
        "name": "mala-lab-gpu",
        "imageName": cfg.get("runpod_image") or DEFAULT_IMAGE,
        "cloudType": "SECURE",
        "gpuTypeIds": GPU_TYPES,
        "gpuTypePriority": "custom",  # A100s first; H100s only when none are free
        "gpuCount": 1,
        "networkVolumeId": cfg["network_volume_id"],
        "dataCenterIds": [cfg["data_center"]],
        "volumeMountPath": "/workspace",
        "containerDiskInGb": 40,
        "ports": [f"{PORT}/http", f"{STATUS_PORT}/http"],
        "env": env,
        "dockerStartCmd": ["bash", "-c", START],
    }
    pod = await _call("POST", key, "/pods", body)
    return {"pod_id": pod["id"], "interp_url": proxy_url(pod["id"]), "interp_token": token}


async def pod_status(key: str, pod_id: str) -> dict:
    pod = await _call("GET", key, f"/pods/{pod_id}")
    return {
        "id": pod.get("id", pod_id),
        "status": pod.get("desiredStatus"),
        "gpu": (pod.get("machine") or {}).get("gpuTypeId") or (pod.get("gpu") or {}).get("id"),
        "cost_per_hr": pod.get("costPerHr"),
    }


async def stop_pod(key: str, pod_id: str) -> None:
    await _call("DELETE", key, f"/pods/{pod_id}")


async def engine_health(url: str) -> str:
    """'ready', 'loading' (the server is up but the model isn't), or 'starting'."""
    try:
        async with httpx.AsyncClient(timeout=10) as http:
            r = await http.get(f"{url}/health")
        if r.status_code == 200:
            return "ready"
        return "loading" if r.status_code == 503 else "starting"
    except httpx.HTTPError:
        return "starting"


async def pod_readout(pod_id: str) -> dict | None:
    """What the pod's status page says, or None if it has none (an older pod) or isn't up yet."""
    base = f"https://{pod_id}-{STATUS_PORT}.proxy.runpod.net"
    out: dict = {}
    try:
        async with httpx.AsyncClient(timeout=10) as http:
            for name in ("log.txt", "hf_mb.txt", "gpu.txt", "engine_tail.txt", "errors.txt"):
                r = await http.get(f"{base}/{name}")
                if r.status_code == 200:
                    out[name] = r.text
    except httpx.HTTPError:
        return None
    if not out:
        return None
    gpu = [x.strip() for x in out.get("gpu.txt", "").split(",")]
    mb = out.get("hf_mb.txt", "").strip()
    return {
        "log": out.get("log.txt", "").strip().splitlines()[-8:],
        "downloaded_gb": round(int(mb) / 1024, 1) if mb.isdigit() else None,
        "model_gb": MODEL_GB,
        "gpu": {"name": gpu[0], "mem_used_mb": int(gpu[1]), "mem_total_mb": int(gpu[2]), "util": int(gpu[3])}
        if len(gpu) == 4 and gpu[1].isdigit() else None,
        "engine_tail": out.get("engine_tail.txt", "").strip().splitlines()[-6:],
        "errors": [ln.split("] ", 1)[-1].strip() for ln in out.get("errors.txt", "").strip().splitlines()][-3:],
    }
