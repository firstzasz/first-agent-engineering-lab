"""Public WSGI reproduction; run unchanged before and after the fix."""

import json

from relayboard.testing import request
from relayboard.web import create_seeded_app


app = create_seeded_app()
trace = []
failed_run_ids = []
for source in ("manual", "scheduled"):
    code, payload = request(
        app, "POST", "/api/jobs/daily-report/runs", {"source": source}
    )
    assert code == 201
    run_id = payload["run"]["id"]
    failed_run_ids.append(run_id)
    for number in (1, 2):
        code, payload = request(
            app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False}
        )
        assert code == 200
        alerts_code, alerts_payload = request(app, "GET", "/api/alerts")
        assert alerts_code == 200
        trace.append(
            {
                "source": source,
                "run_id": run_id,
                "attempt_number": number,
                "attempt_result": payload["status"],
                "run_status": payload["run"]["status"],
                "alert_run_ids": [a["run_id"] for a in alerts_payload["alerts"]],
            }
        )

print(json.dumps({"trace": trace}, indent=2), flush=True)
assert [t["attempt_result"] for t in trace] == ["retry", "failed", "retry", "failed"]
assert [t["run_status"] for t in trace] == ["running", "failed", "running", "failed"]
assert [t["alert_run_ids"] for t in trace] == [
    [], [failed_run_ids[0]], [failed_run_ids[0]], failed_run_ids
], "Each Run must alert only on terminal failure"
print("PASS: public API preserves retries and emits one failure alert per distinct failed Run")
