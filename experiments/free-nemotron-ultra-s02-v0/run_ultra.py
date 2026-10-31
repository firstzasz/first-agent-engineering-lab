#!/usr/bin/env python3
"""Four-cell Nemotron 3 Ultra NVIDIA-only S02 experiment, frozen v0 controls."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"free-s02-screen-v0"))
import screen

ULTRA = "nvidia/nemotron-3-ultra-550b-a55b"
def main():
    old = screen.PROVIDERS["nvidia"]
    assert old[2] == "openai/gpt-oss-20b", "Historical source baseline unexpectedly changed"
    assert screen.MAX_CALLS == 9 and screen.MAX_OUTPUT_TOKENS == 3000
    assert screen.REQUEST_TIMEOUT == 90
    assert screen.ORDERS["nvidia"] == ["matt","neutral","first","pstack"]
    screen.PROVIDERS["nvidia"] = (old[0], old[1], ULTRA)
    sys.argv = [sys.argv[0],"--provider","nvidia","--output","screen-output/nvidia"]
    screen.main()
    output = Path("screen-output/nvidia")
    cohort=json.loads((output/"cohort.json").read_text(encoding="utf-8"))
    assert len(cohort)==4
    for run in cohort:
        assert run["provider"]=="nvidia" and run["model"]==ULTRA
        assert run["requests"]<=9
    (output/"MODEL_VARIANT.json").write_text(json.dumps({
        "experiment":"FREE_NEMOTRON_ULTRA_S02_V0",
        "base_protocol":"FREE_S02_METHOD_SCREEN_V0",
        "comparison_run":"https://github.com/firstzasz/first-agent-engineering-lab/actions/runs/41211207214",
        "only_changed_variable":"nvidia model id: openai/gpt-oss-20b -> nvidia/nemotron-3-ultra-550b-a55b",
        "model":ULTRA,"run_count":len(cohort),
        "method_order":screen.ORDERS["nvidia"],
        "hard_request_cap_per_run":9,
    },indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":
    main()
