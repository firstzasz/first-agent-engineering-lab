import sqlite3
import tempfile
import unittest
from pathlib import Path

from relayboard.store import Store
from relayboard.testing import request
from relayboard.web import RelayBoardApp, create_seeded_app


class PauseJobTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_seeded_app()

    def test_pause_and_resume_missing_jobs_use_existing_not_found_response(self) -> None:
        for action in ("pause", "resume"):
            self.assertEqual(
                request(self.app, "POST", f"/api/jobs/missing/{action}"),
                (404, {"error": "not found: missing"}),
            )
            self.assertEqual(
                request(self.app, "GET", f"/api/jobs/daily-report/{action}"),
                (404, {"error": "not found"}),
            )

    def test_repeated_pause_and_resume_are_idempotent(self) -> None:
        for action, paused in (("pause", True), ("resume", False)):
            first = request(self.app, "POST", f"/api/jobs/daily-report/{action}")
            second = request(self.app, "POST", f"/api/jobs/daily-report/{action}")
            self.assertEqual(first, second)
            self.assertEqual(first[0], 200)
            self.assertEqual(first[1]["job"]["paused"], paused)
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs",
                                {"source": "scheduled"})
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["id"], "run-001")

    def test_enable_changes_do_not_clear_pause(self) -> None:
        request(self.app, "POST", "/api/jobs/daily-report/pause")
        for enabled in (False, True):
            code, payload = request(self.app, "POST", "/api/jobs/daily-report/enabled",
                                    {"enabled": enabled})
            self.assertEqual(code, 200)
            self.assertTrue(payload["job"]["paused"])
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/runs",
                                 {"source": "scheduled"})[0], 409)

    def test_resume_does_not_enable_a_disabled_job(self) -> None:
        code, payload = request(self.app, "POST", "/api/jobs/cleanup/pause")
        self.assertEqual(code, 200)
        self.assertTrue(payload["job"]["paused"])
        self.assertFalse(payload["job"]["enabled"])
        code, payload = request(self.app, "POST", "/api/jobs/cleanup/resume")
        self.assertEqual(code, 200)
        self.assertFalse(payload["job"]["paused"])
        self.assertFalse(payload["job"]["enabled"])
        code, payload = request(self.app, "POST", "/api/jobs/cleanup/runs",
                                {"source": "scheduled"})
        self.assertEqual((code, payload), (409, {"error": "job cleanup is disabled"}))

    def test_pause_preserves_existing_run_retries_alerts_and_result(self) -> None:
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs",
                                {"source": "scheduled"})
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]
        request(self.app, "POST", "/api/jobs/daily-report/pause")
        code, payload = request(self.app, "POST", f"/api/runs/{run_id}/attempts",
                                {"succeeded": False})
        self.assertEqual(code, 200)
        self.assertEqual(payload["status"], "retry")
        self.assertEqual(payload["run"]["id"], "run-001")
        code, payload = request(self.app, "POST", f"/api/runs/{run_id}/attempts",
                                {"succeeded": True})
        self.assertEqual(code, 200)
        self.assertEqual(payload["status"], "succeeded")
        self.assertEqual(payload["run"]["id"], "run-001")
        code, payload = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        # Preserve the fixture's existing alert on a failed retryable attempt.
        self.assertEqual(payload, {"alerts": [{
            "id": 1, "job_id": "daily-report", "run_id": "run-001",
            "kind": "run_failed", "message": "Job Daily report failed for run run-001",
        }]})
        code, body = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<td>Daily report</td><td>yes</td><td>yes</td><td>succeeded</td>", body)

    def test_pause_keeps_manual_runs_available(self) -> None:
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/pause")[0], 200)
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs")
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"], {
            "id": "run-001", "job_id": "daily-report", "source": "manual",
            "status": "running",
        })

    def test_existing_database_upgrades_and_retains_pause_on_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "jobs.sqlite"
            connection = sqlite3.connect(database)
            connection.executescript("""
                CREATE TABLE jobs (
                    id TEXT PRIMARY KEY, name TEXT NOT NULL,
                    enabled INTEGER NOT NULL,
                    max_attempts INTEGER NOT NULL CHECK(max_attempts >= 1)
                );
                INSERT INTO jobs VALUES ('old-job', 'Old Job', 1, 2);
            """)
            app = RelayBoardApp(Store(connection))
            code, payload = request(app, "GET", "/api/jobs")
            self.assertEqual(code, 200)
            self.assertEqual(payload, {"jobs": [{
                "id": "old-job", "name": "Old Job", "enabled": True,
                "max_attempts": 2, "paused": False,
            }]})
            self.assertEqual(request(app, "POST", "/api/jobs/old-job/pause")[0], 200)
            connection.close()
            reopened = sqlite3.connect(database)
            try:
                app = RelayBoardApp(Store(reopened))
                code, payload = request(app, "GET", "/api/jobs")
                self.assertEqual(code, 200)
                self.assertTrue(payload["jobs"][0]["paused"])
                self.assertEqual(request(app, "POST", "/api/jobs/old-job/runs",
                                         {"source": "scheduled"})[0], 409)
            finally:
                reopened.close()

    def test_dashboard_shows_pause_beside_existing_job_state(self) -> None:
        request(self.app, "POST", "/api/jobs/daily-report/pause")
        code, body = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<th>Enabled</th><th>Paused</th><th>Last result</th>", body)
        self.assertIn("<td>Daily report</td><td>yes</td><td>yes</td><td>never</td>", body)
        self.assertIn("<td>Cleanup</td><td>no</td><td>no</td><td>never</td>", body)

    def test_resume_allows_future_scheduling_without_catch_up(self) -> None:
        request(self.app, "POST", "/api/jobs/daily-report/pause")
        code, _ = request(self.app, "POST", "/api/jobs/daily-report/runs",
                          {"source": "scheduled"})
        self.assertEqual(code, 409)
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/resume")
        self.assertEqual(code, 200)
        self.assertFalse(payload["job"]["paused"])
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs",
                                {"source": "scheduled"})
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"], {
            "id": "run-001", "job_id": "daily-report", "source": "scheduled",
            "status": "running",
        })

    def test_pause_blocks_new_scheduled_runs(self) -> None:
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/pause")
        self.assertEqual(code, 200)
        self.assertEqual(payload, {"job": {
            "id": "daily-report", "name": "Daily report", "enabled": True,
            "max_attempts": 2, "paused": True,
        }})
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs",
                                {"source": "scheduled"})
        self.assertEqual(code, 409)
        self.assertEqual(payload, {"error": "job daily-report is paused"})


if __name__ == "__main__":
    unittest.main()
