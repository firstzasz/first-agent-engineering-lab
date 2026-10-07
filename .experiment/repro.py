"""Deterministic duplicate-failure-alert repro through real WSGI/SQLite."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from relayboard.testing import request
from relayboard.web import RelayBoardApp, create_seeded_app

parser = argparse.ArgumentParser()
parser.add_argument("--minimal", action="store_true")
parser.add_argument("--attempts", type=int, default=2)
parser.add_argument("--policy", type=int, default=2)
args = parser.parse_args()
if args.minimal:
    app = RelayBoardApp()
    app.store.add_job("daily-report", "Daily report", max_attempts=args.policy)
else:
    app = create_seeded_app()
code, payload = request(app, "POST", "/api/jobs/daily-report/runs", {})
assert code == 201
run_id = payload["run"]["id"]
for number in range(1, args.attempts + 1):
    code, payload = request(app, "POST", f"/api/runs/{run_id}/attempts",
                            {"succeeded": False})
    assert code == 200
    print({"attempt": number, "response": payload})
code, payload = request(app, "GET", "/api/alerts")
assert code == 200
print({"alerts": payload["alerts"]})
assert len(payload["alerts"]) <= 1, "duplicate failure alerts for one Run"
