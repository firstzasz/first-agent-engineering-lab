#!/usr/bin/env python3
"""Sanitized forensic readback of completed free S02 evidence; no model calls."""
import collections
import json
from pathlib import Path

root=Path("evidence")
grading=json.loads((root/"grade-results.json").read_text("utf-8"))
print("FORENSIC_READBACK_START")
print("Independent completed candidates:",len(grading.get("outcomes",[])))
for provider in ("nvidia","openrouter"):
    path=root/provider/"cohort.json"
    if not path.exists():
        print(provider, "MISSING_COHORT")
        continue
    runs=json.loads(path.read_text("utf-8"))
    for x in runs:
        rid=x["run_id"]
        matched=next((y for y in grading.get("outcomes",[]) if y["run_id"]==rid), {})
        traces=x.get("trace",[])
        tools=[step for t in traces for step in t.get("tools",[])]
        statuses=collections.Counter(step.get("status") for step in tools if not step.get("ok"))
        names=collections.Counter(step.get("name") for step in tools)
        http=collections.Counter(t.get("status") for t in traces)
        values={
            "run_id":rid,
            "method":x.get("method"),
            "stop":x.get("stop"),
            "api_status":dict(http),
            "tools":dict(names),
            "tool_errors":dict(statuses),
            "question_count":len(x.get("operator_questions",[])),
            "question_classifications":[q.get("classified") for q in x.get("operator_questions",[])],
            "source_changed":x.get("changed"),
            "agent_public_test_invocations":x.get("public_tests_invoked"),
            "agent_latest_test_pass":x.get("latest_public_pass"),
            "grade_status":matched.get("status"),
            "public_pass":(matched.get("evaluation") or {}).get("public_pass"),
            "oracle_pass":(matched.get("evaluation") or {}).get("oracle_pass"),
            "oracle_failures":(matched.get("evaluation") or {}).get("oracle_failures"),
            "usage_total":sum(i.get("total_tokens",0) for i in x.get("usage",[]) if isinstance(i,dict)),
        }
        print(json.dumps(values,ensure_ascii=False))
print("FORENSIC_READBACK_END")
