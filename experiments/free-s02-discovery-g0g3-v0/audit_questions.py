#!/usr/bin/env python3
"""No-inference readback of frozen S02 discovery questions for human audit."""
import json
from pathlib import Path

root=Path("evidence")
graded=json.loads((root/"discovery-grade.json").read_text(encoding="utf-8"))
print("QUESTION_AUDIT_START")
for provider in ("nvidia","openrouter"):
    cohort_file=root/provider/"cohort.json"
    if not cohort_file.is_file():
        print("MISSING",provider)
        continue
    cohort=json.loads(cohort_file.read_text(encoding="utf-8")).get("cohort",[])
    for item in cohort:
        method=item.get("method")
        print("=== RUN",provider,method,"stop",item.get("stop"),"===")
        for i,event in enumerate(item.get("questions",[]),start=1):
            print("QUESTION_AUDIT:",json.dumps({"p":provider,"m":method,"i":i,
                "question":event.get("question"),"classified":event.get("matched",[])},ensure_ascii=False))
        score=next((x for x in graded.get("results",[]) if x["provider"]==provider and x["method"]==method),None)
        if score:
            print("SCORE_AUDIT:",json.dumps({
                "p":provider,"m":method,
                "valid":score.get("valid"),
                "matched_ids":score.get("matched_ids"),
                "decision_count":score.get("decision_count"),
                "unclassified_count":score.get("unclassified_count"),
                "verified":score.get("verified_discovery"),
            }))
print("QUESTION_AUDIT_END")
