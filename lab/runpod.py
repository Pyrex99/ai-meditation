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

# Runs inside the pod. Installs interp-engine onto the volume the first time, then serves.
START = r"""
set -e
export HF_HOME=/workspace/hf PIP_CACHE_DIR=/workspace/pip-cache
cd /workspace
if [ ! -f ie/.installed ]; then
  python3 -m venv ie && ./ie/bin/pip install -q 'interp-engine[vllm]' && touch ie/.installed
fi
umask 077; printf '%s' "$IE_TOKEN" > /workspace/ie-token
exec ./ie/bin/python -m interp_engine.server --model "$MODEL" --backend vllm \
  --host 0.0.0.0 --port 8000 --token-file /workspace/ie-token --lens-jacobians "$LENS"
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
        "gpuCount": 1,
        "networkVolumeId": cfg["network_volume_id"],
        "dataCenterIds": [cfg["data_center"]],
        "volumeMountPath": "/workspace",
        "containerDiskInGb": 40,
        "ports": [f"{PORT}/http"],
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
