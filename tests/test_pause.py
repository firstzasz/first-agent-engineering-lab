import sqlite3
import unittest

from relayboard import JobNotSchedulable, RelayBoardService, Store
from relayboard.testing import request
from relayboard.web import create_seeded_app


class PauseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_seeded_app()

    def test_pause_resume_api_is_idempotent_and_reports_state(self) -> None:
        for action, paused in (
            ("pause", True), ("pause", True),
            ("resume", False), ("resume", False),
        ):
            with self.subTest(action=action, paused=paused):
                code, payload = request(
                    self.app, "POST", f"/api/jobs/daily-report/{action}"
                )
                self.assertEqual(code, 200)
                self.assertEqual(payload["job"], {
                    "id": "daily-report", "name": "Daily report",
                    "enabled": True, "max_attempts": 2, "paused": paused,
                })
                code, listed = request(self.app, "GET", "/api/jobs")
                self.assertEqual(code, 200)
                self.assertIn(payload["job"], listed["jobs"])

    def test_scheduled_starts_are_skipped_until_resume_without_queuing(self) -> None:
        self.app.service.pause_job("daily-report")
        for _ in range(2):
            code, payload = request(
                self.app, "POST", "/api/jobs/daily-report/runs",
                {"source": "scheduled"},
            )
            self.assertEqual(code, 409)
            self.assertEqual(payload, {"error": "job daily-report is paused"})
        self.assertEqual(self.app.store.next_run_id(), "run-001")
        self.assertEqual(self.app.store.list_alerts(), [])
        self.app.service.resume_job("daily-report")
        self.assertEqual(self.app.store.next_run_id(), "run-001")
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs",
            {"source": "scheduled"},
        )
        self.assertEqual(code, 201)
        self.assertEqual(payload["run"]["id"], "run-001")
        self.assertEqual(payload["run"]["source"], "scheduled")

    def test_pause_is_per_job(self) -> None:
        self.app.store.add_job("other", "Other")
        self.app.service.pause_job("daily-report")
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("daily-report")
        self.assertEqual(
            self.app.service.begin_scheduled_run("other").job_id, "other"
        )

    def test_paused_jobs_allow_manual_runs_even_when_disabled(self) -> None:
        for job_id in ("daily-report", "cleanup"):
            with self.subTest(job_id=job_id):
                self.app.service.pause_job(job_id)
                code, payload = request(
                    self.app, "POST", f"/api/jobs/{job_id}/runs"
                )
                self.assertEqual(code, 201)
                self.assertEqual(payload["run"]["source"], "manual")
                self.assertEqual(payload["run"]["status"], "running")

    def test_pause_resume_preserves_enabled_and_retry_policy(self) -> None:
        for job_id in ("daily-report", "cleanup"):
            with self.subTest(job_id=job_id):
                before = self.app.store.get_job(job_id)
                paused = self.app.service.pause_job(job_id)
                self.assertEqual(paused.enabled, before.enabled)
                resumed = self.app.service.resume_job(job_id)
                self.assertEqual(resumed, before)
                if not before.enabled:
                    with self.assertRaises(JobNotSchedulable):
                        self.app.service.begin_scheduled_run(job_id)

    def test_enabled_changes_do_not_clear_pause(self) -> None:
        self.app.service.pause_job("cleanup")
        code, payload = request(
            self.app, "POST", "/api/jobs/cleanup/enabled", {"enabled": True}
        )
        self.assertEqual(code, 200)
        self.assertTrue(payload["job"]["paused"])
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("cleanup")
        self.app.service.set_job_enabled("cleanup", False)
        self.app.service.resume_job("cleanup")
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("cleanup")

    def test_existing_runs_retries_alerts_and_results_are_preserved(self) -> None:
        for final_success in (True, False):
            with self.subTest(final_success=final_success):
                snapshots = []
                for paused in (False, True):
                    app = create_seeded_app()
                    run = app.service.begin_scheduled_run("daily-report")
                    if paused:
                        app.service.pause_job("daily-report")
                    outcomes = [
                        app.service.record_attempt(run.id, succeeded=False),
                        app.service.record_attempt(run.id, succeeded=final_success),
                    ]
                    snapshots.append((
                        outcomes, app.store.get_run(run.id),
                        app.store.list_attempts(run.id),
                        app.store.list_alerts(),
                        app.store.last_result_for_job("daily-report"),
                    ))
                self.assertEqual(snapshots[0], snapshots[1])
                self.assertEqual(snapshots[1][0], [
                    "retry", "succeeded" if final_success else "failed"
                ])

    def test_missing_jobs_and_invalid_routes_follow_api_conventions(self) -> None:
        for action in ("pause", "resume"):
            code, payload = request(
                self.app, "POST", f"/api/jobs/missing/{action}"
            )
            self.assertEqual(code, 404)
            self.assertEqual(payload, {"error": "not found: missing"})
            code, _ = request(
                self.app, "GET", f"/api/jobs/daily-report/{action}"
            )
            self.assertEqual(code, 404)
            code, _ = request(
                self.app, "POST", f"/api/jobs/daily-report/extra/{action}"
            )
            self.assertEqual(code, 404)
        self.assertFalse(self.app.store.get_job("daily-report").paused)

    def test_dashboard_shows_pause_and_preserves_last_result(self) -> None:
        run = self.app.service.begin_manual_run("daily-report")
        self.app.service.record_attempt(run.id, succeeded=True)
        self.app.service.pause_job("daily-report")
        code, body = request(self.app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertIn("<th>Enabled</th><th>Paused</th><th>Last result</th>", body)
        self.assertIn(
            "<td>Daily report</td><td>yes</td><td>yes</td><td>succeeded</td>", body
        )
        self.app.service.resume_job("daily-report")
        self.assertIn(
            "<td>Daily report</td><td>yes</td><td>no</td><td>succeeded</td>",
            self.app.render_dashboard(),
        )

    def test_pause_state_is_stored_across_store_reconstruction(self) -> None:
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        store = Store(connection)
        store.add_job("persisted", "Persisted")
        RelayBoardService(store).pause_job("persisted")
        restored = Store(connection)
        self.assertTrue(restored.get_job("persisted").paused)
        with self.assertRaises(JobNotSchedulable):
            RelayBoardService(restored).begin_scheduled_run("persisted")
        RelayBoardService(restored).resume_job("persisted")
        self.assertFalse(Store(connection).get_job("persisted").paused)

    def test_legacy_schema_migrates_existing_jobs_without_data_loss(self) -> None:
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.executescript("""
            CREATE TABLE jobs (
                id TEXT PRIMARY KEY, name TEXT NOT NULL,
                enabled INTEGER NOT NULL, max_attempts INTEGER NOT NULL
            );
            INSERT INTO jobs VALUES ('legacy', 'Legacy', 0, 3);
        """)
        store = Store(connection)
        job = store.get_job("legacy")
        self.assertFalse(job.paused)
        self.assertFalse(job.enabled)
        self.assertEqual(job.max_attempts, 3)
        self.assertEqual(job.name, "Legacy")
        RelayBoardService(store).pause_job("legacy")
        self.assertTrue(Store(connection).get_job("legacy").paused)


if __name__ == "__main__":
    unittest.main()
