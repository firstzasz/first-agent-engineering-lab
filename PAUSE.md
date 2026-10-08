# Pausing Jobs

`POST /api/jobs/{id}/pause` pauses a Job; `POST /api/jobs/{id}/resume`
resumes it. Neither endpoint requires a request body. Both return `200` with
`{"job": ...}` containing the current Job, including its `paused` boolean.
Repeating either action succeeds with the same state. Unknown Jobs return the
existing `404` error envelope. `GET /api/jobs` also includes `paused`.

Pause blocks new scheduled Runs through the existing `409` scheduling-conflict
response. Blocked starts do not create Runs or queue work for resume. Manual
Runs remain available, and Runs already in progress continue through their
Attempts, retries, terminal outcomes, and existing alert behavior.

The persisted pause flag defaults to false and is independent of `enabled`.
Pause and resume preserve enabled state and retry policy. Enabling a paused Job
does not resume it; resuming a disabled Job does not enable it. Existing SQLite
Job tables gain the default-false column when a Store opens them.

The dashboard shows a Paused column alongside the existing enabled state and
last result. Pausing does not change historical results.

Verify with `python -m unittest discover -s tests -v`.
