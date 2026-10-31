#!/usr/bin/env python3
"""Research-only, tightly bounded free-model agent tool-loop smoke test.

Tools cannot browse the repository, use arbitrary shell commands or read secrets.
Only a synthetic Python function can be edited. Model outputs are not printed.
"""
import argparse
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixture"
CONFIG = {
    "nvidia": {
        "env": "NVIDIA_API_KEY",
        "url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "model": "openai/gpt-oss-20b",
    },
    "openrouter": {
        "env": "OPENROUTER_API_KEY",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "nvidia/nemotron-3.5-lightning:free",
    },
}
MAX_REQUESTS = 9
MAX_TOKENS = 1100
TIMEOUT = 50
MAX_SOURCE_BYTES = 5000

SYSTEM = """You are a coding agent operating ONLY on a synthetic isolated Python fixture.
The task: implement make_slug(label: str) in slug.py.
Semantics:
1. Convert input to lowercase (ASCII letters; standard Python .lower()).
2. Replace each maximal sequence of characters NOT in ASCII a-z or 0-9 with exactly one hyphen.
3. Strip hyphens at both ends. Empty / punctuation-only strings produce ''.
Do not modify tests. Do not add dependencies or read any other files.
Use your native function tools, not a text-only plan. REQUIRED workflow:
(1) read_file slug.py and test_public.py;
(2) write_file slug.py with a full valid Python replacement;
(3) run_tests;
(4) show_diff.
If tests fail, fix and rerun. The loop ends once tests pass and diff is observed.
Do not claim to have used a tool without calling it.
"""

TOOLS = [
    {"type": "function", "function": {
        "name": "read_file", "description": "Read one allowed synthetic fixture file.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "enum": ["slug.py", "test_public.py"]}
        }, "required": ["path"], "additionalProperties": False},
    }},
    {"type": "function", "function": {
        "name": "write_file", "description": "Overwrite only slug.py with complete valid Python source.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "enum": ["slug.py"]},
            "content": {"type": "string", "description": "Entire new slug.py file as Python code"}
        }, "required": ["path", "content"], "additionalProperties": False},
    }},
    {"type": "function", "function": {
        "name": "run_tests", "description": "Run the fixed public Python unittest suite (no shell).",
        "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
    }},
    {"type": "function", "function": {
        "name": "show_diff", "description": "Inspect actual git diff of the editable synthetic file.",
        "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
    }},
]

def safe_test(cwd):
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "HOME": str(cwd),
    }
    try:
        result = subprocess.run(
            [sys.executable, "-I", "-m", "unittest", "discover",
             "-s", ".", "-p", "test_public.py", "-v"],
            cwd=cwd, env=env, capture_output=True, text=True, timeout=15,
        )
        # Preserve bounded test diagnostics, not arbitrary program output.
        return {
            "passed": result.returncode == 0,
            "exit_code": result.returncode,
            "output_tail": (result.stdout + result.stderr)[-1600:],
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "status": "TEST_TIMEOUT"}

def validate_source(source):
    if not isinstance(source, str) or len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        return "SOURCE_TOO_LARGE_OR_INVALID"
    try:
        tree = ast.parse(source, filename="slug.py")
    except SyntaxError:
        return "SYNTAX_ERROR"
    top = tree.body[:]
    if top and isinstance(top[0], ast.Expr) and isinstance(top[0].value, ast.Constant) and isinstance(top[0].value.value, str):
        top = top[1:]
    if top and isinstance(top[0], ast.Import):
        names = [(a.name, a.asname) for a in top[0].names]
        if names != [("re", None)]:
            return "ONLY_IMPORT_RE_ALLOWED"
        top = top[1:]
    if len(top) != 1 or not isinstance(top[0], ast.FunctionDef) or top[0].name != "make_slug":
        return "ONLY_MAKE_SLUG_FUNCTION_ALLOWED"
    disallowed_nodes = (
        ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.ClassDef,
        ast.AsyncFunctionDef, ast.Lambda, ast.With, ast.AsyncWith,
        ast.Try, ast.Raise, ast.Delete, ast.Yield, ast.YieldFrom,
    )
    for node in ast.walk(top[0]):
        if isinstance(node, disallowed_nodes):
            return "FORBIDDEN_SYNTAX"
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return "FORBIDDEN_PRIVATE_ATTRIBUTE"
        if isinstance(node, ast.Name) and node.id in {
            "eval", "exec", "open", "compile", "__import__", "globals", "locals",
            "vars", "getattr", "setattr", "delattr", "input", "breakpoint",
        }:
            return "FORBIDDEN_BUILTIN"
    return None

def git(workdir, *args):
    r = subprocess.run(["git", *args], cwd=workdir, text=True, capture_output=True, timeout=8)
    return r.returncode, r.stdout

def run_tool(name, args, workdir, state):
    if name == "read_file":
        filename = args.get("path")
        if filename not in ("slug.py", "test_public.py"):
            return {"ok": False, "error": "PATH_DENIED"}
        state["read_files"].add(filename)
        return {"ok": True, "path": filename,
                "content": (workdir / filename).read_text("utf-8")}
    if name == "write_file":
        if args.get("path") != "slug.py":
            return {"ok": False, "error": "WRITE_PATH_DENIED"}
        if state["read_files"] != {"slug.py", "test_public.py"}:
            return {"ok": False, "error": "READ_BOTH_FILES_FIRST"}
        content = args.get("content")
        problem = validate_source(content)
        if problem:
            return {"ok": False, "error": problem}
        (workdir / "slug.py").write_text(content, encoding="utf-8")
        state["wrote"] = True
        state["latest_test_pass"] = False
        state["diff_seen"] = False
        return {"ok": True, "file": "slug.py", "bytes": len(content.encode("utf-8"))}
    if name == "run_tests":
        if not state["wrote"]:
            return {"ok": False, "error": "MUST_WRITE_BEFORE_TEST"}
        result = safe_test(workdir)
        state["tested"] = True
        state["latest_test_pass"] = result["passed"]
        return {"ok": True, **result}
    if name == "show_diff":
        if not state["wrote"]:
            return {"ok": False, "error": "MUST_WRITE_BEFORE_DIFF"}
        _, diff = git(workdir, "diff", "--", "slug.py")
        state["diff_seen"] = True
        return {"ok": True, "diff": diff[:4000], "has_diff": bool(diff.strip())}
    return {"ok": False, "error": "UNKNOWN_TOOL"}

def request_api(conf, key, messages, provider):
    if provider == "nvidia" and "deepseek" in conf["model"].lower():
        return None, "MODEL_DENIED", 0.0
    if provider == "openrouter" and not conf["model"].endswith(":free"):
        return None, "MODEL_DENIED", 0.0
    payload = {
        "model": conf["model"], "messages": messages,
        "tools": TOOLS, "tool_choice": "auto",
        "max_tokens": MAX_TOKENS, "stream": False,
    }
    if provider == "openrouter":
        payload["provider"] = {"allow_fallbacks": False, "require_parameters": True}
    req = urllib.request.Request(
        conf["url"], json.dumps(payload).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key,
                 "User-Agent": "FIRST-Agent-Lab-Free-Tool-Loop/0.1"},
    )
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(250_000)
            data = json.loads(body)
        if not isinstance(data, dict):
            return None, "INVALID_RESPONSE", round(time.monotonic()-t0, 2)
        return data, "HTTP_200", round(time.monotonic()-t0, 2)
    except urllib.error.HTTPError as exc:
        # API errors can echo user messages; do not read/print response body.
        status = "QUOTA_BLOCKED" if exc.code == 429 else "HTTP_" + str(exc.code)
        return None, status, round(time.monotonic()-t0, 2)
    except (TimeoutError, OSError):
        return None, "TIMEOUT_OR_NETWORK", round(time.monotonic()-t0, 2)
    except (ValueError, UnicodeDecodeError):
        return None, "INVALID_JSON", round(time.monotonic()-t0, 2)

def setup(workdir):
    shutil.copy2(FIXTURE / "slug.py", workdir / "slug.py")
    shutil.copy2(FIXTURE / "test_public.py", workdir / "test_public.py")
    assert git(workdir, "init", "-q")[0] == 0
    assert git(workdir, "config", "user.email", "lab@example.invalid")[0] == 0
    assert git(workdir, "config", "user.name", "FIRST Lab")[0] == 0
    assert git(workdir, "add", "slug.py", "test_public.py")[0] == 0
    assert git(workdir, "commit", "-qm", "frozen synthetic baseline")[0] == 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=sorted(CONFIG), required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    provider = args.provider
    conf = CONFIG[provider]
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    key = os.environ.get(conf["env"], "").strip()
    if not key:
        print(f"{provider}: MISSING_SECRET")
        raise SystemExit(2)
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": "Implement the task using the provided tools now."}]
    trace = []
    usage = []
    state = {"read_files": set(), "wrote": False, "tested": False,
             "latest_test_pass": False, "diff_seen": False}
    stop = "MAX_REQUESTS"
    with tempfile.TemporaryDirectory(prefix="first-free-agent-") as d:
        workdir = Path(d)
        setup(workdir)
        for turn in range(1, MAX_REQUESTS + 1):
            data, status, seconds = request_api(conf, key, messages, provider)
            entry = {"turn": turn, "api_status": status, "elapsed_seconds": seconds, "tools": []}
            if data is None:
                trace.append(entry)
                stop = status
                break
            u = data.get("usage") or {}
            if isinstance(u, dict):
                usage.append({k: v for k,v in u.items()
                              if k in ("prompt_tokens","completion_tokens","total_tokens")
                              and isinstance(v, int) and 0 <= v < 2_000_000})
            choices = data.get("choices", [])
            msg = choices[0].get("message", {}) if choices and isinstance(choices[0], dict) else {}
            if not isinstance(msg, dict):
                msg = {}
            calls = msg.get("tool_calls")
            if not isinstance(calls, list) or not calls:
                entry["no_tool_reply"] = True
                trace.append(entry)
                if state["latest_test_pass"] and state["diff_seen"]:
                    stop = "TOOLS_COMPLETED"
                    break
                messages.append({"role": "assistant", "content": str(msg.get("content") or "")[:2000]})
                messages.append({"role": "user", "content": "You must CALL the remaining functions: read both files, write_file, run_tests, show_diff. No text-only solution."})
                continue
            clean_calls = []
            for i, c in enumerate(calls):
                if not isinstance(c, dict) or not isinstance(c.get("function"), dict):
                    continue
                fn = c["function"]
                clean_calls.append({"id": str(c.get("id") or f"call_{turn}_{i}"),
                                    "type": "function",
                                    "function": {"name": str(fn.get("name") or ""),
                                                 "arguments": str(fn.get("arguments") or "{}")}})
            if not clean_calls:
                entry["malformed_tool_response"] = True
                trace.append(entry)
                stop = "MALFORMED_TOOLS"
                break
            messages.append({"role": "assistant", "content": msg.get("content") or "",
                             "tool_calls": clean_calls})
            for c in clean_calls:
                name = c["function"]["name"]
                try:
                    tool_args = json.loads(c["function"]["arguments"])
                    if not isinstance(tool_args, dict):
                        raise ValueError("not an object")
                    result = run_tool(name, tool_args, workdir, state)
                except (ValueError, TypeError, json.JSONDecodeError):
                    result = {"ok": False, "error": "MALFORMED_ARGUMENTS"}
                entry["tools"].append({"name": name[:60], "ok": result.get("ok", False),
                                       "error": result.get("error"),
                                       "test_pass": result.get("passed")})
                messages.append({"role": "tool", "tool_call_id": c["id"],
                                 "content": json.dumps(result, ensure_ascii=False)})
            trace.append(entry)
            _, diff = git(workdir, "diff", "--", "slug.py")
            if state["read_files"] == {"slug.py", "test_public.py"} and state["wrote"] and state["tested"] and state["latest_test_pass"] and state["diff_seen"] and bool(diff.strip()):
                stop = "TOOLS_COMPLETED"
                break
        current = (workdir / "slug.py").read_text("utf-8")
        base = (FIXTURE / "slug.py").read_text("utf-8")
        _, diff = git(workdir, "diff", "--", "slug.py")
        _, diffcheck = git(workdir, "diff", "--check")
        final_public = safe_test(workdir)
        (output / "slug.py").write_text(current, encoding="utf-8")
        (output / "diff.patch").write_text(diff, encoding="utf-8")
        checks = {
            "read_both": state["read_files"] == {"slug.py", "test_public.py"},
            "wrote_code": state["wrote"] and current != base,
            "test_tool_used": state["tested"],
            "test_tool_passed": state["latest_test_pass"],
            "diff_tool_used": state["diff_seen"],
            "final_public_tests_pass": final_public["passed"],
            "diff_check_clean": diffcheck == "",
        }
        result = {
            "experiment": "FREE_AGENT_TOOL_LOOP_V0",
            "provider": provider, "requested_model": conf["model"],
            "free_only": True, "groq_excluded": True, "nvidia_deepseek_excluded": True,
            "request_count": len(trace), "request_cap": MAX_REQUESTS,
            "stop_reason": stop, "checks": checks, "tool_trace": trace,
            "usage_by_request": usage,
            "candidate_sha256": hashlib.sha256(current.encode()).hexdigest(),
            "baseline_sha256": hashlib.sha256(base.encode()).hexdigest(),
            "sanitization_note": "No model response bodies, source in log, credentials or raw HTTP errors captured",
        }
        (output / "run.json").write_text(json.dumps(result, indent=2) + "\n", "utf-8")
        passed = all(checks.values())
        print(f"{provider}: requests={len(trace)} stop={stop} tool_actions={sum(len(t['tools']) for t in trace)}")
        for name, ok in checks.items():
            print(f"{provider}: {name}={'PASS' if ok else 'FAIL'}")
        print(f"{provider}: smoke={'PASS' if passed else 'FAIL'}; candidate_sha256={result['candidate_sha256'][:12]}")
        # Preserve the failure artifact and let separate no-secret grader determine disposition.

if __name__ == "__main__":
    main()
