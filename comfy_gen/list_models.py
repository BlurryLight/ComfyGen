"""List model files on the RunPod network volume via a serverless job."""

import json
import time
import urllib.error
import urllib.request
from typing import Any

from comfy_gen import output


def submit_list(
    model_type: str = "loras",
    timeout: int = 60,
    poll_interval: int = 3,
    endpoint_id: str | None = None,
) -> dict[str, Any]:
    """Submit a list_models job to the serverless endpoint.

    Args:
        model_type: Model subfolder to list (e.g. loras, checkpoints).
        timeout: Max seconds to wait for completion.
        poll_interval: Seconds between status checks.
        endpoint_id: Override endpoint ID from config.

    Returns:
        Result dict with files list from the worker.
    """
    from comfy_gen import config

    cfg = config.load()
    api_key = cfg.get("runpod_api_key", "")
    if not endpoint_id:
        endpoint_id = cfg.get("endpoint_id", "")

    if not api_key:
        raise ValueError(
            "No RunPod API key configured. Run 'comfy-gen init' or set via:\n"
            "  comfy-gen config --set runpod_api_key=rpa_..."
        )
    if not endpoint_id:
        raise ValueError(
            "No RunPod endpoint configured. Run 'comfy-gen init' or set via:\n"
            "  comfy-gen config --set endpoint_id=<id>"
        )

    payload = {
        "input": {
            "command": "list_models",
            "model_type": model_type,
        }
    }

    output.log(f"Listing {model_type} on network volume...")
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://api.runpod.ai/v2/{endpoint_id}/run",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        resp = json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:1000]
        raise RuntimeError(f"RunPod API returned {e.code}: {body}")

    job_id = resp.get("id")
    if not job_id:
        raise RuntimeError(f"RunPod API did not return a job ID: {resp}")

    output.log(f"Job submitted: {job_id}")

    # Poll for completion
    status_url = f"https://api.runpod.ai/v2/{endpoint_id}/status/{job_id}"
    elapsed = 0
    status = "UNKNOWN"

    while elapsed < timeout:
        time.sleep(poll_interval)
        elapsed += poll_interval

        req = urllib.request.Request(
            status_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )
        try:
            resp = json.loads(urllib.request.urlopen(req).read())
        except Exception:
            continue

        status = resp.get("status", "UNKNOWN")

        if status == "COMPLETED":
            worker_output = resp.get("output", {})
            worker_output["job_id"] = job_id

            files = worker_output.get("files", [])
            output.log(f"Found {len(files)} {model_type} file(s)")
            for f in files:
                output.log(f"  {f.get('filename', '?')} ({f.get('size_mb', '?')} MB)")
            return worker_output

        elif status == "FAILED":
            error_msg = resp.get("error", "Unknown error")
            raise RuntimeError(f"List job failed: {error_msg}")

        elif status == "TIMED_OUT":
            raise RuntimeError("List job timed out on server")

        elif status == "CANCELLED":
            raise RuntimeError("List job was cancelled")

        else:
            output.log(f"[{elapsed}s] {status}")

    raise TimeoutError(f"List did not complete within {timeout}s (last status: {status})")
