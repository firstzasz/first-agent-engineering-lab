Add the ability to pause and resume a RelayBoard Job.

A paused Job must not start normal scheduled work until it is resumed.

Preserve existing Run, retry, alert, and dashboard behavior unless the pause feature requires a change.

Expose the feature through `POST /api/jobs/{id}/pause` and `POST /api/jobs/{id}/resume`, following the existing API conventions.

Implement the feature and verify it.
