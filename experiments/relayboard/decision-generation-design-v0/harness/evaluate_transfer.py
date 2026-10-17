from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Evaluation:
    scenario: str
    failures: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures


def load_workspace(workspace: Path):
    sys.path.insert(0, str(workspace))
    from relayboard.testing import request
    from relayboard.web import create_seeded_app
    return request, create_seeded_app


def evaluate_c1(workspace: Path) -> Evaluation:
    request, create_seeded_app = load_workspace(workspace)
    result = Evaluation("RD-C1-v0")

    # Explicit prompt behavior: cancel a running Run; no later Attempts.
    app = create_seeded_app()
    code, payload = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "manual"},
    )
    if code != 201:
        result.failures.append("could_not_create_running_run")
        return result
    run_id = payload["run"]["id"]

    code, payload = request(
        app,
        "POST",
        f"/api/runs/{run_id}/cancel",
        {},
    )
    if code != 200 or payload.get("run", {}).get("status") != "cancelled":
        result.failures.append("cancel_interface_or_status")
        return result

    code, _ = request(
        app,
        "POST",
        f"/api/runs/{run_id}/attempts",
        {"succeeded": True},
    )
    if code != 409:
        result.failures.append("cancelled_run_accepted_attempt")

    # Oracle 1: already-terminal succeeded/failed Run cannot be cancelled.
    app = create_seeded_app()
    run = app.service.begin_manual_run("cleanup")
    app.service.record_attempt(run.id, succeeded=True)
    code, _ = request(
        app,
        "POST",
        f"/api/runs/{run.id}/cancel",
        {},
    )
    if code != 409:
        result.failures.append("terminal_run_cancel_not_conflict")

    # Oracle 2: cancellation itself emits no Alert.
    app = create_seeded_app()
    run = app.service.begin_manual_run("daily-report")
    code, _ = request(
        app,
        "POST",
        f"/api/runs/{run.id}/cancel",
        {},
    )
    if code != 200:
        result.failures.append("running_cancel_not_200")
    if app.store.list_alerts():
        result.failures.append("cancel_emitted_alert")

    # Oracle 3: cancelled is the dashboard last result.
    code, body = request(app, "GET", "/dashboard")
    if code != 200 or "cancelled" not in body:
        result.failures.append("cancelled_not_dashboard_last_result")

    # Oracle 4: repeated cancel is idempotent success.
    code, payload = request(
        app,
        "POST",
        f"/api/runs/{run.id}/cancel",
        {},
    )
    if code != 200 or payload.get("run", {}).get("status") != "cancelled":
        result.failures.append("repeat_cancel_not_idempotent")

    return result


def evaluate_c2(workspace: Path) -> Evaluation:
    request, create_seeded_app = load_workspace(workspace)
    result = Evaluation("RD-C2-v0")

    # Explicit prompt behavior: hide from normal listing/dashboard; restore.
    app = create_seeded_app()
    code, _ = request(
        app,
        "POST",
        "/api/jobs/daily-report/archive",
        {},
    )
    if code != 200:
        result.failures.append("archive_interface_missing")
        return result

    code, payload = request(app, "GET", "/api/jobs")
    if code != 200 or "daily-report" in {
        job.get("id") for job in payload.get("jobs", [])
    }:
        result.failures.append("archived_job_visible_in_jobs_list")

    code, body = request(app, "GET", "/dashboard")
    if code != 200 or "Daily report" in body:
        result.failures.append("archived_job_visible_in_dashboard")

    # Oracle 1: archived blocks scheduled.
    code, _ = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "scheduled"},
    )
    if code != 409:
        result.failures.append("archived_job_allowed_scheduled_run")

    # Oracle 2: archived blocks manual.
    code, _ = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "manual"},
    )
    if code != 409:
        result.failures.append("archived_job_allowed_manual_run")

    # Oracle 3: a Run that existed before archive continues.
    app = create_seeded_app()
    code, payload = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "manual"},
    )
    if code != 201:
        result.failures.append("could_not_create_pre_archive_run")
        return result
    run_id = payload["run"]["id"]
    request(app, "POST", "/api/jobs/daily-report/archive", {})
    code, payload = request(
        app,
        "POST",
        f"/api/runs/{run_id}/attempts",
        {"succeeded": True},
    )
    if (
        code != 200
        or payload.get("run", {}).get("status") != "succeeded"
    ):
        result.failures.append("archive_interrupted_existing_run")

    # Oracle 4: restore preserves pre-archive enabled/disabled state.
    app = create_seeded_app()
    request(app, "POST", "/api/jobs/cleanup/archive", {})
    code, _ = request(app, "POST", "/api/jobs/cleanup/restore", {})
    if code != 200:
        result.failures.append("restore_interface_missing")
    code, _ = request(
        app,
        "POST",
        "/api/jobs/cleanup/runs",
        {"source": "scheduled"},
    )
    if code != 409:
        result.failures.append("restore_did_not_preserve_disabled")

    request(app, "POST", "/api/jobs/daily-report/archive", {})
    request(app, "POST", "/api/jobs/daily-report/restore", {})
    code, _ = request(
        app,
        "POST",
        "/api/jobs/daily-report/runs",
        {"source": "scheduled"},
    )
    if code != 201:
        result.failures.append("restore_did_not_preserve_enabled")

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if args.scenario == "RD-C1-v0":
        evaluation = evaluate_c1(workspace)
    elif args.scenario == "RD-C2-v0":
        evaluation = evaluate_c2(workspace)
    else:
        raise SystemExit(f"unsupported scenario: {args.scenario}")

    payload = {
        "scenario": evaluation.scenario,
        "passed": evaluation.passed,
        "failures": evaluation.failures,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0 if evaluation.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
