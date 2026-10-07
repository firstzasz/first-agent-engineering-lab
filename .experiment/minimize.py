import sys
from relayboard.testing import request
from relayboard.web import create_seeded_app
app = create_seeded_app()
count = int(sys.argv[1])
job = sys.argv[2]
_, payload = request(app, "POST", f"/api/jobs/{job}/runs")
run_id = payload["run"]["id"]
for _ in range(count):
    request(app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False})
_, payload = request(app, "GET", "/api/alerts")
print("failed_attempts", count, "job", job, "alerts", payload["alerts"])
assert len(payload["alerts"]) <= 1, "duplicate alerts"
