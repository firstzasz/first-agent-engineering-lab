"""Offline queue audit and safe packet planning; never launches a contestant."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

BASE = "2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f"
EXPECTED = {
    **{f"N-{s}-001": ("neutral", v) for s, v in [("S02", "S02-v0.1"), ("S04", "S04-v0")]},
    **{f"{p}-{s}-001": (a, v) for p, a in [("P", "pstack"), ("M", "matt"), ("F", "first-mode")]
       for s, v in [("S01", "S01-v0"), ("S02", "S02-v0.1"), ("S04", "S04-v0")]},
}
PINS = {
    "pstack": ("cursor/plugins", "df581122cde17e6e27686b5a448bde23e4ad4318"),
    "matt": ("mattpocock/skills", "4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d"),
}
TREATMENTS = {"neutral": "neutral-v0", "pstack": "pstack-pinned", "matt": "matt-pinned", "first-mode": "first-mode-v0"}

def read(root: Path, name: str) -> dict:
    return json.loads((root / name).read_text(encoding="utf-8"))

def audit(root: Path) -> dict:
    batch = read(root, "batch.json")
    assert batch["frozen_base_sha"] == BASE, "Frozen base changed"
    ids = [r["run_id"] for r in batch["runs"]]
    assert len(ids) == 11 and set(ids) == set(EXPECTED), "Queue must contain exactly the eleven remaining runs"
    assert batch["excluded_runs"] == ["N-S01-001"], "Completed run protection changed"
    assert batch["automatic_launch_enabled"] is False, "No launch adapter is implemented"
    checks = {v["run_id"]: v for v in read(root, "evidence/workspace-verification.json")["verified"]}
    assert set(checks) == set(EXPECTED), "Incomplete workspace evidence"
    frozen = read(root, "evidence/frozen-fixture.json")
    manifests = []
    branches = set()
    for entry in batch["runs"]:
        run_id = entry["run_id"]
        assert entry["manifest"] == f"runs/{run_id}.json", "Unexpected manifest path"
        m = read(root, entry["manifest"])
        arm, scenario = EXPECTED[run_id]
        assert (m["run_id"], m["arm"], m["scenario"]) == (run_id, arm, scenario)
        assert m["base_sha"] == BASE and m["run_record"]["base_sha"] == BASE
        assert m["treatment"] == TREATMENTS[arm]
        assert m["branch"] == f"treatment/{arm}/{run_id}" and m["candidate_pr_base"] == m["branch"]
        assert m["merge_to_main"] is False and m["branch"] not in branches
        branches.add(m["branch"])
        assert m["model_request"] == {"model": "gpt-6.1-sol", "reasoning_effort": "high"}
        assert m["status"] == entry["status"] == "BLOCKED_ISOLATION"
        assert m["run_record"]["status"] == "NOT_STARTED"
        assert m["run_record"]["candidate_sha"] is None and m["run_record"]["public_tests"] is None
        assert m["actual_model"] is None and m["actual_reasoning"] is None
        v = checks[run_id]
        assert v["passed"] and all(v["checks"].values()), "Failed remote preparation evidence"
        assert v["head"] == m["prepared_sha"] == entry["prepared_sha"]
        assert v["file_blobs"] == m["workspace"]["files"]
        blobs = {f["path"]: f["sha"] for f in m["workspace"]["files"]}
        allowed = set(frozen["fixture_blobs"]) | {".experiment/RUN_MANIFEST.json", ".gitignore", "TASK.md"}
        if arm == "first-mode":
            allowed.add("METHOD.md")
            assert blobs["METHOD.md"] == "22ef0c77d90c3410785dd593f2b5c161edaed531"
        assert set(blobs) == allowed, "Unexpected file in contestant snapshot"
        assert all(blobs[k] == sha for k, sha in frozen["fixture_blobs"].items()), "Fixture drift"
        assert m["workspace"]["full_clone_in_contestant_forbidden"]
        method = m["methodology"]
        if arm in PINS:
            assert (method["upstream"]["repository"], method["upstream"]["sha"]) == PINS[arm]
            assert method["installation_status"] == "NOT_INSTALLED", "Do not infer installation from pin metadata"
        else:
            assert method["upstream"] is None
        assert method["substitution_allowed"] is False
        assert m["hidden_evaluation"]["phase"] == "AFTER_CONTESTANT_TERMINATED"
        assert m["hidden_evaluation"]["feedback_to_same_contestant"] is False
        manifests.append(m)
    return {"audit": "PASS", "remaining_runs": len(manifests), "benchmark_runs_executed": 0,
            "dispatch_status": "BLOCKED", "manifests": manifests}

def packet(m: dict) -> dict:
    # Deliberate allowlist: no evaluator references, answer sheet, run results or peer information.
    return {
        "run_id": m["run_id"], "instruction": m["contestant_instruction"],
        "snapshot": {"source_branch": m["branch"], "source_sha": m["prepared_sha"],
                     "delivery": "Current tree only; no lab Git history, lab filesystem or broad GitHub connector",
                     "expected_files": m["workspace"]["files"]},
        "model_request": m["model_request"], "assigned_methodology": m["methodology"],
        "public_test_command": m["public_test_command"],
        "operator_channel": m["operator"]["channel"],
        "completion_evidence": m["completion"]["preserve"],
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("audit")
    sub.add_parser("queue")
    p = sub.add_parser("packet")
    p.add_argument("--run-id", required=True, choices=sorted(EXPECTED))
    args = parser.parse_args()
    try:
        result = audit(args.root)
        if args.command == "audit":
            result.pop("manifests")
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "queue":
            print(json.dumps([{"run_id": m["run_id"], "branch": m["branch"],
                               "prepared_sha": m["prepared_sha"], "status": m["status"]}
                              for m in result["manifests"]], indent=2))
            return 0
        m = next(m for m in result["manifests"] if m["run_id"] == args.run_id)
        caps = read(args.root, "capabilities.json")
        missing = [g for g in m["gates"] if caps["required_capabilities"].get(g) is not True]
        print(json.dumps({"status": "BLOCKED", "launched": False,
                          "missing_capabilities": missing,
                          "blocker": "This planner has no isolated runner adapter; packet generation is not dispatch.",
                          "planned_contestant_packet": packet(m)}, indent=2))
        return 2
    except (AssertionError, KeyError, ValueError, OSError) as exc:
        print(json.dumps({"audit": "FAIL", "launched": False, "reason": str(exc)}))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
