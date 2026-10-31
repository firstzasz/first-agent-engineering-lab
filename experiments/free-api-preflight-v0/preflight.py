#!/usr/bin/env python3
"""One-shot, free-only provider API preflight. Never prints prompts, completions or secrets.

This is a connectivity/tool-schema smoke test, NOT a scored RelayBoard treatment.
Only synthetic prompts, two fixed providers/models, maximum two requests per provider.
"""
import json
import os
import re
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TESTS = (
    ("nvidia", "NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1/chat/completions", "openai/gpt-oss-20b"),
    ("openrouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/chat/completions", "nvidia/nemotron-3.5-lightning:free"),
)
TIMEOUT_SECONDS = 35
MAX_COMPLETION_TOKENS = 320
REPORT_PATH = Path("api-preflight-result.json")
SAFE_CHARS = re.compile(r"[^a-zA-Z0-9_./:-]+")

def safe_id(text):
    return SAFE_CHARS.sub("_", str(text))[:100]

def api_call(key, url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "User-Agent": "FIRST-Agent-Engineering-Lab-Preflight/0.1",
        },
        method="POST",
    )
    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            body = resp.read(200_000)
            if resp.status != 200:
                return None, "HTTP_" + str(resp.status), round(time.monotonic()-start, 2)
        data = json.loads(body)
        if not isinstance(data, dict):
            return None, "INVALID_RESPONSE", round(time.monotonic()-start, 2)
        return data, "HTTP_200", round(time.monotonic()-start, 2)
    except urllib.error.HTTPError as exc:
        # Intentionally never read/log the response body; it may echo request data.
        return None, "HTTP_" + str(exc.code), round(time.monotonic()-start, 2)
    except (TimeoutError, socket.timeout):
        return None, "TIMEOUT", round(time.monotonic()-start, 2)
    except urllib.error.URLError:
        return None, "NETWORK_ERROR", round(time.monotonic()-start, 2)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None, "INVALID_JSON", round(time.monotonic()-start, 2)
    except Exception:
        # No exception strings in logs (URLs/proxy details may be sensitive).
        return None, "UNEXPECTED_ERROR", round(time.monotonic()-start, 2)

def response_profile(data):
    choices = data.get("choices")
    valid = isinstance(choices, list) and bool(choices) and isinstance(choices[0], dict)
    message = choices[0].get("message", {}) if valid else {}
    if not isinstance(message, dict):
        message = {}
    calls = message.get("tool_calls")
    if not isinstance(calls, list):
        calls = []
    is_tool = any(
        isinstance(c, dict)
        and c.get("type") == "function"
        and isinstance(c.get("function"), dict)
        and c["function"].get("name") == "add_numbers"
        for c in calls
    )
    usage = data.get("usage", {})
    if not isinstance(usage, dict):
        usage = {}
    counts = {k: v for k, v in usage.items()
              if k in ("prompt_tokens", "completion_tokens", "total_tokens")
              and isinstance(v, int) and 0 <= v < 1000000}
    return {
        "response_model": safe_id(data.get("model", "unknown")),
        "choices_valid": valid,
        "content_present": bool(message.get("content")),
        "tool_call_returned": is_tool,
        "usage": counts,
    }

def payload_for(provider, model, mode):
    if provider == "openrouter" and not model.endswith(":free"):
        raise RuntimeError("Refusing non-free OpenRouter model")
    if provider == "nvidia" and "deepseek" in model.lower():
        raise RuntimeError("Refusing DeepSeek on NVIDIA")
    base = {
        "model": model,
        "max_tokens": MAX_COMPLETION_TOKENS,
        "stream": False,
    }
    if provider == "openrouter":
        base["provider"] = {"allow_fallbacks": False}
    if mode == "chat":
        base["messages"] = [
            {"role": "user", "content": "Synthetic connectivity check: reply with exactly PONG."}
        ]
    else:
        base["messages"] = [
            {"role": "user", "content": "Tool interface check. Call add_numbers with a=2 and b=3. Do not calculate the answer in text."}
        ]
        base["tools"] = [{
            "type": "function",
            "function": {
                "name": "add_numbers",
                "description": "Add two integer values.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                        "b": {"type": "integer"},
                    },
                    "required": ["a", "b"],
                    "additionalProperties": False,
                },
            },
        }]
        base["tool_choice"] = "auto"
        if provider == "openrouter":
            base["provider"]["require_parameters"] = True
    return base

def main():
    results = []
    for provider, env_name, url, model in TESTS:
        key = os.getenv(env_name, "").strip()
        if not key:
            record = {"provider": provider, "model": model, "mode": "auth",
                      "status": "MISSING_SECRET"}
            results.append(record)
            print(f"{provider}: MISSING_SECRET")
            continue
        for mode in ("chat", "tool"):
            payload = payload_for(provider, model, mode)
            response, status, elapsed = api_call(key, url, payload)
            record = {
                "provider": provider, "model": model, "mode": mode,
                "status": status, "elapsed_seconds": elapsed,
            }
            if response is not None:
                record.update(response_profile(response))
            results.append(record)
            print(f"{provider}/{mode}: {status}; {elapsed}s; "
                  f"content={record.get('content_present', False)}; "
                  f"tool_call={record.get('tool_call_returned', False)}")
            # One attempt per mode: never retry a failure or switch provider/model.
            if status != "HTTP_200" and mode == "chat":
                break
    report = {
        "experiment": "FREE_API_PREFLIGHT_V0",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "synthetic connectivity + tool schema; not benchmark scoring",
        "free_only": True,
        "nvidia_deepseek_excluded": True,
        "groq_excluded": True,
        "requests_max": 4,
        "results": results,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary_file = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as out:
            out.write("## Free API preflight (synthetic, non-scored)\n\n")
            out.write("| Provider | Model | Mode | HTTP status | Content | Tool call | Seconds |\n")
            out.write("|---|---|---|---|---|---|---|\n")
            for x in results:
                out.write(
                    f"| {x['provider']} | `{x['model']}` | {x['mode']} | {x['status']} | "
                    f"{x.get('content_present', '')} | {x.get('tool_call_returned', '')} | "
                    f"{x.get('elapsed_seconds', '')} |\n"
                )
    # A failed provider is observable as job failure but retains the sanitized report.
    if any(x["status"] != "HTTP_200" for x in results):
        raise SystemExit(1)
    if not any(x.get("tool_call_returned") for x in results if x["mode"] == "tool"):
        raise SystemExit(2)

if __name__ == "__main__":
    main()
