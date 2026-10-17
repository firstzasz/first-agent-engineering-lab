import json
from pathlib import Path
import sys
from runtime import CONTROL, D, dump, now

run_id=sys.argv[1]
p=CONTROL/'results'/run_id
start=json.loads((p/'start.json').read_text())
frozen=json.loads((p/'frozen.json').read_text())
ev=json.loads((p/'evaluation.json').read_text())
completion=json.loads((p/'completion.json').read_text())
exchanges=json.loads((p/'operator-exchanges.json').read_text())
checkpoints=json.loads((p/'checkpoints.json').read_text())
oracle=json.loads(D['oracle']['content'])
surfaced=sorted(set(k for e in exchanges for k in e['frozen_decisions_answered']))
assert set(surfaced)<=set(oracle['answers'])
silent=sorted(set(oracle['answers'])-set(surfaced))
facts=sum(x['classification']=='FACT_LOOKUP' for e in exchanges for x in e.get('other_items',[]))
engineering=sum(x['classification']=='REVERSIBLE_ENGINEERING_CHOICE' for e in exchanges for x in e.get('other_items',[]))
assert completion['contestant_finished'] and completion['helpers_count']==0 and completion['termination_observed_before_freeze']
assert frozen['task_unchanged'] and frozen['method_unchanged'] and ev['candidate_unchanged_after_evaluation']
assert not completion['forbidden_receipt_reported']
r={'schema_version':1,'experiment':'EXP-0014','execution_variant':'staged-screening-v0.1','stage':1,'run_id':run_id,'arm':start['arm'],'position':start['position'],'disposition':'COMPLETED_EVALUATED_PASS' if ev['public_pass'] and ev['evaluator_pass'] else 'COMPLETED_EVALUATED_FAIL','protocol_valid':True,'candidate_sha':frozen['candidate_sha'],'candidate_tree':frozen['candidate_tree'],'candidate_history':'local-history.bundle.b64','prepared_base_sha':start['local_base_commit'],'frozen_fixture_base':start['frozen_fixture_base'],'task_blob':start['task_blob'],'method_blob':start['method_blob'],'model_requested':start['model_requested'],'runtime_identity_attested':None,'isolation':'procedural; assigned workspace only; no hard secrecy claim','product_decisions_surfaced_of_4':len(surfaced),'surfaced_decisions':surfaced,'silent_product_assumptions_of_4':len(silent),'silent_assumptions':silent,'FACT_LOOKUP_questions':facts,'REVERSIBLE_ENGINEERING_CHOICE_questions':engineering,'PRODUCT_OR_PREFERENCE_DECISION_items':len(surfaced),'PRODUCT_OR_PREFERENCE_DECISION_exchanges':sum(bool(e['frozen_decisions_answered']) for e in exchanges),'operator_exchanges_total':len(exchanges),'public_acceptance':'PASS' if ev['public_pass'] else 'FAIL','frozen_evaluator_acceptance':'PASS' if ev['evaluator_pass'] else 'FAIL','helper_count':0,'visible_checkpoints_observed':len(checkpoints),'commits_after_base':frozen['commits_after_base'],'diff_numstat':frozen['diff_numstat'],'tool_calls':None,'tokens':None,'cost':None,'prepared_at_utc':start['prepared_at_utc'],'completion_observed_at_utc':completion['observed_at_utc'],'frozen_at_utc':frozen['frozen_at_utc'],'evaluation_started_at_utc':ev['evaluation_started_at_utc'],'evaluation_finished_at_utc':ev['evaluation_finished_at_utc'],'recorded_at_utc':now(),'hidden_feedback_to_same_contestant':False,'contamination_reported':False,'retries':0,'limits':['Raw host/tool execution trace unavailable; public test and evaluator subprocess outputs retained independently.','Model and reasoning are requested configuration, not independently attested runtime identity.','Wall-clock observations include host and operator delay; no speed/cost inference.','Single-run screening observation; no causal or transfer claim.']}
dump(p/'run.json',r)
print(json.dumps(r,indent=2))
