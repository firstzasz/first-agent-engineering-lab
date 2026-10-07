from relayboard.testing import request
from relayboard.web import create_seeded_app

app = create_seeded_app()
code, payload = request(app, "POST", "/api/jobs/daily-report/runs", {"source": "manual"})
assert code == 201
run_id = payload["run"]["id"]
for expected in ("running", "failed"):
    code, payload = request(app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False})
    print("attempt", code, payload["run"]["status"])
    assert code == 200
    assert payload["run"]["status"] == expected
code, payload = request(app, "GET", "/api/alerts")
print("alerts", payload)
assert code == 200
assert len(payload["alerts"]) == 1, payload["alerts"]
assert payload["alerts"][0]["run_id"] == run_id
