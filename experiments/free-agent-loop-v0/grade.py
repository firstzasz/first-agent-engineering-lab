#!/usr/bin/env python3
"""Independent no-secret examiner of free model tool-loop artifacts."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixture"
HIDDEN = ROOT / "evaluator" / "test_hidden.py"
PROVIDERS = ("nvidia", "openrouter")

def execute_tests(workdir, pattern):
    environment = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": str(workdir),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
    }
    try:
        r = subprocess.run(
            [sys.executable, "-I", "-m", "unittest", "discover",
             "-s", ".", "-p", pattern, "-v"],
            cwd=workdir, env=environment, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, timeout=15,
        )
        return {"passed": r.returncode == 0, "exit_code": r.returncode}
    except subprocess.TimeoutExpired:
        return {"passed": False, "status": "TEST_TIMEOUT"}

def verify_provider(evidence, provider):
    folder = evidence / ("agent-loop-" + provider)
    checks = {}
    report_path = folder / "run.json"
    code_path = folder / "slug.py"
    patch_path = folder / "diff.patch"
    if not all(x.is_file() for x in (report_path, code_path, patch_path)):
        return {"provider": provider, "checks": {"artifacts_present": False}, "verified": False}
    try:
        report = json.loads(report_path.read_text("utf-8"))
        source = code_path.read_text("utf-8")
        baseline = (FIXTURE / "slug.py").read_text("utf-8")
        from agent_loop import validate_source
        checks["provider_identity"] = report.get("provider") == provider
        checks["scope_free_only"] = report.get("free_only") is True and report.get("nvidia_deepseek_excluded") is True and report.get("groq_excluded") is True
        checks["model_identity"] = report.get("requested_model") == {
            "nvidia": "openai/gpt-oss-20b",
            "openrouter": "nvidia/nemotron-3.5-lightning:free",
        }[provider]
        checks["source_shape_safe"] = validate_source(source) is None
        checks["candidate_hash_matches"] = hashlib.sha256(source.encode("utf-8")).hexdigest() == report.get("candidate_sha256")
        checks["baseline_hash_matches"] = hashlib.sha256(baseline.encode("utf-8")).hexdigest() == report.get("baseline_sha256")
        checks["source_changed"] = baseline != source
        recorded = report.get("checks") or {}
        for field in ("read_both", "wrote_code", "test_tool_used", "test_tool_passed", "diff_tool_used", "final_public_tests_pass", "diff_check_clean"):
            checks["agent_" + field] = recorded.get(field) is True
        trace = report.get("tool_trace") or []
        names = [x.get("name") for t in trace for x in t.get("tools", []) if x.get("ok")]
        checks["trace_evidence_all_tools"] = all(n in names for n in ("read_file", "write_file", "run_tests", "show_diff"))
        checks["bounded_requests"] = 1 <= int(report.get("request_count", 0)) <= 9
        checks["diff_artifact_nonempty"] = bool(patch_path.read_text("utf-8").strip())
        with tempfile.TemporaryDirectory(prefix="first-free-grade-") as root:
            wd = Path(root)
            shutil.copy2(code_path, wd / "slug.py")
            shutil.copy2(FIXTURE / "test_public.py", wd / "test_public.py")
            shutil.copy2(HIDDEN, wd / "test_hidden.py")
            pub = execute_tests(wd, "test_public.py")
            hid = execute_tests(wd, "test_hidden.py")
            checks["independent_public_tests"] = pub["passed"]
            checks["independent_hidden_tests"] = hid["passed"]
        return {"provider": provider, "checks": checks, "verified": all(checks.values()),
                "request_count": report.get("request_count"),
                "candidate_sha256": report.get("candidate_sha256")}
    except Exception:
        # Do not surface model-owned code or exception strings in public logs.
        return {"provider": provider, "checks": {"grader_error": False}, "verified": False}

def main():
    evidence = Path("evidence")
    reports = [verify_provider(evidence, p) for p in PROVIDERS]
    summary = {"experiment": "FREE_AGENT_TOOL_LOOP_V0", "independent_grader": True,
               "status": "VERIFIED" if all(x["verified"] for x in reports) else "NOT_VERIFIED",
               "results": reports}
    Path("grade-results.json").write_text(json.dumps(summary, indent=2) + "\n", "utf-8")
    for record in reports:
        print(f"{record['provider']}: {'VERIFIED' if record['verified'] else 'NOT_VERIFIED'}")
        for name, passed in record["checks"].items():
            print(f"  {name}: {'PASS' if passed else 'FAIL'}")
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("## Independent free-agent tool-loop grading\n\n")
            f.write("| Model provider | Read | Edit | Test tool | Diff tool | Independent public | Hidden | Verdict |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            for row in reports:
                c = row["checks"]
                f.write("| " + row["provider"] + " | " + " | ".join(
                    "PASS" if c.get(k) else "FAIL" for k in (
                        "agent_read_both", "agent_wrote_code", "agent_test_tool_used",
                        "agent_diff_tool_used", "independent_public_tests",
                        "independent_hidden_tests")) + " | " +
                    ("VERIFIED" if row["verified"] else "NOT_VERIFIED") + " |\n")
    if not all(x["verified"] for x in reports):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
