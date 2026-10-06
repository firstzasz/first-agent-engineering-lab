from __future__ import annotations

import html
import json
from collections.abc import Callable, Iterable

from .service import JobNotSchedulable, RelayBoardService
from .store import Store

StartResponse = Callable[[str, list[tuple[str, str]]], None]


class RelayBoardApp:
    def __init__(self, store: Store | None = None) -> None:
        self.store = store or Store()
        self.service = RelayBoardService(self.store)

    def __call__(
        self,
        environ: dict,
        start_response: StartResponse,
    ) -> Iterable[bytes]:
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = environ.get("PATH_INFO", "/")

        try:
            if method == "GET" and path == "/dashboard":
                return self._html(start_response, self.render_dashboard())

            if method == "GET" and path == "/api/jobs":
                return self._json(
                    start_response,
                    200,
                    {
                        "jobs": [
                            self._job_json(job)
                            for job in self.store.list_jobs()
                        ]
                    },
                )

            if method == "GET" and path == "/api/alerts":
                return self._json(
                    start_response,
                    200,
                    {
                        "alerts": [
                            alert.__dict__
                            for alert in self.store.list_alerts()
                        ]
                    },
                )

            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/enabled")
            ):
                job_id = path.split("/")[3]
                body = self._read_json(environ)
                self.service.set_job_enabled(
                    job_id,
                    bool(body["enabled"]),
                )
                return self._json(
                    start_response,
                    200,
                    {"job": self._job_json(self.store.get_job(job_id))},
                )

            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/pause")
            ):
                job_id = path.split("/")[3]
                self.service.pause_job(job_id)
                return self._json(
                    start_response,
                    200,
                    {"job": self._job_json(self.store.get_job(job_id))},
                )

            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/resume")
            ):
                job_id = path.split("/")[3]
                self.service.resume_job(job_id)
                return self._json(
                    start_response,
                    200,
                    {"job": self._job_json(self.store.get_job(job_id))},
                )

            if (
                method == "POST"
                and path.startswith("/api/jobs/")
                and path.endswith("/runs")
            ):
                job_id = path.split("/")[3]
                body = self._read_json(environ)
                source = body.get("source", "manual")

                if source == "scheduled":
                    run = self.service.begin_scheduled_run(job_id)
                elif source == "manual":
                    run = self.service.begin_manual_run(job_id)
                else:
                    return self._json(
                        start_response,
                        400,
                        {"error": "invalid source"},
                    )

                return self._json(
                    start_response,
                    201,
                    {"run": run.__dict__},
                )

            if (
                method == "POST"
                and path.startswith("/api/runs/")
                and path.endswith("/attempts")
            ):
                run_id = path.split("/")[3]
                body = self._read_json(environ)
                status = self.service.record_attempt(
                    run_id,
                    succeeded=bool(body["succeeded"]),
                )
                return self._json(
                    start_response,
                    200,
                    {
                        "status": status,
                        "run": self.store.get_run(run_id).__dict__,
                    },
                )

        except KeyError as exc:
            return self._json(
                start_response,
                404,
                {"error": f"not found: {exc.args[0]}"},
            )
        except JobNotSchedulable as exc:
            return self._json(
                start_response,
                409,
                {"error": str(exc)},
            )

        return self._json(
            start_response,
            404,
            {"error": "not found"},
        )

    def render_dashboard(self) -> str:
        rows: list[str] = []
        for job in self.store.list_jobs():
            last = self.store.last_result_for_job(job.id) or "never"
            rows.append(
                "<tr>"
                f"<td>{html.escape(job.name)}</td>"
                f"<td>{'yes' if job.enabled else 'no'}</td>"
                f"<td>{html.escape(last)}</td>"
                "</tr>"
            )

        return (
            "<!doctype html>"
            "<html><head><title>RelayBoard</title></head><body>"
            "<h1>Jobs</h1>"
            "<table id='jobs'><thead><tr>"
            "<th>Job</th><th>Enabled</th><th>Last result</th>"
            "</tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table></body></html>"
        )

    @staticmethod
    def _job_json(job) -> dict:
        return {
            "id": job.id,
            "name": job.name,
            "enabled": job.enabled,
            "max_attempts": job.max_attempts,
            "paused": job.paused,
        }

    @staticmethod
    def _read_json(environ: dict) -> dict:
        length = int(environ.get("CONTENT_LENGTH") or 0)
        raw = (
            environ["wsgi.input"].read(length)
            if length
            else b"{}"
        )
        return json.loads(raw.decode("utf-8"))

    @staticmethod
    def _json(
        start_response: StartResponse,
        status_code: int,
        payload: dict,
    ) -> Iterable[bytes]:
        body = json.dumps(
            payload,
            sort_keys=True,
        ).encode("utf-8")
        reason = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            404: "Not Found",
            409: "Conflict",
        }[status_code]
        start_response(
            f"{status_code} {reason}",
            [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(body))),
            ],
        )
        return [body]

    @staticmethod
    def _html(
        start_response: StartResponse,
        markup: str,
    ) -> Iterable[bytes]:
        body = markup.encode("utf-8")
        start_response(
            "200 OK",
            [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Content-Length", str(len(body))),
            ],
        )
        return [body]


def create_seeded_app() -> RelayBoardApp:
    app = RelayBoardApp()
    app.store.add_job(
        "daily-report",
        "Daily report",
        enabled=True,
        max_attempts=2,
    )
    app.store.add_job(
        "cleanup",
        "Cleanup",
        enabled=False,
        max_attempts=1,
    )
    return app
