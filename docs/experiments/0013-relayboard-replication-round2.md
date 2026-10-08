# EXP-0013: RelayBoard Benchmark Replication Round 2

Date: 2026-10-08
Status: IMPLEMENTED and VERIFIED within the frozen deterministic fixture and procedural-isolation limits.

## Hypothesis and setup

Repeated fresh-context executions may reproduce scenario-specific behavior seen in Round 1. This is an independent twelve-cell cohort, with exact reverse order frozen before outcomes, Pilot Start State v0.1, unchanged scoring/evaluator and pre-outcome methodology bundles. No aggregate winner was prespecified or assigned.

## Result and evidence

All twelve dispositions are durable: eleven public/evaluator PASS runs and P-S02-002 INVALID_HOST_FAILURE, excluded without retry. P-S01-002, N-S04-002, N-S02-002 and N-S01-002 completed the resumed fixed order. All eleven candidate PRs remain draft and unmerged.

[Cross-round report](../../experiments/relayboard/orchestration/replication-round2-v0/cross-round-report.md), [profiles](../../experiments/relayboard/orchestration/replication-round2-v0/profiles.json), [metrics](../../experiments/relayboard/orchestration/replication-round2-v0/cross-round-metrics.json) and [audit](../../experiments/relayboard/orchestration/replication-round2-v0/final-audit.json) are the durable evidence.

Ten valid matched pairs passed acceptance in both rounds. S01 application scope and method-arm helper structure repeated, while artifact counts and relative port footprint varied. Matt surfaced all four S02 semantics in both rounds; FIRST went 3→2 and Neutral 0→3. Pstack S02 has no complete valid pair. FIRST/Matt/Neutral reproduced the S04 mechanism with valid red/green checks; contaminated P-S04-001 prevents a matched pstack debugging claim.

## Incidents and limitations

Round 1 P-S04-001 was contaminated by peer-status output and remains excluded. Round 2 P-S02-002 lost host contexts/history and has only partial process evidence; it was not restarted. Other archived provenance/write-scope incidents did not establish forbidden-information receipt.

Two single-shot rounds, procedural isolation, missing original Neutral S01 overhead, unknown runtime identity/usage and unequal evidence packaging limit causal and statistical inference. Wall time is not model compute time. No universal, native-host, speed/cost, guaranteed-discovery or production-quality conclusion follows.

## Recommendation

Retain all results/exclusions. Declare any new repeated-run or mechanism-isolation cohort before outcomes, improve trace/identity capture and independent review, and keep frozen pilot inputs unchanged. No production integration or main merge was performed.
