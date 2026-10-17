import unittest

from relayboard.testing import request
from relayboard.web import create_seeded_app


class ArchiveJobPublicTests(unittest.TestCase):
    def test_archive_hides_and_restore_reveals_job(self) -> None:
        app = create_seeded_app()

        code, _ = request(
            app,
            "POST",
            "/api/jobs/daily-report/archive",
            {},
        )
        self.assertEqual(code, 200)

        code, payload = request(app, "GET", "/api/jobs")
        self.assertEqual(code, 200)
        self.assertNotIn(
            "daily-report",
            [job["id"] for job in payload["jobs"]],
        )

        code, body = request(app, "GET", "/dashboard")
        self.assertEqual(code, 200)
        self.assertNotIn("Daily report", body)

        code, _ = request(
            app,
            "POST",
            "/api/jobs/daily-report/restore",
            {},
        )
        self.assertEqual(code, 200)

        code, payload = request(app, "GET", "/api/jobs")
        self.assertIn(
            "daily-report",
            [job["id"] for job in payload["jobs"]],
        )


if __name__ == "__main__":
    unittest.main()
