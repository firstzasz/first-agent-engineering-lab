from pathlib import Path
import datetime,json
p=Path('.experiment')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
records=[json.loads(line) for line in p.joinpath('commands.jsonl').read_text().splitlines()]
missing=[r['output_path'] for r in records if not Path(r['output_path']).is_file()]
assert not missing, missing
public=[]
for r in records:
 if r['argv'][:3] == ['python','-m','unittest'] or r['output_path'] in ['.experiment/lead-api-surface.log','.experiment/review-preexisting-history.log']:
  item=dict(r)
  label=Path(item['output_path']).stem
  item['wrapper_invocation']=['python','.experiment/run_command.py',label,'--']+item['argv']
  public.append(item)
report={
 'task':'P-S02-001','treatment':'pstack-codex-port-v0','declared_status':'completed, public verification passed, fresh serial review accepted',
 'workspace':str(Path.cwd()),'initial_commit':'6621c8b2f3618b35dc6f0c784acf51f44fa053e8',
 'local_commits':[{'sha':'087535a1e0b0ddf43cf4e9e843f76c297d6bce66','role':'tests-first public behavior specification'},{'sha':'b04219d12bf6e1d60782a75e354bac273a7168bd','role':'verified implementation'}],
 'evidence_commit':'The local commit containing this REPORT.json; its exact SHA is recorded after creation in finalization.log and the final handoff. This file cannot contain its own enclosing commit SHA.',
 'finalization_commands':['git add .experiment','git commit -m "chore: preserve pause feature method and public evidence"','git rev-parse HEAD','git status --short'],
 'finalization_output_path':'.experiment/finalization.log','finalization_note':'Post-commit output log is intentionally retained as an untracked local artifact; implementation and pre-finalization evidence are committed.',
 'feature':{'state_shape':'independent Job.paused bool default False, persisted in SQLite, Store is single writer','routes':['POST /api/jobs/{id}/pause','POST /api/jobs/{id}/resume'],'behavior':'200 Job envelopes; paused blocks normal scheduled admission through existing 409; manual Runs and existing Run/Attempt/retry/alert behavior retained; enabled unchanged; dashboard appends Paused','compatibility':'additive legacy jobs schema migration, tested including genuinely preexisting Run/Attempt/Alert history'},
 'source_version':'cursor/plugins pstack df581122cde17e6e27686b5a448bde23e4ad4318',
 'method_routes':['Poteto Mode','Feature','How serial lead explainer','Architect two serial structural lead sketches with bundled rationale/red flags','Arena read; native fan-out/cross-model replaced by METHOD serial lead design synthesis','Show me your work append-only decisions and fresh same-model trail review','Laziness Protocol','Model the Domain','Prove It Works','Test Behavior Not Implementation','Sequence Work into Verifiable Units','Never Block on the Human','Fix Root Causes read; applied to reproduced exact-route issue only','TDD read but feature route uses red-before evidence without claiming bug TDD invocation'],
 'method_sources_and_adaptations_path':'.experiment/sources.json',
 'throughput_checkpoint_path':'.experiment/throughput.md','design_path':'.experiment/design.md','checklist_path':'.experiment/TODO.md',
 'public_commands_results_and_output_paths':public,'all_captured_commands_path':'.experiment/commands.jsonl','command_snapshot_note':'Canonical command log includes later evidence/finalization actions; this report snapshots checks through generation time.',
 'verification':{'baseline':'5 existing public tests pass','failing_before':'10 focused feature tests produce 7 failures and 3 errors on unchanged production baseline','passing_after':'10 focused pause tests and all 15 public tests pass independently for lead','original_surface':'literal WSGI pause 200, scheduled 409, manual 201, resume 200, scheduled 201','additional_review_check':'genuinely preexisting legacy Run/Attempt/Alert history survives migration','diff_check':'exit0 scoped git diff --check','upstream_changes':'none, empty recorded diff'},
 'helpers':[{'task':'/root/contestant_p_s02_001/pause_implementation','status':'finished','role':'bounded code-writing helper','fork_turns':'none','requested_model':'gpt-6.1-sol','requested_reasoning':'high','observed_identity':'unknown','report':'.experiment/helper-implementation-report.md','descendants':False},{'task':'/root/contestant_p_s02_001/pause_review','status':'finished','role':'fresh code and evidence reviewer','fork_turns':'none','requested_model':'gpt-6.1-sol','requested_reasoning':'high','observed_identity':'unknown','report':'.experiment/helper-review-report.md','descendants':False}],
 'helper_assignments_path':'.experiment/helper-assignments.jsonl',
 'operator_interactions_path':'.experiment/operator-interactions.jsonl','operator_decisions':'Manual Runs remain allowed; existing Runs continue including current retry/alerts; representation/dashboard chosen under preservation requirement','open_product_decisions':[],
 'action_path_logs':['.experiment/initial-actions.json','.experiment/lead-direct-actions.json','.experiment/sources.json','.experiment/commands.jsonl','.experiment/decisions.tsv','.experiment/helper-assignments.jsonl','.experiment/helper-implementation-report.md','.experiment/helper-review-report.md'],
 'review_verdict':'accept with no code blocker; evidence-only flags corrected','attention_path':'.experiment/ATTENTION.md',
 'attention_remaining':['Initial direct calls reconstructed rather than fully command-archived','Early inline Python input source not archived','No complete raw transcript exported','Observed model identity and usage metrics unknown','Existing read-then-create scheduling admission not atomic across concurrent connections'],
 'boundary':{'evaluator_material_accessed':False,'oracle_reference_material_accessed':False,'peer_other_run_material_accessed':False,'deliberate_hidden_material_retrieval':False,'external_network_or_remote_git':False,'credentials_accessed':False,'production_or_paid_API_accessed':False,'deployed_or_merged_to_main':False,'basis':'Lead and helper declarations plus available captured command/path evidence; unavailable full transcript is not independently attested'},
 'attestation':{'lead_requested_model':'gpt-6.1-sol','lead_requested_reasoning':'high','lead_observed_model':'unknown','helpers_observed_models':'unknown','full_raw_transcript':'unavailable','token_usage':'unknown','cost':'unknown','wall_time_usage_metrics':'unknown','native_model_diversity':False,'native_Cursor_pstack_execution':False,'native_parallel_throughput':False},
 'created_at':now
}
p.joinpath('REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
with p.joinpath('decisions.tsv').open('a') as f:
 f.write('\t'.join([now,'handoff','Freeze completed feature with public evidence and declared limits','Both serial helpers finished; review found no code blocker','.experiment/REPORT.json; .experiment/ATTENTION.md','Ready for local evidence commit; no hidden checks'])+'\n')
with p.joinpath('operator-interactions.jsonl').open('a') as f:
 f.write(json.dumps({'direction':'incoming','source':'/root','message':'Orchestration checkpoint request: preserve current status, public verification and fresh-review findings in your run evidence, and send a concise checkpoint. Continue the assigned method to completion; do not run hidden checks. No new product guidance is supplied.'})+'\n')
 f.write(json.dumps({'direction':'outgoing','target':'/root','message':'P-S02-001 checkpoint. Code candidate b04219d12bf6e1d60782a75e354bac273a7168bd follows tests-first commit 087535a1e0b0ddf43cf4e9e843f76c297d6bce66. Lead independently passes 10 focused pause tests, all 15 public tests, literal WSGI pause/resume/manual/scheduled scenario, and diff check. Fresh serial GPT-6.1 Sol High reviewer finished and accepted with no code blocker; additional genuine preexisting legacy Run/Attempt/Alert migration check passed. Evidence-only TODO/provenance/pointer flags corrected append-only. Both helpers finished. Remaining disclosed limits are early capture gaps, no full raw transcript, unknown observed identity/usage, and existing concurrent admission limitation. Final REPORT.json/evidence commit underway. No hidden/peer material or remote/network operation.'})+'\n')
print('REPORT.json written; all existing captured command output paths resolve. Both helpers finished. Public verification and fresh review accepted.')
