import unittest

from relayboard.service import RelayBoardService, RunAlreadyTerminal
from relayboard.store import Store
from relayboard.testing import request
from relayboard.web import create_seeded_app


class RetryAlertTests(unittest.TestCase):
    def test_failure_alert_waits_for_terminal_attempt(self) -> None:
        for budget in (1, 2, 4):
            for source in ("manual", "scheduled"):
                with self.subTest(budget=budget, source=source):
                    store = Store()
                    store.add_job("job", "Test job", max_attempts=budget)
                    service = RelayBoardService(store)
                    if source == "manual":
                        run = service.begin_manual_run("job")
                    else:
                        run = service.begin_scheduled_run("job")

                    for number in range(1, budget + 1):
                        result = service.record_attempt(run.id, succeeded=False)
                        if number < budget:
                            self.assertEqual(result, "retry")
                            self.assertEqual(store.get_run(run.id).status, "running")
                            self.assertEqual(store.list_alerts(), [])
                        else:
                            self.assertEqual(result, "failed")
                            self.assertEqual(store.get_run(run.id).status, "failed")
                            alerts = store.list_alerts()
                            self.assertEqual(len(alerts), 1)
                            self.assertEqual(alerts[0].run_id, run.id)
                            self.assertEqual(alerts[0].job_id, "job")
                            self.assertEqual(alerts[0].kind, "run_failed")

                    attempts = store.list_attempts(run.id)
                    self.assertEqual([a.number for a in attempts], list(range(1, budget + 1)))
                    self.assertTrue(all(not a.succeeded for a in attempts))
                    with self.assertRaises(RunAlreadyTerminal):
                        service.record_attempt(run.id, succeeded=False)
                    self.assertEqual(len(store.list_attempts(run.id)), budget)
                    self.assertEqual(len(store.list_alerts()), 1)

    def test_success_after_retries_emits_no_failure_alert(self) -> None:
        for budget in (2, 4):
            for success_number in range(1, budget + 1):
                with self.subTest(budget=budget, success_number=success_number):
                    store = Store()
                    store.add_job("job", "Test job", max_attempts=budget)
                    service = RelayBoardService(store)
                    run = service.begin_manual_run("job")

                    for _ in range(success_number - 1):
                        self.assertEqual(service.record_attempt(run.id, succeeded=False), "retry")
                    self.assertEqual(service.record_attempt(run.id, succeeded=True), "succeeded")
                    self.assertEqual(store.get_run(run.id).status, "succeeded")
                    self.assertEqual(len(store.list_attempts(run.id)), success_number)
                    self.assertEqual(store.list_alerts(), [])

    def test_distinct_failed_runs_keep_their_own_alerts_via_api(self) -> None:
        app = create_seeded_app()
        failed_run_ids = []
        # Same job and different jobs, including interleaved retries, must alert independently.
        for job_id, source in (
            ("daily-report", "manual"),
            ("daily-report", "scheduled"),
            ("cleanup", "manual"),
        ):
            code, payload = request(
                app, "POST", f"/api/jobs/{job_id}/runs", {"source": source}
            )
            self.assertEqual(code, 201)
            failed_run_ids.append(payload["run"]["id"])

        for run_id in failed_run_ids[:2]:
            code, payload = request(
                app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False}
            )
            self.assertEqual(code, 200)
            self.assertEqual(payload["status"], "retry")
            self.assertEqual(payload["run"]["status"], "running")
        code, payload = request(app, "GET", "/api/alerts")
        self.assertEqual(code, 200)
        self.assertEqual(payload["alerts"], [])

        for completed_count, run_id in enumerate(failed_run_ids, start=1):
            code, payload = request(
                app, "POST", f"/api/runs/{run_id}/attempts", {"succeeded": False}
            )
            self.assertEqual(code, 200)
            self.assertEqual(payload["status"], "failed")
            self.assertEqual(payload["run"]["status"], "failed")
            code, payload = request(app, "GET", "/api/alerts")
            self.assertEqual(code, 200)
            self.assertEqual(
                [a["run_id"] for a in payload["alerts"]],
                failed_run_ids[:completed_count],
            )


if __name__ == "__main__":
    unittest.main()
