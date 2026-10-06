from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

SCENARIO_FUNCTIONS = {
    "S01-v0": "evaluate_s01",
    "S02-v0.1": "evaluate_s02",
    "S04-v0": "evaluate_s04",
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


def run_public_tests(workspace: Path) -> dict:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(workspace)

    proc = subprocess.run(
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
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    return {
        "returncode": proc.returncode,
        "passed": proc.returncode == 0,
        "output": proc.stdout,
    }


def load_evaluator(workspace: Path):
    repo = repo_root()
    evaluator_path = (
        repo
        / "experiments"
        / "relayboard"
        / "evaluator"
        / "evaluator.py"
    )

    sys.path.insert(0, str(workspace))

    spec = importlib.util.spec_from_file_location(
        "relayboard_lab_evaluator",
        evaluator_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load evaluator")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git_capture(workspace: Path) -> dict:
    def command(*args: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(workspace), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return proc.stdout

    return {
        "status": command("status", "--short"),
        "diff_stat": command("diff", "--stat", "HEAD"),
        "diff": command("diff", "HEAD"),
        "commits": command(
            "log",
            "--oneline",
            "--decorate",
            "-20",
        ),
    }


def evaluate(scenario: str, workspace: Path) -> dict:
    if scenario not in SCENARIO_FUNCTIONS:
        raise ValueError(f"unsupported scenario: {scenario}")

    manifest_path = (
        workspace
        / ".experiment"
        / "RUN_MANIFEST.json"
    )
    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    if manifest["scenario"] != scenario:
        raise RuntimeError(
            "workspace scenario does not match evaluator request"
        )

    public = run_public_tests(workspace)
    evaluator = load_evaluator(workspace)
    evaluation = getattr(
        evaluator,
        SCENARIO_FUNCTIONS[scenario],
    )()

    return {
        "schema_version": 1,
        "manifest": manifest,
        "public_tests": public,
        "oracle": {
            "scenario": evaluation.scenario,
            "passed": evaluation.passed,
            "failures": evaluation.failures,
        },
        "git": git_capture(workspace),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        required=True,
        choices=sorted(SCENARIO_FUNCTIONS),
    )
    parser.add_argument(
        "--workspace",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "--output",
        type=Path,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = evaluate(
        args.scenario,
        args.workspace.resolve(),
    )

    rendered = json.dumps(
        result,
        indent=2,
        sort_keys=True,
    ) + "\n"

    if args.output:
        args.output.write_text(
            rendered,
            encoding="utf-8",
        )
        print(args.output.resolve())
    else:
        print(rendered, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
