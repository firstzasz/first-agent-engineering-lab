import unittest

from relayboard.testing import request
from relayboard.web import create_seeded_app


class CancelRunPublicTests(unittest.TestCase):
    def test_cancel_running_run_blocks_further_attempts(self) -> None:
        app = create_seeded_app()

        code, payload = request(
            app,
            "POST",
            "/api/jobs/daily-report/runs",
            {"source": "manual"},
        )
        self.assertEqual(code, 201)
        run_id = payload["run"]["id"]

        code, payload = request(
            app,
            "POST",
            f"/api/runs/{run_id}/cancel",
            {},
        )
        self.assertEqual(code, 200)
        self.assertEqual(payload["run"]["status"], "cancelled")

        code, _ = request(
            app,
            "POST",
            f"/api/runs/{run_id}/attempts",
            {"succeeded": True},
        )
        self.assertEqual(code, 409)


if __name__ == "__main__":
    unittest.main()
