#!/usr/bin/env python3
"""Eight-run free-provider S02 portable-proxy experiment. Research-only.

Restricted function tools; local Docker without network for generated Python;
the hidden evaluator never enters the contestant's allowed tool workspace.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PORT_REF = "226a03a883c65c81223ca49e00ddd058e1b38691"
BASE = "2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f"
PROVIDERS = {
    "nvidia": ("NVIDIA_API_KEY", "https://integrate.api.nvidia.com/v1/chat/completions", "openai/gpt-oss-20b"),
    "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/chat/completions", "nvidia/nemotron-3.5-lightning:free"),
}
ORDERS = {
    "nvidia": ["matt", "neutral", "first", "pstack"],
    "openrouter": ["pstack", "first", "matt", "neutral"],
}
TREATMENTS = {"matt":"matt-pinned", "neutral":"neutral-v0", "first":"first-mode-v0", "pstack":"pstack-pinned"}
PORT_PATHS = {
    "pstack": "experiments/relayboard/orchestration/codex-ports-v0/PSTACK_CODEX_PORT_V0.md",
    "matt": "experiments/relayboard/orchestration/codex-ports-v0/MATT_CODEX_PORT_V0.md",
}
MAX_CALLS = 9
MAX_OUTPUT_TOKENS = 3000
MAX_WRITES = 6
REQUEST_TIMEOUT = 90
ALLOWED_READ = ["TASK.md", "METHOD.md", "GLOSSARY.md", "README.md", "relayboard/__init__.py",
                "relayboard/models.py", "relayboard/store.py", "relayboard/service.py",
                "relayboard/web.py", "relayboard/testing.py", "tests/test_public.py",
                "tests/test_pause.py"]
ALLOWED_WRITE = {"relayboard/models.py", "relayboard/store.py", "relayboard/service.py",
                 "relayboard/web.py", "tests/test_pause.py"}
QUESTION_RULES = [
    ("pause_in_progress_run", re.compile(r"(?:in.progress|in.flight|already.running|active.run|ongoing.run|currently.running)", re.I), re.compile(r"paus", re.I), "An already-running Run continues to its terminal outcome; pause must not cancel it."),
    ("scheduled_start_while_paused", re.compile(r"(?:schedul|missed.start|missed.trigger)", re.I), re.compile(r"(?:paus|while.*paus|during.*paus)", re.I), "Scheduled starts during pause are skipped and not queued."),
    ("manual_run_while_paused", re.compile(r"manual", re.I), re.compile(r"paus", re.I), "Manual Runs remain allowed while the Job is paused."),
    ("resume_behavior", re.compile(r"(?:resum|unpaus)", re.I), re.compile(r"(?:catch.?up|missed|schedul|backlog|queue)", re.I), "Resume allows only future scheduled starts; do not catch up missed work."),
]
COMMON = """You are the coding contestant in a synthetic RelayBoard benchmark.
Work only from your fresh isolated TASK.md and public fixture. Use the provided function
tools to inspect, change, test, and inspect the diff. The tool environment contains no
shell, internet browser, hidden evaluator or other runs. Keep the smallest correct change.
If product behavior is materially unspecified, you may ASK the frozen operator explicitly
using ask_operator; the operator will answer only genuine product questions asked.
Never invent that you ran tools. Do not inspect other experiments, evaluator, or GitHub.
You have at most nine model requests; batch independent reads or writes when practical.
"""
HOST_BINDING = """FREE-PROVIDER HOST BINDING, portable proxy rather than native Codex/Cursor/Claude execution:
- The frozen text below is the tested method source, but this restricted harness has no
  collaboration.spawn_agent, slash-command router, native bundled upstream skills,
  task tracker or independent subagent service. Do not claim these steps were executed.
- Use ask_operator(question) instead of collaboration.send_message for a genuine product question.
- Use provided read_file/write_file/run_public_tests/show_diff instead of shell commands.
- Adapt helper/reviewer stages to a single-agent written review where possible, noting lost fidelity.
- Ignore source instructions that require GPT-6.1 Sol, paid models, host plugins or external services.
- Preserve method intent; do not read evaluator, oracle, peer runs, or outside repository content.
"""

TOOLS = [
    {"type":"function","function":{"name":"list_files","description":"List allowed synthetic fixture paths.",
       "parameters":{"type":"object","properties":{},"additionalProperties":False}}},
    {"type":"function","function":{"name":"read_file","description":"Read one allowed file in the isolated fixture.",
       "parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"],"additionalProperties":False}}},
    {"type":"function","function":{"name":"write_file","description":"Replace one allowlisted Python source file with complete content, at most 6 writes/run.",
       "parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"],"additionalProperties":False}}},
    {"type":"function","function":{"name":"run_public_tests","description":"Run public Python unit tests in an isolated network-disabled Docker container; no evaluator.",
       "parameters":{"type":"object","properties":{},"additionalProperties":False}}},
    {"type":"function","function":{"name":"show_diff","description":"Show the actual git diff from the frozen baseline for allowed application/test files.",
       "parameters":{"type":"object","properties":{},"additionalProperties":False}}},
    {"type":"function","function":{"name":"ask_operator","description":"Ask only a genuine unresolved product/preference question. Operator answers only matched requested decisions.",
       "parameters":{"type":"object","properties":{"question":{"type":"string"}},"required":["question"],"additionalProperties":False}}},
]

def git(*args, cwd=ROOT):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=25)
    if p.returncode:
        raise RuntimeError("GIT_FAILURE")
    return p.stdout

def safe_path(wd, path, paths):
    if not isinstance(path, str) or path not in paths:
        return None
    resolved = (wd / path).resolve()
    if not resolved.is_relative_to(wd.resolve()):
        return None
    return resolved

def docker_public(wd):
    command = [
        "docker", "run", "--rm", "--pull=never", "--network=none",
        "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges",
        "--pids-limit=64", "--memory=384m", "--cpus=1",
        "--user=65534:65534", "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
        "--mount", f"type=bind,src={wd.resolve()},dst=/work,readonly",
        "--workdir=/work", "-e", "PYTHONDONTWRITEBYTECODE=1",
        "-e", "PYTHONPATH=/work", "python:3.12-slim",
        "python", "-m", "unittest", "discover", "-s", "tests", "-v",
    ]
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=40,
                           env={"PATH":os.getenv("PATH","/usr/bin:/bin"),"HOME":"/tmp"})
        return {"passed":p.returncode==0, "exit_code":p.returncode,
                "diagnostic":(p.stdout+"\n"+p.stderr)[-1900:]}
    except subprocess.TimeoutExpired:
        return {"passed":False,"status":"TEST_TIMEOUT"}
    except Exception:
        return {"passed":False,"status":"TEST_HOST_ERROR"}

def ask(question, state):
    if not isinstance(question,str) or not question.strip():
        return {"ok":False,"status":"INVALID_QUESTION"}
    found=[]
    for key, a, b, answer in QUESTION_RULES:
        if a.search(question) and b.search(question):
            found.append({"decision":key,"answer":answer})
            state["surfaced"].add(key)
    state["questions"].append({"question":question[:650],
                               "classified": [x["decision"] for x in found]})
    if found:
        return {"ok":True,"answers":found,
                "notice":"Only decisions explicitly requested were answered."}
    return {"ok":False,"status":"UNCLASSIFIED_QUESTION",
            "notice":"Look up code facts autonomously; ask a specific product-policy question if necessary."}

def tool_result(name, params, wd, state):
    if name == "list_files":
        return {"ok":True,"paths":[x for x in ALLOWED_READ if (wd/x).is_file()]}
    if name == "read_file":
        path=params.get("path")
        file=safe_path(wd,path,ALLOWED_READ)
        if not file or not file.exists():
            return {"ok":False,"status":"READ_DENIED"}
        return {"ok":True,"path":path,"content":file.read_text("utf-8")[:13000]}
    if name == "write_file":
        path=params.get("path")
        file=safe_path(wd,path,ALLOWED_WRITE)
        content=params.get("content")
        if not file or not isinstance(content,str) or len(content.encode("utf-8"))>18000:
            return {"ok":False,"status":"WRITE_DENIED"}
        if state["writes"]>=MAX_WRITES:
            return {"ok":False,"status":"WRITE_LIMIT"}
        if not path.endswith(".py") or "\x00" in content:
            return {"ok":False,"status":"INVALID_SOURCE"}
        try:
            import ast
            ast.parse(content, filename=path)
        except SyntaxError:
            return {"ok":False,"status":"SYNTAX_ERROR"}
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content,"utf-8")
        state["writes"]+=1
        return {"ok":True,"path":path,"bytes":len(content.encode("utf-8"))}
    if name == "run_public_tests":
        state["test_count"]+=1
        result=docker_public(wd)
        state["last_test"]=result.get("passed",False)
        return {"ok":True,**result}
    if name == "show_diff":
        state["diff_seen"]=True
        diff=git("diff","HEAD","--","relayboard","tests",cwd=wd)
        return {"ok":True,"diff":diff[:12500],"truncated":len(diff)>12500}
    if name == "ask_operator":
        return ask(params.get("question"),state)
    return {"ok":False,"status":"UNKNOWN_TOOL"}

def api_request(provider, model, key, messages):
    if provider=="nvidia" and "deepseek" in model.lower():
        return None,"MODEL_DENIED",0
    if provider=="openrouter" and not model.endswith(":free"):
        return None,"MODEL_DENIED",0
    body={"model":model,"messages":messages,"tools":TOOLS,"tool_choice":"auto",
          "max_tokens":MAX_OUTPUT_TOKENS,"stream":False}
    if provider=="openrouter":
        body["provider"]={"allow_fallbacks":False,"require_parameters":True}
    req=urllib.request.Request(
        PROVIDERS[provider][1], data=json.dumps(body).encode(),method="POST",
        headers={"Content-Type":"application/json",
                 "Authorization":"Bearer "+key,"User-Agent":"FIRST-Lab-Free-S02-Screen/0"})
    t=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=REQUEST_TIMEOUT) as r:
            response=json.loads(r.read(400000))
        if not isinstance(response,dict):
            return None,"INVALID_RESPONSE",round(time.monotonic()-t,2)
        return response,"HTTP_200",round(time.monotonic()-t,2)
    except urllib.error.HTTPError as e:
        return None,("QUOTA_BLOCKED" if e.code==429 else "HTTP_"+str(e.code)),round(time.monotonic()-t,2)
    except (TimeoutError,OSError):
        return None,"TIMEOUT_OR_NETWORK",round(time.monotonic()-t,2)
    except (ValueError,UnicodeDecodeError):
        return None,"INVALID_JSON",round(time.monotonic()-t,2)

def prepare_workspace(runid,method,provider,model,wd):
    cmd=[sys.executable,
         str(ROOT/"experiments/relayboard/runner/prepare_workspace.py"),
         "--scenario","S02-v0.1","--treatment",TREATMENTS[method],
         "--host","free-single-agent-portable-proxy-v0",
         "--model",model,"--output",str(wd)]
    p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=45)
    if p.returncode:
        raise RuntimeError("PREPARE_WORKSPACE_FAILURE")
    if method in PORT_PATHS:
        text=git("show",PORT_REF+":"+PORT_PATHS[method],cwd=ROOT)
        (wd/"METHOD.md").write_text(text,"utf-8")
        git("add","METHOD.md",cwd=wd)
        git("commit","-m","freeze: insert pinned Codex methodology port",cwd=wd)
    # Do not allow evaluator, oracle or another experiment in workspace.
    bad=[str(x) for x in wd.rglob("*") if x.is_file() and
         ("evaluator" in str(x.relative_to(wd)).lower() or
          "oracle" in str(x.relative_to(wd)).lower() or
          "reference_solution" in str(x.relative_to(wd)).lower())]
    if bad:
        raise RuntimeError("WORKSPACE_CONTAMINATED")
    assert git("remote","-v",cwd=wd).strip()==""

def system_for(method,wd):
    if method=="neutral":
        return COMMON
    text=(wd/"METHOD.md").read_text("utf-8")
    return COMMON+"\n"+HOST_BINDING+"\n## Frozen methodology source\n"+text

def run_one(provider,method,key,out):
    model=PROVIDERS[provider][2]
    runid=f"FREES02-{provider.upper()}-{method.upper()}-001"
    wd=out/runid/"workspace"
    wd.parent.mkdir(parents=True,exist_ok=True)
    prepare_workspace(runid,method,provider,model,wd)
    st={"writes":0,"test_count":0,"last_test":False,"diff_seen":False,
        "surfaced":set(),"questions":[]}
    messages=[
        {"role":"system","content":system_for(method,wd)},
        {"role":"user","content":"Read TASK.md and execute the requested feature. Use tools; do not just describe a patch."},
    ]
    trace=[]
    tokens=[]
    stop="MAX_CALLS"
    for turn in range(1,MAX_CALLS+1):
        data,status,elapsed=api_request(provider,model,key,messages)
        item={"request":turn,"status":status,"seconds":elapsed,"tools":[]}
        if data is None:
            trace.append(item);stop=status;break
        usage=data.get("usage")
        if isinstance(usage,dict):
            tokens.append({k:v for k,v in usage.items()
                           if k in ("prompt_tokens","completion_tokens","total_tokens")
                           and isinstance(v,int) and v>=0})
        choices=data.get("choices")
        msg=choices[0].get("message",{}) if isinstance(choices,list) and choices and isinstance(choices[0],dict) else {}
        if not isinstance(msg,dict): msg={}
        raw=msg.get("tool_calls")
        calls=[]
        if isinstance(raw,list):
            for i,c in enumerate(raw[:12]):
                if isinstance(c,dict) and isinstance(c.get("function"),dict):
                    calls.append({"id":str(c.get("id") or f"call_{turn}_{i}"),
                                  "type":"function",
                                  "function":{"name":str(c["function"].get("name") or ""),
                                              "arguments":str(c["function"].get("arguments") or "{}")}})
        if not calls:
            item["no_tools"]=True;trace.append(item)
            if st["last_test"] and st["diff_seen"]:
                stop="AGENT_FINISHED";break
            messages.append({"role":"assistant","content":str(msg.get("content") or "")[:1500]})
            messages.append({"role":"user","content":"Continue using tools to inspect, implement, run public tests, inspect diff. If product decisions are missing, ask operator."})
            continue
        messages.append({"role":"assistant","content":str(msg.get("content") or ""),
                         "tool_calls":calls})
        for c in calls:
            name=c["function"]["name"]
            try:
                args=json.loads(c["function"]["arguments"])
                if not isinstance(args,dict): raise ValueError()
                result=tool_result(name,args,wd,st)
            except (ValueError,TypeError):
                result={"ok":False,"status":"MALFORMED_ARGS"}
            event={"name":name[:60],"ok":result.get("ok",False),
                   "status":result.get("status"),"path":result.get("path"),
                   "test_pass":result.get("passed")}
            if name=="ask_operator":
                event["question"]=str(args.get("question",""))[:650] if isinstance(args,dict) else ""
                event["decisions"]=[a["decision"] for a in result.get("answers",[])]
            item["tools"].append(event)
            messages.append({"role":"tool","tool_call_id":c["id"],
                             "content":json.dumps(result,ensure_ascii=False)})
        trace.append(item)
        if st["test_count"] and st["last_test"] and st["diff_seen"] and st["writes"]:
            stop="AGENT_FINISHED";break
    source_changes=git("diff","HEAD","--name-only",cwd=wd).splitlines()
    diff=git("diff","HEAD","--","relayboard","tests",cwd=wd)
    changed={p:hashlib.sha256((wd/p).read_bytes()).hexdigest() for p in source_changes if (wd/p).is_file()}
    results={
        "run_id":runid,"provider":provider,"model":model,"method":method,
        "method_class":"NON_NATIVE_PORTABLE_PROXY" if method in ("matt","pstack") else ("SINGLE_AGENT_FIRST_PROXY" if method=="first" else "NEUTRAL"),
        "base_sha":BASE,"port_ref":PORT_REF,"stop":stop,
        "requests":len(trace),"tools":sum(len(t["tools"]) for t in trace),
        "writes":st["writes"],"public_tests_invoked":st["test_count"],
        "latest_public_pass":st["last_test"],"diff_seen":st["diff_seen"],
        "surfaced":sorted(st["surfaced"]),"surfaced_count":len(st["surfaced"]),
        "silent_count":4-len(st["surfaced"]),
        "operator_questions":st["questions"],"changed":source_changes,
        "changed_sha256":changed,"trace":trace,"usage":tokens,
        "method_sha256":hashlib.sha256((wd/"METHOD.md").read_bytes()).hexdigest() if (wd/"METHOD.md").exists() else None,
        "no_evaluator_in_workspace":True,
    }
    outdir=out/runid
    (outdir/"result.json").write_text(json.dumps(results,indent=2)+"\n","utf-8")
    (outdir/"diff.patch").write_text(diff,"utf-8")
    with tarfile.open(outdir/"candidate.tar.gz","w:gz") as tf:
        for item in wd.rglob("*"):
            if item.is_file() and ".git" not in item.relative_to(wd).parts:
                tf.add(item,arcname=str(item.relative_to(wd)))
    print(f"{runid} stop={stop} requests={len(trace)} actions={results['tools']} "
          f"surfaced={len(st['surfaced'])}/4 public={st['last_test']} changed={len(source_changes)}",flush=True)
    shutil.rmtree(wd)
    return results

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--provider",required=True,choices=PROVIDERS)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    if git("rev-parse",BASE).strip()!=BASE:
        raise RuntimeError("BASE_NOT_AVAILABLE")
    provider=a.provider
    key=os.environ.get(PROVIDERS[provider][0],"").strip()
    if not key:
        raise RuntimeError("MISSING_SECRET")
    if provider=="openrouter" and not PROVIDERS[provider][2].endswith(":free"):
        raise RuntimeError("PAID_MODEL_BLOCKED")
    output=a.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    results=[]
    for method in ORDERS[provider]:
        if any(r.get("stop")=="QUOTA_BLOCKED" for r in results):
            results.append({"run_id":f"FREES02-{provider.upper()}-{method.upper()}-001",
                            "provider":provider,"method":method,"stop":"NOT_ATTEMPTED_QUOTA","requests":0})
            continue
        try:
            results.append(run_one(provider,method,key,output))
        except Exception as exc:
            # Do not expose secret-bearing exceptions.
            print(f"{provider}/{method}: HOST_FAILURE ({type(exc).__name__})",flush=True)
            results.append({"run_id":f"FREES02-{provider.upper()}-{method.upper()}-001",
                            "provider":provider,"method":method,"stop":"HOST_FAILURE","requests":0})
    (output/"cohort.json").write_text(json.dumps(results,indent=2)+"\n","utf-8")
    print(provider,"DISPOSITIONS",[(r["method"],r["stop"]) for r in results],flush=True)

if __name__=="__main__":
    main()
