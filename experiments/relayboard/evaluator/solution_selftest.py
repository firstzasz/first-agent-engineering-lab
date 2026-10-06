from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCENARIOS = {
    "S01-v0": "S01.patch",
    "S02-v0.1": "S02.patch",
    "S04-v0": "S04.patch",
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


def init_workspace(source: Path, workspace: Path) -> None:
    shutil.copytree(source, workspace)
    subprocess.run(
        ["git", "init", "-b", "main", str(workspace)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(workspace), "config", "user.name", "RelayBoard Reference"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(workspace), "config", "user.email", "reference@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(workspace), "add", "."],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(workspace), "commit", "-m", "reference base"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def apply_patch(workspace: Path, patch: Path) -> None:
    subprocess.run(
        ["git", "-C", str(workspace), "apply", str(patch)],
        check=True,
    )


def evaluate(root: Path, scenario: str, workspace: Path, output: Path) -> dict:
    subprocess.run(
        [
            sys.executable,
            str(root / "experiments" / "relayboard" / "runner" / "evaluate_workspace.py"),
            "--scenario",
            scenario,
            "--workspace",
            str(workspace),
            "--output",
            str(output),
        ],
        cwd=root,
        check=True,
    )
    return json.loads(output.read_text(encoding="utf-8"))


def main() -> int:
    root = repo_root()
    fixture = root / "fixtures" / "relayboard"
    patches = root / "experiments" / "relayboard" / "evaluator" / "reference_patches"

    failures: list[str] = []

    with tempfile.TemporaryDirectory() as temp_name:
        temp = Path(temp_name)

        for scenario, patch_name in SCENARIOS.items():
            workspace = temp / scenario
            init_workspace(fixture, workspace)
            apply_patch(workspace, patches / patch_name)

            result = evaluate(
                root,
                scenario,
                workspace,
                temp / f"{scenario}.json",
            )

            if not result["public_tests"]["passed"]:
                failures.append(
                    f"{scenario}: public tests failed after reference solution"
                )

            if not result["oracle"]["passed"]:
                failures.append(
                    f"{scenario}: oracle failed after reference solution: "
                    f"{result['oracle']['failures']}"
                )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(
        "PASS: evaluator accepts frozen reference solutions "
        "for S01-v0, S02-v0.1, and S04-v0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
