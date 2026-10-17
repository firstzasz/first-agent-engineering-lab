import json
from runtime import CONTROL,D,dump,now

order=D['order']['stage1'];persisted=json.loads((CONTROL/'persistence.json').read_text())
assert set(persisted)=={r['run_id'] for r in order} and all(len(v)==40 for v in persisted.values())
results={r['arm']:json.loads((CONTROL/'results'/r['run_id']/'run.json').read_text()) for r in order}
def valid(r):return r['protocol_valid'] and r['disposition'] not in ['CONTAMINATED','INVALID_HOST_FAILURE']
g0=results['G0'];baseline_valid=valid(g0);ceiling=baseline_valid and g0['product_decisions_surfaced_of_4']==4 and g0['silent_product_assumptions_of_4']==0
arms={}
for arm in ['G1','G2','G3']:
    r=results[arm];protocol_valid=valid(r);correct=r['correctness_pass'];fact_limit=g0['FACT_LOOKUP_items']+1;fact_ok=r['FACT_LOOKUP_items']<=fact_limit
    complete=r['product_decisions_surfaced_of_4']==4 and r['silent_product_assumptions_of_4']==0 and not ceiling
    surfaced_ok=r['product_decisions_surfaced_of_4']>=g0['product_decisions_surfaced_of_4']+2
    silent_ok=r['silent_product_assumptions_of_4']<=g0['silent_product_assumptions_of_4']-2
    qualifies=baseline_valid and protocol_valid and correct and fact_ok and (complete or surfaced_ok or silent_ok)
    eligible=baseline_valid and protocol_valid and ((ceiling and correct and fact_ok) or qualifies)
    label='INCONCLUSIVE_INVALID_G0' if not baseline_valid else ('EXCLUDED_INVALID_MECHANISM' if not protocol_valid else ('CEILING_CONTINUATION_ELIGIBLE' if ceiling and eligible else ('QUALIFIES_FOR_C2_SCREEN' if qualifies else 'NOT_SELECTED_BY_SCREEN')))
    arms[arm]={'run_id':r['run_id'],'protocol_valid':protocol_valid,'correctness_pass':correct,'FACT_LOOKUP_items':r['FACT_LOOKUP_items'],'fact_burden_limit_G0_plus_1':fact_limit,'fact_burden_guard_pass':fact_ok,'arithmetic':{'surfaced':r['product_decisions_surfaced_of_4'],'silent':r['silent_product_assumptions_of_4'],'G0_surfaced':g0['product_decisions_surfaced_of_4'],'G0_silent':g0['silent_product_assumptions_of_4'],'complete_where_G0_incomplete':complete,'surfaced_threshold':g0['product_decisions_surfaced_of_4']+2,'surfaced_difference':r['product_decisions_surfaced_of_4']-g0['product_decisions_surfaced_of_4'],'surfaced_threshold_met':surfaced_ok,'silent_threshold':g0['silent_product_assumptions_of_4']-2,'silent_reduction':g0['silent_product_assumptions_of_4']-r['silent_product_assumptions_of_4'],'silent_threshold_met':silent_ok,'discovery_thresholds_combine':'OR'},'qualifies_by_discovery_rule':qualifies,'ceiling_rule_applies':ceiling,'continuation_eligible':eligible,'screening':label,'public_base_acceptance':r['public_base_acceptance'],'public_feature_acceptance':r['public_feature_acceptance'],'frozen_evaluator_acceptance':r['frozen_evaluator_acceptance']}
selected=[a for a in arms if arms[a]['continuation_eligible']]
eligible_runs=[r['run_id'] for r in D['order']['stage2_possible'] if selected and (r['arm']=='G0' or r['arm'] in selected)] if baseline_valid else []
status='STOP_INCONCLUSIVE_REDESIGN' if not baseline_valid else ('STAGE1_CEILING_C2_SCREEN_ELIGIBLE' if ceiling else ('STAGE1_SIGNAL_C2_SCREEN_ELIGIBLE' if selected else 'SCREEN_STOP_NO_STRONG_SIGNAL'))
decision={'schema_version':1,'experiment':'EXP-0017','stage':1,'created_at_utc':now(),'frozen_protocol_commit':D['head'],'stage1_order':[r['run_id'] for r in order],'all_four_stage1_dispositions_durable':True,'stage1_persistence_commits':persisted,'status':status,'G0':{'run_id':g0['run_id'],'protocol_valid':baseline_valid,'correctness_pass':g0['correctness_pass'],'surfaced':g0['product_decisions_surfaced_of_4'],'silent':g0['silent_product_assumptions_of_4'],'FACT_LOOKUP_items':g0['FACT_LOOKUP_items'],'public_base_acceptance':g0['public_base_acceptance'],'public_feature_acceptance':g0['public_feature_acceptance'],'frozen_evaluator_acceptance':g0['frozen_evaluator_acceptance']},'ceiling_rule_applies':ceiling,'arms':arms,'continuation_eligible_mechanism_arms':selected,'authorized_stage2_run_ids':eligible_runs,'stage2_execution_authorized_by_user':False,'stage2_runs_started':0,'stage2_launched':False,'task_stop_reason':'User limited execution to Stage 1 and durable screening decision; no C2 contestant may be launched in this task.','cohort_stop_reason':'No qualifying mechanism against valid incomplete G0.' if status=='SCREEN_STOP_NO_STRONG_SIGNAL' else None,'multi_scenario_signal_evaluated':False,'replication_eligible':False,'automatic_first_adoption':False,'first_mode_modified':False,'interpretation':'One-shot screening; C2 eligibility is not evidence of cross-scenario transfer, causal proof, or FIRST adoption.'}
dump(CONTROL/'SCREENING_DECISION.json',decision);dump(CONTROL/'profiles.json',[results[r['arm']] for r in order])
b=json.loads(D['batch']['content'])
for item in b['stage1_runs']:
    r=results[item['arm']];item.update(status=r['disposition'],result='results/'+r['run_id']+'/run.json')
for item in b['stage2_runs']:item['status']='PROTOCOL_ELIGIBLE_NOT_LAUNCHED' if item['run_id'] in eligible_runs else 'NOT_SELECTED_BY_STAGE1_SCREEN'
b.update(status=status,completed_count=sum(r['disposition'].startswith('COMPLETED_') for r in results.values()),excluded_count=sum(not r['disposition'].startswith('COMPLETED_') for r in results.values()),stage1_disposition_count=4,stage2_started_count=0,screening_decision='SCREENING_DECISION.json',stage2_execution_authorized_by_user=False)
dump(CONTROL/'final-batch.json',b);print(json.dumps(decision,indent=2))
