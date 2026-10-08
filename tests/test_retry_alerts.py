import unittest

from relayboard.service import RelayBoardService, RunAlreadyTerminal
from relayboard.store import Store
from relayboard.testing import request
from relayboard.web import create_seeded_app


class RetryAlertTests(unittest.TestCase):
    def test_failure_alert_waits_for_retry_exhaustion(self) -> None:
        for max_attempts in (1, 2, 4):
            for source in ("manual", "scheduled"):
                with self.subTest(max_attempts=max_attempts, source=source):
                    store = Store()
                    store.add_job("report", "Report", max_attempts=max_attempts)
                    service = RelayBoardService(store)
                    begin = (
                        service.begin_manual_run
                        if source == "manual"
                        else service.begin_scheduled_run
                    )
                    run = begin("report")

                    for number in range(1, max_attempts + 1):
                        result = service.record_attempt(run.id, succeeded=False)
                        exhausted = number == max_attempts
                        self.assertEqual(result, "failed" if exhausted else "retry")
                        self.assertEqual(
                            store.get_run(run.id).status,
                            "failed" if exhausted else "running",
                        )
                        attempts = store.list_attempts(run.id)
                        self.assertEqual(
                            [attempt.number for attempt in attempts],
                            list(range(1, number + 1)),
                        )
                        self.assertTrue(all(not attempt.succeeded for attempt in attempts))
                        self.assertEqual(len(store.list_alerts()), int(exhausted))

                    alert = store.list_alerts()[0]
                    self.assertEqual(alert.run_id, run.id)
                    self.assertEqual(alert.job_id, "report")
                    self.assertEqual(alert.kind, "run_failed")
                    self.assertEqual(alert.message, f"Job Report failed for run {run.id}")
                    with self.assertRaises(RunAlreadyTerminal):
                        service.record_attempt(run.id, succeeded=False)
                    self.assertEqual(len(store.list_attempts(run.id)), max_attempts)
                    self.assertEqual(len(store.list_alerts()), 1)

    def test_success_after_retries_emits_no_failure_alert(self) -> None:
        for success_number in (1, 2, 4):
            with self.subTest(success_number=success_number):
                store = Store()
                store.add_job("report", "Report", max_attempts=4)
                service = RelayBoardService(store)
                run = service.begin_manual_run("report")

                for _ in range(success_number - 1):
                    self.assertEqual(
                        service.record_attempt(run.id, succeeded=False), "retry"
                    )
                self.assertEqual(service.record_attempt(run.id, succeeded=True), "succeeded")
                self.assertEqual(store.get_run(run.id).status, "succeeded")
                self.assertEqual(
                    [attempt.succeeded for attempt in store.list_attempts(run.id)],
                    [False] * (success_number - 1) + [True],
                )
                self.assertEqual(store.list_alerts(), [])
                with self.assertRaises(RunAlreadyTerminal):
                    service.record_attempt(run.id, succeeded=False)
                self.assertEqual(store.list_alerts(), [])

    def test_distinct_runs_of_same_job_each_emit_an_alert(self) -> None:
        store = Store()
        store.add_job("report", "Report", max_attempts=2)
        service = RelayBoardService(store)
        runs = [service.begin_manual_run("report"), service.begin_scheduled_run("report")]

        for run in runs:
            self.assertEqual(service.record_attempt(run.id, succeeded=False), "retry")
        self.assertEqual(store.list_alerts(), [])
        for number, run in enumerate(runs, start=1):
            self.assertEqual(service.record_attempt(run.id, succeeded=False), "failed")
            self.assertEqual(len(store.list_alerts()), number)
            self.assertEqual(len(store.list_attempts(run.id)), 2)
        self.assertEqual([alert.run_id for alert in store.list_alerts()], [run.id for run in runs])

    def test_api_reports_retry_before_emitting_terminal_alert(self) -> None:
        app = create_seeded_app()
        code, payload = request(app, "POST", "/api/jobs/daily-report/runs", {})
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]

        for expected, run_status, alert_count in (("retry", "running", 0), ("failed", "failed", 1)):
            code, payload = request(
                app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False}
            )
            self.assertEqual(code, 200)
            self.assertEqual(payload["status"], expected)
            self.assertEqual(payload["run"]["status"], run_status)
            code, payload = request(app, "GET", "/api/alerts")
            self.assertEqual(code, 200)
            self.assertEqual(len(payload["alerts"]), alert_count)
        self.assertEqual(payload["alerts"][0]["run_id"], run_id)


if __name__ == "__main__":
    unittest.main()
