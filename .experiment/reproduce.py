import json
from relayboard.testing import request
from relayboard.web import create_seeded_app

app = create_seeded_app()
code, payload = request(app, "POST", "/api/jobs/daily-report/runs", {"source": "manual"})
assert code == 201
run_id = payload["run"]["id"]
print("created", json.dumps(payload, sort_keys=True))
for number in (1, 2):
    code, payload = request(app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False})
    assert code == 200
    alert_code, alerts = request(app, "GET", "/api/alerts")
    assert alert_code == 200
    print("attempt", number, json.dumps(payload, sort_keys=True))
    print("alerts", json.dumps(alerts, sort_keys=True))
print("attempt_numbers", [attempt.number for attempt in app.store.list_attempts(run_id)])
print("failure_alert_count", len(alerts["alerts"]))
assert payload["status"] == "failed"
assert len(alerts["alerts"]) == 1, f"expected 1 failure alert; observed {len(alerts['alerts'])}"
