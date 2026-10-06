from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from prepare_workspace import BASE_SHA, prepare


def run_public_tests(workspace: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(workspace)

    subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(workspace / "tests"),
            "-v",
        ],
        cwd=workspace,
        env=env,
        check=True,
    )


def assert_clean(workspace: Path) -> None:
    proc = subprocess.run(
        [
            "git",
            "-C",
            str(workspace),
            "status",
            "--porcelain",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.stdout.strip():
        raise AssertionError(
            f"prepared workspace is dirty: {proc.stdout}"
        )


def main() -> int:
    scenarios = [
        "S01-v0",
        "S02-v0.1",
        "S04-v0",
    ]

    with tempfile.TemporaryDirectory() as temp_name:
        root = Path(temp_name)

        for scenario in scenarios:
            workspace = root / scenario
            prepare(
                scenario,
                "neutral-v0",
                "ci-selftest",
                "ci-selftest",
                workspace,
            )

            if (workspace / "experiments").exists():
                raise AssertionError(
                    "evaluator material leaked into workspace"
                )

            if not (workspace / "TASK.md").exists():
                raise AssertionError("TASK.md missing")

            manifest = json.loads(
                (
                    workspace
                    / ".experiment"
                    / "RUN_MANIFEST.json"
                ).read_text(encoding="utf-8")
            )

            if manifest["base_sha"] != BASE_SHA:
                raise AssertionError(
                    "workspace base SHA mismatch"
                )

            run_public_tests(workspace)
            assert_clean(workspace)

        first_workspace = root / "first-mode"
        prepare(
            "S01-v0",
            "first-mode-v0",
            "ci-selftest",
            "ci-selftest",
            first_workspace,
        )

        method = (
            first_workspace
            / "METHOD.md"
        ).read_text(encoding="utf-8")

        if "# FIRST-mode v0" not in method:
            raise AssertionError(
                "FIRST-mode method was not pinned into workspace"
            )

        assert_clean(first_workspace)

    print(
        "PASS: treatment runner prepares clean, "
        "evaluator-blind workspaces from "
        f"{BASE_SHA}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
