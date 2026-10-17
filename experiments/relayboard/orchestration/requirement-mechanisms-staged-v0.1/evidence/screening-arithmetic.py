import json
from runtime import CONTROL, D, dump, now

order=D['cohort']['stage1']['order']
persisted=json.loads((CONTROL/'persistence.json').read_text())
assert set(persisted)=={r['run_id'] for r in order} and all(len(v)==40 for v in persisted.values())
results={x['arm']:json.loads((CONTROL/'results'/x['run_id']/'run.json').read_text()) for x in order}
def valid(r):
    return r['protocol_valid'] and r['disposition'] not in ['CONTAMINATED','INVALID_HOST_FAILURE']
m0=results['M0']; baseline_valid=valid(m0)
arms={}
for arm in ['M1','M2','M3']:
    r=results[arm]
    if not baseline_valid:
        arms[arm]={'screening':'INCONCLUSIVE_INVALID_M0','qualifies':False,'continuation_eligible':False,'arithmetic':None}
    elif not valid(r):
        arms[arm]={'screening':'INCONCLUSIVE_MECHANISM','qualifies':False,'continuation_eligible':True,'arithmetic':None}
    else:
        surfaced=r['product_decisions_surfaced_of_4']; silent=r['silent_product_assumptions_of_4']; bs=m0['product_decisions_surfaced_of_4']; ba=m0['silent_product_assumptions_of_4']
        first=surfaced>=bs+2; second=silent<=ba-2; q=first or second
        arms[arm]={'screening':'QUALIFIES_FOR_REPLICATION' if q else 'NOT_SELECTED_BY_SCREEN','qualifies':q,'continuation_eligible':q,'arithmetic':{'surfaced':surfaced,'M0_surfaced':bs,'surfaced_threshold':bs+2,'surfaced_difference':surfaced-bs,'surfaced_threshold_met':first,'silent':silent,'M0_silent':ba,'silent_threshold':ba-2,'silent_reduction':ba-silent,'silent_threshold_met':second,'combine':'OR'},'FACT_LOOKUP_burden':r['FACT_LOOKUP_questions'],'public_acceptance':r['public_acceptance'],'frozen_evaluator_acceptance':r['frozen_evaluator_acceptance']}
selected=[a for a in arms if arms[a]['continuation_eligible']]
eligible=[r['run_id'] for r in D['cohort']['stage2']['global_order'] if selected and (r['arm']=='M0' or r['arm'] in selected)] if baseline_valid else []
status='STOP_INCONCLUSIVE_REDESIGN' if not baseline_valid else ('SCREEN_CONTINUE_ELIGIBLE_AWAITING_SEPARATE_AUTHORIZATION' if selected else 'SCREEN_STOP_NO_STRONG_SIGNAL')
decision={'schema_version':1,'experiment':'EXP-0014','execution_variant':'staged-screening-v0.1','stage':1,'created_at_utc':now(),'frozen_protocol_commit':D['head'],'stage1_all_four_dispositions_durable':True,'stage1_persistence_commits':json.loads((CONTROL/'persistence.json').read_text()),'stage1_order':[r['run_id'] for r in order],'status':status,'M0':{'valid':baseline_valid,'run_id':m0['run_id'],'surfaced':m0['product_decisions_surfaced_of_4'],'silent':m0['silent_product_assumptions_of_4'],'FACT_LOOKUP_burden':m0['FACT_LOOKUP_questions'],'public_acceptance':m0['public_acceptance'],'frozen_evaluator_acceptance':m0['frozen_evaluator_acceptance']},'arms':arms,'continuation_eligible_mechanism_arms':selected,'protocol_authorized_stage2_run_ids_if_separately_requested':eligible,'authorized_stage2_run_ids':eligible,'stage2_execution_authorized_by_user':False,'stage2_launched':False,'stage2_runs_started':0,'stop_reason':'User explicitly scoped this task to Stage 1 and screening persistence only. Protocol eligibility does not authorize launching Stage 2 in this task.','transfer_eligible':False,'automatic_first_adoption':False,'first_mode_modified':False,'interpretation':'One-run exploratory screen; not a confirmatory test, no proof of no effect for unselected arms, and no transfer or production adoption claim.'}
if status=='SCREEN_STOP_NO_STRONG_SIGNAL':
    decision['stop_reason']='No mechanism met either frozen continuation threshold against valid M0; stop the cohort under STAGED_PROTOCOL.md. The user also explicitly prohibited Stage 2 execution in this task.'
dump(CONTROL/'SCREENING_DECISION.json',decision)
batch=json.loads(D['batch']['content'])
for item in batch['stage1_runs']:
    r=results[item['arm']];item['status']=r['disposition'];item['result']='results/'+r['run_id']+'/run.json'
for item in batch['stage2_runs']:
    item['status']='ELIGIBLE_NOT_LAUNCHED_AWAITING_USER_AUTHORIZATION' if item['run_id'] in eligible else 'NOT_SELECTED_BY_STAGE1_SCREEN'
batch.update(status=status,completed_count=sum(r['disposition'].startswith('COMPLETED_') for r in results.values()),excluded_count=sum(not r['disposition'].startswith('COMPLETED_') for r in results.values()),stage1_disposition_count=4,stage2_started_count=0,screening_decision='SCREENING_DECISION.json',stage2_execution_authorized_by_user=False)
dump(CONTROL/'final-batch.json',batch)
dump(CONTROL/'profiles.json',[results[x['arm']] for x in order])
print(json.dumps(decision,indent=2))
