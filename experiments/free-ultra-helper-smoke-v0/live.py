#!/usr/bin/env python3
"""Free Ultra lead -> implementer -> reviewer live API smoke.

No model-generated source is executed. No model output, secret or prompt body is logged.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import socket
import time
import urllib.error
import urllib.request

MODEL="nvidia/nemotron-3-ultra-550b-a55b"
URL="https://integrate.api.nvidia.com/v1/chat/completions"
MARKER="LEAD_ONLY_SYNTHETIC_SCOPE_MARKER_7X9"
MAX_REQUESTS=3
MAX_OUTPUT=320
TIMEOUT=90
ROLES=("lead","implementer","reviewer")
FUNCTIONS={
    "lead":("submit_plan",{"type":"object","properties":{
        "steps":{"type":"array","items":{"type":"string"},"minItems":1,"maxItems":4}},
        "required":["steps"],"additionalProperties":False}),
    "implementer":("submit_patch",{"type":"object","properties":{
        "source":{"type":"string"}},
        "required":["source"],"additionalProperties":False}),
    "reviewer":("submit_review",{"type":"object","properties":{
        "approved":{"type":"boolean"},
        "reason_code":{"type":"string","enum":["APPROVE","REVISION_REQUIRED"]}},
        "required":["approved","reason_code"],"additionalProperties":False}),
}

class Stop(Exception):
    def __init__(self,code):
        super().__init__(code)
        self.code=code

def source_safe(source):
    if not isinstance(source,str) or len(source.encode("utf-8"))>3500:
        return False,"SIZE_OR_TYPE"
    try:
        tree=ast.parse(source)
    except SyntaxError:
        return False,"SYNTAX_ERROR"
    body=tree.body
    if body and isinstance(body[0],ast.Expr) and isinstance(body[0].value,ast.Constant) and isinstance(body[0].value.value,str):
        body=body[1:]
    if len(body)!=1 or not isinstance(body[0],ast.FunctionDef) or body[0].name!="normalize_tag":
        return False,"FUNCTION_SHAPE"
    for node in ast.walk(body[0]):
        if isinstance(node,(ast.Import,ast.ImportFrom,ast.Global,ast.Nonlocal,
                            ast.ClassDef,ast.With,ast.AsyncWith,ast.Try,
                            ast.Raise,ast.Yield,ast.YieldFrom)):
            return False,"FORBIDDEN_SYNTAX"
        if isinstance(node,ast.Name) and node.id in {"open","eval","exec","compile",
           "__import__","globals","locals","input","getattr","setattr","delattr"}:
            return False,"FORBIDDEN_BUILTIN"
        if isinstance(node,ast.Attribute) and node.attr.startswith("__"):
            return False,"FORBIDDEN_ATTRIBUTE"
    return True,"SYNTAX_AND_SHAPE_OK"

def make_payload(role,source=None):
    task=("Implement a pure Python function normalize_tag(s: str) -> str. "
          "Lowercase the input, replace each maximal sequence of non-ASCII-alphanumeric "
          "characters with one hyphen, and strip leading/trailing hyphens. "
          "Use no dependencies or imports. This is synthetic, not production.")
    if role=="lead":
        messages=[{"role":"system","content":"You are an isolated synthetic planning lead. Marker: "+MARKER+
                    ". Do not forward it. Use submit_plan only."},
                  {"role":"user","content":task+" Reply with a submit_plan function call."}]
    elif role=="implementer":
        messages=[{"role":"system","content":"You are a fresh coding implementer with no conversation history. Use submit_patch only."},
                  {"role":"user","content":task+" Return the entire source with a submit_patch function call."}]
    elif role=="reviewer":
        messages=[{"role":"system","content":"You are a fresh independent read-only reviewer. Use submit_review only."},
                  {"role":"user","content":task+"\nReview this synthetic candidate. Say APPROVE if it looks correct, "
                  "otherwise REVISION_REQUIRED. Do not execute code:\n"+str(source)}]
    else:
        raise Stop("UNKNOWN_ROLE")
    name,schema=FUNCTIONS[role]
    payload={"model":MODEL,"messages":messages,"tools":[{
        "type":"function","function":{"name":name,"description":"Submit synthetic "+role+" result.",
                                      "parameters":schema}}],
        "tool_choice":"auto","max_tokens":MAX_OUTPUT,"stream":False}
    return payload

def call_api(api_key,payload):
    req=urllib.request.Request(URL,
        data=json.dumps(payload,separators=(",",":")).encode("utf-8"),
        method="POST",
        headers={"Content-Type":"application/json","Authorization":"Bearer "+api_key,
                 "User-Agent":"FIRST-Lab-Ultra-Helper-Capability/0"})
    start=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=TIMEOUT) as r:
            data=json.loads(r.read(200000))
        return data,"HTTP_200",round(time.monotonic()-start,2)
    except urllib.error.HTTPError as e:
        return None,("QUOTA_BLOCKED" if e.code==429 else "HTTP_"+str(e.code)),round(time.monotonic()-start,2)
    except (TimeoutError,socket.timeout,urllib.error.URLError,OSError):
        return None,"NETWORK_OR_TIMEOUT",round(time.monotonic()-start,2)
    except (ValueError,UnicodeDecodeError):
        return None,"INVALID_JSON",round(time.monotonic()-start,2)

def run():
    api_key=os.getenv("NVIDIA_API_KEY","").strip()
    if not api_key: raise Stop("MISSING_SECRET")
    rows=[]
    ledger={"request_count":0,"usage_prompt_tokens":0,"usage_completion_tokens":0,
            "usage_total_tokens":0,"usage_missing":False}
    source=None
    for i,role in enumerate(ROLES,1):
        if ledger["request_count"]>=MAX_REQUESTS:
            raise Stop("REQUEST_LIMIT")
        payload=make_payload(role,source)
        request_text=json.dumps(payload,separators=(",",":"),ensure_ascii=False)
        contains_marker=MARKER in request_text
        if contains_marker != (role=="lead"):
            raise Stop("CONTEXT_MARKER_ISOLATION_FAILED")
        if len(request_text.encode("utf-8"))>6500:
            raise Stop("PROMPT_TOO_LARGE")
        row={"role":role,"ordinal":i,"messages_count":len(payload["messages"]),
             "model_requested":MODEL,
             "lead_marker_present":contains_marker,
             "request_sha256":hashlib.sha256(request_text.encode()).hexdigest(),
             "expected_tool":FUNCTIONS[role][0],
             "api_status":None,"elapsed_seconds":None}
        ledger["request_count"]+=1
        data,status,elapsed=call_api(api_key,payload)
        row["api_status"]=status
        row["elapsed_seconds"]=elapsed
        if status!="HTTP_200" or not isinstance(data,dict):
            rows.append(row)
            break
        row["response_model_matches"]=data.get("model")==MODEL
        usage=data.get("usage")
        if isinstance(usage,dict) and all(isinstance(usage.get(k),int) for k in
                                          ("prompt_tokens","completion_tokens","total_tokens")):
            for k in ("prompt_tokens","completion_tokens","total_tokens"):
                ledger["usage_"+k]+=usage[k]
        else:
            ledger["usage_missing"]=True
        choices=data.get("choices") or []
        message=choices[0].get("message",{}) if choices and isinstance(choices[0],dict) else {}
        calls=message.get("tool_calls") if isinstance(message,dict) else []
        if not isinstance(calls,list): calls=[]
        valid=[]
        for call in calls[:3]:
            if not isinstance(call,dict): continue
            fn=call.get("function")
            if not isinstance(fn,dict) or fn.get("name")!=FUNCTIONS[role][0]:
                continue
            try:
                args=json.loads(fn.get("arguments") or "{}")
                if not isinstance(args,dict): continue
                valid.append(args)
            except (ValueError,TypeError):
                continue
        row["expected_tool_emitted"]=bool(valid)
        row["tool_call_count"]=len(calls)
        if not valid:
            rows.append(row)
            break
        args=valid[0]
        if role=="lead":
            steps=args.get("steps")
            row["plan_valid"]=isinstance(steps,list) and 1<=len(steps)<=4 and all(
                isinstance(x,str) and len(x)<=500 for x in steps)
            if not row["plan_valid"]:
                rows.append(row)
                break
        if role=="implementer":
            source=args.get("source")
            good,reason=source_safe(source)
            row["patch_source_shape_valid"]=good
            row["source_validation_code"]=reason
            if isinstance(source,str):
                row["candidate_sha256"]=hashlib.sha256(source.encode()).hexdigest()
            if not good:
                rows.append(row)
                break
        if role=="reviewer":
            row["review_schema_valid"]=(
                type(args.get("approved")) is bool
                and args.get("reason_code") in ("APPROVE","REVISION_REQUIRED"))
            row["reviewer_approved"]=args.get("approved") if row["review_schema_valid"] else None
            if not row["review_schema_valid"]:
                rows.append(row)
                break
        rows.append(row)
    return {
        "experiment":"FREE_ULTRA_HELPER_SMOKE_V0",
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "requested_model":MODEL,
        "free_only":True,"no_fallback":True,
        "no_paid_provider":True,"no_deepseek_nvidia":True,"no_groq":True,
        "request_cap":MAX_REQUESTS,"max_output_tokens_per_request":MAX_OUTPUT,
        "per_role_network_timeout_seconds":TIMEOUT,
        "host_event_status":"ALL_THREE_ROLE_TOOLS_EMITTED" if len(rows)==3 and all(
            r.get("expected_tool_emitted") for r in rows) else "INCOMPLETE",
        "rows":rows,"shared_ledger":ledger,
        "no_model_source_executed":True,
        "source_content_not_persisted":True,
        "note":"Evidence records host-constructed request markers; not cryptographic proof of provider internal context isolation or correct model source."
    }

def main():
    try:
        result=run()
    except Stop as e:
        result={"experiment":"FREE_ULTRA_HELPER_SMOKE_V0","host_event_status":e.code,
                "rows":[],"no_model_source_executed":True}
    Path("helper-smoke-report.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    for row in result["rows"]:
        print(f"ROLE {row['role']} {row['api_status']} {row['elapsed_seconds']}s "
              f"expected_tool={row.get('expected_tool_emitted',False)} "
              f"model_id={row.get('response_model_matches',False)}")
    print("HOST_SMOKE",result["host_event_status"],"requests",len(result["rows"]))
    if result["host_event_status"]!="ALL_THREE_ROLE_TOOLS_EMITTED":
        raise SystemExit(1)

if __name__=="__main__":
    main()
