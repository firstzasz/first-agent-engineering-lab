import json
import subprocess
import sys
from pathlib import Path

label, *command = sys.argv[1:]
result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = Path(".experiment") / f"{label}.txt"
output.write_text(result.stdout)
entry = {"command": command, "cwd": str(Path.cwd()), "exit_code": result.returncode, "output_path": str(output)}
with Path(".experiment/commands.jsonl").open("a") as stream:
    stream.write(json.dumps(entry) + "\n")
print(json.dumps(entry))
print(result.stdout, end="")
sys.exit(result.returncode)
