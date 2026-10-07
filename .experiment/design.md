# Problem

Pausing a Job must block new scheduled Runs while preserving manual Runs, current Attempts, retries, alerts and historical results. Enabled/disabled already governs scheduling and must survive pause/resume. The operator explicitly confirmed manual and current-Run behavior.

# Usage (caller’s view)

POST /api/jobs/daily-report/pause with no body returns 200 and {"job": {"id": "daily-report", "name": "Daily report", "enabled": true, "max_attempts": 2, "paused": true}}.
POST /api/jobs/daily-report/runs with {"source":"scheduled"} returns 409 while paused. A manual request still returns 201. POST /api/jobs/daily-report/resume returns the same Job envelope with paused false. Repeating either command converges to that state. Unknown Job ids return the existing 404 error envelope. GET /api/jobs includes paused. Dashboard includes a Paused column alongside existing data.

# Shape

Candidate A adds Job.paused: bool = False as an independent persisted scheduling control. All four enabled/paused combinations are valid. Pause is not represented by temporarily overwriting enabled. Store owns set_job_paused(job_id, paused) and SQLite paused INTEGER NOT NULL DEFAULT 0. Additive migration handles a preexisting jobs table. Service pause_job/resume_job return Job after Store mutation and own scheduling admission. begin_scheduled_run checks paused before creating a Run and raises existing JobNotSchedulable. API routes adapt command names and return the existing envelope. Neither Run state nor record_attempt changes.

Usage sketch derives signatures pause_job(job_id: str) -> Job and resume_job(job_id: str) -> Job. Paused state belongs to the existing Job domain per Model the Domain, with no synchronized derived flags. One Store write path owns it. Small service methods preserve the established command boundary rather than add new layering. Public interface hides state persistence and scheduler policy; callers need only two commands and one readable field. This keeps interface depth in the current service.

Candidate B stores pause membership in a separate paused_jobs(job_id PRIMARY KEY REFERENCES jobs) relation. pause inserts idempotently, resume deletes, scheduler reads membership, and Job serialization/dashboard join the relation. No migration of jobs is needed. This hides a separate persistence representation, but either spreads pause queries across readers or requires joining all Job reads and projecting the same boolean anyway. Its public API has no extra useful capability over A.

# Synthesis decision

Choose A as the base. Its Job snapshot directly carries scheduling controls and a single Store method owns state. B avoids a column migration but adds a second table and lookup/join ownership for one independent bit. No graft is useful. Rubric results favor A on preservation of enabled state, single state ownership, compatibility with existing snapshots, and compact service policy. Both can satisfy user behavior and idempotence. The lead produced and screened both sketches serially under METHOD. Native parallel arena/cross-model synthesis is not claimed.

# Red-flag screen and interface depth

A has no new module, no multi-call public protocol, no internal options exposed, and no second writer of paused state. The bool remains independent rather than synchronized with enabled. SQLite shape stays behind Store. Existing web projection must include the new public field, as it already explicitly lists existing fields. The service forwards mutations through the established application boundary and also owns scheduling policy.

B has potential split ownership between membership and Job snapshots, exposes the same public interface while hiding less cohesive domain state, and requires coordination of joins/readers. Reject it on interface depth and maintenance cost rather than claiming it cannot work.

# Tradeoffs accepted

- We accept one additive schema migration in exchange for self-contained Job snapshots and preserving existing connections.
- We accept one added dashboard column in exchange for making the new state visible without changing Enabled or Last result.
- We accept sequential helpers in exchange for the frozen port’s confined shared workspace; no native throughput claim is made.

# Open questions and risks

No product decisions remain open after the operator answer and task preservation requirement. Existing retry failure alert emission appears broader than the glossary terminal-only description. Preserve its observed behavior as explicitly instructed. Atomic scheduling across concurrent SQLite connections is an existing limitation and is not expanded into this feature.

# Next implementation step

Delegate tests-first WSGI behavior checks, then the bounded Job/Store/service/web additions to one fresh serial helper.
