from pathlib import Path
import datetime,json
p=Path('.experiment')
with p.joinpath('helper-assignments.jsonl').open('a') as f:
 f.write(json.dumps({'task':'/root/contestant_p_s02_001/pause_review','role':'fresh scoped code/evidence reviewer','fork_turns':'none','requested_model':'gpt-6.1-sol','requested_reasoning':'high','observed_identity':'unknown, no independent runtime attestation','workspace':str(Path.cwd()),'scope':'Read assigned task/method, local candidate code/tests, lead design and audit evidence. Write review report under .experiment only. No code mutations, no descendants, no external/forbidden material. Audit correctness and evidence limitations; full prompt exists in visible collaboration call, no exported raw transcript.'})+'\n')
initial=json.loads(p.joinpath('initial-actions.json').read_text())
initial['commands'][2]['command']="cat upstream/pstack/skills/poteto-mode/SKILL.md && rg --files upstream/pstack && rg --files -g '!upstream/**' -g '!.git/**'"
initial['commands'][2]['result']='core mode read; assigned bundle and application paths listed'
initial['commands'][3]['command']='cat upstream/pstack/skills/poteto-mode/playbooks/feature.md upstream/pstack/skills/how/SKILL.md upstream/pstack/skills/architect/SKILL.md upstream/pstack/skills/architect/references/design-red-flags.md upstream/pstack/skills/architect/references/rationale-template.md upstream/pstack/skills/show-me-your-work/SKILL.md upstream/pstack/skills/principle-{laziness-protocol,model-the-domain,prove-it-works,fix-root-causes,test-behavior-not-implementation,sequence-verifiable-units,never-block-on-the-human}/SKILL.md'
p.joinpath('initial-actions.json').write_text(json.dumps(initial,indent=2)+'\n')
p.joinpath('lead-direct-actions.json').write_text(json.dumps({'note':'Available direct command/action log reconstructed from lead visible tool calls; raw shell stdin before runner archive unavailable. All cwd values assigned root.', 'cwd':str(Path.cwd()),'actions':[
{'command':'mkdir -p .experiment && python - [stdin]','purpose':'Create runner, initial record, sources manifest, TSV and copied playbook TODO','output':'success with no output','raw_stdin_archived':False},
{'command':'python - [stdin]','purpose':'Write grounding/design/throughput and record operator reply','output':'success with no output','raw_stdin_archived':False},
{'command':'python - [stdin]','purpose':'Correct paths-read manifest and record first helper assignment','output':'success with no output','raw_stdin_archived':False},
{'command':'git status --short && rg --files .experiment','purpose':'Read-only helper progress check','output':'only untracked experiment records; no production changes then','dedicated_output':None},
{'command':'tail -n 6 .experiment/commands.jsonl && git status --short','purpose':'Observe focused-before failure and tests-only commit','output':'red check exit1, tests commit; experiment records untracked','dedicated_output':None},
{'command':'python - [stdin]','purpose':'Enhance run_command.py to archive forthcoming python stdin scripts','output':'success with no output','raw_stdin_archived':False},
{'command':'tail -n 5 .experiment/commands.jsonl','purpose':'Read final helper public checks and review progress','output':'focused/full/diff public checks passed','dedicated_output':None}
]},indent=2)+'\n')
