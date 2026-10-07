# Pausing jobs

Pause controls the start of new scheduled Runs. A paused Job still accepts manual
Runs, and existing Runs continue their Attempts, retries, and alerts as before.
Pausing or resuming does not change a Job's enabled state. A scheduled Run requires
both `enabled: true` and `paused: false`, so resuming a disabled Job does not enable it.

`POST /api/jobs/{id}/pause` and `POST /api/jobs/{id}/resume` need no request body.
Both return HTTP 200 with `{"job": ...}` containing the updated Job. Repeating an
action is safe and returns the same state. Unknown Jobs return the existing HTTP
404 error format. Scheduled Run requests for paused Jobs return HTTP 409.

Jobs start unpaused. The `paused` boolean is stored separately, returned by
`GET /api/jobs`, and displayed in a new Paused dashboard column. Existing database
schemas gain the pause field with an unpaused default when the Store opens.
