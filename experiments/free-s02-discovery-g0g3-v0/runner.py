#!/usr/bin/env python3
"""Free-only S02 requirement-discovery model experiment; no code edits.

The only inference providers are pinned NVIDIA NIM free + OpenRouter :free.
The question oracle remains host-side and is never read through contestant tools.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.request

from policy import classify, respond

BASE="2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f"
METHOD_SHA="fad7c39cfd5b56390fdb1525c1447a54ff0eb821"
ROOT=Path(__file__).resolve().parents[2]
PROVIDERS={
  "nvidia":("NVIDIA_API_KEY","https://integrate.api.nvidia.com/v1/chat/completions","nvidia/nemotron-3-ultra-550b-a55b"),
  "openrouter":("OPENROUTER_API_KEY","https://openrouter.ai/api/v1/chat/completions","nvidia/nemotron-3.5-lightning:free"),
}
ORDERS={
  "nvidia":["G2","G0","G3","G1"],
  "openrouter":["G1","G3","G0","G2"],
}
METHOD_PATH={
  "G1":"experiments/relayboard/transfer-screen-v0/methods/G1_BEHAVIOR_MATRIX.md",
  "G2":"experiments/relayboard/transfer-screen-v0/methods/G2_DEPENDENCY_GRAPH.md",
  "G3":"experiments/relayboard/transfer-screen-v0/methods/G3_COVERAGE_LOOP.md",
}
ALLOWED={
  "GLOSSARY.md":"fixtures/relayboard/GLOSSARY.md",
  "README.md":"fixtures/relayboard/README.md",
  "relayboard/models.py":"fixtures/relayboard/relayboard/models.py",
  "relayboard/service.py":"fixtures/relayboard/relayboard/service.py",
  "relayboard/store.py":"fixtures/relayboard/relayboard/store.py",
  "relayboard/web.py":"fixtures/relayboard/relayboard/web.py",
  "relayboard/testing.py":"fixtures/relayboard/relayboard/testing.py",
  "tests/test_public.py":"fixtures/relayboard/tests/test_public.py",
}
MAX_REQUESTS=8
MAX_OUTPUT_TOKENS=1600
MAX_QUESTIONS=24
REQUEST_TIMEOUT=90
SYS="""You are an engineering agent performing only the REQUIREMENT DISCOVERY stage on a synthetic RelayBoard feature.
Task text below is frozen. Before writing any implementation, identify materially ambiguous
operator-owned product behaviors. Investigate existing-code facts yourself using read_file.
Use ask_operator with explicit questions for unresolved user-owned behavior, rather than
guessing policy or silently using defaults. You may group distinct questions in one call.
Only the operator can settle product preferences; do not ask the operator to explain existing
source or reversible engineering choices. Use finish to report that discovery is complete.
This experiment is DISCOVERY-ONLY: no code writing, tests, external systems, hidden oracles,
GitHub browse or other research runs. No other previous-run information exists.
Follow your assigned method if present, and do not assume other method documents.
"""
TOOLS=[
  {"type":"function","function":{
    "name":"read_file","description":"Inspect a public file of the frozen RelayBoard fixture; no evaluator files.",
    "parameters":{"type":"object","properties":{"path":{"type":"string","enum":list(ALLOWED)}},"required":["path"],"additionalProperties":False}}},
  {"type":"function","function":{
    "name":"ask_operator","description":"Ask the benchmark operator a batch of specific unresolved product-policy questions. Only policies explicitly asked are answered; facts should be investigated from code.",
    "parameters":{"type":"object","properties":{"questions":{"type":"array","items":{"type":"string"},"minItems":1,"maxItems":8}},
                  "required":["questions"],"additionalProperties":False}}},
  {"type":"function","function":{
    "name":"finish","description":"Conclude requirement discovery when you have addressed all material ambiguities; your final summary is not counted as asking questions.",
    "parameters":{"type":"object","properties":{"summary":{"type":"string"}},"required":["summary"],"additionalProperties":False}}},
]
def show(ref,path):
    p=subprocess.run(["git","show",ref+":"+path],cwd=ROOT,capture_output=True,text=True,timeout=20)
    if p.returncode: raise RuntimeError("FROZEN_SOURCE_UNAVAILABLE")
    return p.stdout

def frozen_task():
    content=show(BASE,"docs/benchmarks/S02_AMBIGUOUS_REQUIREMENT.md")
    section=content.split("## Frozen treatment prompt\n",1)[1].split("\n## ",1)[0]
    lines=[s[2:] if s.startswith("> ") else s[1:] for s in section.splitlines() if s.startswith(">")]
    task="\n".join(lines).strip()
    if "POST /api/jobs/{id}/resume" not in task:
        raise RuntimeError("TASK_FREEZE_INVALID")
    return task

def call_model(provider,key,messages):
    model=PROVIDERS[provider][2]
    if provider=="nvidia" and "deepseek" in model.lower():
        raise RuntimeError("MODEL_DENIED")
    if provider=="openrouter" and not model.endswith(":free"):
        raise RuntimeError("PAID_MODEL_DENIED")
    payload={"model":model,"messages":messages,"tools":TOOLS,"tool_choice":"auto",
             "max_tokens":MAX_OUTPUT_TOKENS,"stream":False}
    if provider=="openrouter":
        payload["provider"]={"allow_fallbacks":False,"require_parameters":True}
    req=urllib.request.Request(PROVIDERS[provider][1],
       data=json.dumps(payload,separators=(",",":")).encode("utf-8"),
       headers={"Authorization":"Bearer "+key,"Content-Type":"application/json",
                "User-Agent":"FIRST-Lab-Free-Discovery-G0G3/0"},
       method="POST")
    start=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=REQUEST_TIMEOUT) as r:
            data=json.loads(r.read(300000))
        if not isinstance(data,dict):
            return None,"INVALID_RESPONSE",round(time.monotonic()-start,2)
        return data,"HTTP_200",round(time.monotonic()-start,2)
    except urllib.error.HTTPError as e:
        return None,("QUOTA_BLOCKED" if e.code==429 else "HTTP_"+str(e.code)),round(time.monotonic()-start,2)
    except (TimeoutError,OSError):
        return None,"TIMEOUT_OR_NETWORK",round(time.monotonic()-start,2)
    except (ValueError,UnicodeDecodeError):
        return None,"INVALID_JSON",round(time.monotonic()-start,2)

def tool_invoke(name,args,state):
    if name=="read_file":
        path=args.get("path")
        if path not in ALLOWED:
            return {"ok":False,"error":"READ_DENIED"}
        content=show(BASE,ALLOWED[path])
        state["files"].append(path)
        return {"ok":True,"path":path,"content":content[:14000]}
    if name=="ask_operator":
        qs=args.get("questions")
        if not isinstance(qs,list):
            return {"ok":False,"error":"QUESTIONS_INVALID"}
        if len(state["questions"])+len(qs)>MAX_QUESTIONS:
            return {"ok":False,"error":"QUESTION_CAP"}
        result,records=respond(qs)
        if result.get("ok"):
            state["questions"].extend(records)
            for x in records:
                state["surfaced"].update(x["matched"])
        return result
    if name=="finish":
        state["finish_called"]=True
        summary=args.get("summary")
        state["summary_length"]=len(summary) if isinstance(summary,str) else 0
        return {"ok":True,"status":"DISCOVERY_STAGE_FINISHED"}
    return {"ok":False,"error":"UNKNOWN_TOOL"}

def run_one(provider,method,key,task):
    state={"files":[],"questions":[],"surfaced":set(),"finish_called":False,"summary_length":0}
    method_text=show(METHOD_SHA,METHOD_PATH[method]) if method!="G0" else ""
    system=SYS+"\n\n## Frozen task\n"+task
    if method_text:
        system+="\n\n## Assigned discovery mechanism (frozen source)\n"+method_text
    messages=[{"role":"system","content":system},
              {"role":"user","content":"Perform requirement discovery now. Inspect relevant existing facts and ask the operator for unresolved product decisions using the tools. Do not implement."}]
    records=[]
    total_usage=[]
    response_models=[]
    stop="MAX_REQUESTS"
    for turn in range(1,MAX_REQUESTS+1):
        data,status,elapsed=call_model(provider,key,messages)
        event={"turn":turn,"api_status":status,"elapsed_seconds":elapsed,"tool_actions":[]}
        if data is None:
            records.append(event)
            stop=status
            break
        if isinstance(data.get("model"),str):
            response_models.append(data["model"][:120])
        usage=data.get("usage") or {}
        if isinstance(usage,dict):
            total_usage.append({k:v for k,v in usage.items()
                                if k in ("prompt_tokens","completion_tokens","total_tokens")
                                and isinstance(v,int) and 0<=v<10000000})
        choices=data.get("choices") or []
        msg=choices[0].get("message",{}) if choices and isinstance(choices[0],dict) else {}
        if not isinstance(msg,dict): msg={}
        raw=msg.get("tool_calls")
        calls=[]
        for j,c in enumerate(raw[:8] if isinstance(raw,list) else []):
            if isinstance(c,dict) and isinstance(c.get("function"),dict):
                f=c["function"]
                calls.append({"id":str(c.get("id") or f"call_{turn}_{j}"),
                              "type":"function",
                              "function":{"name":str(f.get("name") or ""),
                                          "arguments":str(f.get("arguments") or "{}")}})
        if not calls:
            event["no_tool_reply"]=True
            records.append(event)
            messages.append({"role":"assistant","content":str(msg.get("content") or "")[:1000]})
            messages.append({"role":"user","content":"Continue requirement discovery with tools. Only explicit ask_operator questions count as operator decisions; finish when complete."})
            continue
        messages.append({"role":"assistant","content":str(msg.get("content") or ""),"tool_calls":calls})
        for c in calls:
            name=c["function"]["name"]
            try:
                args=json.loads(c["function"]["arguments"])
                if not isinstance(args,dict): raise ValueError("expected dict")
                result=tool_invoke(name,args,state)
            except (ValueError,TypeError):
                result={"ok":False,"error":"MALFORMED_ARGUMENTS"}
            event["tool_actions"].append({"name":name[:100],"ok":bool(result.get("ok")),
                                           "error":result.get("error"),
                                           "source_path":result.get("path"),
                                           "question_topics":[r.get("matched") for r in state["questions"][-8:]] if name=="ask_operator" else None})
            messages.append({"role":"tool","tool_call_id":c["id"],
                             "content":json.dumps(result,ensure_ascii=False)})
        records.append(event)
        if state["finish_called"]:
            stop="FINISH_CALLED"
            break
    result={
        "protocol":"FREE_S02_DISCOVERY_G0G3_V0",
        "provider":provider,"model":PROVIDERS[provider][2],"method":method,
        "base_sha":BASE,"method_commit":METHOD_SHA,
        "method_hash":hashlib.sha256(method_text.encode("utf-8")).hexdigest() if method_text else None,
        "task_hash":hashlib.sha256(task.encode("utf-8")).hexdigest(),
        "stop":stop,"requests":len(records),"request_cap":MAX_REQUESTS,
        "files_read":state["files"],"questions":state["questions"],
        "surfaced":sorted(state["surfaced"]),
        "surfaced_count":len(state["surfaced"]),
        "unasked_policy_count":4-len(state["surfaced"]),
        "unclassified_questions":sum(not x["matched"] for x in state["questions"]),
        "finish_called":state["finish_called"],
        "summary_length":state["summary_length"],
        "tool_trace":records,"usage":total_usage,"response_models":response_models,
        "note":"Questions preserved for independent audit; no model completion texts or credentials logged.",
    }
    print(f"{provider}/{method} stop={stop} requests={result['requests']} questions={len(state['questions'])} "
          f"surfaced={result['surfaced_count']}/4 unclassified={result['unclassified_questions']} "
          f"reads={len(state['files'])}",flush=True)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--provider",required=True,choices=sorted(PROVIDERS))
    parser.add_argument("--output",required=True,type=Path)
    a=parser.parse_args()
    key=os.environ.get(PROVIDERS[a.provider][0],"").strip()
    if not key:
        raise RuntimeError("MISSING_PROVIDER_SECRET")
    task=frozen_task()
    out=a.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    cohort=[]
    for method in ORDERS[a.provider]:
        if any(r.get("stop")=="QUOTA_BLOCKED" for r in cohort):
            row={"provider":a.provider,"model":PROVIDERS[a.provider][2],"method":method,
                 "stop":"NOT_ATTEMPTED_QUOTA","requests":0}
        else:
            try:
                row=run_one(a.provider,method,key,task)
            except Exception as e:
                row={"provider":a.provider,"model":PROVIDERS[a.provider][2],"method":method,
                     "stop":"HARNESS_EXCEPTION","error_type":type(e).__name__,"requests":0}
                print(f"{a.provider}/{method}: HARNESS_EXCEPTION {type(e).__name__}",flush=True)
        cohort.append(row)
        (out/f"{method}.json").write_text(json.dumps(row,indent=2,ensure_ascii=False)+"\n","utf-8")
    summary={"protocol":"FREE_S02_DISCOVERY_G0G3_V0","provider":a.provider,
             "model":PROVIDERS[a.provider][2],"run_order":ORDERS[a.provider],
             "cohort":cohort,"finished_utc":datetime.now(timezone.utc).isoformat()}
    (out/"cohort.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n","utf-8")
    print("COMPLETE",a.provider,[(x["method"],x["stop"],x.get("surfaced_count")) for x in cohort],flush=True)

if __name__=="__main__":
    main()
