# EXP-0017 Orchestrator Handoff

Role: **orchestrator, not contestant**

Repository: `firstzasz/first-agent-engineering-lab`
Branch: `research/exp0017-transfer-screen`

## Goal

Execute an economical transfer screen for vendor-neutral requirement-discovery mechanisms.

This experiment does **not** modify FIRST-mode and does not test Matt/pstack/FIRST as whole systems.

Read first:
- `experiments/relayboard/transfer-screen-v0/COHORT.json`
- `experiments/relayboard/transfer-screen-v0/EXECUTION_ORDER.json`
- `experiments/relayboard/transfer-screen-v0/batch.json`
- `experiments/relayboard/transfer-screen-v0/SCORING_TRANSFER_V0.md`
- `experiments/relayboard/transfer-screen-v0/PRE_RUN_AUDIT.json`

## Stage 1 only on first task

Execute the four RD-C1-v0 runs serially in the frozen order from EXECUTION_ORDER.json.

For every contestant:
1. fresh `fork_turns=none` context;
2. request GPT-6.1 Sol / High where supported;
3. independent workspace from RelayBoard Pilot Start State v0.1 `2b2e67cb2de2e72e442bffc9fe4b5d7790c1ee4f`;
4. deliver only:
   - the exact task blob for the assigned scenario;
   - the scenario public feature test;
   - exact assigned METHOD.md for G1/G2/G3;
   - no METHOD.md for G0;
5. do not deliver scenario benchmark docs, oracle, evaluator, reference patch, EXP-0014/15/16 conclusions, other treatment packets or peer outcomes;
6. normal workspace facts may be investigated by the contestant;
7. operator answers only genuinely asked PRODUCT_OR_PREFERENCE decisions from the frozen scenario oracle;
8. do not volunteer unasked decisions;
9. record FACT and REVERSIBLE_ENGINEERING escalations as burden without supplying product guidance;
10. preserve available questions, classifications, answers, checkpoints, tests, commits and diffs;
11. terminate contestant and same-run helpers before hidden evaluation;
12. independently rerun existing public tests + scenario public feature test + frozen transfer evaluator;
13. never feed hidden evaluator results back to the same contestant;
14. persist exact disposition;
15. no silent retry of contamination or host failure;
16. no merge to main.

After all four C1 dispositions:
- mechanically apply the frozen Stage-1 selection rule from COHORT.json;
- persist `SCREENING_DECISION.json` with arithmetic;
- STOP if no mechanism qualifies and no ceiling rule applies;
- if Stage 2 is authorized, persist the exact authorized C2 run IDs before launching any C2 contestant.

If Stage 2 runs:
- execute only filtered authorized C2 runs in the frozen relative order;
- after completion, apply the frozen multi-scenario signal rule;
- label qualifying mechanisms only `REPLICATION_ELIGIBLE`.

No result creates FIRST-mode v1, a FIRST skill, or a FIRST workflow. FIRST adoption requires a separate user-approved design later.
