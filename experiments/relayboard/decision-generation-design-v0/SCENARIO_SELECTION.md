# EXP-0016 Scenario Selection Decision

Date: 2026-10-18
Status: SELECTED FOR HARNESS IMPLEMENTATION; no contestant execution

## Selected

### RD-C1 Cancel Run

Why:
- strong black-box seams;
- four distinct hidden product semantics;
- terminal-state/alert/dashboard/idempotence ambiguity differs from S02;
- exact reference prototype passed 5 existing public checks + 1 candidate public feature check + 4 hidden semantics = 10/10;
- four targeted wrong-but-reasonable mutations were each rejected.

### RD-C2 Archive Job

Why:
- lifecycle/visibility and operational availability ambiguity;
- four distinct hidden product semantics;
- corrected exact reference prototype passed 5 existing public checks + 1 candidate public feature check + 3 hidden test methods covering four semantics = 9/9;
- four targeted wrong-but-reasonable mutations were each rejected;
- first prototype regression in existing alert behavior was caught and fixed before scenario selection.

## Deferred

### RD-C3 Retry Policy Update

Deferred because the frozen Pilot base intentionally carries S04's retry-alert defect. A transfer benchmark should not conflate requirement discovery with a known retry bug unless a new corrected fixture base is explicitly versioned and validated.

## Next gate

Implement repository-native, reproducible harnesses for RD-C1 and RD-C2:

1. exact treatment prompts;
2. public feature tests;
3. hidden evaluator cases;
4. frozen operator-oracle answers;
5. reference-solution overlays;
6. base red-capability selftest;
7. reference green selftest;
8. mutation-sensitivity selftest or equivalent reproducible checks;
9. packet builder proving contestants do not receive oracle/evaluator/reference material.

Only after all gates pass may a G0-G3 transfer cohort be frozen.

FIRST-mode remains unchanged.
