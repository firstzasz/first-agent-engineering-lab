import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

CONTROL=Path(__file__).resolve().parent
WORK=CONTROL.parent
D=json.loads((CONTROL/'input.json').read_text(encoding='utf-8'))
def now(): return datetime.now(timezone.utc).isoformat()
def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def blob(content):
    raw=content.encode('utf-8') if isinstance(content,str) else content
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def command(args,cwd,check=True):
    env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='NUL',PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,encoding='utf-8',errors='replace')
    r={'command':args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    if check and p.returncode: raise RuntimeError(json.dumps(r))
    return r
def git(args,cwd): return command(['git']+args,cwd)['stdout'].strip()
def preflight():
    t={x['path']:x['sha'] for x in D['tree']['tree']};bt={x['path']:x['sha'] for x in D['base_tree']['tree']}
    c=D['cohort'];a=D['audit'];fr=D['readback'];b=json.loads(D['batch']['content']);checks={}
    checks['expected_head']=D['head']=='ad1ecf32eb6248d764a44157422257c330595f44'
    checks['frozen_audit_and_readback']=a['status']=='PASS' and all(a['checks'].values()) and fr['status']=='VERIFIED_PRE_RUN_FREEZE' and fr['contestant_runs_started']==fr['results_present']==0 and fr['stage1_authorized'] and not fr['stage2_authorized']
    expected=['DG-C1-G2-001','DG-C1-G1-001','DG-C1-G0-001','DG-C1-G3-001']
    checks['exact_stage1_order']=expected==[r['run_id'] for r in D['order']['stage1']]==[r['run_id'] for r in c['stage1']['runs']]==[r['run_id'] for r in b['stage1_runs']]==a['stage1_order']==fr['stage1_order']
    checks['stage2_order_frozen']=D['order']['stage2_possible']==c['stage2']['possible_runs'] and [r['run_id'] for r in b['stage2_runs']]==a['stage2_possible_order']
    checks['orders_sha256_recomputed']=True
    for key in ['stage1','stage2_possible']:
        rows=D['order'][key];digests=[hashlib.sha256(f"EXP-0017|transfer-screen-v0|{r['scenario'].split('-')[1]}-{r['arm']}".encode()).hexdigest() for r in rows]
        checks['orders_sha256_recomputed'] &= digests==[r['digest'] for r in rows] and digests==sorted(digests)
    checks['batch_not_started']=b['status']=='STAGE1_READY_NOT_STARTED' and b['completed_count']==b['excluded_count']==0 and all(r['status']=='READY' for r in b['stage1_runs']) and all(r['status']=='CONDITIONAL_NOT_AUTHORIZED' for r in b['stage2_runs'])
    checks['downloaded_control_docs_match_blobs']=all(blob(v['content'])==v['sha']==t[D['prefix']+k] for k,v in D['docs'].items()) and blob(D['batch']['content'])==D['batch']['sha']==a['frozen_blobs']['batch']
    pins=[(c['scoring']['path'],c['scoring']['blob']),(c['evaluator']['path'],c['evaluator']['blob'])]
    for short,sc in [('C1',c['scenarios']['RD-C1-v0']),('C2',c['scenarios']['RD-C2-v0'])]:
        for key in ['task','public_test','oracle']: pins.append((sc[key]['path'],sc[key]['blob']))
    pins += [(v['method']['path'],v['method']['blob']) for v in c['arms'].values() if v.get('method')]
    checks['all_frozen_packet_pins_match_tree']=all(t[p]==s for p,s in pins)
    checks['downloaded_task_feature_methods_evaluator_oracle_exact']=all(blob(v['content'])==v['sha'] for v in [D['task'],D['feature'],D['evaluator'],D['oracle'],D['scoring'],*D['methods'].values()])
    checks['fixture_tree_matches_frozen_start']=t['fixtures/relayboard']==bt['fixtures/relayboard']==a['frozen_trees']['fixture']
    checks['fixture_bytes_complete_and_exact']=len(D['fixture'])==len([p for p in bt if p.startswith('fixtures/relayboard/') and not any(p==x['path'] and x['type']=='tree' for x in D['base_tree']['tree'])]) and all(blob(v['content'])==v['sha']==v['expected_sha']==bt[v['path']]==t[v['path']] for v in D['fixture'])
    checks['first_mode_unchanged']=t['docs/approaches/FIRST_MODE_V0.md']==bt['docs/approaches/FIRST_MODE_V0.md']==a['frozen_blobs']['FIRST_MODE_V0']
    checks['protected_refs_unchanged']=D['refs']=={'main':a['protected_refs']['main'],'research/batch-orchestration-pilot':a['protected_refs']['round1'],'research/batch-orchestration-round2':a['protected_refs']['round2']}
    checks['eight_manifests_untouched_and_unstarted']=len(D['manifests'])==8
    for m in D['manifests']:
        r=json.loads(m['content']);sc=c['scenarios'][r['scenario']];method=c['arms'][r['arm']].get('method')
        checks['eight_manifests_untouched_and_unstarted'] &= blob(m['content'])==m['sha']==a['manifest_blobs'][r['run_id']] and r['result'] is None and r['status']==('READY' if r['scenario']=='RD-C1-v0' else 'CONDITIONAL_NOT_AUTHORIZED') and r['fixture_base_sha']==c['fixture_base_sha'] and r['packet']['task']['blob']==sc['task']['blob'] and r['packet']['task']['public_blob']==sc['public_test']['blob'] and r['packet']['method']==method and r['evaluation']['evaluator_blob']==c['evaluator']['blob']
    checks['no_existing_results_or_decision']=not any(p.startswith(D['prefix']+'results/') or p==D['prefix']+'SCREENING_DECISION.json' for p in t)
    result={'experiment':'EXP-0017','head':D['head'],'checked_at_utc':now(),'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'passed':sum(checks.values()),'total':len(checks),'refs_before':D['refs'],'contestants_started':0,'stage2_execution_authorized':False,'procedural_isolation':True,'runtime_identity_attestation':None}
    dump(CONTROL/'evidence/preflight-verification.json',result)
    (CONTROL/'frozen_evaluator.py').write_bytes(D['evaluator']['content'].encode())
    print(json.dumps(result,indent=2));assert result['status']=='PASS'
def prepare(run_id):
    r=next(v for v in D['order']['stage1'] if v['run_id']==run_id);path=WORK/f"transfer-contestant-{r['position']:02d}"
    if path.exists(): raise RuntimeError('Workspace exists; no silent retry')
    path.mkdir()
    for v in D['fixture']:
        p=path/v['path'].removeprefix('fixtures/relayboard/');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v['content'].encode())
    (path/'TASK.md').write_bytes(D['task']['content'].encode())
    (path/'tests/test_public_feature.py').write_bytes(D['feature']['content'].encode())
    if r['arm']!='G0': (path/'METHOD.md').write_bytes(D['methods'][r['arm']]['content'].encode())
    git(['-c','init.templateDir=','init','--initial-branch=contestant'],path)
    for k,v in [('user.name','RelayBoard Contestant'),('user.email','contestant@example.invalid'),('core.autocrlf','false')]:git(['config',k,v],path)
    (path/'.git/info').mkdir(exist_ok=True);(path/'.git/info/exclude').write_text('__pycache__/\n*.pyc\n.pytest_cache/\n',encoding='utf-8')
    git(['add','--all'],path);git(['commit','-m','Prepared assigned workspace'],path)
    s={'run_id':run_id,'arm':r['arm'],'scenario':r['scenario'],'position':r['position'],'prepared_at_utc':now(),'workspace':str(path),'frozen_fixture_base':D['cohort']['fixture_base_sha'],'local_base_commit':git(['rev-parse','HEAD'],path),'local_base_tree':git(['rev-parse','HEAD^{tree}'],path),'independent_history':True,'remotes':git(['remote','-v'],path),'task_blob':blob((path/'TASK.md').read_bytes()),'feature_test_blob':blob((path/'tests/test_public_feature.py').read_bytes()),'method_blob':None if r['arm']=='G0' else blob((path/'METHOD.md').read_bytes()),'fixture_blobs_verified':all(blob((path/v['path'].removeprefix('fixtures/relayboard/')).read_bytes())==v['sha'] for v in D['fixture']),'model_requested':D['cohort']['model_request'],'runtime_identity_attested':None}
    dump(CONTROL/f'results/{run_id}/start.json',s);print(json.dumps(s,indent=2))
def freeze(run_id):
    result=CONTROL/'results'/run_id;s=json.loads((result/'start.json').read_text());path=Path(s['workspace'])
    if (result/'frozen.json').exists():raise RuntimeError('Already frozen')
    status=git(['status','--porcelain'],path)
    if status:raise RuntimeError('Uncommitted work: '+status)
    files=git(['ls-files'],path).splitlines();dump(result/'candidate-files.json',{'encoding':'base64','files':{f:base64.b64encode((path/f).read_bytes()).decode() for f in files}})
    (result/'candidate-diff.patch').write_bytes(command(['git','diff','--binary',s['local_base_commit'],'HEAD'],path)['stdout'].encode())
    bundle=result/'local-history.bundle';git(['bundle','create',str(bundle),'--all'],path);(result/'local-history.bundle.b64').write_text(base64.b64encode(bundle.read_bytes()).decode()+'\n',encoding='ascii')
    f={'frozen_at_utc':now(),'run_id':run_id,'candidate_sha':git(['rev-parse','HEAD'],path),'candidate_tree':git(['rev-parse','HEAD^{tree}'],path),'clean':not status,'commits_after_base':int(git(['rev-list','--count',s['local_base_commit']+'..HEAD'],path)),'diff_numstat':git(['diff','--numstat',s['local_base_commit'],'HEAD'],path),'task_unchanged':blob((path/'TASK.md').read_bytes())==s['task_blob'],'method_unchanged':not (path/'METHOD.md').exists() if s['arm']=='G0' else blob((path/'METHOD.md').read_bytes())==s['method_blob'],'public_feature_test_unchanged':blob((path/'tests/test_public_feature.py').read_bytes())==s['feature_test_blob'],'public_base_test_unchanged':blob((path/'tests/test_public.py').read_bytes())==next(v['sha'] for v in D['fixture'] if v['path']=='fixtures/relayboard/tests/test_public.py'),'bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),'tracked_files':files}
    dump(result/'frozen.json',f);print(json.dumps(f,indent=2))
def evaluate(run_id):
    result=CONTROL/'results'/run_id;f=json.loads((result/'frozen.json').read_text());path=CONTROL/'evaluation'/run_id;path.parent.mkdir(exist_ok=True)
    if path.exists():raise RuntimeError('Evaluation snapshot exists')
    command(['git','clone',str(result/'local-history.bundle'),str(path)],CONTROL)
    assert git(['rev-parse','HEAD'],path)==f['candidate_sha']
    assert blob((CONTROL/'frozen_evaluator.py').read_bytes())==D['cohort']['evaluator']['blob']
    began=now()
    outputs={}
    for label,pattern in [('public-base','test_public.py'),('public-feature','test_public_feature.py'),('candidate-suite','test*.py')]:
        outputs[label]=command([sys.executable,'-B','-m','unittest','discover','-s','tests','-p',pattern,'-v'],path,False);dump(result/(label+'-tests.json'),outputs[label])
    hidden=command([sys.executable,'-B',str(CONTROL/'frozen_evaluator.py'),'--scenario','RD-C1-v0','--workspace',str(path)],path,False);dump(result/'frozen-evaluator-output.json',hidden)
    ev={'run_id':run_id,'candidate_sha':f['candidate_sha'],'candidate_tree':f['candidate_tree'],'evaluation_started_at_utc':began,'evaluation_finished_at_utc':now(),'evaluator_blob':D['cohort']['evaluator']['blob'],'public_base_pass':outputs['public-base']['returncode']==0,'public_feature_pass':outputs['public-feature']['returncode']==0,'candidate_suite_pass':outputs['candidate-suite']['returncode']==0,'evaluator_pass':hidden['returncode']==0,'frozen_evaluator_result':json.loads(hidden['stdout']) if hidden['stdout'].strip().startswith('{') else None,'candidate_unchanged_after_evaluation':git(['rev-parse','HEAD'],path)==f['candidate_sha'] and not git(['status','--porcelain'],path),'hidden_feedback_to_same_contestant':False}
    dump(result/'evaluation.json',ev);print(json.dumps(ev,indent=2))
if __name__=='__main__':{'preflight':preflight,'prepare':prepare,'freeze':freeze,'evaluate':evaluate}[sys.argv[1]](*sys.argv[2:])
