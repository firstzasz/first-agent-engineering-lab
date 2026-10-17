import base64
from datetime import datetime, timezone
import hashlib
import json
from runtime import CONTROL, D, dump, blob, now

readback=json.loads((CONTROL/'readback.json').read_text())
remote={x['path']:x['sha'] for x in readback['tree']['tree'] if x['type']=='blob'}
original={x['path']:x['sha'] for x in D['tree']['tree'] if x['type']=='blob'}
order=D['cohort']['stage1']['order'];results=[];records=[];checks={}
drift=[p for p,s in original.items() if p!=D['prefix']+'batch.json' and remote.get(p)!=s]
checks['all_original_files_except_mutable_batch_unchanged']=not drift
checks['protected_refs_unchanged']=D['refs']==readback['refs']
artifact_drift=[]
for x in order:
    p=CONTROL/'results'/x['run_id'];r=json.loads((p/'run.json').read_text());results.append(r)
    for f in p.iterdir():
        if f.is_file() and f.suffix!='.bundle':
            key=D['prefix']+'results/'+x['run_id']+'/'+f.name
            if remote.get(key)!=blob(f.read_text(encoding='utf-8')): artifact_drift.append(key)
    files=json.loads((p/'candidate-files.json').read_text())['files']
    fixture_public=next(v['sha'] for v in D['fixture'] if v['path']=='fixtures/relayboard/tests/test_public.py')
    public_unchanged=blob(base64.b64decode(files['tests/test_public.py']))==fixture_public
    task_unchanged=blob(base64.b64decode(files['TASK.md']))==D['cohort']['task']['blob']
    method_unchanged='METHOD.md' not in files if x['arm']=='M0' else blob(base64.b64decode(files['METHOD.md']))==D['cohort']['methods'][x['arm']]['blob']
    f=json.loads((p/'frozen.json').read_text());ev=json.loads((p/'evaluation.json').read_text())
    checks[x['run_id']+'_immutable_packet_and_public_tests']=task_unchanged and method_unchanged and public_unchanged
    checks[x['run_id']+'_independent_accepted_evaluation']=ev['public_pass'] and ev['evaluator_pass'] and ev['candidate_sha']==f['candidate_sha']==r['candidate_sha'] and ev['candidate_tree']==f['candidate_tree']==r['candidate_tree'] and ev['candidate_unchanged_after_evaluation']
    records.append({'run_id':x['run_id'],'candidate_sha':r['candidate_sha'],'candidate_tree':r['candidate_tree'],'disposition':r['disposition'],'result_blob':remote.get(D['prefix']+'results/'+x['run_id']+'/run.json'),'persisted_at_commit':json.loads((CONTROL/'persistence.json').read_text())[x['run_id']]})
checks['all_result_artifacts_readback_match']=not artifact_drift
checks['four_dispositions_only']=len(results)==4 and [r['run_id'] for r in results]==[x['run_id'] for x in order] and all(r['stage']==1 for r in results)
def instant(s):
    return datetime.strptime(s,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc) if s.endswith(' UTC') else datetime.fromisoformat(s)
checks['freeze_after_completed_context_before_evaluation']=all(instant(r['completion_observed_at_utc'])<instant(r['frozen_at_utc'])<instant(r['evaluation_started_at_utc'])<instant(r['evaluation_finished_at_utc']) for r in results)
checks['serial_frozen_order_without_overlap']=all(instant(results[i]['evaluation_finished_at_utc'])<instant(results[i+1]['prepared_at_utc']) for i in range(3))
checks['no_hidden_feedback_or_retries']=all(not r['hidden_feedback_to_same_contestant'] and not r['retries'] and r['helper_count']==0 for r in results)
checks['no_stage2_result_files']=not any(p.startswith(D['prefix']+'results/') and not any(p.startswith(D['prefix']+'results/'+r['run_id']+'/') for r in results) for p in remote)
screen=json.loads((CONTROL/'SCREENING_DECISION.json').read_text())
checks['screening_readback_matches']=remote.get(D['prefix']+'SCREENING_DECISION.json')==blob((CONTROL/'SCREENING_DECISION.json').read_text())
checks['no_stage2_launched']=screen['stage2_runs_started']==0 and not screen['stage2_execution_authorized_by_user'] and not screen['stage2_launched']
audit={'schema_version':1,'experiment':'EXP-0014','execution_variant':'staged-screening-v0.1','audited_at_utc':now(),'audited_commit':readback['head'],'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'passed':sum(checks.values()),'total':len(checks),'frozen_file_drift':drift,'artifact_drift':artifact_drift,'stage1_results':records,'refs_after':readback['refs'],'main_merge_performed':False,'stage2_started_count':0,'requested_contexts':{'fork_turns':'none','model':'gpt-6.1-sol','reasoning_effort':'high','serial':True,'same_run_helpers':0},'runtime_identity_attestation':'unknown','limitations':['Procedural isolation; no exhaustive filesystem or raw tool-access trace.','Requested runtime identity and reasoning not independently attested.','Single observation per arm; screening only.']}
dump(CONTROL/'FINAL_AUDIT.json',audit)
print(json.dumps(audit,indent=2));assert audit['status']=='PASS'
