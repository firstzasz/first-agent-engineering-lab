#!/usr/bin/env python3
"""Read back already frozen Ultra trace and grade artifacts, no model calls/secrets."""
import collections
import json
from pathlib import Path
p=Path("evidence/nvidia")
runs=json.loads((p/"cohort.json").read_text(encoding="utf-8"))
grade=json.loads(Path("evidence/grade-ultra.json").read_text(encoding="utf-8"))
print("ULTRA_V0_FROZEN_FORENSIC_BEGIN")
for x in runs:
    g=next((z for z in grade["results"] if z["run_id"]==x["run_id"]),{})
    trace=x.get("trace",[])
    tools=[t for r in trace for t in r.get("tools",[])]
    tool_names=collections.Counter(t.get("name") for t in tools)
    errors=collections.Counter(t.get("status") for t in tools if not t.get("ok"))
    api_status=collections.Counter(r.get("status") for r in trace)
    first_write=next((r.get("request") for r in trace if any(t.get("name")=="write_file" and t.get("ok") for t in r.get("tools",[]))),None)
    first_test=next((r.get("request") for r in trace if any(t.get("name")=="run_public_tests" for t in r.get("tools",[]))),None)
    record={
        "run_id":x["run_id"],"model":x.get("model"),"method":x.get("method"),
        "requests":x.get("requests"),"stop":x.get("stop"),
        "api_status":dict(api_status),"tool_names":dict(tool_names),
        "tool_errors":dict(errors),"first_write_request":first_write,
        "first_test_request":first_test,
        "public_tests_invoked":x.get("public_tests_invoked"),
        "latest_agent_public_pass":x.get("latest_public_pass"),
        "questions_count":len(x.get("operator_questions",[])),
        "decisions_surfaced":x.get("surfaced_count"),
        "changed_files":x.get("changed"),
        "input_output_usage_total":sum(i.get("total_tokens",0) for i in x.get("usage",[]) if isinstance(i,dict)),
        "independent_public":(g.get("grade") or {}).get("public_pass"),
        "independent_oracle":(g.get("grade") or {}).get("oracle_pass"),
        "oracle_failures":(g.get("grade") or {}).get("oracle_failures"),
        "verified":g.get("verified"),
    }
    print(json.dumps(record,ensure_ascii=False))
print("ULTRA_V0_FROZEN_FORENSIC_END")
