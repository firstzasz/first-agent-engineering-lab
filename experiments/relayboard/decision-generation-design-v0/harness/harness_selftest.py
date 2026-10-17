from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCENARIOS = {
    "RD-C1-v0": {
        "patch": "reference_patches/RD-C1-v0.py",
        "public_test": "public_tests/RD-C1-v0/test_public_feature.py",
        "base_red": "cancel_interface_or_status",
    },
    "RD-C2-v0": {
        "patch": "reference_patches/RD-C2-v0.py",
        "public_test": "public_tests/RD-C2-v0/test_public_feature.py",
        "base_red": "archive_interface_missing",
    },
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


def copy_workspace(fixture: Path, destination: Path) -> None:
    shutil.copytree(fixture, destination)


def copy_public_test(root: Path, scenario: str, workspace: Path) -> None:
    source = (
        root
        / "experiments"
        / "relayboard"
        / "decision-generation-design-v0"
        / SCENARIOS[scenario]["public_test"]
    )
    destination = workspace / "tests" / "test_transfer_feature.py"
    shutil.copy2(source, destination)


def run_public_tests(workspace: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(workspace)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        cwd=workspace,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def run_evaluator(
    root: Path,
    scenario: str,
    workspace: Path,
    output: Path,
) -> tuple[subprocess.CompletedProcess[str], dict]:
    evaluator = (
        root
        / "experiments"
        / "relayboard"
        / "decision-generation-design-v0"
        / "harness"
        / "evaluate_transfer.py"
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(evaluator),
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
    return proc, payload


def apply_reference(root: Path, scenario: str, workspace: Path) -> None:
    patch = (
        root
        / "experiments"
        / "relayboard"
        / "decision-generation-design-v0"
        / SCENARIOS[scenario]["patch"]
    )
    subprocess.run(
        [
            sys.executable,
            str(patch),
            "--workspace",
            str(workspace),
        ],
        cwd=root,
        check=True,
    )


def main() -> int:
    root = repo_root()
    fixture = root / "fixtures" / "relayboard"
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as temp_name:
        temp = Path(temp_name)

        for scenario, config in SCENARIOS.items():
            # Red capability on unchanged frozen fixture.
            base = temp / f"{scenario}-base"
            copy_workspace(fixture, base)
            copy_public_test(root, scenario, base)

            public = run_public_tests(base)
            if public.returncode == 0:
                failures.append(
                    f"{scenario}: feature public test unexpectedly "
                    "passed on frozen base"
                )

            eval_proc, evaluation = run_evaluator(
                root,
                scenario,
                base,
                temp / f"{scenario}-base-eval.json",
            )
            if eval_proc.returncode == 0:
                failures.append(
                    f"{scenario}: evaluator unexpectedly passed "
                    "on frozen base"
                )
            if config["base_red"] not in evaluation.get(
                "failures",
                [],
            ):
                failures.append(
                    f"{scenario}: expected base red signal "
                    f"{config['base_red']} missing; "
                    f"actual={evaluation.get('failures')}"
                )

            # Green reference path.
            reference = temp / f"{scenario}-reference"
            copy_workspace(fixture, reference)
            apply_reference(root, scenario, reference)
            copy_public_test(root, scenario, reference)

            public = run_public_tests(reference)
            if public.returncode != 0:
                failures.append(
                    f"{scenario}: reference public tests failed:\n"
                    f"{public.stdout}"
                )

            eval_proc, evaluation = run_evaluator(
                root,
                scenario,
                reference,
                temp / f"{scenario}-reference-eval.json",
            )
            if eval_proc.returncode != 0 or not evaluation.get(
                "passed",
                False,
            ):
                failures.append(
                    f"{scenario}: reference evaluator failed: "
                    f"{evaluation}; stdout={eval_proc.stdout}"
                )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(
        "PASS: RD-C1-v0 and RD-C2-v0 are red-capable on the "
        "frozen base and green with their reference patches"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
