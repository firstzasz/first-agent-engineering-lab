import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

CONTROL = Path(__file__).resolve().parent
WORK = CONTROL.parent
D = json.loads((CONTROL/'input.json').read_text(encoding='utf-8'))
def now(): return datetime.now(timezone.utc).isoformat()
def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
def blob(content):
    raw = content.encode('utf-8') if isinstance(content, str) else content
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def command(args, cwd, check=True):
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='NUL', PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, encoding='utf-8', errors='replace')
    result = {'command': args, 'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    if check and p.returncode: raise RuntimeError(json.dumps(result))
    return result
def git(args, cwd): return command(['git']+args, cwd)['stdout'].strip()
def preflight():
    t = {x['path']:x['sha'] for x in D['tree']['tree'] if x['type']=='blob'}
    bt = {x['path']:x['sha'] for x in D['base_tree']['tree'] if x['type']=='blob'}
    c = D['cohort']; audit = json.loads(D['docs']['PRE_RUN_AUDIT.json']['content']); b = json.loads(D['batch']['content'])
    checks = {}
    checks['expected_head'] = D['head']=='63aea9e37dca19beb476e07eaac36fe46d0b2cf1' and D['tree']['sha']==D['head']
    checks['audit_declared_pass'] = audit['status']=='PASS' and not audit['errors'] and audit['checked_before_contestant_runs']
    checks['balanced_exact_stage1_order'] = [r['run_id'] for r in c['stage1']['order']]==audit['stage1_runs']==[r['run_id'] for r in b['stage1_runs']]==['RD-M1-S1','RD-M0-S1','RD-M2-S1','RD-M3-S1'] and {r['arm'] for r in c['stage1']['order']}=={'M0','M1','M2','M3'}
    checks['not_started_no_stage2_authorization'] = b['status']=='STAGE1_READY_NOT_STARTED' and b['completed_count']==b['excluded_count']==0 and all(r['status']=='READY' for r in b['stage1_runs']) and all(r['status']=='CONDITIONAL_NOT_AUTHORIZED' for r in b['stage2_runs']) and not audit['stage2_authorized']
    checks['all_downloaded_docs_match_blobs'] = all(blob(v['content'])==v['sha']==t[D['prefix']+k] for k,v in D['docs'].items()) and blob(D['batch']['content'])==D['batch']['sha']==t[D['prefix']+'batch.json']
    checks['task_exact_frozen_blob'] = blob(D['task']['content'])==D['task']['sha']==c['task']['blob']==audit['frozen_blobs']['task']==t[c['task']['path']]
    checks['methods_exact_frozen_blobs'] = all(blob(v['content'])==v['sha']==c['methods'][arm]['blob']==audit['frozen_blobs'][arm]==t[c['methods'][arm]['path']] for arm,v in D['methods'].items()) and c['methods']['M0']['method'] is None
    checks['evaluator_exact_frozen_blob'] = blob(D['evaluator']['content'])==D['evaluator']['sha']==c['evaluator_blob']==audit['frozen_blobs']['evaluator']==bt['experiments/relayboard/evaluator/evaluator.py']
    checks['oracle_exact_frozen_blob'] = blob(D['oracle']['content'])==D['oracle']['sha']==c['oracle_blob']==audit['frozen_blobs']['oracle']==bt['experiments/relayboard/evaluator/S02_OPERATOR_ORACLE_V0_1.json']
    checks['fixture_download_complete_exact_base'] = len(D['fixture'])==len([p for p in bt if p.startswith('fixtures/relayboard/')]) and all(blob(v['content'])==v['sha']==v['expected_sha']==bt[v['path']]==t[v['path']] for v in D['fixture'])
    checks['no_staged_results_preexisting'] = not any(p.startswith(D['prefix']+'results/') or p==D['prefix']+'SCREENING_DECISION.json' for p in t)
    protected=['docs/benchmarks/SCORING_V0.md','docs/benchmarks/EVALUATOR_PROTOCOL_V0.md','docs/approaches/FIRST_MODE_V0.md']
    checks['frozen_protocol_scoring_first_mode_match_base'] = all(t[p]==bt[p] for p in protected)
    checks['continuation_thresholds_unchanged'] = c['continuation_rule']['mechanism_qualifies_if']==['surfaced_decisions >= valid_M0_surfaced + 2','silent_assumptions <= valid_M0_silent - 2']
    result={'status':'PASS' if all(checks.values()) else 'FAIL','checked_at_utc':now(),'head':D['head'],'refs_before':D['refs'],'checks':checks,'passed':sum(checks.values()),'total':len(checks),'contestants_started':0,'runtime_identity_attestation':'unknown','procedural_isolation':True,'hard_secrecy_claimed':False,'stage2_execution_authorized_by_user':False}
    dump(CONTROL/'evidence/preflight-verification.json',result)
    (CONTROL/'frozen_evaluator.py').write_bytes(D['evaluator']['content'].encode('utf-8'))
    print(json.dumps(result,indent=2)); assert result['status']=='PASS'
def prepare(run_id):
    order=D['cohort']['stage1']['order']; r=next(v for v in order if v['run_id']==run_id)
    path=WORK/f"contestant-{r['position']:02d}"
    if path.exists(): raise RuntimeError('Workspace already exists; no silent retry')
    path.mkdir()
    for v in D['fixture']:
        p=path/v['path'].removeprefix('fixtures/relayboard/'); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(v['content'].encode('utf-8'))
    (path/'TASK.md').write_bytes(D['task']['content'].encode('utf-8'))
    if r['arm']!='M0': (path/'METHOD.md').write_bytes(D['methods'][r['arm']]['content'].encode('utf-8'))
    git(['-c','init.templateDir=','init','--initial-branch=contestant'],path)
    for key,value in [('user.name','RelayBoard Contestant'),('user.email','contestant@example.invalid'),('core.autocrlf','false')]: git(['config',key,value],path)
    (path/'.git/info').mkdir(exist_ok=True)
    (path/'.git/info/exclude').write_text('__pycache__/\n*.pyc\n.pytest_cache/\n',encoding='utf-8')
    git(['add','--all'],path);git(['commit','-m','Prepared assigned workspace'],path)
    s={'run_id':run_id,'arm':r['arm'],'position':r['position'],'prepared_at_utc':now(),'workspace':str(path),'frozen_fixture_base':D['cohort']['base_sha'],'local_base_commit':git(['rev-parse','HEAD'],path),'local_base_tree':git(['rev-parse','HEAD^{tree}'],path),'independent_history':True,'remotes':git(['remote','-v'],path),'task_blob':blob((path/'TASK.md').read_bytes()),'method_blob':None if r['arm']=='M0' else blob((path/'METHOD.md').read_bytes()),'fixture_blobs_verified':all(blob((path/v['path'].removeprefix('fixtures/relayboard/')).read_bytes())==v['sha'] for v in D['fixture']),'model_requested':D['cohort']['model_request'],'runtime_identity_attested':None}
    dump(CONTROL/f'results/{run_id}/start.json',s); print(json.dumps(s,indent=2))
def freeze(run_id):
    result=CONTROL/'results'/run_id; start=json.loads((result/'start.json').read_text()); path=Path(start['workspace'])
    if (result/'frozen.json').exists(): raise RuntimeError('Already frozen')
    status=git(['status','--porcelain'],path)
    if status: raise RuntimeError('Contestant left uncommitted work: '+status)
    sha=git(['rev-parse','HEAD'],path);tree=git(['rev-parse','HEAD^{tree}'],path)
    files=git(['ls-files'],path).splitlines(); candidate={f:base64.b64encode((path/f).read_bytes()).decode() for f in files}
    dump(result/'candidate-files.json',{'encoding':'base64','files':candidate})
    diff=command(['git','diff','--binary',start['local_base_commit'],'HEAD'],path)['stdout'];(result/'candidate-diff.patch').write_bytes(diff.encode())
    bundle=result/'local-history.bundle';git(['bundle','create',str(bundle),'--all'],path)
    (result/'local-history.bundle.b64').write_text(base64.b64encode(bundle.read_bytes()).decode()+'\n',encoding='ascii')
    check={'frozen_at_utc':now(),'run_id':run_id,'candidate_sha':sha,'candidate_tree':tree,'clean':not status,'commits_after_base':int(git(['rev-list','--count',start['local_base_commit']+'..HEAD'],path)),'diff_numstat':git(['diff','--numstat',start['local_base_commit'],'HEAD'],path),'task_unchanged':blob((path/'TASK.md').read_bytes())==D['cohort']['task']['blob'],'method_unchanged':not (path/'METHOD.md').exists() if start['arm']=='M0' else blob((path/'METHOD.md').read_bytes())==D['cohort']['methods'][start['arm']]['blob'],'public_test_blob_unchanged':blob((path/'tests/test_public.py').read_bytes())==next(v['sha'] for v in D['fixture'] if v['path']=='fixtures/relayboard/tests/test_public.py'),'bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),'tracked_files':files}
    dump(result/'frozen.json',check); print(json.dumps(check,indent=2))
def evaluate(run_id):
    result=CONTROL/'results'/run_id; frozen=json.loads((result/'frozen.json').read_text()); start=json.loads((result/'start.json').read_text()); path=CONTROL/'evaluation'/run_id
    path.parent.mkdir(exist_ok=True)
    if path.exists(): raise RuntimeError('Evaluation snapshot already exists; inspect before any repeat')
    command(['git','clone',str(result/'local-history.bundle'),str(path)],CONTROL)
    assert git(['rev-parse','HEAD'],path)==frozen['candidate_sha']
    assert blob((CONTROL/'frozen_evaluator.py').read_bytes())==D['cohort']['evaluator_blob']
    began=now(); public=command([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],path,False)
    code="import importlib.util,json,sys; p=sys.argv[1]; s=importlib.util.spec_from_file_location('frozen_eval',p); m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m); r=m.evaluate_s02(); print(json.dumps({'scenario':r.scenario,'passed':r.passed,'failures':r.failures})); sys.exit(0 if r.passed else 1)"
    hidden=command([sys.executable,'-B','-c',code,str(CONTROL/'frozen_evaluator.py')],path,False)
    for name,obj in [('public-tests.json',public),('frozen-evaluator-output.json',hidden)]: dump(result/name,obj)
    ev={'run_id':run_id,'candidate_sha':frozen['candidate_sha'],'candidate_tree':frozen['candidate_tree'],'evaluation_started_at_utc':began,'evaluation_finished_at_utc':now(),'evaluator_blob':D['cohort']['evaluator_blob'],'public_pass':public['returncode']==0,'evaluator_pass':hidden['returncode']==0,'frozen_evaluator_result':json.loads(hidden['stdout']) if hidden['stdout'].strip().startswith('{') else None,'candidate_unchanged_after_evaluation':git(['rev-parse','HEAD'],path)==frozen['candidate_sha'] and not git(['status','--porcelain'],path),'hidden_feedback_to_same_contestant':False}
    dump(result/'evaluation.json',ev);print(json.dumps(ev,indent=2))
if __name__=='__main__':
    {'preflight':preflight,'prepare':prepare,'freeze':freeze,'evaluate':evaluate}[sys.argv[1]](*sys.argv[2:])
