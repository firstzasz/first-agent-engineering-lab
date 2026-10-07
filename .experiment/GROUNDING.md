# Classification and done predicate

Reported defect. Bug fix route.
Done means the public API exposes no alert during retry, one run_failed alert when a Run exhausts attempts, no failure alert after eventual success, and separate alerts for distinct failed Runs. Retry statuses, stable Run ids, attempt numbering and configured limits stay unchanged. Focused tests and the full public suite must pass. A fresh serial helper must review the code and evidence before the local candidate is committed.

# How grounding

Simple affected scope. The lead performs the serial direct explainer allowed by METHOD.md.
The caller POSTs /api/jobs/{id}/runs through RelayBoardApp. The service creates one running Run through Store. POST /api/runs/{id}/attempts calls RelayBoardService.record_attempt, which checks the Run is running, persists one Attempt, compares its number to Job.max_attempts, and returns retry or a terminal outcome. Store persists attempts and alerts without deciding retry policy. GET /api/alerts serializes every persisted alert. Alert records reference the Run, not an Attempt. Existing frozen dataclasses and the running/succeeded/failed state machine already encode the necessary data shape.

# Falsifiable hypotheses

1. Public transport duplicates one stored alert in the response. Refuted by API ids 1 and 2 and the insert-per-attempt service branches.
2. Retries create distinct Runs. Refuted by the same run-001 id in both attempt responses and both alerts.
3. The retry branch emits a terminal Run failure alert too early. Confirmed by an alert while the Run still has running status after attempt 1, followed by a second persisted alert after terminal failure. Current source has a call to _emit_failure_alert in both branches.
4. Terminal failure is processed twice. Refuted for this reproduction by exactly one API call per Attempt and attempt_numbers [1, 2]. The first alert is already observable before terminal processing.

Runtime evidence is .experiment/outputs/baseline-api.txt. No targeted instrumentation was needed because public responses expose Run state and alert ids directly. Supplementary attempt numbering was inspected through the existing public fixture Store interface. Baseline public tests passed but omit retry-failure alert semantics.

# Throughput checkpoint before implementation

- Blocking first steps. Reproduce on the public WSGI surface and confirm the terminal-versus-attempt mechanism. Completed before design and delegation.
- Independent workstreams. API reproduction and baseline public tests were independent read-only calls. Diagnosis, regression, implementation, and review are sequential under the frozen port. No native parallel throughput claim.
- Shared mutable state. One assigned Git index, working tree and evidence directory. Only one helper runs at a time. Tests use fresh in-memory stores. The lead does not edit helper-owned code while a helper runs.
- Smallest safe decomposition. Capture baseline, compare two sketches, delegate failing tests and one-line service deletion to one fresh helper, then lead verify and fresh helper review. One test-only local commit precedes the fix commit.

# Native route adaptations and unsupported sources

Poteto Mode and Bug fix invoked by reading bundled files. How reduced to the direct lead trace. Architect reduced to two written serial designs. TDD uses existing unittest and WSGI seams. Show me your work uses append-only decisions.tsv and command output paths.
why, unslop, create-skill, technical-writing, Opening a PR, native control plugins, deslop and no-comments are unbundled or unavailable here. Their source is neither invented nor fetched. METHOD.md binds direct API checks, scoped diff cleanup/review and local commit handoff. Native Cursor Task/poteto-agent become fresh serial collaboration helpers. Native Arena's multi-model design exploration is replaced by two lead-written sketches under METHOD.md. No native model diversity is claimed. No bundled upstream source is changed.
Standing authorization covers local fixture seams and reversible tests. No product decision is open. No operator question is needed.

# Identity and evidence limits

Requested lead and helper model is gpt-6.1-sol with high reasoning. The lead runtime has no exposed identity or token-usage telemetry. No raw transcript export is available. early-actions.json preserves summarized pre-capture commands and paths. commands.jsonl and outputs preserve subsequent command evidence. Public checks only. No forbidden source links from README were followed.
