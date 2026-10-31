#!/usr/bin/env python3
"""Independent no-secret examiner for eight free S02 contestants."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE="2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f"
PROVIDERS=("nvidia","openrouter")
METHODS=("neutral","pstack","matt","first")

def evaluate_bundle(path, report):
    with tempfile.TemporaryDirectory(prefix="first-s02-grade-") as tmp:
        work=Path(tmp)/"candidate"
        work.mkdir()
        with tarfile.open(path,"r:gz") as tf:
            if any(not m.isfile() and not m.isdir() for m in tf.getmembers()):
                return {"status":"INVALID_ARCHIVE"}
            tf.extractall(work,filter="data")
        manifest=work/".experiment"/"RUN_MANIFEST.json"
        if not manifest.exists():
            return {"status":"MISSING_MANIFEST"}
        info=json.loads(manifest.read_text(encoding="utf-8"))
        if info.get("base_sha")!=BASE or info.get("scenario")!="S02-v0.1":
            return {"status":"INVALID_BASE_OR_SCENARIO"}
        hashes={}
        for key,sha in (report.get("changed_sha256") or {}).items():
            f=work/key
            if not f.is_file() or not f.resolve().is_relative_to(work.resolve()):
                return {"status":"HASH_PATH_DENIED"}
            hashes[key]=hashlib.sha256(f.read_bytes()).hexdigest()==sha
        if not all(hashes.values()):
            return {"status":"CANDIDATE_HASH_MISMATCH"}
        if (work/"TASK.md").is_file() is False:
            return {"status":"NO_TASK"}
        script=HERE/"inside_grade.py"
        cmd=["docker","run","--rm","--pull=never","--network","none",
             "--read-only","--cap-drop=ALL","--security-opt=no-new-privileges",
             "--pids-limit","64","--memory","384m","--cpus","1",
             "--user","65534:65534",
             "--tmpfs","/tmp:rw,noexec,nosuid,size=16m",
             "--mount",f"type=bind,src={ROOT},dst=/lab,readonly",
             "--mount",f"type=bind,src={work},dst=/work,readonly",
             "-e","PYTHONDONTWRITEBYTECODE=1","-e","PYTHONPATH=/work",
             "python:3.12-slim","python","/lab/experiments/free-s02-screen-v0/inside_grade.py"]
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=50,
                             env={"PATH":os.getenv("PATH","/usr/bin:/bin"),"HOME":"/tmp"})
            matched=[x.split("GRADE_JSON:",1)[1] for x in p.stdout.splitlines() if x.startswith("GRADE_JSON:")]
            if not matched:
                return {"status":"GRADER_OUTPUT_INVALID","returncode":p.returncode}
            grade=json.loads(matched[-1])
            return {"status":"EVALUATED","public_pass":bool(grade.get("public_pass")),
                    "public_tests":grade.get("public_tests"),
                    "oracle_pass":bool(grade.get("frozen_oracle_pass")),
                    "oracle_failures":grade.get("frozen_oracle_failures",[]),
                    "candidate_hashes_valid":True}
        except Exception as exc:
            return {"status":"GRADER_ERROR","exception_type":type(exc).__name__}

def main():
    evidence=Path("evidence")
    results=[]
    for provider in PROVIDERS:
        meta=evidence/provider/"cohort.json"
        records=[]
        if meta.is_file():
            try: records=json.loads(meta.read_text("utf-8"))
            except Exception: records=[]
        for method in METHODS:
            rid=f"FREES02-{provider.upper()}-{method.upper()}-001"
            item=next((x for x in records if x.get("run_id")==rid),None)
            if not item:
                results.append({"run_id":rid,"provider":provider,"method":method,
                                "status":"NO_RESULT","verified":False})
                continue
            status=item.get("stop","UNKNOWN")
            row={"run_id":rid,"provider":provider,"method":method,
                 "agent_stop":status,"requests":item.get("requests",0),
                 "surfaced":item.get("surfaced_count"),
                 "silent":item.get("silent_count"),
                 "question_count":len(item.get("operator_questions",[])),
                 "method_class":item.get("method_class"),
                 "candidate_changed":item.get("changed",[]),
                 "verified":False}
            bundle=evidence/provider/rid/"candidate.tar.gz"
            if not bundle.is_file():
                row["status"]="NO_CANDIDATE"
                results.append(row)
                continue
            grade=evaluate_bundle(bundle,item)
            row["evaluation"]=grade
            row["status"]=grade["status"]
            row["verified"]=grade.get("public_pass") is True and grade.get("oracle_pass") is True
            results.append(row)
    summary={"experiment":"FREE_S02_METHOD_SCREEN_V0",
             "methods":["pstack","matt","first"],
             "baseline":"neutral",
             "sources":["nvidia:NIM/openai-gpt-oss-20b","openrouter:nemotron-3.5-lightning:free"],
             "level":"NON_NATIVE_SINGLE_AGENT_PROXY_SCREEN",
             "independent_grader_no_api_keys":True,
             "frozen_scenario":"S02-v0.1",
             "frozen_base_sha":BASE,
             "outcomes":results}
    Path("grade-results.json").write_text(json.dumps(summary,indent=2)+"\n","utf-8")
    print("INDEPENDENT_S02_SCREEN_BEGIN")
    for r in results:
        ev=r.get("evaluation",{})
        print(f"{r['run_id']}: {r.get('agent_stop',r['status'])} "
              f"requests={r.get('requests','?')} surfaced={r.get('surfaced','?')} "
              f"public={ev.get('public_pass','?')} frozen={ev.get('oracle_pass','?')} "
              f"grade_status={r.get('status')} verified={r['verified']}")
    print("INDEPENDENT_S02_SCREEN_END")
    f=os.getenv("GITHUB_STEP_SUMMARY")
    if f:
        with open(f,"a",encoding="utf-8") as out:
            out.write("## Free S02 four-arm single-agent proxy screen\n\n")
            out.write("| Provider | Method | Requests | Decisions | Public | Frozen oracle | Status |\n")
            out.write("|---|---|---:|---:|---|---|---|\n")
            for r in results:
                ev=r.get("evaluation",{})
                out.write(f"| {r['provider']} | {r['method']} | {r.get('requests','?')} | "
                          f"{r.get('surfaced','?')}/4 | {ev.get('public_pass','?')} | "
                          f"{ev.get('oracle_pass','?')} | {r['status']} |\n")
            out.write("\nThese are **non-native single-agent ports**, not full pstack/Matt host implementations. One run per cell; no winner or causal claim.\n")

if __name__=="__main__":
    main()
