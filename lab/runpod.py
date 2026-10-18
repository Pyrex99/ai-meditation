"""Start, stop and check the GPU pod through the RunPod REST API.

Useful when this app runs somewhere other than the pod (your laptop, a small always-on box).
When the app runs on the pod itself, start the pod from the RunPod console instead.
"""

from __future__ import annotations

import httpx

BASE = "https://rest.runpod.io/v1"


async def _call(method: str, key: str, path: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as http:
        r = await http.request(method, f"{BASE}{path}", headers={"Authorization": f"Bearer {key}"})
    if r.status_code >= 400:
        raise RuntimeError(f"RunPod returned {r.status_code}: {r.text[:300]}")
    return r.json() if r.content else {}


async def status(key: str, pod_id: str) -> dict:
    pod = await _call("GET", key, f"/pods/{pod_id}")
    return {
        "id": pod.get("id", pod_id),
        "name": pod.get("name"),
        "status": pod.get("desiredStatus"),
        "gpu": (pod.get("machine") or {}).get("gpuTypeId") or pod.get("gpuTypeId"),
        "cost_per_hr": pod.get("costPerHr"),
    }


async def start(key: str, pod_id: str) -> dict:
    await _call("POST", key, f"/pods/{pod_id}/start")
    return await status(key, pod_id)


async def stop(key: str, pod_id: str) -> dict:
    await _call("POST", key, f"/pods/{pod_id}/stop")
    return await status(key, pod_id)
