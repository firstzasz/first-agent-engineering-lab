import datetime
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
label, *command = sys.argv[1:]
result = subprocess.run(command, cwd=root, text=True, capture_output=True)
output = root / ".experiment" / "outputs" / (label + ".txt")
output.write_text(result.stdout + result.stderr)
record = {
    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "label": label,
    "cwd": str(root),
    "argv": command,
    "exit_code": result.returncode,
    "stdout_stderr_path": str(output.relative_to(root)),
}
with (root / ".experiment" / "commands.jsonl").open("a") as stream:
    stream.write(json.dumps(record) + "\n")
print(result.stdout + result.stderr, end="")
print("Captured", label, "exit", result.returncode, "at", output.relative_to(root))
sys.exit(result.returncode)
