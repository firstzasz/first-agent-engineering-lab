# Route and boundary

Starting commit: 2f337252199d4b4658a6abb15f8037e2b147bc58.
Source: mattpocock/skills 4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d, bundled unchanged under upstream/matt.
Assigned treatment: matt-codex-port-v0, explicitly non-native Codex port.
Read METHOD.md, TASK.md, GLOSSARY.md, README.md, pyproject.toml, public Python code/tests, .gitignore and RUN_MANIFEST.json only within this run.
Available commands observed: Python 3.12.14, git, rg; exact discovery output was captured in the tool transcript.

Invoked bundled diagnosing-bugs, implement, tdd (including tests.md/mocking.md), code-review by opening their exact source files.
No interview/spec/tickets ceremony: narrow reported bug; TASK.md supplies complete scope and GLOSSARY.md explicitly associates alerts with terminal Runs, not Attempts.
Existing WSGI, service and Store public interfaces are pre-agreed seams by frozen METHOD.md. Standing authorization covers reversible seam/ticket decisions; no product decision needed or asked yet.
No ADR: correcting existing behavior, no durable tradeoff introduced.
No Python typechecker invented for a standard-library fixture.

Adaptations: local TASK.md tracker/spec; manual source reading replaces native invocation; fresh serial same-model helpers replace native parallel/model diversity; local commit replaces shipping/tracker closure.
Requested identity: GPT-6.1 Sol, High reasoning (per task/method). Observed lead identity and usage are not independently exposed by runtime; no claim of native model diversity or throughput.
Boundaries: supplied run only; no evaluator/peer/lab-history material, network, paid APIs, credentials, production, deployment, external messaging or merges.

Diagnosis phase 1: build a deterministic WSGI feedback loop with actual SQLite and assert the exact duplicate-alert symptom. Read code to locate public interfaces, not to formulate a theory before the loop.

Phase 2: original-red and repeat-red each show two run_failed alerts for run-001 after retry then terminal failure; five baseline public tests pass. Minimal-red removes the unrelated seeded cleanup Job and retains the exact failure. Removing the second failed Attempt makes the duplicate assertion green. A one-attempt policy/control emits one alert. Remaining bug-bearing scenario: one Job with retry permission, one Run, two failed Attempts. HTTP request setup is necessary seam plumbing, not an independent domain trigger.

Phase 3 ranked hypotheses (before testing):
1. An intermediate failed Attempt emits a Run failure alert before the Run is terminal. Prediction: inspect alerts after the first failed Attempt; it has one alert while status remains running, then a second alert after terminal failure.
2. Store insertion duplicates each requested alert. Prediction: a single failure-emission boundary inserts two rows, including the no-retry control, instead of one row per boundary.
3. The WSGI/request path replays an Attempt or creates multiple Runs. Prediction: the first request records two Attempts or creates a second Run; direct service invocation with one Run will remove the duplication.
No product questions: glossary and scope determine intended behavior. Hypothesis checkpoint sent to operator without waiting, as prescribed.

Phase 4: diagnostic-only .experiment/probe.py observes GET /api/alerts after each failed Attempt, plus public Store.list_attempts. No production instrumentation introduced. Output boundary-probe.txt shows one alert after attempt 1 while running and two after attempt 2 when failed; exactly one stored Attempt per call, same Run id throughout. Confirms hypothesis 1, falsifies per-boundary double insertion and request replay alternatives. Relevant cause: record_attempt calls _emit_failure_alert in retry branch before terminal status, then again after exhausted retries. No bisection/fuzz/production phases: deterministic local boundary probe establishes cause directly, no environment access needed.

Phase 5 seam: regression in tests/test_public.py through real WSGI endpoints/SQLite; assert zero alerts during retry, one associated terminal alert, retry/status preserved. Implementation unit: remove only premature emission from retry branch. No deduplication by Job or suppression of distinct Run alerts.

Regression-red failed at the independently specified empty-alerts assertion during retry. Removed one service call; regression-green and original-green pass. Afterwards, added public behavioral verification for distinct manual/scheduled Runs and success after two retries; no additional implementation was needed. These are verification guards after the single red/green slice, not additional feature slices; their pre-fix failure was not measured.
Cleanup: diagnostic harnesses are clearly marked and retained only in .experiment for reproducibility. No app instrumentation was added; rg DEBUG- relayboard tests exits 1 with no matches (successful cleanup signal). Original repro passes with exactly one alert; focused public file has 8 passing tests.
Review fixed point: initial independent commit 2f337252199d4b4658a6abb15f8037e2b147bc58. Standards and Spec axes will remain distinct, using fresh serial read-only helpers on GPT-6.1 Sol High as requested; no descendants.

Final review: both helpers completed serially against implementation commit 6e8ae0ce540aa33bec3640932b7650c0ee196f5f. Standards: 0 documented violations, 0 actionable smells; TDD history unknown from diff alone (lead's exact red/green outputs retained separately). Spec: 0 findings; helper independently reran full public suite (8 pass). No fixes requested. No product/operator questions or answers. Hypothesis checkpoint only, no blocking operator interaction.
Completion: TASK.md's single implementation unit done, no tickets created. Candidate change removes only premature retry alert; verification covers terminal retry failure, distinct manual/scheduled Runs, multi-retry success and baseline behavior. No hidden evaluation performed. Evidence artifacts will be committed separately; this documentation commit changes no application behavior.
