#!/usr/bin/env python3
"""One-call capability handshake for free NVIDIA Nemotron 3 Ultra (no prompts logged)."""
import json
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "free-s02-screen-v0"))
import screen

MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
EXPECTED = {"list_files", "read_file", "write_file", "run_public_tests", "show_diff", "ask_operator"}

def main():
    # Fixed exact NVIDIA API endpoint and allowlisted model. Never use paid fallback.
    original = screen.PROVIDERS["nvidia"]
    screen.PROVIDERS["nvidia"] = (original[0], original[1], MODEL)
    key = os.environ.get("NVIDIA_API_KEY", "").strip()
    report = {"experiment": "FREE_NEMOTRON_ULTRA_S02_V0",
              "model": MODEL, "free_nvidia_direct": True,
              "excluded": ["groq", "deepseek", "paid_fallback"],
              "phase": "preflight"}
    if not key:
        report["status"] = "MISSING_SECRET"
    else:
        data, status, elapsed = screen.api_request("nvidia", MODEL, key, [
            {"role": "system", "content": "Synthetic one-step function tool API check. Call list_files with {}. Do not supply text."},
            {"role": "user", "content": "Call the list_files tool now."},
        ])
        report["status"] = status
        report["seconds"] = elapsed
        if data:
            report["response_model"] = str(data.get("model", ""))[:120]
            choices = data.get("choices") or []
            msg = choices[0].get("message", {}) if choices else {}
            calls = msg.get("tool_calls") or []
            names = [x.get("function", {}).get("name") for x in calls if isinstance(x,dict)]
            report["tools_count"] = len(names)
            report["tool_schema_valid"] = bool(names) and all(name in EXPECTED for name in names)
            report["tool_name_list_files"] = "list_files" in names
            report["tool_emitted"] = bool(names)
            report["response_has_text"] = bool(msg.get("content"))
            usage = data.get("usage") or {}
            report["usage"] = {k:usage[k] for k in ("prompt_tokens", "completion_tokens", "total_tokens")
                               if isinstance(usage.get(k),int)}
    Path("ultra-preflight.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("ULTRA_PREFLIGHT:", json.dumps(report))
    if report.get("status") != "HTTP_200" or not report.get("tool_schema_valid"):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
