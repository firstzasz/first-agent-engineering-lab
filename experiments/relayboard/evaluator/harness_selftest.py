from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "fixtures" / "relayboard"

sys.path.insert(0, str(FIXTURE))

from evaluator import (  # noqa: E402
    evaluate_s01,
    evaluate_s02,
    evaluate_s04,
)


def main() -> int:
    expected = {
        "S01-v0": {
            "latest_result_heading_missing",
            "old_heading_still_present",
        },
        "S02-v0.1": {
            "pause_interface_missing",
        },
        "S04-v0": {
            "retry_terminal_failure_alert_count=2",
            "distinct_runs_not_independently_alerted",
            "successful_run_emitted_failure_alert",
        },
    }

    evaluations = [
        evaluate_s01(),
        evaluate_s02(),
        evaluate_s04(),
    ]

    failures: list[str] = []

    for evaluation in evaluations:
        actual = set(evaluation.failures)
        missing = expected[evaluation.scenario] - actual

        if missing:
            failures.append(
                f"{evaluation.scenario} did not expose "
                f"expected red signals: {sorted(missing)}; "
                f"actual={sorted(actual)}"
            )

        if evaluation.passed:
            failures.append(
                f"{evaluation.scenario} unexpectedly "
                "passed on the frozen starting fixture"
            )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    for evaluation in evaluations:
        print(
            "PASS: "
            f"{evaluation.scenario} is red-capable "
            f"on the frozen base: {evaluation.failures}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
