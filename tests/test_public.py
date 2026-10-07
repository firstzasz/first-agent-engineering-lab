import unittest

from relayboard.service import JobNotSchedulable
from relayboard.testing import request
from relayboard.web import create_seeded_app


class RelayBoardPublicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_seeded_app()

    def test_dashboard_has_jobs_table(self) -> None:
        code, body = request(
            self.app,
            "GET",
            "/dashboard",
        )
        self.assertEqual(code, 200)
        self.assertIn("Daily report", body)

    def test_disabled_job_blocks_scheduled_run(self) -> None:
        with self.assertRaises(JobNotSchedulable):
            self.app.service.begin_scheduled_run("cleanup")

    def test_disabled_job_still_allows_manual_run(self) -> None:
        run = self.app.service.begin_manual_run("cleanup")
        self.assertEqual(run.source, "manual")
        self.assertEqual(run.status, "running")

    def test_single_attempt_failure_emits_one_alert(self) -> None:
        run = self.app.service.begin_manual_run("cleanup")
        state = self.app.service.record_attempt(
            run.id,
            succeeded=False,
        )
        self.assertEqual(state, "failed")

        alerts = self.app.store.list_alerts()
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].run_id, run.id)

    def test_api_can_create_run_and_record_attempt(self) -> None:
        code, payload = request(
            self.app,
            "POST",
            "/api/jobs/daily-report/runs",
            {"source": "manual"},
        )
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]

        code, payload = request(
            self.app,
            "POST",
            f"/api/runs/{run_id}/attempts",
            {"succeeded": True},
        )
        self.assertEqual(code, 200)
        self.assertEqual(
            payload["run"]["status"],
            "succeeded",
        )

    def test_retrying_run_alerts_only_after_terminal_failure(self) -> None:
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs", {}
        )
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]

        code, payload = request(
            self.app, "POST", f"/api/runs/{run_id}/attempts",
            {"succeeded": False},
        )
        self.assertEqual(code, 200)
        self.assertEqual(payload["status"], "retry")
        self.assertEqual(payload["run"]["status"], "running")
        code, payload = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        self.assertEqual(payload["alerts"], [])

        code, payload = request(
            self.app, "POST", f"/api/runs/{run_id}/attempts",
            {"succeeded": False},
        )
        self.assertEqual(code, 200)
        self.assertEqual(payload["status"], "failed")
        self.assertEqual(payload["run"]["status"], "failed")
        code, payload = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        self.assertEqual(len(payload["alerts"]), 1)
        self.assertEqual(payload["alerts"][0]["run_id"], run_id)
        self.assertEqual(payload["alerts"][0]["kind"], "run_failed")

    def test_distinct_failed_runs_each_emit_an_alert(self) -> None:
        manual = self.app.service.begin_manual_run("daily-report")
        scheduled = self.app.service.begin_scheduled_run("daily-report")
        self.assertNotEqual(manual.id, scheduled.id)

        for run in (manual, scheduled):
            self.assertEqual(
                self.app.service.record_attempt(run.id, succeeded=False),
                "retry",
            )
            self.assertEqual(
                self.app.service.record_attempt(run.id, succeeded=False),
                "failed",
            )
            self.assertEqual(
                [attempt.number for attempt in self.app.store.list_attempts(run.id)],
                [1, 2],
            )

        alerts = self.app.store.list_alerts()
        self.assertEqual([alert.run_id for alert in alerts], [manual.id, scheduled.id])
        self.assertEqual([alert.kind for alert in alerts], ["run_failed", "run_failed"])

    def test_run_succeeding_after_multiple_retries_emits_no_failure_alert(self) -> None:
        self.app.store.add_job("three-attempts", "Three attempts", max_attempts=3)
        run = self.app.service.begin_manual_run("three-attempts")
        self.assertEqual(
            self.app.service.record_attempt(run.id, succeeded=False), "retry"
        )
        self.assertEqual(
            self.app.service.record_attempt(run.id, succeeded=False), "retry"
        )
        self.assertEqual(
            self.app.service.record_attempt(run.id, succeeded=True), "succeeded"
        )
        self.assertEqual(self.app.store.get_run(run.id).status, "succeeded")
        self.assertEqual(
            [(attempt.number, attempt.succeeded)
             for attempt in self.app.store.list_attempts(run.id)],
            [(1, False), (2, False), (3, True)],
        )
        self.assertEqual(self.app.store.list_alerts(), [])


if __name__ == "__main__":
    unittest.main()
