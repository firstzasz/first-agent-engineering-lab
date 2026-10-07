(()=>{
const q=load("active_queue");
const profiles=q.runs.filter(x=>/COMPLETED|CONTAMINATED|INVALID|ERROR/.test(x.status)).map(x=>{
const r=load("result:"+x.run_id),c=load("capture:"+x.run_id);
const production=[];let current=null;
for(const line of (c.diff||"").split("\n")){
if(line.startsWith("diff --git ")){const m=line.match(/^diff --git a\/(.+) b\/(.+)$/);current=m&&/^(relayboard\/|tests\/|GLOSSARY\.md$)/.test(m[2])?{path:m[2],added:0,removed:0}:null;if(current)production.push(current);}
else if(current&&line.startsWith("+")&&!line.startsWith("+++"))current.added++;
else if(current&&line.startsWith("-")&&!line.startsWith("---"))current.removed++;
}
let elicitation=null;
if(r.scenario==="S02-v0.1"){
const surfaced=new Set();for(const e of r.operator_interactions){for(const d of (e.frozen_decisions_answered||e.product_decisions_answered||[]))surfaced.add(d);}
elicitation={frozen_product_decisions_surfaced:surfaced.size,total:4,silent_assumptions:4-surfaced.size,basis:"Unique requested/answered frozen product semantics. Frozen rubric counts unasked oracle guesses as silent assumptions; correctness is separate.",exchanges:r.operator_interactions};
}
return {run_id:r.run_id,treatment:r.treatment,scenario:r.scenario,status:r.status,included:r.contamination.included_in_outcome_comparison,correctness:{public:r.public_tests.passed,evaluator:r.hidden_evaluation.passed,hidden_case_count:"unknown; frozen evaluator returns aggregate acceptance/failures"},verification:{basis:"Inspectable public test outputs and separate frozen evaluator where eligible; assigned-method fresh reviews preserved where performed.",subjective_blind_learning_score:null,subjective_review_note:"Not assigned by treatment-aware orchestrator."},requirement_discovery:elicitation,observable_overhead:{local_commit_count_including_start_and_evidence:c.local_commits.length,candidate_file_count:c.files.length,all_diff_stat:c.diff_stat,production_and_test_line_changes:production,visible_checkpoints:r.visible_checkpoints?.length||0,operator_exchange_count:r.operator_interactions.length,start_at:r.start.prepared_at,frozen_at:r.candidate_frozen_at,wall_clock_seconds:(Date.parse(r.candidate_frozen_at)-Date.parse(r.start.prepared_at))/1000,wall_clock_note:"Preparation-to-freeze wall time includes host, operator and archival delays; not model compute time.",raw_tool_calls:null,tokens:null,cost:null},identity:{requested:r.model_request,observed:r.runtime_model_attestation},evidence_limitations:r.unavailable_metrics,disposition_notes:r.run_id==="P-S04-001"?"Peer-result status exposure; stopped/excluded, hidden evaluation not run.":r.run_id==="M-S02-001"?"Same-arm source filename discovery self-flagged; original preserved and allowlist ruling established no forbidden exposure; same incomplete reviewer resumed.":r.notes};
});
store("generated_profiles",{schema_version:1,scoring_source:"docs/benchmarks/SCORING_V0.md (unchanged frozen rubric)",single_shot:true,native_host_comparison:false,universal_ranking:false,profiles});return profiles.map(r=>({id:r.run_id,status:r.status,elicitation:r.requirement_discovery&&{surfaced:r.requirement_discovery.frozen_product_decisions_surfaced,silent:r.requirement_discovery.silent_assumptions}}));})()
