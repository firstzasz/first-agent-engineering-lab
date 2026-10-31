#!/usr/bin/env python3
"""One declared NVIDIA-only diagnostic after separate V0 timeout.

Only experimental change vs V0: per-request network timeout 50 -> 90s.
No hidden evaluator feedback, no paid fallback, no retries per request.
"""
import json
from pathlib import Path
import sys

import agent_loop

assert agent_loop.TIMEOUT == 50
assert agent_loop.CONFIG["nvidia"]["model"] == "openai/gpt-oss-20b"
agent_loop.TIMEOUT = 90
sys.argv = [
    sys.argv[0], "--provider", "nvidia",
    "--output", "agent-output/nvidia",
]
agent_loop.main()

path = Path("agent-output/nvidia/run.json")
if path.exists():
    report = json.loads(path.read_text(encoding="utf-8"))
    report["experiment"] = "FREE_AGENT_TOOL_LOOP_NVIDIA_DIAGNOSTIC_V1"
    report["declared_protocol_delta"] = {"request_timeout_seconds": {"from": 50, "to": 90}}
    report["v0_reference"] = "https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41209522589"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
