import datetime
import json
from pathlib import Path
import subprocess
import sys

label, *command = sys.argv[1:]
if command[:1] == ["--"]:
    command = command[1:]
root = Path(__file__).resolve().parent.parent
script_input = sys.stdin.read() if command[:2] == ["python", "-"] else None
if script_input is not None:
    (root / ".experiment" / (label + ".stdin.py")).write_text(script_input)
result = subprocess.run(command, cwd=root, input=script_input, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
output = root / ".experiment" / (label + ".log")
output.write_text(result.stdout)
record = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), "cwd": str(root), "argv": command, "exit_code": result.returncode, "output_path": str(output.relative_to(root))}
if script_input is not None:
    record["stdin_path"] = ".experiment/" + label + ".stdin.py"
with (root / ".experiment" / "commands.jsonl").open("a") as log:
    log.write(json.dumps(record) + "\n")
print(result.stdout, end="")
sys.exit(result.returncode)
