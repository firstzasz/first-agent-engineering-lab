# Pause and resume Jobs

Status: complete; one implementation unit; independent Standards and Spec reviews complete.

## Problem Statement

Operators need to temporarily stop normal scheduled work for a Job while preserving configured enabled state and ongoing work.

## Solution

Pause a Job through its API and resume it later. Paused scheduled starts are skipped and never queued. Resume affects future scheduled activity only. Manual Runs remain allowed, and existing Runs continue to their terminal outcomes with existing retries and alerts.

## User Stories

1. As an operator, I want to pause a Job so that normal scheduled work does not start.
2. As an operator, I want to resume a Job so that future scheduled activity can proceed.
3. As an operator, I want manual Runs while paused so that I can explicitly request work.
4. As an operator, I want active Runs to finish with existing retry and alert behavior so that pausing does not interrupt them.
5. As an operator, I want skipped starts discarded so that resume causes no catch-up surge.
6. As an operator, I want enabled state preserved so that resume does not inadvertently enable disabled Jobs.
7. As an operator, I want to see pause state in Job responses and the dashboard so that I can distinguish pause from disabled state and last Run result.
8. As an API caller, I want repeated pause/resume to succeed and unknown Jobs to follow existing not-found conventions.

## Implementation Decisions

- Operator decisions: pause skips scheduled starts, allows manual Runs, preserves active Run/retry/alert behavior; resume has no catch-up.
- Engineering judgment (operator supplied no additional preference): persist a separate paused boolean defaulting false, independent of enabled.
- Add explicit service pause/resume operations and gate scheduled starts using the existing scheduling conflict exception.
- POST /api/jobs/{id}/pause and /resume use no required body and return 200 with the existing Job wrapper. Unknown Jobs return 404. Operations are idempotent.
- Existing database schemas acquire a default-unpaused column without changing existing enabled settings or Run records.
- Include paused in Job JSON. Add a Paused dashboard column while preserving Enabled and Last result meanings.
- Keep new model field backward-compatible by placing a default false field after existing fields.

## Testing Decisions

- Existing public WSGI request fixture over real Store/SQLite is the highest pre-agreed seam, authorized by the frozen binding.
- Use independent literal outcomes and statuses; no internal collaborator mocks or private method tests.
- Work one observable test and minimal implementation at a time; record red/green output.
- Exercise scheduled rejection, resume, idempotence, independent enabled state, manual/ongoing retry/alert preservation, unknown Jobs, visibility and persistence through public interfaces.
- Run focused unittest commands during implementation and the full public suite at completion. Standard-library fixture has no configured typechecker.

## Out of Scope

Catch-up queues, cancellation, Run state changes, retry/alert bug fixes, external notifications, deployment and remote operations.

## Further Notes

Separate boolean, idempotence, response shape and presentation are reversible engineering choices, not operator product instructions. No durable ADR warranted. A single small end-to-end feature is one lead implementation unit; no independent vertical delivery units or blocking edges justify a ticket graph or implement-spec. Local files replace the native tracker; no tracker setup is needed under the binding.
