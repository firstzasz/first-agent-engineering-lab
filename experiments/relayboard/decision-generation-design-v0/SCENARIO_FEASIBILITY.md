# Transfer Scenario Feasibility v0

Status: DESIGN-GATE ANALYSIS

Date: 2026-10-18

## Purpose

Choose transfer scenarios for requirement-discovery mechanism experiments without overfitting to S02 or mixing unrelated fixture defects into the score.

## RD-C1 Cancel Run

Decision-shape diversity:
- Run terminal-state transition;
- terminal-vs-running behavior;
- alert semantics;
- dashboard summary semantics;
- repeated-command/idempotence semantics.

Evaluator seam: **GOOD**

Prototype reference semantics used only for feasibility:
- cancelling running Run succeeds;
- cancelled Run rejects later Attempts;
- terminal succeeded/failed Run cannot be cancelled;
- cancellation itself emits no failure Alert;
- cancelled is a dashboard last result;
- repeated cancel is idempotent success.

Executable local prototype:
- existing public regression checks: 5/5 PASS;
- C1 semantic checks: 5/5 PASS;
- combined: 10/10 PASS.

Assessment: **SELECT FOR HARNESS IMPLEMENTATION**

## RD-C2 Archive Job

Decision-shape diversity:
- Job lifecycle/visibility;
- API addressability while hidden;
- scheduled/manual availability;
- existing Run continuity;
- state restoration.

Evaluator seam: **GOOD**

Prototype reference semantics used only for feasibility:
- archived Jobs hidden from normal listing/dashboard;
- archived Job blocks scheduled Runs;
- archived Job blocks manual Runs;
- already-running Run continues;
- restore preserves prior enabled/disabled state.

Executable local prototype:
- first prototype failed one pre-existing public regression check because failure-alert behavior had been accidentally stubbed;
- this was treated as a harness/reference defect, not hidden;
- reference prototype was corrected to preserve original alert behavior;
- corrected existing public regression checks: 5/5 PASS;
- C2 semantic checks: 4/4 PASS;
- corrected combined: 9/9 PASS.

Assessment: **SELECT FOR HARNESS IMPLEMENTATION**

The caught regression is useful design evidence: reference solutions must prove preservation of unrelated behavior, not merely satisfy new hidden semantics.

## RD-C3 Retry Policy Update

Decision-shape diversity:
- temporal configuration;
- snapshot/live policy semantics;
- existing-vs-future Run boundary;
- lowering/raising policy mid-run.

Evaluator seam: **CONDITIONAL**

Risk:
- the Pilot Start State intentionally contains S04's duplicate-alert defect in retry behavior;
- a retry-policy evaluator could accidentally score the known alert defect, or require a different corrected fixture base;
- that would complicate attribution and starting-state comparability.

Assessment: **DEFER FROM FIRST TRANSFER COHORT**

RD-C3 remains valuable for a later cohort after a clean versioned fixture base or a demonstrably isolated evaluator seam exists.

## Selection

First transfer-harness implementation will target:

1. RD-C1 Cancel Run
2. RD-C2 Archive Job

They differ meaningfully from each other and from S02 while remaining implementable on the current synthetic fixture.

## Evidence status

The prototype executions were local design checks, not frozen benchmark runs and not CI-attested repository harness evidence.

Therefore:

- scenario feasibility: IMPLEMENTED;
- reference semantics: PROVISIONAL;
- runnable benchmark harness: NOT YET VERIFIED;
- contestant execution: NOT STARTED.

The next gate is to implement durable public tests, hidden evaluator cases, oracle files, reference solutions, red-capability selftests and green reference selftests in the repository before freezing any G0-G3 cohort.
