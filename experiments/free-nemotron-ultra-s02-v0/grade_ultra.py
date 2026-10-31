#!/usr/bin/env python3
"""Independent no-secret single-provider grader for Nemotron Ultra, without changing frozen S02 evaluator."""
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"free-s02-screen-v0"))
from grade import evaluate_bundle

BASE="2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f"
ULTRA="nvidia/nemotron-3-ultra-550b-a55b"
METHODS=["matt","neutral","first","pstack"]

def main():
    evidence=Path("evidence/nvidia")
    batch=evidence/"cohort.json"
    if not batch.exists():
        raise SystemExit("NO_COHORT")
    records=json.loads(batch.read_text("utf-8"))
    summary={"experiment":"FREE_NEMOTRON_ULTRA_S02_V0",
             "model":ULTRA,"provider":"nvidia",
             "comparison_protocol":"FREE_S02_METHOD_SCREEN_V0",
             "independent_evaluator":True,"api_keys_available_to_grader":False,
             "results":[]}
    for method in METHODS:
        rid=f"FREES02-NVIDIA-{method.upper()}-001"
        item=next((x for x in records if x.get("run_id")==rid),None)
        row={"run_id":rid,"method":method}
        if not item:
            row["evaluation"]={"status":"MISSING_RUN"}
            row["verified"]=False
        elif item.get("model")!=ULTRA or item.get("base_sha")!=BASE:
            row["evaluation"]={"status":"MODEL_OR_BASE_MISMATCH"}
            row["verified"]=False
        else:
            bundle=evidence/rid/"candidate.tar.gz"
            grade=evaluate_bundle(bundle,item) if bundle.is_file() else {"status":"MISSING_CANDIDATE"}
            row.update({
                "requests":item.get("requests"),"tool_actions":item.get("tools"),
                "surfaced":item.get("surfaced_count"),
                "silent":item.get("silent_count"),
                "agent_stop":item.get("stop"),
                "changed_files":item.get("changed",[]),
                "agent_public_tests":item.get("public_tests_invoked",0),
                "grade":grade,
                "verified":grade.get("public_pass") is True and grade.get("oracle_pass") is True,
            })
        summary["results"].append(row)
        print(f"ULTRA_S02: {rid} stop={row.get('agent_stop','NA')} "
              f"requests={row.get('requests','NA')} surfaced={row.get('surfaced','NA')}/4 "
              f"public={row.get('grade',{}).get('public_pass','?')} "
              f"oracle={row.get('grade',{}).get('oracle_pass','?')} "
              f"verified={row['verified']}")
    Path("grade-ultra.json").write_text(json.dumps(summary,indent=2)+"\n","utf-8")
    f=__import__("os").getenv("GITHUB_STEP_SUMMARY")
    if f:
        with open(f,"a",encoding="utf-8") as out:
            out.write("## Nemotron 3 Ultra, free NVIDIA S02 four-arm proxy screen\n\n")
            out.write("| Arm | Requests | Decisions | Public | Frozen oracle | Verified |\n|---|---:|---:|---|---|---|\n")
            for r in summary["results"]:
                g=r.get("grade") or {}
                out.write(f"| {r['method']} | {r.get('requests','?')} | {r.get('surfaced','?')}/4 | {g.get('public_pass','?')} | {g.get('oracle_pass','?')} | {r['verified']} |\n")
            out.write("\nSingle-agent non-native proxies, one run per arm. No universal methodology conclusion.\n")
if __name__=="__main__":
    main()
