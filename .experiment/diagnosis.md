# Diagnosis checkpoint

Route: diagnosing-bugs → implement + tdd → code-review.
Source: upstream/matt frozen commit 4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d; files bundled unchanged. TASK.md is the tiny originating spec. No product ambiguity: glossary states alerts are per terminal Run, Attempts are not Runs. Interview/to-spec/to-tickets ceremony omitted because one mechanical implementation unit suffices. No ADR exists in assigned files; no durable tradeoff requires one.

Public seam: real WSGI via relayboard.testing.request and real in-memory SQLite, as already exposed by tests/test_public.py. Standing approval under METHOD.md replaces seam/ticket approval. No typechecker required for this standard-library Python fixture.

Phase 1 errors retained: relative -m invocation unsupported; then guessed retrying Run status was incorrect. Corrected harness uses existing running Run status. Exact symptom reproduced twice: two identical run_failed alerts for one Run after two failed Attempts.

Minimization: one Run, retry-enabled Job, two failed Attempts, inspect alerts. Red with two failures; dropping one failure removes duplicate (but exposes a premature single alert while Run is running). Single-attempt no-retry Job has one terminal alert. Seed includes unrelated cleanup Job but repro never exercises it; no need to mutate seed merely to remove inert setup. Removing Run/Job makes path unavailable; removing outcome/second attempt removes duplicate. Sources were read for public seams first; service/store cause logic read only after red/minimization and checkpoint.

Ranked hypotheses sent nonblocking to operator before probes:
1. Per-failed-Attempt alert before terminal Run: predicts premature first alert.
2. Separate retry and terminal alert paths: predicts origins differ.
3. Store duplicates emission insert: predicts two rows from one emission.
4. WSGI replays record_attempt: predicts direct service differs / too many Attempts.

Phase 4 probe: direct service public call, print public Run/Attempts/Alerts state only at return boundary. No production instrumentation or mocks. Inspection confirms distinct nonterminal/terminal emission branches; add_alert inserts once. Probe should show one Attempt and one alert after retry, then two Attempts and two alerts. This supports 1/2 and rejects 3/4. Hypotheses 1/2 overlap: concrete cause is alert emission in retry branch.

Implementation unit: remove retry-branch alert call; preserve retry return, Attempt recording and terminal failure emission. Regression written before fix at WSGI seam. No broad deduplication, schema/interface change, or job-level suppression needed. Debug harnesses intentionally retained under .experiment as evidence, never imported by production/tests.
