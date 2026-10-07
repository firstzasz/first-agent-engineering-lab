import sqlite3
import unittest

from relayboard.service import JobNotSchedulable
from relayboard.store import Store
from relayboard.testing import request
from relayboard.web import create_seeded_app


class PauseTests(unittest.TestCase):
    def setUp(self):
        self.app = create_seeded_app()

    def change_pause(self, action, job_id="daily-report"):
        return request(self.app, "POST", f"/api/jobs/{job_id}/{action}")

    def test_pause_blocks_scheduled_runs_until_resume(self):
        code, payload = self.change_pause("pause")
        self.assertEqual(code, 200)
        self.assertTrue(payload["job"]["paused"])
        self.assertTrue(payload["job"]["enabled"])
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("daily-report")
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs", {"source": "scheduled"}
        )
        self.assertEqual(code, 409)
        self.assertIn("paused", payload["error"])
        self.assertEqual(self.app.store.next_run_id(), "run-001")
        code, payload = self.change_pause("resume")
        self.assertEqual(code, 200)
        self.assertFalse(payload["job"]["paused"])
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs", {"source": "scheduled"}
        )
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["source"], "scheduled")

    def test_manual_runs_allowed_while_paused(self):
        self.assertEqual(self.change_pause("pause")[0], 200)
        code, payload = request(self.app, "POST", "/api/jobs/daily-report/runs")
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["source"], "manual")

    def test_existing_run_retries_and_alerts_unchanged(self):
        run = self.app.service.begin_scheduled_run("daily-report")
        self.assertEqual(self.change_pause("pause")[0], 200)
        code, payload = request(
            self.app, "POST", f"/api/runs/{run.id}/attempts", {"succeeded": False}
        )
        self.assertEqual(code, 200)
        self.assertEqual(payload["status"], "retry")
        self.assertEqual(payload["run"]["status"], "running")
        self.assertEqual(len(self.app.store.list_alerts()), 1)
        code, payload = request(
            self.app, "POST", f"/api/runs/{run.id}/attempts", {"succeeded": False}
        )
        self.assertEqual(code, 200)
        self.assertEqual(payload["run"]["id"], run.id)
        self.assertEqual(payload["status"], "failed")
        self.assertEqual(len(self.app.store.list_attempts(run.id)), 2)
        self.assertEqual(len(self.app.store.list_alerts()), 2)
        self.assertTrue(all(a.run_id == run.id for a in self.app.store.list_alerts()))

    def test_existing_run_can_succeed_while_paused(self):
        run = self.app.service.begin_manual_run("daily-report")
        self.assertEqual(self.change_pause("pause")[0], 200)
        self.assertEqual(self.app.service.record_attempt(run.id, succeeded=True), "succeeded")
        self.assertEqual(self.app.store.list_alerts(), [])

    def test_pause_and_enabled_are_independent(self):
        for action in ("pause", "resume"):
            code, payload = self.change_pause(action, "cleanup")
            self.assertEqual(code, 200)
            self.assertFalse(payload["job"]["enabled"])
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("cleanup")
        self.change_pause("pause", "cleanup")
        code, payload = request(
            self.app, "POST", "/api/jobs/cleanup/enabled", {"enabled": True}
        )
        self.assertEqual(code, 200)
        self.assertTrue(payload["job"]["paused"])
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("cleanup")
        self.change_pause("resume", "cleanup")
        self.assertEqual(self.app.service.begin_scheduled_run("cleanup").source, "scheduled")

    def test_endpoints_idempotent_and_missing_jobs_return_404(self):
        for action, paused in (("resume", False), ("pause", True), ("resume", False)):
            first = self.change_pause(action)
            self.assertEqual(first[0], 200)
            self.assertEqual(first[1]["job"]["paused"], paused)
            self.assertEqual(self.change_pause(action), first)
            code, payload = self.change_pause(action, "missing")
            self.assertEqual(code, 404)
            self.assertEqual(payload, {"error": "not found: missing"})
        self.assertEqual(self.app.store.next_run_id(), "run-001")
        self.assertEqual(self.app.store.list_alerts(), [])

    def test_list_and_dashboard_expose_pause_preserving_existing_fields(self):
        run = self.app.service.begin_manual_run("daily-report")
        self.app.service.record_attempt(run.id, succeeded=True)
        self.assertEqual(self.change_pause("pause")[0], 200)
        code, payload = request(self.app, "GET", "/api/jobs")
        self.assertEqual(code, 200)
        jobs = {job["id"]: job for job in payload["jobs"]}
        self.assertTrue(jobs["daily-report"]["paused"])
        self.assertFalse(jobs["cleanup"]["paused"])
        self.assertEqual(jobs["daily-report"]["max_attempts"], 2)
        code, markup = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<th>Enabled</th>", markup)
        self.assertIn("<th>Last result</th>", markup)
        self.assertIn("<th>Paused</th>", markup)
        self.assertIn("<td>Daily report</td><td>yes</td><td>yes</td><td>succeeded</td>", markup)

    def test_only_post_and_exact_paths_change_pause(self):
        for method, path in (
            ("GET", "/api/jobs/daily-report/pause"),
            ("POST", "/api/jobs/daily-report/nested/pause"),
            ("POST", "/api/jobs/daily-report/resume/extra"),
        ):
            self.assertEqual(request(self.app, method, path)[0], 404)
        self.assertFalse(self.app.store.get_job("daily-report").paused)

    def test_pause_survives_store_reopen(self):
        self.assertEqual(self.change_pause("pause")[0], 200)
        reopened = Store(self.app.store.connection)
        self.assertTrue(reopened.get_job("daily-report").paused)
        self.assertTrue(reopened.list_jobs()[1].paused)

    def test_old_schema_upgrades_with_unpaused_default(self):
        connection = sqlite3.connect(":memory:")
        connection.executescript(
            "CREATE TABLE jobs (id TEXT PRIMARY KEY, name TEXT NOT NULL, "
            "enabled INTEGER NOT NULL, max_attempts INTEGER NOT NULL);"
            "INSERT INTO jobs VALUES ('old', 'Old Job', 0, 3);"
        )
        store = Store(connection)
        job = store.get_job("old")
        self.assertFalse(job.paused)
        self.assertFalse(job.enabled)
        self.assertEqual(job.max_attempts, 3)
        self.assertEqual(store.list_jobs(), [job])
        store.set_job_paused("old", True)
        self.assertTrue(Store(connection).get_job("old").paused)


if __name__ == "__main__":
    unittest.main()
