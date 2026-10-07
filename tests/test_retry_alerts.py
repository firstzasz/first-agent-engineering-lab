import unittest

from relayboard.service import RelayBoardService, RunAlreadyTerminal
from relayboard.store import Store


class RetryAlertTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = Store()
        self.service = RelayBoardService(self.store)

    def test_failure_alert_waits_for_exhausted_retries(self) -> None:
        for max_attempts in (1, 2, 4):
            with self.subTest(max_attempts=max_attempts):
                job = self.store.add_job(
                    f"retry-{max_attempts}",
                    "Retry job",
                    max_attempts=max_attempts,
                )
                run = self.service.begin_scheduled_run(job.id)
                alerts_before = len(self.store.list_alerts())

                for number in range(1, max_attempts):
                    self.assertEqual(
                        self.service.record_attempt(run.id, succeeded=False),
                        "retry",
                    )
                    self.assertEqual(self.store.get_run(run.id).status, "running")
                    self.assertEqual(len(self.store.list_alerts()), alerts_before)
                    attempts = self.store.list_attempts(run.id)
                    self.assertEqual(len(attempts), number)
                    self.assertEqual(attempts[-1].number, number)
                    self.assertEqual(attempts[-1].run_id, run.id)

                self.assertEqual(
                    self.service.record_attempt(run.id, succeeded=False),
                    "failed",
                )
                self.assertEqual(self.store.get_run(run.id).status, "failed")
                attempts = self.store.list_attempts(run.id)
                self.assertEqual(len(attempts), max_attempts)
                self.assertTrue(all(not attempt.succeeded for attempt in attempts))
                alerts = self.store.list_alerts()
                self.assertEqual(len(alerts), alerts_before + 1)
                self.assertEqual(alerts[-1].run_id, run.id)
                self.assertEqual(alerts[-1].job_id, job.id)
                self.assertEqual(alerts[-1].kind, "run_failed")

    def test_success_after_failed_attempts_has_no_failure_alert(self) -> None:
        self.store.add_job("retry", "Retry job", max_attempts=3)
        run = self.service.begin_manual_run("retry")

        for _ in range(2):
            self.assertEqual(
                self.service.record_attempt(run.id, succeeded=False), "retry"
            )
        self.assertEqual(
            self.service.record_attempt(run.id, succeeded=True), "succeeded"
        )

        self.assertEqual(self.store.get_run(run.id).status, "succeeded")
        self.assertEqual(
            [attempt.succeeded for attempt in self.store.list_attempts(run.id)],
            [False, False, True],
        )
        self.assertEqual(self.store.list_alerts(), [])

    def test_distinct_failed_runs_each_emit_an_alert(self) -> None:
        self.store.add_job("retry", "Retry job", max_attempts=2)
        self.store.add_job("other", "Other job", max_attempts=2)
        runs = [
            self.service.begin_manual_run("retry"),
            self.service.begin_scheduled_run("retry"),
            self.service.begin_manual_run("other"),
        ]

        # Interleave Runs to catch deduplication at the Job or global level.
        for run in runs:
            self.assertEqual(
                self.service.record_attempt(run.id, succeeded=False), "retry"
            )
        for run in runs:
            self.assertEqual(
                self.service.record_attempt(run.id, succeeded=False), "failed"
            )

        self.assertEqual(
            [alert.run_id for alert in self.store.list_alerts()],
            [run.id for run in runs],
        )

    def test_terminal_run_rejects_further_attempts_without_another_alert(self) -> None:
        self.store.add_job("retry", "Retry job", max_attempts=2)
        run = self.service.begin_manual_run("retry")
        self.service.record_attempt(run.id, succeeded=False)
        self.service.record_attempt(run.id, succeeded=False)
        alerts = self.store.list_alerts()
        attempts = self.store.list_attempts(run.id)

        with self.assertRaises(RunAlreadyTerminal):
            self.service.record_attempt(run.id, succeeded=False)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(self.store.list_alerts(), alerts)
        self.assertEqual(self.store.list_attempts(run.id), attempts)


if __name__ == "__main__":
    unittest.main()
