#!/usr/bin/env python3
"""Independent no-secret check of a sanitized live helper smoke report."""
import json
from pathlib import Path
from live import ROLES,MODEL,MARKER,MAX_REQUESTS,FUNCTIONS

def evaluate(report):
    rows=report.get("rows",[])
    ledger=report.get("shared_ledger",{})
    checks={
        "expected_experiment":report.get("experiment")=="FREE_ULTRA_HELPER_SMOKE_V0",
        "free_only_pinned":report.get("free_only") is True and report.get("no_fallback") is True
           and report.get("no_paid_provider") is True and report.get("no_groq") is True
           and report.get("no_deepseek_nvidia") is True,
        "model_pinned":report.get("requested_model")==MODEL,
        "three_sequential_roles":len(rows)==3 and [r.get("role") for r in rows]==list(ROLES)
            and [r.get("ordinal") for r in rows]==[1,2,3],
        "fresh_two_message_contexts":len(rows)==3 and all(r.get("messages_count")==2 for r in rows),
        "host_marker_scope_attested":len(rows)==3 and [r.get("lead_marker_present") for r in rows]==[True,False,False],
        "distinct_request_payload_hashes":len(rows)==3 and all(
            isinstance(r.get("request_sha256"),str) and len(r["request_sha256"])==64 for r in rows)
            and len({r.get("request_sha256") for r in rows})==3,
        "all_http_200":len(rows)==3 and all(r.get("api_status")=="HTTP_200" for r in rows),
        "response_model_identity":len(rows)==3 and all(r.get("response_model_matches") is True for r in rows),
        "role_specific_tool_calls":len(rows)==3 and all(
            r.get("expected_tool_emitted") is True
            and r.get("expected_tool")==FUNCTIONS[r["role"]][0] for r in rows),
        "valid_plan":len(rows)==3 and rows[0].get("plan_valid") is True,
        "synthetic_code_shape":len(rows)==3 and rows[1].get("patch_source_shape_valid") is True
            and len(str(rows[1].get("candidate_sha256","")))==64,
        "read_only_review_schema":len(rows)==3 and rows[2].get("review_schema_valid") is True,
        "hard_request_cap":report.get("request_cap")==MAX_REQUESTS
            and ledger.get("request_count")==len(rows)
            and len(rows)<=MAX_REQUESTS,
        "candidate_not_executed":report.get("no_model_source_executed") is True,
        "candidate_not_persisted":report.get("source_content_not_persisted") is True,
    }
    return {"experiment":"FREE_ULTRA_HELPER_SMOKE_V0",
            "independent_no_secret_grader":True,
            "host_attested_not_cryptographically_verified":True,
            "no_full_method_comparison":True,
            "checks":checks,
            "capability_verified":all(checks.values()),
            "roles":[{"role":r.get("role"),"api_status":r.get("api_status"),
                      "elapsed_seconds":r.get("elapsed_seconds"),
                      "expected_tool_emitted":r.get("expected_tool_emitted")}
                     for r in rows]}

def main():
    path=Path("evidence/helper-smoke-report.json")
    if not path.exists():
        report={"experiment":"FREE_ULTRA_HELPER_SMOKE_V0","rows":[]}
    else:
        report=json.loads(path.read_text("utf-8"))
    graded=evaluate(report)
    Path("helper-smoke-grade.json").write_text(json.dumps(graded,indent=2)+"\n","utf-8")
    print("LIVE_HELPER_SMOKE:", "VERIFIED" if graded["capability_verified"] else "NOT_VERIFIED")
    for k,v in graded["checks"].items():
        print(k, "PASS" if v else "FAIL")
    import os
    f=os.getenv("GITHUB_STEP_SUMMARY")
    if f:
        with open(f,"a",encoding="utf-8") as out:
            out.write("## Free NVIDIA Ultra helper role host smoke\n\n")
            for r in graded["roles"]:
                out.write(f"- {r['role']}: {r['api_status']}, tool emitted={r['expected_tool_emitted']}, {r['elapsed_seconds']}s\n")
            out.write(f"\nCapability verified: **{graded['capability_verified']}** (host-attested, not cryptographic). Not native pstack/Matt/FIRST workflow execution.\n")
    if not graded["capability_verified"]:
        raise SystemExit(1)

if __name__=="__main__":
    main()
