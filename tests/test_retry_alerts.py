import unittest

from relayboard.service import RunAlreadyTerminal
from relayboard.testing import request
from relayboard.web import create_seeded_app


class RetryAlertTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_seeded_app()

    def begin_run(self, job_id="daily-report", source="manual"):
        code, body = request(
            self.app, "POST", f"/api/jobs/{job_id}/runs", {"source": source}
        )
        self.assertEqual(code, 201)
        return body["run"]["id"]

    def record_attempt(self, run_id, succeeded):
        code, body = request(
            self.app, "POST", f"/api/runs/{run_id}/attempts",
            {"succeeded": succeeded},
        )
        self.assertEqual(code, 200)
        self.assertEqual(body["run"]["id"], run_id)
        return body

    def alerts(self):
        code, body = request(self.app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        return body["alerts"]

    def test_retry_exhaustion_emits_only_one_terminal_alert(self):
        for max_attempts in (1, 2, 3):
            for source in ("manual", "scheduled"):
                with self.subTest(max_attempts=max_attempts, source=source):
                    self.app = create_seeded_app()
                    self.app.store.add_job(
                        "retry-job", "Retry job", max_attempts=max_attempts
                    )
                    run_id = self.begin_run("retry-job", source)
                    for _ in range(max_attempts - 1):
                        body = self.record_attempt(run_id, False)
                        self.assertEqual(body["status"], "retry")
                        self.assertEqual(body["run"]["status"], "running")
                        self.assertEqual(self.alerts(), [])
                    body = self.record_attempt(run_id, False)
                    self.assertEqual(body["status"], "failed")
                    self.assertEqual(body["run"]["status"], "failed")
                    alerts = self.alerts()
                    self.assertEqual(len(alerts), 1)
                    self.assertEqual(alerts[0]["run_id"], run_id)
                    self.assertEqual(alerts[0]["job_id"], "retry-job")
                    self.assertEqual(alerts[0]["kind"], "run_failed")
                    attempts = self.app.store.list_attempts(run_id)
                    self.assertEqual(
                        [a.number for a in attempts], list(range(1, max_attempts + 1))
                    )
                    self.assertTrue(all(not a.succeeded for a in attempts))
                    with self.assertRaises(RunAlreadyTerminal):
                        self.app.service.record_attempt(run_id, succeeded=False)
                    self.assertEqual(self.alerts(), alerts)
                    self.assertEqual(self.app.store.list_attempts(run_id), attempts)

    def test_success_after_retry_emits_no_failure_alert(self):
        run_id = self.begin_run()
        self.assertEqual(self.record_attempt(run_id, False)["status"], "retry")
        body = self.record_attempt(run_id, True)
        self.assertEqual(body["status"], "succeeded")
        self.assertEqual(body["run"]["status"], "succeeded")
        self.assertEqual(self.alerts(), [])
        self.assertEqual(
            [(a.number, a.succeeded) for a in self.app.store.list_attempts(run_id)],
            [(1, False), (2, True)],
        )

    def test_distinct_runs_of_same_job_each_emit_failure_alert(self):
        run_ids = [self.begin_run(source=source) for source in ("manual", "scheduled")]
        self.assertNotEqual(run_ids[0], run_ids[1])
        # Interleave attempts to ensure suppression cannot be scoped to the Job.
        for run_id in run_ids:
            self.assertEqual(self.record_attempt(run_id, False)["status"], "retry")
        for run_id in run_ids:
            self.assertEqual(self.record_attempt(run_id, False)["status"], "failed")
        alerts = self.alerts()
        self.assertEqual([alert["run_id"] for alert in alerts], run_ids)
        self.assertTrue(all(alert["job_id"] == "daily-report" for alert in alerts))


if __name__ == "__main__":
    unittest.main()
