# Procedural remaining batch v0

Status: RUNNING. 6/11 dispositions preserved: 5 public/evaluator PASS, 0 FAIL, 1 excluded. N-S01-001 remains independently verified, untouched and outside this batch.

| Treatment | S01 | S02 | S04 |
| --- | --- | --- | --- |
| Neutral | [Prior verified run](../../runs/neutral/N-S01-001.json) | [PASS](./results/N-S02-001/run.json) | [PASS](./results/N-S04-001/run.json) |
| pstack-codex-port-v0 | [PASS](./results/P-S01-001/run.json) | [PASS](./results/P-S02-001/run.json) | [CONTAMINATED](./results/P-S04-001/run.json) |
| matt-codex-port-v0 | [PASS](./results/M-S01-001/run.json) | [RUNNING](./results/M-S02-001/run.json) | [READY_PROCEDURAL](./results/M-S04-001/run.json) |
| FIRST-mode v0 | [READY_PROCEDURAL](./results/F-S01-001/run.json) | [READY_PROCEDURAL](./results/F-S02-001/run.json) | [READY_PROCEDURAL](./results/F-S04-001/run.json) |

This control plane supersedes the historical hard-access gate without modifying Frozen Evaluator Protocol v0. That prior gate exceeded the frozen public-repository protocol. Synthetic clean and deliberate-contamination controls passed; all synthetic material was removed before real delivery. See evidence/procedural-pilot.json and the correction record.

All runs start from Pilot Start State v0.1 fixture SHA 2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f. Dedicated areas contain only the frozen fixture, selected exact task, assigned method/source bundle and minimal run metadata. Local history begins independently, without a lab remote. Contestants and same-run helpers run serially in fresh fork_turns=none contexts with requested GPT-6.1 Sol / High. Broad inherited public tools remain technically accessible; no hard-secrecy claim is made.

The explicit non-native pstack and Matt Codex ports were frozen at 311871987a48a072e36f434e199b1cb28563c81b before outcomes. Exact pinned sources, licenses and semantic losses are in ../codex-ports-v0/. These are not native Cursor/pstack or native Matt-host executions. FIRST uses exact frozen FIRST_MODE_V0.md; Neutral uses normal host behavior.

P-S04-001 reported accidental peer-result exposure through an unscoped collaboration.list_agents call. It stopped, its helper terminated, and files/history/incident were preserved as CONTAMINATED. It is excluded, not silently rerun; hidden evaluation was skipped. Subsequent contexts receive an explicit identical own-run-only status-query clarification. See results/P-S04-001/contamination-incident.json and evidence/status-scope-clarification.json.

Eligible candidates freeze after contestants and helpers terminate. Their exact local tree is checked against the GitHub candidate tree before separate orchestrator-owned evaluation with frozen evaluator blob 3aaaa9924f09ba18a5888d94373a9edc04187926. Evaluator material is never placed in contestant areas and is removed before the next delivery. No hidden feedback returns to a run. Candidate draft PRs target only their treatment branches; nothing merges to main.

Per-run records preserve packet hashes, requested/observed identity, operator exchanges, available command/path/test logs, local commit metadata, exact Git history bundle and frozen public/hidden outputs. Separate local source-copy/archive incidents were caught by hashes and retained: N-S02 evaluator trailing-newline copy, P-S02 tool output limit, P-S04 CRLF evidence-copy normalization. Corrected archival/evaluation copies did not retry contestants or change frozen inputs.

Passing behavior is separate from elicitation: Neutral S02 surfaced 0/4 frozen product decisions, pstack S02 2/4; the frozen rubric counts remaining oracle guesses as silent assumptions. See profiles.json when finalized. No aggregate methodology winner or stable model effect is inferred from single-shot runs. Blind subjective rationale scores are not assigned here.

The interface does not export exhaustive raw host tool transcripts, independently attested runtime model/reasoning or token usage. Available evidence supports procedural boundaries and observed dispositions; NO_EVIDENCE_OBSERVED is not proof of technical inaccessibility or absence of invisible access.

Resume from batch.json and per-run start/result files, not historical batch-v0.1. runtime.py and the functions.exec recipes are the orchestration host binding; reconstruct delivery from exact prepared branch trees if needed. Never rerun a completed or contaminated run silently.
