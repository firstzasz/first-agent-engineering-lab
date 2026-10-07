import datetime
import json
import pathlib
import subprocess
import sys

root = pathlib.Path.cwd()
if root != pathlib.Path("/workspace/relayboard-active/F-S02-001"):
    raise SystemExit("unexpected workdir")
command = sys.argv[1]
name = sys.argv[2]
result = subprocess.run(command, shell=True, executable="/bin/bash", text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=root)
output = root / ".experiment" / name
output.write_text(result.stdout)
with (root / ".experiment" / "commands.jsonl").open("a") as log:
    log.write(json.dumps({"time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "command": command, "workdir": str(root), "exit_code": result.returncode, "output_path": str(output.relative_to(root))}) + "\n")
print(result.stdout, end="")
raise SystemExit(result.returncode)
