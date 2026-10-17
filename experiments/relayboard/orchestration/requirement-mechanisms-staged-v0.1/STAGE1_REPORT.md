# EXP-0014 staged-screening v0.1: Stage 1

Screening status: **SCREEN_STOP_NO_STRONG_SIGNAL**

The expected pre-run HEAD was verified and the four fresh contestants ran serially in the frozen order M1, M0, M2, M3. All four dispositions were durably persisted before the continuation arithmetic was applied.

| Run | Surfaced / 4 | Silent / 4 | FACT burden | Engineering questions | Public | Frozen evaluator |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| RD-M1-S1 | 2 | 2 | 1 | 2 | PASS | PASS |
| RD-M0-S1 | 2 | 2 | 1 | 1 | PASS | PASS |
| RD-M2-S1 | 2 | 2 | 1 | 1 | PASS | PASS |
| RD-M3-S1 | 2 | 2 | 1 | 1 | PASS | PASS |

## Screening arithmetic

M0 surfaced 2 decisions and silently assumed 2. A mechanism therefore needs at least 4 surfaced decisions OR at most 0 silent assumptions to qualify under the frozen rule.

- M1: 2 >= 4 is False; 2 <= 0 is False. Result: NOT_SELECTED_BY_SCREEN.
- M2: 2 >= 4 is False; 2 <= 0 is False. Result: NOT_SELECTED_BY_SCREEN.
- M3: 2 >= 4 is False; 2 <= 0 is False. Result: NOT_SELECTED_BY_SCREEN.

Protocol-eligible Stage 2 run IDs: none.

**Stage 2 was not launched.** The user explicitly limited this task to Stage 1 and durable screening persistence. Nothing merged to main. Frozen treatment/task/evaluator/oracle/scoring/protocol/FIRST-mode files and the original Round 1/2 evidence remain unchanged.

See SCREENING_DECISION.json for machine-readable arithmetic, profiles.json for per-run measurements, results/<run_id>/ for candidates/history/tests/operator exchanges, MEASUREMENT_NOTES.md for classification choices and evidence limits, and FINAL_AUDIT.json for repository/readback verification.

These are single-observation screening results. A mechanism not selected by this screen has not been proven ineffective. No transfer, universal winner, cost/speed, or FIRST adoption claim follows. Runtime identity, token/cost usage, and raw host traces remain unavailable.
