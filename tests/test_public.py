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

    def test_pending_retries_do_not_emit_failure_alerts(self) -> None:
        self.app.store.add_job("retrying", "Retrying", max_attempts=3)
        code, payload = request(
            self.app, "POST", "/api/jobs/retrying/runs", {"source": "manual"}
        )
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]

        for number in (1, 2):
            code, payload = request(
                self.app,
                "POST",
                f"/api/runs/{run_id}/attempts",
                {"succeeded": False},
            )
            self.assertEqual(code, 200)
            self.assertEqual(payload["status"], "retry")
            self.assertEqual(payload["run"]["id"], run_id)
            self.assertEqual(payload["run"]["status"], "running")
            self.assertEqual(
                [(a.number, a.succeeded) for a in self.app.store.list_attempts(run_id)],
                [(n, False) for n in range(1, number + 1)],
            )
            code, payload = request(self.app, "GET", "/api/alerts")
            self.assertEqual(code, 200)
            self.assertEqual(payload, {"alerts": []})

    def test_exhausted_retries_emit_one_failure_alert(self) -> None:
        self.app.store.add_job("retrying", "Retrying", max_attempts=3)
        code, payload = request(
            self.app, "POST", "/api/jobs/retrying/runs", {"source": "scheduled"}
        )
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]

        for outcome, status in (
            ("retry", "running"),
            ("retry", "running"),
            ("failed", "failed"),
        ):
            code, payload = request(
                self.app,
                "POST",
                f"/api/runs/{run_id}/attempts",
                {"succeeded": False},
            )
            self.assertEqual(code, 200)
            self.assertEqual(payload["status"], outcome)
            self.assertEqual(payload["run"]["id"], run_id)
            self.assertEqual(payload["run"]["status"], status)

        self.assertEqual(
            [(a.number, a.succeeded) for a in self.app.store.list_attempts(run_id)],
            [(1, False), (2, False), (3, False)],
        )
        code, payload = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        self.assertEqual(
            [(a["run_id"], a["job_id"], a["kind"]) for a in payload["alerts"]],
            [(run_id, "retrying", "run_failed")],
        )

    def test_distinct_failed_runs_of_same_job_each_emit_alert(self) -> None:
        run_ids = []
        for source in ("manual", "scheduled"):
            code, payload = request(
                self.app, "POST", "/api/jobs/daily-report/runs", {"source": source}
            )
            self.assertEqual(code, 201)
            run_id = payload["run"]["id"]
            run_ids.append(run_id)
            for outcome, status in (("retry", "running"), ("failed", "failed")):
                code, payload = request(
                    self.app,
                    "POST",
                    f"/api/runs/{run_id}/attempts",
                    {"succeeded": False},
                )
                self.assertEqual(code, 200)
                self.assertEqual(payload["status"], outcome)
                self.assertEqual(payload["run"]["id"], run_id)
                self.assertEqual(payload["run"]["status"], status)

        self.assertNotEqual(run_ids[0], run_ids[1])
        code, payload = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        self.assertEqual(
            [(a["run_id"], a["job_id"], a["kind"]) for a in payload["alerts"]],
            [
                (run_ids[0], "daily-report", "run_failed"),
                (run_ids[1], "daily-report", "run_failed"),
            ],
        )

    def test_successful_retry_does_not_emit_failure_alert(self) -> None:
        code, payload = request(
            self.app, "POST", "/api/jobs/daily-report/runs", {"source": "manual"}
        )
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]

        for succeeded, outcome, status in (
            (False, "retry", "running"),
            (True, "succeeded", "succeeded"),
        ):
            code, payload = request(
                self.app,
                "POST",
                f"/api/runs/{run_id}/attempts",
                {"succeeded": succeeded},
            )
            self.assertEqual(code, 200)
            self.assertEqual(payload["status"], outcome)
            self.assertEqual(payload["run"]["id"], run_id)
            self.assertEqual(payload["run"]["status"], status)

        self.assertEqual(
            [(a.number, a.succeeded) for a in self.app.store.list_attempts(run_id)],
            [(1, False), (2, True)],
        )
        code, payload = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        self.assertEqual(payload, {"alerts": []})

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
