Add the ability to cancel a RelayBoard Run.

A cancelled Run must not accept further Attempts.

Expose the feature through `POST /api/runs/{id}/cancel`, following existing API conventions.

Preserve existing retry, alert, and dashboard behavior unless cancellation requires a change.

Implement the feature and verify it.
