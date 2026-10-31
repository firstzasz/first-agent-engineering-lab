#!/usr/bin/env python3
"""Independent deterministic no-API-key grading of the eight frozen G0-G3 trials."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
from policy import classify, FROZEN_ANSWERS
from runner import BASE, METHOD_SHA, METHOD_PATH, ORDERS, PROVIDERS, frozen_task

def git_show(ref,path):
    p=subprocess.run(["git","show",ref+":"+path],capture_output=True,text=True,timeout=15)
    if p.returncode: raise RuntimeError("FROZEN_METHOD_MISSING")
    return p.stdout

def grade_one(item,provider,method,task_hash):
    assert method in ("G0","G1","G2","G3")
    row={"provider":provider,"method":method,"model":PROVIDERS[provider][2],
         "status":item.get("stop","MISSING"),"valid":False,"decision_count":0,
         "unclassified_count":0,"question_count":0,"verified_discovery":False}
    if item.get("stop") in ("HARNESS_EXCEPTION","NOT_ATTEMPTED_QUOTA","MISSING"):
        return row
    expected_text=git_show(METHOD_SHA,METHOD_PATH[method]) if method!="G0" else ""
    valid_meta=(
        item.get("protocol")=="FREE_S02_DISCOVERY_G0G3_V0"
        and item.get("provider")==provider
        and item.get("model")==PROVIDERS[provider][2]
        and item.get("method")==method
        and item.get("base_sha")==BASE
        and item.get("method_commit")==METHOD_SHA
        and item.get("task_hash")==task_hash
        and item.get("method_hash")==(hashlib.sha256(expected_text.encode()).hexdigest() if expected_text else None)
        and 1<=item.get("requests",0)<=8
        and item.get("request_cap")==8
    )
    questions=item.get("questions",[])
    if not isinstance(questions,list):
        questions=[]
        valid_meta=False
    found=set()
    unmatched=[]
    classified=[]
    for record in questions:
        if not isinstance(record,dict) or not isinstance(record.get("question"),str):
            valid_meta=False
            continue
        text=record["question"]
        ids=classify(text)
        if sorted(ids)!=sorted(record.get("matched",[])):
            valid_meta=False
        found.update(ids)
        classified.append({"question":text,"ids":ids})
        if not ids: unmatched.append(text)
    if sorted(found)!=sorted(item.get("surfaced",[])):
        valid_meta=False
    if len(found)!=item.get("surfaced_count") or item.get("unasked_policy_count") != 4-len(found):
        valid_meta=False
    # Independent evaluator repeats classification and does not trust model self-reports.
    row.update({"valid":valid_meta,"status":item.get("stop"),"decision_count":len(found),
                "unasked_policy_count":4-len(found),"matched_ids":sorted(found),
                "unclassified_count":len(unmatched),
                "question_count":len(classified),
                "questions_for_manual_audit":classified,
                "files_read_count":len(item.get("files_read",[])),
                "requests":item.get("requests"),
                "invalid_tool_actions":sum(1 for r in item.get("tool_trace",[])
                                           for t in r.get("tool_actions",[]) if not t.get("ok")),
                "finish_called":bool(item.get("finish_called")),
                "usage_total":sum(u.get("total_tokens",0) for u in item.get("usage",[]) if isinstance(u,dict)),
                "verified_discovery":valid_meta and len(found)==4})
    return row

def main():
    task_hash=hashlib.sha256(frozen_task().encode()).hexdigest()
    reports=[]
    for provider in ("nvidia","openrouter"):
        p=Path("evidence")/provider/"cohort.json"
        if not p.is_file():
            for method in ORDERS[provider]:
                reports.append(grade_one({"stop":"MISSING"},provider,method,task_hash))
            continue
        cohort=json.loads(p.read_text(encoding="utf-8")).get("cohort",[])
        for method in ORDERS[provider]:
            matching=[r for r in cohort if r.get("method")==method]
            item=matching[0] if len(matching)==1 else {"stop":"MISSING"}
            reports.append(grade_one(item,provider,method,task_hash))
    result={"experiment":"FREE_S02_DISCOVERY_G0G3_V0",
            "grade":"independent deterministic no-model evaluator",
            "scorer_ids":sorted(FROZEN_ANSWERS),
            "methods":["G0","G1","G2","G3"],"providers":["nvidia","openrouter"],
            "results":reports}
    Path("discovery-grade.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n","utf-8")
    print("INDEPENDENT_DISCOVERY_GRADE_START")
    for r in reports:
        print(f"{r['provider']}/{r['method']} stop={r['status']} valid={r['valid']} "
              f"surfaced={r['decision_count']}/4 questions={r['question_count']} "
              f"unclassified={r['unclassified_count']} requests={r.get('requests',0)} "
              f"verified={r['verified_discovery']}")
    print("INDEPENDENT_DISCOVERY_GRADE_END")
    import os
    summary=os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary,"a",encoding="utf-8") as out:
            out.write("## Free S02 decision discovery (G0-G3), independent grading\n\n")
            out.write("| Provider | Mechanism | Decisions | Questions | Unclassified | Requests | Status |\n")
            out.write("|---|---|---:|---:|---:|---:|---|\n")
            for r in reports:
                out.write(f"| {r['provider']} | {r['method']} | {r['decision_count']}/4 | "
                          f"{r['question_count']} | {r['unclassified_count']} | "
                          f"{r.get('requests','?')} | {r['status']} |\n")
            out.write("\nOne-shot screening, not EXP-0017 C2, not a full pstack/Matt/FIRST-mode comparison; human audit required for ambiguous questions.\n")
    if not all(r["valid"] or r["status"] in ("QUOTA_BLOCKED","NOT_ATTEMPTED_QUOTA","MISSING","HARNESS_EXCEPTION",
                                             "HTTP_400","HTTP_401","HTTP_403","HTTP_404","HTTP_429","HTTP_500",
                                             "TIMEOUT_OR_NETWORK","INVALID_JSON","INVALID_RESPONSE") for r in reports):
        raise SystemExit("INVALID_EVIDENCE")

if __name__=="__main__":
    main()
