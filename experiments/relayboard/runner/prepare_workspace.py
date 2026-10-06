from __future__ import annotations

import argparse
import io
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

BASE_SHA = "3a3315c3647474a03842d9405bb9a23aa41681b6"

SCENARIOS = {
    "S01-v0": "docs/benchmarks/S01_TINY_CHANGE.md",
    "S02-v0.1": "docs/benchmarks/S02_AMBIGUOUS_REQUIREMENT.md",
    "S04-v0": "docs/benchmarks/S04_HARD_BUG.md",
}

TREATMENTS = {
    "neutral-v0": {
        "method_source": None,
        "upstream": None,
    },
    "first-mode-v0": {
        "method_source": "docs/approaches/FIRST_MODE_V0.md",
        "upstream": None,
    },
    "pstack-pinned": {
        "method_source": None,
        "upstream": {
            "repository": "cursor/plugins",
            "scope": "pstack/",
            "sha": "df581122cde17e6e27686b5a448bde23e4ad4318",
            "native_install_required": True,
        },
    },
    "matt-pinned": {
        "method_source": None,
        "upstream": {
            "repository": "mattpocock/skills",
            "sha": "4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d",
            "native_install_required": True,
        },
    },
}


def run_git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return proc.stdout


def repo_root() -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return Path(proc.stdout.strip()).resolve()


def show_file(repo: Path, path: str) -> str:
    return run_git(repo, "show", f"{BASE_SHA}:{path}")  # type: ignore[return-value]


def extract_prompt(markdown: str) -> str:
    lines = markdown.splitlines()
    try:
        start = lines.index("## Frozen treatment prompt") + 1
    except ValueError as exc:
        raise RuntimeError("scenario document has no frozen prompt section") from exc

    prompt: list[str] = []
    started = False

    for line in lines[start:]:
        if line.startswith(">"):
            started = True
            value = line[1:]
            if value.startswith(" "):
                value = value[1:]
            prompt.append(value)
            continue

        if started:
            break

    result = "\n".join(prompt).strip()
    if not result:
        raise RuntimeError("frozen prompt is empty")
    return result


def export_fixture(repo: Path, output: Path) -> None:
    archive = run_git(
        repo,
        "archive",
        "--format=tar",
        BASE_SHA,
        "fixtures/relayboard",
        text=False,
    )
    assert isinstance(archive, bytes)

    with tempfile.TemporaryDirectory() as temp_name:
        temp = Path(temp_name)
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
            tar.extractall(temp, filter="data")

        source = temp / "fixtures" / "relayboard"
        for item in source.iterdir():
            destination = output / item.name
            if item.is_dir():
                shutil.copytree(item, destination)
            else:
                shutil.copy2(item, destination)


def initialize_workspace_git(output: Path) -> None:
    subprocess.run(
        ["git", "init", "-b", "main", str(output)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    run_git(output, "config", "user.name", "RelayBoard Benchmark")
    run_git(output, "config", "user.email", "benchmark@example.invalid")
    run_git(output, "add", ".")
    run_git(
        output,
        "commit",
        "-m",
        "benchmark: frozen treatment starting state",
    )


def prepare(
    scenario: str,
    treatment: str,
    host: str,
    model: str,
    output: Path,
) -> None:
    repo = repo_root()

    if scenario not in SCENARIOS:
        raise ValueError(f"unsupported scenario: {scenario}")
    if treatment not in TREATMENTS:
        raise ValueError(f"unsupported treatment: {treatment}")
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"output directory is not empty: {output}")

    output.mkdir(parents=True, exist_ok=True)
    export_fixture(repo, output)

    scenario_doc = show_file(repo, SCENARIOS[scenario])
    prompt = extract_prompt(scenario_doc)
    (output / "TASK.md").write_text(
        f"# Task\n\n{prompt}\n",
        encoding="utf-8",
    )

    treatment_config = TREATMENTS[treatment]
    method_source = treatment_config["method_source"]

    if method_source:
        method = show_file(repo, method_source)
        (output / "METHOD.md").write_text(
            method,
            encoding="utf-8",
        )

    gitignore = output / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(
            "__pycache__/\n"
            "*.py[cod]\n"
            ".pytest_cache/\n",
            encoding="utf-8",
        )

    metadata_dir = output / ".experiment"
    metadata_dir.mkdir()

    manifest = {
        "schema_version": 1,
        "base_sha": BASE_SHA,
        "scenario": scenario,
        "scenario_source": SCENARIOS[scenario],
        "treatment": treatment,
        "host": host,
        "model": model,
        "method_source": method_source,
        "upstream": treatment_config["upstream"],
        "evaluator_material_in_workspace": False,
        "contamination_rule": (
            "Deliberately fetching lab evaluator material invalidates the run."
        ),
    }

    (metadata_dir / "RUN_MANIFEST.json").write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    initialize_workspace_git(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        required=True,
        choices=sorted(SCENARIOS),
    )
    parser.add_argument(
        "--treatment",
        required=True,
        choices=sorted(TREATMENTS),
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prepare(
        args.scenario,
        args.treatment,
        args.host,
        args.model,
        args.output.resolve(),
    )
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
