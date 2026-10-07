import sqlite3
import unittest

from relayboard.models import Job
from relayboard.service import JobNotSchedulable
from relayboard.store import Store
from relayboard.testing import request
from relayboard.web import RelayBoardApp, create_seeded_app


class JobPauseTests(unittest.TestCase):
    def setUp(self):
        self.app = create_seeded_app()

    def action(self, job_id, action):
        return request(self.app, "POST", f"/api/jobs/{job_id}/{action}")

    def test_pause_skips_scheduled_start_and_resume_does_not_queue_work(self):
        for _ in range(2):
            code, payload = self.action("daily-report", "pause")
            self.assertEqual(code, 200)
            self.assertTrue(payload["job"]["paused"])
            self.assertTrue(payload["job"]["enabled"])
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs", {"source": "scheduled"}
        )
        self.assertEqual(code, 409)
        self.assertIn("paused", payload["error"])
        self.assertEqual(self.app.store.connection.execute("SELECT COUNT(*) FROM runs").fetchone()[0], 0)
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("daily-report")
        for _ in range(2):
            code, payload = self.action("daily-report", "resume")
            self.assertEqual(code, 200)
            self.assertFalse(payload["job"]["paused"])
        self.assertEqual(self.app.store.connection.execute("SELECT COUNT(*) FROM runs").fetchone()[0], 0)
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs", {"source": "scheduled"}
        )
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["id"], "run-001")
        self.assertEqual(payload["run"]["source"], "scheduled")

    def test_pause_allows_manual_run_and_preserves_disabled_state(self):
        for job_id in ("daily-report", "cleanup"):
            before = self.app.store.get_job(job_id)
            self.assertEqual(self.action(job_id, "pause")[0], 200)
            code, payload = request(self.app, "POST", f"/api/jobs/{job_id}/runs")
            self.assertEqual(code, 201)
            self.assertEqual(payload["run"]["source"], "manual")
            self.assertEqual(self.action(job_id, "resume")[0], 200)
            self.assertEqual(self.app.store.get_job(job_id).enabled, before.enabled)
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("cleanup")

    def test_enabled_changes_do_not_clear_pause(self):
        self.assertEqual(self.action("daily-report", "pause")[0], 200)
        for enabled in (False, True):
            code, payload = request(
                self.app, "POST", "/api/jobs/daily-report/enabled", {"enabled": enabled}
            )
            self.assertEqual(code, 200)
            self.assertEqual(payload["job"]["enabled"], enabled)
            self.assertTrue(payload["job"]["paused"])
            with self.assertRaises(JobNotSchedulable):
                self.app.service.begin_scheduled_run("daily-report")

    def test_active_runs_retries_and_alerts_match_unpaused_behavior(self):
        for outcomes in ((False, True), (False, False)):
            with self.subTest(outcomes=outcomes):
                reference = create_seeded_app()
                paused = create_seeded_app()
                run1 = reference.service.begin_scheduled_run("daily-report")
                run2 = paused.service.begin_scheduled_run("daily-report")
                code, _ = request(paused, "POST", "/api/jobs/daily-report/pause")
                self.assertEqual(code, 200)
                self.assertEqual(paused.store.get_run(run2.id).status, "running")
                for outcome in outcomes:
                    expected = request(reference, "POST", f"/api/runs/{run1.id}/attempts", {"succeeded": outcome})
                    actual = request(paused, "POST", f"/api/runs/{run2.id}/attempts", {"succeeded": outcome})
                    self.assertEqual(actual, expected)
                    self.assertEqual(paused.store.list_alerts(), reference.store.list_alerts())
                self.assertEqual(paused.store.list_attempts(run2.id), reference.store.list_attempts(run1.id))
                self.assertEqual(paused.store.last_result_for_job("daily-report"), reference.store.last_result_for_job("daily-report"))

    def test_pause_state_visible_and_last_result_preserved(self):
        run = self.app.service.begin_manual_run("daily-report")
        self.app.service.record_attempt(run.id, succeeded=True)
        self.assertEqual(self.action("daily-report", "pause")[0], 200)
        code, payload = request(self.app, "GET", "/api/jobs")
        self.assertEqual(code, 200)
        job = next(job for job in payload["jobs"] if job["id"] == "daily-report")
        self.assertTrue(job["paused"])
        code, markup = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<th>Enabled</th>", markup)
        self.assertIn("<th>Paused</th>", markup)
        self.assertIn("<th>Last result</th>", markup)
        self.assertIn("<td>Daily report</td><td>yes</td><td>yes</td><td>succeeded</td>", markup)
        self.assertEqual(self.action("daily-report", "resume")[0], 200)
        self.assertEqual(self.app.store.last_result_for_job("daily-report"), "succeeded")

    def test_unknown_job_actions_follow_not_found_convention(self):
        for action in ("pause", "resume"):
            code, payload = self.action("missing", action)
            self.assertEqual(code, 404)
            self.assertEqual(payload, {"error": "not found: missing"})
        self.assertEqual(request(self.app, "GET", "/api/jobs/daily-report/pause")[0], 404)

    def test_state_survives_store_reconstruction(self):
        connection = sqlite3.connect(":memory:")
        app = RelayBoardApp(Store(connection))
        app.store.add_job("saved", "Saved", enabled=False)
        self.assertEqual(request(app, "POST", "/api/jobs/saved/pause")[0], 200)
        reconstructed = RelayBoardApp(Store(connection))
        self.assertTrue(reconstructed.store.get_job("saved").paused)
        self.assertFalse(reconstructed.store.get_job("saved").enabled)
        self.assertEqual(request(reconstructed, "POST", "/api/jobs/saved/resume")[0], 200)
        self.assertFalse(app.store.get_job("saved").paused)
        self.assertFalse(app.store.get_job("saved").enabled)

    def test_existing_schema_defaults_to_unpaused_and_preserves_configuration(self):
        connection = sqlite3.connect(":memory:")
        connection.execute("CREATE TABLE jobs (id TEXT PRIMARY KEY, name TEXT NOT NULL, enabled INTEGER NOT NULL, max_attempts INTEGER NOT NULL)")
        connection.execute("INSERT INTO jobs VALUES ('legacy', 'Legacy', 0, 3)")
        connection.commit()
        store = Store(connection)
        job = store.get_job("legacy")
        self.assertFalse(job.paused)
        self.assertFalse(job.enabled)
        self.assertEqual(job.max_attempts, 3)
        self.assertEqual(store.list_jobs(), [job])
        self.assertFalse(Job("old", "Old", True, 1).paused)


if __name__ == "__main__":
    unittest.main()
