# EXP-0014 Orchestrator Handoff

Role: **orchestrator, not contestant**

Repository: `firstzasz/first-agent-engineering-lab`

Branch: `research/exp0014-requirement-mechanisms`

## Goal

Execute the already frozen EXP-0014 requirement-discovery mechanism cohort without changing its treatments, run order, thresholds, benchmark inputs, or FIRST-mode.

Read first:

- `experiments/relayboard/orchestration/requirement-mechanisms-v0/README.md`
- `experiments/relayboard/orchestration/requirement-mechanisms-v0/COHORT.json`
- `experiments/relayboard/orchestration/requirement-mechanisms-v0/batch.json`
- `experiments/relayboard/orchestration/requirement-mechanisms-v0/EXECUTION_ORDER.json`
- `experiments/relayboard/orchestration/requirement-mechanisms-v0/PRE_RUN_AUDIT.json`
- all `experiments/relayboard/orchestration/requirement-mechanisms-v0/runs/*.json`

Require the pre-run audit to be PASS before the first contestant.

## Frozen treatments

- M0 / rd-neutral-v0: no METHOD.md is delivered.
- M1 / rd-authority-v0: deliver the exact frozen M1 blob as METHOD.md.
- M2 / rd-frontier-v0: deliver the exact frozen M2 blob as METHOD.md.
- M3 / rd-authority-frontier-v0: deliver the exact frozen M3 blob as METHOD.md.

Do not substitute FIRST-mode, Matt skills, pstack, summaries of those systems, or an improved version of any mechanism.

Do not modify a treatment after any cohort outcome is observed.

## Execution

Run all 12 entries **serially and exactly in EXECUTION_ORDER.json**.

For every run:

1. Start a fresh contestant context with `fork_turns=none`.
2. Request GPT-6.1 Sol / High where supported; record requested versus actually attested identity separately.
3. Construct a clean independent-history workspace from the RelayBoard fixture tree at Pilot Start State v0.1 `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`.
4. Deliver only the exact frozen task and the assigned method, if any.
5. Do not deliver lab Git history, Round 1/2 results, peer cohort results, evaluator files, operator oracle, reference solutions, comparison reports, or treatment-aware analysis.
6. Normal procedural-isolation rules from Evaluator Protocol v0 apply. Broad public tools may be technically available; forbidden-information receipt contaminates the run.
7. The operator answers only genuinely asked PRODUCT_OR_PREFERENCE decisions from the frozen S02-v0.1 oracle. Do not volunteer unasked requirements. FACT and REVERSIBLE_ENGINEERING questions receive no product guidance and are recorded as burden.
8. Preserve available questions, classifications, answers, checkpoints, command/test evidence, commits, diffs, and process artifacts.
9. When the contestant and same-run helpers finish, terminate them and freeze the exact candidate.
10. Independently rerun public tests and the unchanged frozen evaluator blob `3aaaa9924f09ba18a5888d94373a9edc04187926`.
11. Never return hidden evaluator feedback to the same contestant.
12. Persist the result under `experiments/relayboard/orchestration/requirement-mechanisms-v0/results/<run_id>/` and update batch state.
13. Candidate PRs, if used, must be draft and target dedicated treatment branches. Never merge to main.

If a run becomes CONTAMINATED or suffers unrecoverable host failure, preserve and exclude it. Do not silently retry or replace it.

## Required measurement

For every valid run record:

- product decisions surfaced / 4;
- silent assumptions / 4;
- FACT_LOOKUP questions;
- REVERSIBLE_ENGINEERING_CHOICE questions;
- PRODUCT_OR_PREFERENCE exchanges;
- public acceptance;
- frozen evaluator acceptance;
- helper count;
- visible checkpoints;
- production/test diff;
- process/evidence footprint where observable;
- wall-clock observation with host-delay caveat;
- unavailable metrics explicitly null/unknown.

Correctness and requirement discovery remain separate.

## Final analysis

After all 12 dispositions:

- build a machine-readable profile table;
- report per-arm distributions, medians and individual runs;
- apply the predeclared **transfer gate** from COHORT.json;
- compare M1 vs M0, M2 vs M0, M3 vs M2 and M3 vs M1 descriptively;
- distinguish observation, repeated signal, hypothesis and unsupported conclusion;
- do not tune mechanisms retroactively;
- do not declare a universal workflow winner;
- do not create or modify FIRST-mode v1.

A treatment that passes the transfer gate is only **eligible for a new-task transfer experiment**. It is not adopted into FIRST.

Persist a final audit proving frozen inputs, run order, candidate/result refs, main, Round 1, Round 2 and FIRST_MODE_V0.md remained unchanged.

Proceed autonomously on reversible research work. Stop only for a genuine security/cost/access/frozen-protocol blocker.
