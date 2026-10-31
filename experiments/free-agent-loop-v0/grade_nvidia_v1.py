#!/usr/bin/env python3
"""No-key independent grader, one separate diagnostic NVIDIA model artifact."""
import json
from pathlib import Path
from grade import verify_provider

p = Path("evidence")
result = verify_provider(p, "nvidia")
meta = p / "agent-loop-nvidia" / "run.json"
protocol_valid = False
if meta.exists():
    x = json.loads(meta.read_text(encoding="utf-8"))
    protocol_valid = (
        x.get("experiment") == "FREE_AGENT_TOOL_LOOP_NVIDIA_DIAGNOSTIC_V1"
        and x.get("declared_protocol_delta") == {
            "request_timeout_seconds": {"from": 50, "to": 90}
        }
        and x.get("request_cap") == 9
    )
result["protocol_v1_valid"] = protocol_valid
result["verified"] = result["verified"] and protocol_valid
summary = {
    "experiment": "FREE_AGENT_TOOL_LOOP_NVIDIA_DIAGNOSTIC_V1",
    "previous_v0_timeout_is_preserved": True,
    "outcome": "VERIFIED" if result["verified"] else "NOT_VERIFIED",
    "result": result,
}
Path("nvidia-v1-grade.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print("NVIDIA diagnostic V1:", summary["outcome"])
for k,v in result["checks"].items():
    print(k, "PASS" if v else "FAIL")
print("protocol_v1_valid", protocol_valid)
if not result["verified"]:
    raise SystemExit(1)
