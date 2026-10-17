from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


MUTATIONS = {
    "RD-C1-v0": [
        {
            "name": "terminal_cancel_success",
            "path": "relayboard/service.py",
            "old": '        if run.status != "running":\n            raise RunNotCancellable(run_id)\n',
            "new": '        if run.status != "running":\n            return run\n',
            "expected": "terminal_run_cancel_not_conflict",
        },
        {
            "name": "cancel_emits_alert",
            "path": "relayboard/service.py",
            "old": '        return self.store.set_run_status(run_id, "cancelled")\n',
            "new": '        self._emit_failure_alert(run_id)\n        return self.store.set_run_status(run_id, "cancelled")\n',
            "expected": "cancel_emitted_alert",
        },
        {
            "name": "dashboard_ignores_cancelled",
            "path": "relayboard/store.py",
            "old": "WHERE job_id = ? AND status != 'running'\n",
            "new": "WHERE job_id = ? AND status NOT IN ('running', 'cancelled')\n",
            "expected": "cancelled_not_dashboard_last_result",
        },
        {
            "name": "repeat_cancel_conflict",
            "path": "relayboard/service.py",
            "old": '        if run.status == "cancelled":\n            return run\n',
            "new": '        if run.status == "cancelled":\n            raise RunNotCancellable(run_id)\n',
            "expected": "repeat_cancel_not_idempotent",
        },
    ],
    "RD-C2-v0": [
        {
            "name": "allow_scheduled_while_archived",
            "path": "relayboard/service.py",
            "old": '        if job.archived:\n            raise JobNotSchedulable(f"job {job_id} is archived")\n',
            "new": "",
            "expected": "archived_job_allowed_scheduled_run",
        },
        {
            "name": "allow_manual_while_archived",
            "path": "relayboard/service.py",
            "old": '        if job.archived:\n            raise JobArchived(f"job {job_id} is archived")\n',
            "new": "",
            "expected": "archived_job_allowed_manual_run",
        },
        {
            "name": "archive_interrupts_existing_run",
            "path": "relayboard/service.py",
            "old": '        run = self.store.get_run(run_id)\n        if run.status != "running":\n',
            "new": '        run = self.store.get_run(run_id)\n        if self.store.get_job(run.job_id).archived:\n            self.store.set_run_status(run_id, "failed")\n            return "failed"\n        if run.status != "running":\n',
            "expected": "archive_interrupted_existing_run",
        },
        {
            "name": "restore_forces_enabled",
            "path": "relayboard/service.py",
            "old": '    def restore_job(self, job_id: str):\n        return self.store.set_job_archived(job_id, False)\n',
            "new": '    def restore_job(self, job_id: str):\n        self.store.set_job_enabled(job_id, True)\n        return self.store.set_job_archived(job_id, False)\n',
            "expected": "restore_did_not_preserve_disabled",
        },
    ],
}


def repo_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return Path(proc.stdout.strip()).resolve()


def patch_script(root: Path, scenario: str) -> Path:
    return (
        root
        / "experiments"
        / "relayboard"
        / "decision-generation-design-v0"
        / "reference_patches"
        / f"{scenario}.py"
    )


def evaluator_script(root: Path) -> Path:
    return (
        root
        / "experiments"
        / "relayboard"
        / "decision-generation-design-v0"
        / "harness"
        / "evaluate_transfer.py"
    )


def apply_reference(root: Path, scenario: str, workspace: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(patch_script(root, scenario)),
            "--workspace",
            str(workspace),
        ],
        cwd=root,
        check=True,
    )


def apply_mutation(workspace: Path, mutation: dict) -> None:
    path = workspace / mutation["path"]
    text = path.read_text(encoding="utf-8")
    old = mutation["old"]
    if text.count(old) != 1:
        raise RuntimeError(
            f"{mutation['name']}: expected one mutation target, "
            f"found {text.count(old)}"
        )
    path.write_text(
        text.replace(old, mutation["new"]),
        encoding="utf-8",
    )


def evaluate(
    root: Path,
    scenario: str,
    workspace: Path,
    output: Path,
) -> tuple[int, dict]:
    proc = subprocess.run(
        [
            sys.executable,
            str(evaluator_script(root)),
            "--scenario",
            scenario,
            "--workspace",
            str(workspace),
            "--output",
            str(output),
        ],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    payload = (
        json.loads(output.read_text(encoding="utf-8"))
        if output.exists()
        else {}
    )
    return proc.returncode, payload


def main() -> int:
    root = repo_root()
    fixture = root / "fixtures" / "relayboard"
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as temp_name:
        temp = Path(temp_name)

        for scenario, mutations in MUTATIONS.items():
            for mutation in mutations:
                workspace = (
                    temp / f"{scenario}-{mutation['name']}"
                )
                shutil.copytree(fixture, workspace)
                apply_reference(root, scenario, workspace)
                apply_mutation(workspace, mutation)

                code, payload = evaluate(
                    root,
                    scenario,
                    workspace,
                    temp
                    / f"{scenario}-{mutation['name']}.json",
                )
                observed = payload.get("failures", [])

                if code == 0:
                    failures.append(
                        f"{scenario}/{mutation['name']}: "
                        "mutation unexpectedly passed"
                    )
                if mutation["expected"] not in observed:
                    failures.append(
                        f"{scenario}/{mutation['name']}: expected "
                        f"{mutation['expected']} not observed; "
                        f"actual={observed}"
                    )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(
        "PASS: all eight targeted wrong-but-reasonable mutations "
        "are rejected by the transfer evaluator"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
