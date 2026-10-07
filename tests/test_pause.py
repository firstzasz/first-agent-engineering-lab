import sqlite3
import unittest

from relayboard.service import JobNotSchedulable, RelayBoardService
from relayboard.store import Store
from relayboard.testing import request
from relayboard.web import create_seeded_app


class PauseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_seeded_app()

    def test_pause_resume_blocks_only_new_scheduled_runs(self) -> None:
        run = self.app.service.begin_scheduled_run("daily-report")
        job = self.app.service.pause_job("daily-report")
        self.assertTrue(job.paused)
        self.assertTrue(job.enabled)
        with self.assertRaisesRegex(JobNotSchedulable, "paused"):
            self.app.service.begin_scheduled_run(job.id)
        manual = self.app.service.begin_manual_run(job.id)
        self.assertEqual(manual.source, "manual")
        self.assertEqual(self.app.store.get_run(run.id).status, "running")
        self.assertEqual(
            self.app.service.record_attempt(run.id, succeeded=True), "succeeded"
        )
        self.assertFalse(self.app.service.resume_job(job.id).paused)
        self.assertEqual(
            self.app.service.begin_scheduled_run(job.id).source, "scheduled"
        )

    def test_enabled_and_paused_are_independent(self) -> None:
        self.app.service.pause_job("cleanup")
        self.app.service.resume_job("cleanup")
        self.assertFalse(self.app.store.get_job("cleanup").enabled)
        with self.assertRaisesRegex(JobNotSchedulable, "disabled"):
            self.app.service.begin_scheduled_run("cleanup")
        self.app.service.pause_job("daily-report")
        self.app.service.set_job_enabled("daily-report", False)
        self.app.service.set_job_enabled("daily-report", True)
        self.assertTrue(self.app.store.get_job("daily-report").paused)
        with self.assertRaisesRegex(JobNotSchedulable, "paused"):
            self.app.service.begin_scheduled_run("daily-report")

    def test_pause_preserves_retry_and_alert_behavior(self) -> None:
        def outcomes(paused):
            app = create_seeded_app()
            run = app.service.begin_scheduled_run("daily-report")
            if paused:
                app.service.pause_job("daily-report")
            statuses = [
                app.service.record_attempt(run.id, succeeded=False),
                app.service.record_attempt(run.id, succeeded=False),
            ]
            return (
                statuses,
                app.store.get_run(run.id),
                app.store.list_attempts(run.id),
                app.store.list_alerts(),
                app.store.last_result_for_job("daily-report"),
            )

        self.assertEqual(outcomes(True), outcomes(False))

    def test_api_pause_resume_and_list_jobs(self) -> None:
        code, payload = request(self.app, "GET", "/api/jobs")
        self.assertEqual(code, 200)
        self.assertTrue(all(not job["paused"] for job in payload["jobs"]))
        for action, paused in [("pause", True), ("resume", False)]:
            for _ in range(2):
                code, payload = request(
                    self.app, "POST", f"/api/jobs/daily-report/{action}"
                )
                self.assertEqual(code, 200)
                self.assertEqual(payload["job"]["paused"], paused)
                self.assertTrue(payload["job"]["enabled"])
            code, listing = request(self.app, "GET", "/api/jobs")
            self.assertEqual(code, 200)
            listed = next(j for j in listing["jobs"] if j["id"] == "daily-report")
            self.assertEqual(listed, payload["job"])
            code, run_payload = request(
                self.app, "POST", "/api/jobs/daily-report/runs",
                {"source": "scheduled"},
            )
            self.assertEqual(code, 409 if paused else 201)
            if paused:
                self.assertIn("paused", run_payload["error"])
                code, _ = request(
                    self.app, "POST", "/api/jobs/daily-report/runs"
                )
                self.assertEqual(code, 201)

    def test_missing_jobs_and_invalid_pause_routes(self) -> None:
        for action in ("pause", "resume"):
            code, payload = request(self.app, "POST", f"/api/jobs/missing/{action}")
            self.assertEqual(code, 404)
            self.assertEqual(payload, {"error": "not found: missing"})
            for method, path in [
                ("GET", f"/api/jobs/daily-report/{action}"),
                ("POST", f"/api/jobs/daily-report/extra/{action}"),
            ]:
                self.assertEqual(request(self.app, method, path)[0], 404)
        self.assertFalse(self.app.store.get_job("daily-report").paused)

    def test_dashboard_keeps_enabled_and_last_result_and_shows_pause(self) -> None:
        run = self.app.service.begin_manual_run("daily-report")
        self.app.service.record_attempt(run.id, succeeded=True)
        self.app.service.pause_job("daily-report")
        code, dashboard = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<th>Paused</th>", dashboard)
        self.assertIn(
            "<td>Daily report</td><td>yes</td><td>yes</td><td>succeeded</td>",
            dashboard,
        )
        self.app.service.resume_job("daily-report")
        self.assertIn(
            "<td>Daily report</td><td>yes</td><td>no</td><td>succeeded</td>",
            self.app.render_dashboard(),
        )

    def test_pause_is_stored_and_survives_store_reinitialization(self) -> None:
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        store = Store(connection)
        store.add_job("job", "Job")
        RelayBoardService(store).pause_job("job")
        reopened = Store(connection)
        self.assertTrue(reopened.get_job("job").paused)
        self.assertTrue(reopened.list_jobs()[0].paused)
        RelayBoardService(reopened).resume_job("job")
        self.assertFalse(store.get_job("job").paused)

    def test_legacy_schema_defaults_to_unpaused(self) -> None:
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.executescript(
            "CREATE TABLE jobs (id TEXT PRIMARY KEY, name TEXT NOT NULL, "
            "enabled INTEGER NOT NULL, max_attempts INTEGER NOT NULL);"
            "INSERT INTO jobs VALUES ('legacy', 'Legacy', 0, 2);"
        )
        store = Store(connection)
        job = store.get_job("legacy")
        self.assertFalse(job.paused)
        self.assertFalse(job.enabled)
        self.assertEqual(job.max_attempts, 2)
        RelayBoardService(store).pause_job(job.id)
        self.assertTrue(store.get_job(job.id).paused)
