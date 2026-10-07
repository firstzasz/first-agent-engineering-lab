"""Preserve exact local check commands and their output; no network access."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
label, *command = sys.argv[1:]
result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
output = root / ".experiment" / f"{label}.txt"
output.write_text(result.stdout)
record = {"label": label, "command": command, "cwd": str(root),
          "exit_code": result.returncode, "output_path": str(output.relative_to(root))}
with (root / ".experiment" / "checks.jsonl").open("a") as stream:
    stream.write(json.dumps(record) + "\n")
print(json.dumps(record))
print(result.stdout, end="")
sys.exit(result.returncode)
