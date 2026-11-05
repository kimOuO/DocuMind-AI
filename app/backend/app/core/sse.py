"""Formatting of server-sent events."""

import json
from typing import Any

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    # Tell proxies not to hold events back.
    "X-Accel-Buffering": "no",
}


def format_sse(name: str, data: Any) -> str:
    return f"event: {name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"
