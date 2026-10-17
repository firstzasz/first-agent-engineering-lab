# Stage 1 evidence and measurement notes

The operator used the unchanged frozen S02 oracle and answered only requested decisions. Multi-item questions were preserved verbatim; no unasked frozen decision was volunteered.

The four scored decisions are the unchanged oracle keys: in-progress Run behavior, skipped scheduled-work queue behavior, manual Run permission, and resume/catch-up behavior. A question that merely repeats the task's scheduled-work prohibition is not counted as discovering the unresolved skip-versus-queue decision. Stated implementation choices are not counted as questions. Correct guesses remain silent assumptions.

For supplementary questions, enabled/disabled preservation was classified as FACT_LOOKUP because preserving existing behavior is already required and the enabled state is inspectable in the supplied fixture. Dashboard presentation and idempotence questions were classified as REVERSIBLE_ENGINEERING_CHOICE. These are explicit orchestrator classifications rather than automatic scores; exact questions and answers remain available for review. A stated idempotence choice that did not request a decision was not counted as a question.

Each candidate was committed locally in a separate, fixture-only Git history. The complete history is retained as base64 Git bundle with its SHA-256, together with candidate files and the patch from the prepared base. Independent public and frozen-evaluator execution used a fresh clone of that exact bundle after the contestant finished and was explicitly interrupted. The contestant never received hidden evaluation feedback.

The public-test log runs the candidate's complete visible unittest suite. The final audit checks that the original frozen public-test file stayed unchanged in each candidate. The frozen evaluator independently checks S02 acceptance; no new hidden cases or changed evaluator logic were introduced.

Host adaptation was common to all four arms: an assigned absolute workspace path; operator communication through collaboration.send_message; isolation restrictions; local commit and completion evidence; no helpers or publication by contestants. M0 received no METHOD.md. M1-M3 received byte-exact frozen method blobs. Each was spawned with fork_turns=none, requested gpt-6.1-sol and high reasoning, serially. Actual runtime identity, raw host tool traces, tokens and cost are unavailable; no hard secrecy or exhaustive access audit is claimed.

The initial M0 test temporary-directory sandbox issue was repaired within its assigned workspace by the same contestant. This was routine verification work, not an unrecoverable host failure or a replacement run.

Stage 1 is a single-observation screen per arm. Eligibility is determined only by the frozen continuation arithmetic. Eligibility does not authorize Stage 2 execution in this user-scoped task, establish transfer, change FIRST-mode, or support a universal methodology winner.
