import sqlite3
import tempfile
import unittest
from pathlib import Path

from relayboard.models import Job
from relayboard.service import JobNotSchedulable
from relayboard.store import Store
from relayboard.testing import request
from relayboard.web import RelayBoardApp, create_seeded_app


class PausePublicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_seeded_app()

    def job_payload(self, *, enabled=True, paused=False):
        return {
            "job": {
                "id": "daily-report",
                "name": "Daily report",
                "enabled": enabled,
                "max_attempts": 2,
                "paused": paused,
            }
        }

    def test_default_unpaused_jobs_can_schedule(self) -> None:
        self.assertFalse(Job("new", "New", True, 1).paused)
        self.assertEqual(request(self.app, "GET", "/api/jobs"), (200, {
            "jobs": [
                {"id": "cleanup", "name": "Cleanup", "enabled": False,
                 "max_attempts": 1, "paused": False},
                self.job_payload()["job"],
            ]
        }))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/runs",
                                 {"source": "scheduled"}), (201, {
            "run": {"id": "run-001", "job_id": "daily-report",
                    "source": "scheduled", "status": "running"}
        }))

    def test_pause_resume_are_idempotent_and_block_only_scheduling(self) -> None:
        for _ in range(2):
            self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/pause"),
                             (200, self.job_payload(paused=True)))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/runs",
                                 {"source": "scheduled"}),
                         (409, {"error": "job daily-report is paused"}))
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("daily-report")
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/runs"),
                         (201, {"run": {"id": "run-001", "job_id": "daily-report",
                                        "source": "manual", "status": "running"}}))
        for _ in range(2):
            self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/resume"),
                             (200, self.job_payload()))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/runs",
                                 {"source": "scheduled"}),
                         (201, {"run": {"id": "run-002", "job_id": "daily-report",
                                        "source": "scheduled", "status": "running"}}))

    def test_service_commands_return_job_and_do_not_change_enabled(self) -> None:
        self.assertEqual(self.app.service.pause_job("cleanup"),
                         Job("cleanup", "Cleanup", False, 1, paused=True))
        self.assertEqual(self.app.service.pause_job("cleanup"),
                         Job("cleanup", "Cleanup", False, 1, paused=True))
        self.assertEqual(self.app.service.resume_job("cleanup"),
                         Job("cleanup", "Cleanup", False, 1, paused=False))
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("cleanup")
        self.assertEqual(self.app.service.begin_manual_run("cleanup").source, "manual")

    def test_enabled_and_paused_remain_independent(self) -> None:
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/pause"),
                         (200, self.job_payload(paused=True)))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/enabled",
                                 {"enabled": False}),
                         (200, self.job_payload(enabled=False, paused=True)))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/resume"),
                         (200, self.job_payload(enabled=False)))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/runs",
                                 {"source": "scheduled"}),
                         (409, {"error": "job daily-report is disabled"}))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/pause"),
                         (200, self.job_payload(enabled=False, paused=True)))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/enabled",
                                 {"enabled": True}),
                         (200, self.job_payload(paused=True)))
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/runs",
                                 {"source": "scheduled"}),
                         (409, {"error": "job daily-report is paused"}))

    def test_unknown_jobs_and_inexact_routes_do_not_mutate(self) -> None:
        for action in ("pause", "resume"):
            self.assertEqual(request(self.app, "POST", f"/api/jobs/missing/{action}"),
                             (404, {"error": "not found: missing"}))
            for path in (f"api/jobs/daily-report/{action}",
                         f"prefix/api/jobs/daily-report/{action}",
                         f"/api/jobs/daily-report/extra/{action}",
                         f"/api/jobs/daily-report/{action}/",
                         f"/api/jobs/daily-report/{action}/extra",
                         f"/api/jobs//{action}"):
                self.assertEqual(request(self.app, "POST", path),
                                 (404, {"error": "not found"}))
            self.assertEqual(request(self.app, "GET", f"/api/jobs/daily-report/{action}"),
                             (404, {"error": "not found"}))
        self.assertEqual(request(self.app, "GET", "/api/jobs")[1]["jobs"][1],
                         self.job_payload()["job"])
        self.assertEqual(self.app.service.begin_scheduled_run("daily-report").id, "run-001")

    def test_current_run_retries_attempts_and_alerts_survive_pause(self) -> None:
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs",
                                {"source": "scheduled"})
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/pause"),
                         (200, self.job_payload(paused=True)))
        self.assertEqual(request(self.app, "POST", f"/api/runs/{run_id}/attempts",
                                 {"succeeded": False}), (200, {
            "status": "retry", "run": {"id": "run-001", "job_id": "daily-report",
                                         "source": "scheduled", "status": "running"}
        }))
        expected_alert = {"id": 1, "run_id": "run-001", "job_id": "daily-report",
                          "kind": "run_failed",
                          "message": "Job Daily report failed for run run-001"}
        self.assertEqual(request(self.app, "GET", "/api/alerts"),
                         (200, {"alerts": [expected_alert]}))
        self.assertEqual(request(self.app, "POST", f"/api/runs/{run_id}/attempts",
                                 {"succeeded": True}), (200, {
            "status": "succeeded", "run": {"id": "run-001", "job_id": "daily-report",
                                           "source": "scheduled", "status": "succeeded"}
        }))
        self.assertEqual([(a.number, a.succeeded) for a in self.app.store.list_attempts(run_id)],
                         [(1, False), (2, True)])
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/resume"),
                         (200, self.job_payload()))
        self.assertEqual(request(self.app, "GET", "/api/alerts"),
                         (200, {"alerts": [expected_alert]}))
        self.assertEqual(self.app.store.get_run(run_id).status, "succeeded")

    def test_paused_manual_run_keeps_terminal_failure_alert(self) -> None:
        self.assertEqual(request(self.app, "POST", "/api/jobs/cleanup/pause")[0], 200)
        self.assertEqual(request(self.app, "POST", "/api/jobs/cleanup/runs"), (201, {
            "run": {"id": "run-001", "job_id": "cleanup", "source": "manual",
                    "status": "running"}
        }))
        self.assertEqual(request(self.app, "POST", "/api/runs/run-001/attempts",
                                 {"succeeded": False}), (200, {
            "status": "failed", "run": {"id": "run-001", "job_id": "cleanup",
                                        "source": "manual", "status": "failed"}
        }))
        self.assertEqual(request(self.app, "GET", "/api/alerts"), (200, {"alerts": [{
            "id": 1, "run_id": "run-001", "job_id": "cleanup", "kind": "run_failed",
            "message": "Job Cleanup failed for run run-001"
        }]}))

    def test_dashboard_preserves_values_and_shows_pause(self) -> None:
        for job_id, succeeded in (("cleanup", False), ("daily-report", True)):
            run = self.app.service.begin_manual_run(job_id)
            self.app.service.record_attempt(run.id, succeeded=succeeded)
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/pause")[0], 200)
        code, markup = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<th>Job</th><th>Enabled</th><th>Last result</th><th>Paused</th>", markup)
        self.assertIn("<tr><td>Cleanup</td><td>no</td><td>failed</td><td>no</td></tr>", markup)
        self.assertIn("<tr><td>Daily report</td><td>yes</td><td>succeeded</td><td>yes</td></tr>", markup)
        self.assertEqual(request(self.app, "POST", "/api/jobs/daily-report/resume")[0], 200)
        self.assertIn("<tr><td>Daily report</td><td>yes</td><td>succeeded</td><td>no</td></tr>",
                      request(self.app, "GET", "/dashboard")[1])


class PausePersistenceTests(unittest.TestCase):
    def test_pause_survives_reopening_file_database(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "relayboard.sqlite"
            connection = sqlite3.connect(database)
            store = Store(connection)
            self.assertFalse(store.add_job("persist", "Persist", enabled=False).paused)
            app = RelayBoardApp(store)
            self.assertEqual(request(app, "POST", "/api/jobs/persist/pause")[0], 200)
            connection.close()
            connection = sqlite3.connect(database)
            try:
                reopened = RelayBoardApp(Store(connection))
                self.assertEqual(request(reopened, "GET", "/api/jobs"), (200, {"jobs": [{
                    "id": "persist", "name": "Persist", "enabled": False,
                    "max_attempts": 1, "paused": True
                }]}))
                self.assertEqual(request(reopened, "POST", "/api/jobs/persist/resume"),
                                 (200, {"job": {"id": "persist", "name": "Persist",
                                               "enabled": False, "max_attempts": 1,
                                               "paused": False}}))
                self.assertEqual(request(reopened, "POST", "/api/jobs/persist/runs",
                                         {"source": "scheduled"}),
                                 (409, {"error": "job persist is disabled"}))
            finally:
                connection.close()

    def test_legacy_database_migration_keeps_jobs_and_history(self) -> None:
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.executescript("""
            CREATE TABLE jobs (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, enabled INTEGER NOT NULL,
                max_attempts INTEGER NOT NULL CHECK(max_attempts >= 1)
            );
            INSERT INTO jobs VALUES ('legacy', 'Legacy', 1, 2);
        """)
        app = RelayBoardApp(Store(connection))
        expected = {"id": "legacy", "name": "Legacy", "enabled": True,
                    "max_attempts": 2, "paused": False}
        self.assertEqual(request(app, "GET", "/api/jobs"), (200, {"jobs": [expected]}))
        run = app.service.begin_scheduled_run("legacy")
        self.assertEqual(app.service.record_attempt(run.id, succeeded=False), "retry")
        self.assertEqual(app.service.record_attempt(run.id, succeeded=True), "succeeded")
        self.assertEqual(request(app, "POST", "/api/jobs/legacy/pause")[0], 200)
        reopened = RelayBoardApp(Store(connection))
        self.assertEqual(request(reopened, "GET", "/api/jobs"), (200, {"jobs": [
            dict(expected, paused=True)
        ]}))
        self.assertEqual(reopened.store.get_run(run.id).status, "succeeded")
        self.assertEqual([(a.number, a.succeeded) for a in reopened.store.list_attempts(run.id)],
                         [(1, False), (2, True)])
        self.assertEqual(request(reopened, "GET", "/api/alerts"), (200, {"alerts": [{
            "id": 1, "run_id": "run-001", "job_id": "legacy", "kind": "run_failed",
            "message": "Job Legacy failed for run run-001"
        }]}))
        self.assertEqual(request(reopened, "POST", "/api/jobs/legacy/resume")[0], 200)
        self.assertEqual(reopened.service.begin_scheduled_run("legacy").id, "run-002")


if __name__ == "__main__":
    unittest.main()
