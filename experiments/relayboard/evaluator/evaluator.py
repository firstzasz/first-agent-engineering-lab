from __future__ import annotations

from dataclasses import dataclass, field

from relayboard.testing import request
from relayboard.web import create_seeded_app


@dataclass
class Evaluation:
    scenario: str
    failures: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures


def evaluate_s01() -> Evaluation:
    result = Evaluation("S01-v0")
    app = create_seeded_app()

    code, body = request(
        app,
        "GET",
        "/dashboard",
    )
    if code != 200:
        result.failures.append("dashboard_not_200")
        return result

    if "<th>Latest result</th>" not in body:
        result.failures.append(
            "latest_result_heading_missing"
        )

    if "<th>Last result</th>" in body:
        result.failures.append(
            "old_heading_still_present"
        )

    code, payload = request(
        app,
        "GET",
        "/api/jobs",
    )
    if code != 200 or len(payload.get("jobs", [])) != 2:
        result.failures.append("jobs_api_regressed")

    return result


def _post_pause(app, job_id: str):
    return request(
        app,
        "POST",
        f"/api/jobs/{job_id}/pause",
        {},
    )


def _post_resume(app, job_id: str):
    return request(
        app,
        "POST",
        f"/api/jobs/{job_id}/resume",
        {},
    )


def evaluate_s02() -> Evaluation:
    result = Evaluation("S02-v0.1")
    app = create_seeded_app()

    code, payload = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "manual"},
    )
    if code != 201:
        result.failures.append(
            "could_not_start_pre_pause_run"
        )
        return result

    run_id = payload["run"]["id"]

    code, _ = _post_pause(
        app,
        "daily-report",
    )
    if code not in (200, 204):
        result.failures.append(
            "pause_interface_missing"
        )
        return result

    code, payload = request(
        app,
        "POST",
        f"/api/runs/{run_id}/attempts",
        {"succeeded": True},
    )
    if (
        code != 200
        or payload.get("run", {}).get("status")
        != "succeeded"
    ):
        result.failures.append(
            "pause_interrupted_existing_run"
        )

    code, _ = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "scheduled"},
    )
    if code not in (409, 423):
        result.failures.append(
            "scheduled_run_not_blocked_while_paused"
        )

    code, payload = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "manual"},
    )
    if code != 201:
        result.failures.append(
            "manual_run_not_allowed_while_paused"
        )
    else:
        request(
            app,
            "POST",
            f"/api/runs/{payload['run']['id']}/attempts",
            {"succeeded": True},
        )

    before = len(
        app.store.connection.execute(
            "SELECT id FROM runs"
        ).fetchall()
    )

    code, _ = _post_resume(
        app,
        "daily-report",
    )
    if code not in (200, 204):
        result.failures.append(
            "resume_interface_missing"
        )
        return result

    after = len(
        app.store.connection.execute(
            "SELECT id FROM runs"
        ).fetchall()
    )
    if after != before:
        result.failures.append(
            "resume_created_catch_up_run"
        )

    code, _ = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "scheduled"},
    )
    if code != 201:
        result.failures.append(
            "future_schedule_not_restored_after_resume"
        )

    return result


def _drive_run(
    app,
    job_id: str,
    outcomes: list[bool],
) -> str:
    run = app.service.begin_manual_run(job_id)

    for outcome in outcomes:
        state = app.service.record_attempt(
            run.id,
            succeeded=outcome,
        )
        if state in ("succeeded", "failed"):
            break

    return run.id


def evaluate_s04() -> Evaluation:
    result = Evaluation("S04-v0")

    app = create_seeded_app()
    run_id = _drive_run(
        app,
        "daily-report",
        [False, False],
    )
    alerts = [
        alert
        for alert in app.store.list_alerts()
        if alert.run_id == run_id
    ]
    if len(alerts) != 1:
        result.failures.append(
            "retry_terminal_failure_alert_count="
            f"{len(alerts)}"
        )

    app = create_seeded_app()
    first = _drive_run(
        app,
        "daily-report",
        [False, False],
    )
    second = _drive_run(
        app,
        "daily-report",
        [False, False],
    )
    ids = [
        alert.run_id
        for alert in app.store.list_alerts()
    ]
    if ids.count(first) != 1 or ids.count(second) != 1:
        result.failures.append(
            "distinct_runs_not_independently_alerted"
        )

    app = create_seeded_app()
    run_id = _drive_run(
        app,
        "cleanup",
        [False],
    )
    alerts = [
        alert
        for alert in app.store.list_alerts()
        if alert.run_id == run_id
    ]
    if len(alerts) != 1:
        result.failures.append(
            "single_attempt_failure_alert_regressed"
        )

    app = create_seeded_app()
    run_id = _drive_run(
        app,
        "daily-report",
        [False, True],
    )
    alerts = [
        alert
        for alert in app.store.list_alerts()
        if alert.run_id == run_id
    ]
    if alerts:
        result.failures.append(
            "successful_run_emitted_failure_alert"
        )

    app = create_seeded_app()
    if app.store.get_job("daily-report").max_attempts != 2:
        result.failures.append(
            "retry_policy_changed"
        )

    return result
