import base64
from datetime import datetime,timezone
import json
from runtime import CONTROL,D,dump,blob,now

rb=json.loads((CONTROL/'readback.json').read_text());remote={x['path']:x['sha'] for x in rb['tree']['tree'] if x['type']=='blob'};original={x['path']:x['sha'] for x in D['tree']['tree'] if x['type']=='blob'}
checks={};drift=[p for p,s in original.items() if p!=D['prefix']+'batch.json' and remote.get(p)!=s]
checks['all_original_files_except_mutable_batch_unchanged']=not drift
checks['protected_refs_unchanged']=D['refs']==rb['refs']
artifact_drift=[];results=[];records=[]
for x in D['order']['stage1']:
    p=CONTROL/'results'/x['run_id'];r=json.loads((p/'run.json').read_text());results.append(r);s=json.loads((p/'start.json').read_text());f=json.loads((p/'frozen.json').read_text());ev=json.loads((p/'evaluation.json').read_text())
    for v in p.iterdir():
        if v.is_file() and v.suffix!='.bundle':
            key=D['prefix']+'results/'+x['run_id']+'/'+v.name
            if remote.get(key)!=blob(v.read_text(encoding='utf-8')):artifact_drift.append(key)
    files=json.loads((p/'candidate-files.json').read_text())['files'];public=next(v['sha'] for v in D['fixture'] if v['path']=='fixtures/relayboard/tests/test_public.py')
    packet=blob(base64.b64decode(files['TASK.md']))==D['task']['sha'] and blob(base64.b64decode(files['tests/test_public_feature.py']))==D['feature']['sha'] and blob(base64.b64decode(files['tests/test_public.py']))==public
    packet &= ('METHOD.md' not in files if x['arm']=='G0' else blob(base64.b64decode(files['METHOD.md']))==D['methods'][x['arm']]['sha'])
    checks[x['run_id']+'_immutable_packet_and_public_tests']=packet
    checks[x['run_id']+'_exact_candidate_independent_evaluation']=ev['candidate_sha']==f['candidate_sha']==r['candidate_sha'] and ev['candidate_tree']==f['candidate_tree']==r['candidate_tree'] and ev['candidate_unchanged_after_evaluation'] and ev['evaluator_blob']==D['cohort']['evaluator']['blob']
    checks[x['run_id']+'_record_matches_acceptance']=r['correctness_pass']==(ev['public_base_pass'] and ev['public_feature_pass'] and ev['evaluator_pass'])
    checks[x['run_id']+'_fixture_only_independent_start']=s['fixture_blobs_verified'] and s['independent_history'] and not s['remotes']
    records.append({'run_id':x['run_id'],'disposition':r['disposition'],'candidate_sha':r['candidate_sha'],'candidate_tree':r['candidate_tree'],'result_blob':remote.get(D['prefix']+'results/'+x['run_id']+'/run.json'),'persistence_commit':json.loads((CONTROL/'persistence.json').read_text())[x['run_id']]})
checks['all_candidate_and_result_artifacts_readback_match']=not artifact_drift
def instant(s):return datetime.strptime(s,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc) if s.endswith(' UTC') else datetime.fromisoformat(s)
checks['freeze_only_after_contestant_completion_before_evaluation']=all(instant(r['completion_observed_at_utc'])<instant(r['frozen_at_utc'])<instant(r['evaluation_started_at_utc'])<instant(r['evaluation_finished_at_utc']) for r in results)
checks['serial_frozen_order_without_overlap']=[r['run_id'] for r in results]==[r['run_id'] for r in D['order']['stage1']] and all(instant(results[i]['evaluation_finished_at_utc'])<instant(results[i+1]['prepared_at_utc']) for i in range(3))
checks['no_hidden_feedback_or_retries']=all(not r['hidden_feedback_to_same_contestant'] and r['retries']==0 and r['helper_count']==0 for r in results)
checks['only_four_stage1_results']=not any(p.startswith(D['prefix']+'results/') and not any(p.startswith(D['prefix']+'results/'+r['run_id']+'/') for r in results) for p in remote)
screen=json.loads((CONTROL/'SCREENING_DECISION.json').read_text());checks['screening_readback_matches']=remote.get(D['prefix']+'SCREENING_DECISION.json')==blob((CONTROL/'SCREENING_DECISION.json').read_text())
batch=json.loads((CONTROL/'final-batch.json').read_text())
checks['mutable_batch_preserves_frozen_order_and_digests']=all([{k:r[k] for k in ['position','run_id','scenario','arm','digest']} for r in batch[bk]]==D['order'][ok] for bk,ok in [('stage1_runs','stage1'),('stage2_runs','stage2_possible')])
checks['mutable_batch_readback_matches']=remote.get(D['prefix']+'batch.json')==blob((CONTROL/'final-batch.json').read_text())
checks['no_stage2_execution']=screen['stage2_runs_started']==0 and not screen['stage2_execution_authorized_by_user'] and not screen['stage2_launched']
out={'experiment':'EXP-0017','audited_at_utc':now(),'audited_commit':rb['head'],'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'passed':sum(checks.values()),'total':len(checks),'frozen_file_drift':drift,'artifact_drift':artifact_drift,'stage1_results':records,'refs_after':rb['refs'],'stage2_started_count':0,'main_merge_performed':False,'runtime_requested':{'fork_turns':'none','model':'gpt-6.1-sol','reasoning_effort':'high','serial':True},'runtime_identity_attested':None,'limitations':['Procedural isolation; no exhaustive raw tool or filesystem-access trace.','Single observation per arm, not causal or generalization proof.']}
dump(CONTROL/'FINAL_AUDIT.json',out);print(json.dumps(out,indent=2));assert out['status']=='PASS'
