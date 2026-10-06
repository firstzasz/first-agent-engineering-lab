import unittest

from relayboard.service import JobNotSchedulable
from relayboard.testing import request
from relayboard.web import create_seeded_app


class RelayBoardPublicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_seeded_app()

    def test_dashboard_has_jobs_table_and_current_heading(self) -> None:
        code, body = request(
            self.app,
            "GET",
            "/dashboard",
        )
        self.assertEqual(code, 200)
        self.assertIn("<th>Last result</th>", body)
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


if __name__ == "__main__":
    unittest.main()
