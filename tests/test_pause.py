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

    def test_pause_skips_scheduled_starts_without_creating_runs(self) -> None:
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/pause")
        self.assertEqual(code, 200)
        self.assertEqual(payload["job"], {
            "id": "daily-report", "name": "Daily report",
            "enabled": True, "max_attempts": 2, "paused": True,
        })
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs",
            {"source": "scheduled"},
        )
        self.assertEqual((code, payload), (409, {"error": "job daily-report is paused"}))
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs")
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["id"], "run-001")
        self.assertEqual(payload["run"]["source"], "manual")

    def test_resume_allows_only_future_scheduled_starts_and_preserves_enabled(self) -> None:
        for job_id, expected_enabled in (("daily-report", True), ("cleanup", False)):
            with self.subTest(job=job_id):
                for _ in range(2):
                    code, payload = request(self.app, "POST", f"/api/jobs/{job_id}/pause")
                    self.assertEqual(code, 200)
                    self.assertIs(payload["job"]["paused"], True)
                code, _ = request(
                    self.app, "POST", f"/api/jobs/{job_id}/runs",
                    {"source": "scheduled"},
                )
                self.assertEqual(code, 409)
                for _ in range(2):
                    code, payload = request(self.app, "POST", f"/api/jobs/{job_id}/resume")
                    self.assertEqual(code, 200)
                    self.assertIs(payload["job"]["paused"], False)
                    self.assertIs(payload["job"]["enabled"], expected_enabled)
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs",
            {"source": "scheduled"},
        )
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["id"], "run-001")
        code, payload = request(
            self.app, "POST", "/api/jobs/cleanup/runs",
            {"source": "scheduled"},
        )
        self.assertEqual((code, payload), (409, {"error": "job cleanup is disabled"}))

    def test_dashboard_and_job_listing_show_pause_without_losing_last_result(self) -> None:
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs")
        run_id = payload["run"]["id"]
        request(self.app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": True})
        request(self.app, "POST", "/api/jobs/daily-report/pause")
        code, jobs = request(self.app, "GET", "/api/jobs")
        self.assertEqual(code, 200)
        self.assertEqual(jobs["jobs"][1]["paused"], True)
        self.assertEqual(jobs["jobs"][0]["paused"], False)
        code, dashboard = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<th>Job</th><th>Enabled</th><th>Paused</th><th>Last result</th>", dashboard)
        self.assertIn("<td>Daily report</td><td>yes</td><td>yes</td><td>succeeded</td>", dashboard)
        self.assertIn("<td>Cleanup</td><td>no</td><td>no</td><td>never</td>", dashboard)

    def test_pause_preserves_active_run_retries_alerts_and_manual_runs(self) -> None:
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs", {"source": "scheduled"},
        )
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]
        request(self.app, "POST", "/api/jobs/daily-report/pause")
        code, payload = request(
            self.app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False},
        )
        self.assertEqual((code, payload["status"], payload["run"]["status"]), (200, "retry", "running"))
        code, payload = request(
            self.app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False},
        )
        self.assertEqual((code, payload["status"], payload["run"]["status"]), (200, "failed", "failed"))
        code, payload = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        self.assertEqual(payload["alerts"], [
            {"id": 1, "run_id": "run-001", "job_id": "daily-report",
             "kind": "run_failed", "message": "Job Daily report failed for run run-001"},
            {"id": 2, "run_id": "run-001", "job_id": "daily-report",
             "kind": "run_failed", "message": "Job Daily report failed for run run-001"},
        ])
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs")
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["source"], "manual")
        self.assertEqual(payload["run"]["id"], "run-002")
        code, payload = request(
            self.app, "POST", "/api/runs/run-002/attempts", {"succeeded": True},
        )
        self.assertEqual((code, payload["status"]), (200, "succeeded"))

    def test_unknown_jobs_follow_not_found_convention_without_changing_jobs(self) -> None:
        for action in ("pause", "resume"):
            with self.subTest(action=action):
                code, payload = request(self.app, "POST", f"/api/jobs/missing/{action}")
                self.assertEqual((code, payload), (404, {"error": "not found: missing"}))
        code, payload = request(self.app, "GET", "/api/jobs")
        self.assertEqual(code, 200)
        self.assertEqual([job["paused"] for job in payload["jobs"]], [False, False])

    def test_pause_and_resume_persist_when_reopening_an_existing_database(self) -> None:
        with tempfile.TemporaryDirectory(dir=".experiment") as directory:
            database = Path(directory) / "jobs.sqlite3"
            connection = sqlite3.connect(database)
            connection.executescript("""
                CREATE TABLE jobs (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    enabled INTEGER NOT NULL,
                    max_attempts INTEGER NOT NULL CHECK(max_attempts >= 1)
                );
                INSERT INTO jobs VALUES ('daily-report', 'Daily report', 1, 2);
            """)
            app = RelayBoardApp(Store(connection))
            code, payload = request(app, "GET", "/api/jobs")
            self.assertEqual(code, 200)
            self.assertIs(payload["jobs"][0]["paused"], False)
            code, _ = request(app, "POST", "/api/jobs/daily-report/pause")
            self.assertEqual(code, 200)
            connection.close()

            connection = sqlite3.connect(database)
            app = RelayBoardApp(Store(connection))
            code, payload = request(app, "GET", "/api/jobs")
            self.assertEqual(code, 200)
            self.assertIs(payload["jobs"][0]["paused"], True)
            code, _ = request(
                app, "POST", "/api/jobs/daily-report/runs", {"source": "scheduled"},
            )
            self.assertEqual(code, 409)
            code, _ = request(app, "POST", "/api/jobs/daily-report/resume")
            self.assertEqual(code, 200)
            connection.close()

            connection = sqlite3.connect(database)
            app = RelayBoardApp(Store(connection))
            code, payload = request(app, "GET", "/api/jobs")
            self.assertEqual(code, 200)
            self.assertIs(payload["jobs"][0]["paused"], False)
            code, payload = request(
                app, "POST", "/api/jobs/daily-report/runs", {"source": "scheduled"},
            )
            self.assertEqual(code, 201)
            self.assertEqual(payload["run"]["id"], "run-001")
            connection.close()
