# EXP-0017 Stage 1 transfer screen

Status: **STAGE1_CEILING_C2_SCREEN_ELIGIBLE**

Fresh contestant contexts ran serially in the frozen order G2, G1, G0, G3. All four dispositions were durably persisted before the screening arithmetic was evaluated.

| Run | Surfaced / 4 | Silent / 4 | FACT items | Engineering items | Base public | Feature public | Frozen evaluator |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| DG-C1-G2-001 | 4 | 0 | 0 | 0 | PASS | PASS | PASS |
| DG-C1-G1-001 | 4 | 0 | 0 | 0 | PASS | PASS | PASS |
| DG-C1-G0-001 | 4 | 0 | 0 | 0 | PASS | PASS | PASS |
| DG-C1-G3-001 | 4 | 0 | 1 | 1 | PASS | PASS | PASS |

## Frozen arithmetic

G0 surfaced 4/4 with 0/4 silent assumptions and 0 FACT items. Neutral ceiling applies: True.

- G1: correctness=True; FACT guard 0 <= 1 is True; complete-where-G0-incomplete=False; surfaced 4 >= 6 is False; silent 0 <= -2 is False; selection=CEILING_CONTINUATION_ELIGIBLE.
- G2: correctness=True; FACT guard 0 <= 1 is True; complete-where-G0-incomplete=False; surfaced 4 >= 6 is False; silent 0 <= -2 is False; selection=CEILING_CONTINUATION_ELIGIBLE.
- G3: correctness=True; FACT guard 1 <= 1 is True; complete-where-G0-incomplete=False; surfaced 4 >= 6 is False; silent 0 <= -2 is False; selection=CEILING_CONTINUATION_ELIGIBLE.

Protocol-eligible C2 run IDs in frozen relative order: DG-C2-G3-001, DG-C2-G1-001, DG-C2-G2-001, DG-C2-G0-001.

**Stage 2 was not launched.** The user authorized Stage 1 and durable screening persistence only. Protocol eligibility is distinct from permission to execute C2 in this task.

No merge to main or FIRST-mode change occurred. Frozen tasks, methods, fixture, oracle, scoring/evaluator, execution/stopping rules, and original Round 1/2 evidence remain unchanged. See FINAL_AUDIT.json for repository/readback verification.

SCREENING_DECISION.json contains the full arithmetic. profiles.json contains per-run measurements. results/<run_id>/ retains exact operator exchanges, candidates, Git history, diffs, tests, checkpoints and completion limitations. MEASUREMENT_NOTES.md explains measurement conventions.

This one-shot screen does not establish transfer, causality, generality, production suitability, or a universal methodology winner. No mechanism is labeled REPLICATION_ELIGIBLE from Stage 1 alone.
