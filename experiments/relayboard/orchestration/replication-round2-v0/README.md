# Benchmark Replication Round 2

Status: RUNNING; 2/12 dispositions. 2 public/evaluator PASS, 0 FAIL, 0 excluded. New independent replication, never a retry of Round 1.

| Fixed order | Run | Treatment | Status | Evidence |
| --- | --- | --- | --- | --- |
| 1 | F-S04-002 | first-mode-v0 | COMPLETED_EVALUATED_PASS | [record](./results/F-S04-002/run.json) |
| 2 | F-S02-002 | first-mode-v0 | COMPLETED_EVALUATED_PASS | [record](./results/F-S02-002/run.json) |
| 3 | F-S01-002 | first-mode-v0 | RUNNING | pending |
| 4 | M-S04-002 | matt-codex-port-v0 | READY_PROCEDURAL | pending |
| 5 | M-S02-002 | matt-codex-port-v0 | READY_PROCEDURAL | pending |
| 6 | M-S01-002 | matt-codex-port-v0 | READY_PROCEDURAL | pending |
| 7 | P-S04-002 | pstack-codex-port-v0 | READY_PROCEDURAL | pending |
| 8 | P-S02-002 | pstack-codex-port-v0 | READY_PROCEDURAL | pending |
| 9 | P-S01-002 | pstack-codex-port-v0 | READY_PROCEDURAL | pending |
| 10 | N-S04-002 | neutral-v0 | READY_PROCEDURAL | pending |
| 11 | N-S02-002 | neutral-v0 | READY_PROCEDURAL | pending |
| 12 | N-S01-002 | neutral-v0 | READY_PROCEDURAL | pending |

The exact reverse of Round 1's chronological order was reconstructed using per-run preparation/freeze timestamps and N-S01-001's earlier independent CI. It was frozen before the first contestant at b9c7da1e8cb797f49d86e46b229d21e9493b483f. See execution-order.json. Order never changes after outcomes.

All twelve runs start from Pilot Start State v0.1, 2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f, with the unchanged frozen task, scoring, evaluator, oracles and methods. Byte-identical pstack-codex-port-v0 and matt-codex-port-v0 bundles are reused from Round 1's pre-outcome freeze, not regenerated or improved. These are non-native Codex ports. FIRST receives exact FIRST_MODE_V0.md as METHOD.md; Neutral uses normal host behavior.

Every lead/helper requests GPT-6.1 Sol / High and fresh fork_turns=none context. Serial contestants and helpers use independent local histories/areas, assigned-only fixture/task/method packets, no lab remote or prior/peer/hidden delivery. Broad tools/shared filesystem remain technically available; any accidental or deliberate forbidden-information exposure contaminates/excludes that run, preserving evidence without silent rerun. Status queries are scoped to the same run's prefix.

The operator answers only genuinely asked frozen S02 product decisions. Facts/reversible choices receive no extra product guidance. After all same-run agents terminate, freeze the exact candidate, verify the GitHub tree, run public tests and the unchanged frozen evaluator separately. No hidden failure is returned to the contestant. Contaminated candidates are archived without hidden evaluation.

Per-run records preserve available checkpoints, operator exchanges, candidate diff, local Git bundle, requested versus unverified identity, public/hidden outputs and action/path evidence. profiles.json distinguishes surfaced/4 versus silent assumptions/4 and production/test changes versus process/evidence footprint. Wall-clock timestamps include host/operator/archival delays, not model compute time. Exhaustive raw tool traces, independently attested runtime identity/reasoning, tokens/cost and some original N-S01 metrics remain unknown.

All Round 2 research is on research/batch-orchestration-round2; new -002 candidate draft PRs target only their own treatment branches. Nothing merges to main. Original Round 1 branch and result/evidence files remain unchanged. Cross-round comparison follows all twelve dispositions, without an aggregate methodology winner. Resume exact pending order from batch.json; never silently replace a completed/contaminated run.
