from pathlib import Path
import datetime,hashlib,importlib.util,json,os,subprocess,sys
root=Path('/workspace/relayboard-round2-control')
run_id=sys.argv[1]
capture=json.loads((root/(run_id+'-capture.json')).read_text())
snapshot=root/'snapshots'/run_id
assert not (Path('/workspace/relayboard-round2-active')/run_id).exists(),'Contestant must be terminated and working area removed'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
env=os.environ.copy();env['PYTHONPATH']=str(snapshot);env['PYTHONDONTWRITEBYTECODE']='1'
started=now()
public=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=snapshot,env=env,capture_output=True,text=True)
sys.path.insert(0,str(snapshot))
evaluator_path=root/'evaluator-active'/'evaluator.py'
spec=importlib.util.spec_from_file_location('frozen_lab_evaluator',evaluator_path)
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
manifest=json.loads((snapshot/'.experiment/RUN_MANIFEST.json').read_text())
scenario=manifest['scenario'];fn={'S01-v0':'evaluate_s01','S02-v0.1':'evaluate_s02','S04-v0':'evaluate_s04'}[scenario]
try:
 result=getattr(module,fn)()
 oracle={'scenario':result.scenario,'passed':result.passed,'failures':result.failures,'error':None}
except Exception as exc:
 import traceback
 oracle={'scenario':scenario,'passed':False,'failures':[],'error':traceback.format_exc()}
b=evaluator_path.read_bytes()
record={'schema_version':1,'run_id':run_id,'started_at':started,'finished_at':now(),'context':'separate orchestrator-owned Python process after contestant termination','local_candidate_sha':capture['local_candidate_sha'],'candidate_tree':capture['local_candidate_tree'],'frozen_evaluator_ref':'b8048c069277ae3a6d15a2ad324d60c4b1500c2a','evaluator_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'public_tests':{'command':'python -m unittest discover -s tests -v','exit_code':public.returncode,'passed':public.returncode==0,'stdout':public.stdout,'stderr':public.stderr},'oracle':oracle,'feedback_to_contestant':False}
(root/(run_id+'-evaluation.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
