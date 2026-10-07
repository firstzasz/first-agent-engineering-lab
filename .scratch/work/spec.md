# Pause and resume a Job

Status: completed
Origin: TASK.md and confirmed operator product answers in .experiment/operator-exchanges.json.

## Problem Statement
Operators need to temporarily stop a Job from starting normal scheduled work without disrupting other Run behavior.

## Solution
Pause a Job to skip scheduled starts; resume it to allow future scheduled activity, with no queue or catch-up.

## User Stories
1. As an operator, I want to pause scheduled starts so that work does not start during a temporary stop.
2. As an operator, I want to resume future scheduling so that skipped work is not replayed.
3. As an operator, I want manual Runs while paused so that I can explicitly request work.
4. As an operator, I want existing Runs to finish with their retries and alerts so that pause does not cancel work.
5. As an operator, I want disabled Jobs to remain disabled after resume so that separate scheduling intent is preserved.
6. As an API consumer, I want repeat pause/resume requests to be safe and unknown Jobs to use existing errors.
7. As an operator, I want pause visibility alongside Enabled and Last result so that I can understand scheduling state.
8. As an operator, I want pause state retained in storage so that rebuilding an app around the same database does not resume work.

## Implementation Decisions
- Separate persistent boolean paused, default false; keep enabled unchanged. These are engineering choices delegated by the operator.
- Add bodyless POST /api/jobs/{id}/pause and /resume; return 200 with a job object including paused. Repeats are idempotent; missing Jobs use existing 404.
- Scheduled starts raise existing not-schedulable conflict while paused; they do not create a Run or queued work.
- Add paused to Jobs JSON and a dashboard Paused column; preserve Enabled and Last result semantics.
- Support existing SQLite jobs tables with a default-false schema upgrade. Preserve the positional Job constructor by appending a defaulted field.
- Do not modify manual start, attempt, retry or alert logic.

## Testing Decisions
- Existing pre-agreed seams: WSGI requests using the public fixture request helper; real SQLite and Store/Service public interfaces for persistence and scheduler verification.
- Literal expectations from the confirmed spec; one test and minimal implementation per red/green cycle. No internal mocks.
- Prior art: existing public unittest tests. Use focused tests throughout, full discovery at completion.

## Out of Scope
Cancellation, new queues, catch-up, new retry or alert policy, scheduling engines, external services and deployment.

## Further Notes
Invoke to-spec without re-interviewing; reversible seam approval is standing in METHOD.md. This is one cohesive small implementation unit: pause/resume plus observable state. No independent ticket frontier or blocking edge would be meaningful; to-tickets and implement-spec are read for routing but not invoked. Lead implements directly using implement and tdd. No durable hard-to-reverse tradeoff warrants an ADR.
