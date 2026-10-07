import json

from relayboard.testing import request
from relayboard.web import create_seeded_app


app = create_seeded_app()
checks = []
for source in ("manual", "scheduled"):
    code, body = request(app, "POST", "/api/jobs/daily-report/runs", {"source": source})
    assert code == 201
    run_id = body["run"]["id"]
    for number in (1, 2):
        code, body = request(app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False})
        assert code == 200
        alert_code, alerts = request(app, "GET", "/api/alerts")
        assert alert_code == 200
        own_alerts = [a for a in alerts["alerts"] if a["run_id"] == run_id]
        snapshot = {"run_id": run_id, "source": source, "attempt": number, "outcome": body["status"], "run_status": body["run"]["status"], "alert_count": len(own_alerts)}
        print(json.dumps(snapshot, sort_keys=True))
        expected = ("retry", "running", 0) if number == 1 else ("failed", "failed", 1)
        checks.append((body["status"], body["run"]["status"], len(own_alerts)) == expected)
code, body = request(app, "POST", "/api/jobs/daily-report/runs", {"source": "manual"})
assert code == 201
recovered_id = body["run"]["id"]
for succeeded in (False, True):
    code, body = request(app, "POST", f"/api/runs/{recovered_id}/attempts", {"succeeded": succeeded})
    assert code == 200
code, body = request(app, "GET", "/api/alerts")
assert code == 200
alert_runs = [a["run_id"] for a in body["alerts"]]
print(json.dumps({"alert_runs": alert_runs, "recovered_run": recovered_id}, sort_keys=True))
checks.append(alert_runs == ["run-001", "run-002"])
assert all(checks), "failure alerts must occur once per failed Run and only after retries are exhausted"
print("PASS: retry outcomes preserved; distinct failed Runs each alert once; recovered Run does not alert")
