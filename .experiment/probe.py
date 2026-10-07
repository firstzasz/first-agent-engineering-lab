"""Diagnostic-only harness: observe a single alert/attempt boundary at a time."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from relayboard.testing import request
from relayboard.web import RelayBoardApp

app = RelayBoardApp()
app.store.add_job("probe", "Probe", max_attempts=2)
code, payload = request(app, "POST", "/api/jobs/probe/runs", {})
run_id = payload["run"]["id"]
for number in (1, 2):
    code, payload = request(app, "POST", f"/api/runs/{run_id}/attempts",
                            {"succeeded": False})
    _, alerts = request(app, "GET", "/api/alerts")
    print("[DEBUG-M-S04-boundary]", {"attempt_request": number,
          "response": payload, "alerts": alerts["alerts"],
          "attempts": [a.__dict__ for a in app.store.list_attempts(run_id)]})
