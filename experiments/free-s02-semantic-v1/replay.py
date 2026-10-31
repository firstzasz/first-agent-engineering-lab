#!/usr/bin/env python3
"""Replay provisional semantic labels against original, immutable synthetic question artifacts.

NO LLM inference. Verifies provenance, exact quote anchoring and scoring arithmetic.
Does NOT certify a single reviewer's semantic interpretation or establish a winner.
"""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE_RUN=41222993755
CRITERIA={
  "pause_in_progress_run",
  "scheduled_start_while_paused",
  "manual_run_while_paused",
  "resume_behavior",
}
STATUSES={"EXPLICIT","PARTIAL","ABSENT","NOT_ADJUDICATED"}

def evidence_hash(question):
    return hashlib.sha256(question.encode("utf-8")).hexdigest()

def judge_record(label,questions):
    status=label.get("status")
    if status not in STATUSES:
        raise ValueError("UNKNOWN_STATUS")
    rationale=label.get("rationale")
    if not isinstance(rationale,str) or len(rationale)<12:
        raise ValueError("RATIONALE_REQUIRED")
    if status in {"EXPLICIT","PARTIAL"}:
        index=label.get("index")
        snippet=label.get("quote")
        if type(index) is not int or not (1<=index<=len(questions)):
            raise ValueError("INVALID_QUESTION_INDEX")
        if not isinstance(snippet,str) or len(snippet)<12:
            raise ValueError("QUOTE_REQUIRED")
        q=questions[index-1].get("question")
        if not isinstance(q,str) or snippet not in q:
            raise ValueError("QUOTE_NOT_IN_FROZEN_QUESTION")
        return {"status":status,"question_index":index,
                "question_sha256":evidence_hash(q),
                "quote":snippet,"rationale":rationale,
                "credit":int(status=="EXPLICIT")}
    if "index" in label or "quote" in label:
        raise ValueError("UNANCHORED_LABEL_HAS_QUOTE")
    return {"status":status,"rationale":rationale,
            "credit":0 if status=="ABSENT" else None}

def evaluate(annotations,cohorts,old_grades):
    if annotations.get("source_run")!=SOURCE_RUN:
        raise ValueError("UNEXPECTED_SOURCE_RUN")
    if annotations.get("reviewer_blinding")!="UNBLINDED_SINGLE_ANALYST":
        raise ValueError("REVIEWER_CLAIM_MISMATCH")
    if annotations.get("authoritative") is not False:
        raise ValueError("PROVISIONAL_MUST_NOT_BE_AUTHORITATIVE")
    if set(annotations.get("criteria",[]))!=CRITERIA:
        raise ValueError("WRONG_CRITERIA")
    if len(annotations.get("cases",{}))!=8:
        raise ValueError("EXPECTED_EIGHT_RUNS")
    history={(g["provider"],g["method"]):g for g in old_grades["results"]}
    results=[]
    for provider in ("nvidia","openrouter"):
        cohort=cohorts.get(provider)
        if not isinstance(cohort,dict) or len(cohort.get("cohort",[]))!=4:
            raise ValueError("FROZEN_COHORT_MISSING")
        found={r.get("method"):r for r in cohort["cohort"]}
        if set(found)!={"G0","G1","G2","G3"}:
            raise ValueError("FROZEN_METHODS_MISMATCH")
        for method in ("G0","G1","G2","G3"):
            key=provider+"/"+method
            raw=found[method]
            if raw.get("provider")!=provider or raw.get("method")!=method:
                raise ValueError("SOURCE_IDENTITY_MISMATCH")
            qs=raw.get("questions")
            if not isinstance(qs,list):
                raise ValueError("NO_SOURCE_QUESTIONS")
            labels=annotations["cases"][key]
            if set(labels)!=CRITERIA:
                raise ValueError("INCOMPLETE_CRITERIA")
            decisions={}
            for criterion in sorted(CRITERIA):
                decisions[criterion]=judge_record(labels[criterion],qs)
            values=[x["credit"] for x in decisions.values()]
            provisional=sum(1 for v in values if v==1)
            old=history[(provider,method)]
            row={
              "run":key,
              "provider":provider,"method":method,
              "source_question_count":len(qs),
              "source_question_corpus_sha256":evidence_hash(json.dumps(qs,sort_keys=True,ensure_ascii=False)),
              "original_frozen_matcher_score":old["decision_count"],
              "original_score_valid_according_to_matcher":old["valid"],
              "provisional_unblinded_explicit_count":provisional,
              "partial_count":sum(x["status"]=="PARTIAL" for x in decisions.values()),
              "not_adjudicated_count":sum(x["status"]=="NOT_ADJUDICATED" for x in decisions.values()),
              "difference_from_original":provisional-old["decision_count"],
              "labels":decisions,
              "replay_anchor_integrity":"PASS",
              "semantic_independent_verification":"NOT_PERFORMED",
            }
            results.append(row)
    return {
      "experiment":"FREE_S02_SEMANTIC_ADJUDICATION_V1",
      "source_workflow_run":SOURCE_RUN,
      "original_scores_unchanged":True,
      "classification":"PROVISIONAL_UNBLINDED",
      "semantic_truth_verified":False,
      "question_anchor_replay_verified":True,
      "results":results,
    }

def main():
    annotations=json.loads((HERE/"ANNOTATIONS_PROVISIONAL.json").read_text("utf-8"))
    root=Path("evidence")
    cohorts={p:json.loads((root/p/"cohort.json").read_text("utf-8"))
             for p in ("nvidia","openrouter")}
    old=json.loads((root/"discovery-grade.json").read_text("utf-8"))
    result=evaluate(annotations,cohorts,old)
    Path("semantic-v1-replay.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("SEMANTIC_V1_REPLAY_BEGIN")
    for r in result["results"]:
        print(f"{r['run']}: old_frozen_matcher={r['original_frozen_matcher_score']}/4 "
              f"provisional_unblinded={r['provisional_unblinded_explicit_count']}/4 "
              f"partial={r['partial_count']} questions={r['source_question_count']} "
              f"anchor={r['replay_anchor_integrity']}")
    print("SEMANTIC_V1_REPLAY_END")
    import os
    file=os.getenv("GITHUB_STEP_SUMMARY")
    if file:
        with open(file,"a",encoding="utf-8") as f:
            f.write("## S02 question adjudication V1 (unblinded, provisional)\n\n")
            f.write("| Provider | Mechanism | Old frozen matcher | Provisional reviewed | Anchors |\n")
            f.write("|---|---|---:|---:|---|\n")
            for x in result["results"]:
                f.write(f"| {x['provider']} | {x['method']} | "
                        f"{x['original_frozen_matcher_score']}/4 | "
                        f"{x['provisional_unblinded_explicit_count']}/4 | PASS |\n")
            f.write("\n**Do not infer a winner**. This replays a single analyst's unblinded labels; it verifies quote provenance, not label truth. Original V0 scores unchanged.\n")

if __name__=="__main__":
    main()
