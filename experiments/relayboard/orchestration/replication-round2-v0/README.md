# Benchmark Replication Round 2

Status: **COMPLETED — 12/12 dispositions; 11 evaluated PASS, 0 evaluated FAIL, 1 excluded host failure.**

[Cross-round report](./cross-round-report.md) · [Profiles](./profiles.json) · [Metrics](./cross-round-metrics.json) · [Final audit](./final-audit.json) · [Resume state](./resume-status.json)

| Fixed order | Run | Treatment | Final disposition | Evidence |
| --- | --- | --- | --- | --- |
| 1 | F-S04-002 | first-mode-v0 | COMPLETED_EVALUATED_PASS | [record](./results/F-S04-002/run.json) |
| 2 | F-S02-002 | first-mode-v0 | COMPLETED_EVALUATED_PASS | [record](./results/F-S02-002/run.json) |
| 3 | F-S01-002 | first-mode-v0 | COMPLETED_EVALUATED_PASS | [record](./results/F-S01-002/run.json) |
| 4 | M-S04-002 | matt-codex-port-v0 | COMPLETED_EVALUATED_PASS | [record](./results/M-S04-002/run.json) |
| 5 | M-S02-002 | matt-codex-port-v0 | COMPLETED_EVALUATED_PASS | [record](./results/M-S02-002/run.json) |
| 6 | M-S01-002 | matt-codex-port-v0 | COMPLETED_EVALUATED_PASS | [record](./results/M-S01-002/run.json) |
| 7 | P-S04-002 | pstack-codex-port-v0 | COMPLETED_EVALUATED_PASS | [record](./results/P-S04-002/run.json) |
| 8 | P-S02-002 | pstack-codex-port-v0 | INVALID_HOST_FAILURE | [record](./results/P-S02-002/run.json) |
| 9 | P-S01-002 | pstack-codex-port-v0 | COMPLETED_EVALUATED_PASS | [record](./results/P-S01-002/run.json) |
| 10 | N-S04-002 | neutral-v0 | COMPLETED_EVALUATED_PASS | [record](./results/N-S04-002/run.json) |
| 11 | N-S02-002 | neutral-v0 | COMPLETED_EVALUATED_PASS | [record](./results/N-S02-002/run.json) |
| 12 | N-S01-002 | neutral-v0 | COMPLETED_EVALUATED_PASS | [record](./results/N-S01-002/run.json) |

P-S02-002 remains INVALID_HOST_FAILURE, excluded without retry. Its valid prepared start, one operator exchange and two visible checkpoints remain archived; no frozen final candidate or independently verified acceptance exists. All four originally remaining runs completed in the requested order: P-S01-002, N-S04-002, N-S02-002, N-S01-002. There is no next contestant.

The exact reverse Round 1 order was frozen before the first contestant at b9c7da1e8cb797f49d86e46b229d21e9493b483f. Every run retains Pilot Start State v0.1 at 2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f and unchanged task, protocol, scoring, evaluator/oracles and methodology bundles. Matt and pstack are unchanged non-native Codex ports reused from their pre-outcome freeze.

Fresh contestants and required serial helpers requested GPT-6.1 Sol / High, fork_turns=none, assigned-only packets and independent local histories with no lab remote. Runtime identity remains independently unverified. Isolation was procedural, with broad tools/shared filesystem technically available; preserved action/path evidence and declarations do not constitute an exhaustive access audit.

All eligible contexts completed before candidate freeze. Exact local/remote trees match. Public tests and the frozen evaluator ran separately after termination. No hidden result was returned to a same-run contestant. Available questions, answers, checkpoints, candidate diffs, history bundles, public/hidden outputs and helper evidence are durable. Archived local contestant/evaluator material was removed before subsequent delivery. Candidate PRs remain draft, target only their treatment branches, and are not merged.

The comparison reports ten valid matched acceptance pairs, S01 overhead stability and variability, S02 discovery stability and variability, S04 debugging replication, incidents, hypotheses and unsupported conclusions. It declares no aggregate score or universal winner. Wall time includes host/operator/archival delays; exhaustive raw traces, tokens/cost and attested identity remain unknown.

Original Round 1 evidence and branch are unchanged. All Round 2 research remains on research/batch-orchestration-round2; nothing merges to main.
