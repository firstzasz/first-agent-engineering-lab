from pathlib import Path
Path('.experiment/finalize_evidence.py').write_text('''import datetime
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
records = []
for command in (["git", "add", ".experiment"], ["git", "commit", "-m", "chore: preserve pause feature method and public evidence"]):
    result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    records.append({"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), "cwd": str(root), "argv": command, "exit_code": result.returncode, "output": result.stdout})
    print(result.stdout, end="")
    if result.returncode:
        (root / ".experiment" / "finalization.log").write_text("\\n".join(json.dumps(record) for record in records) + "\\n")
        raise SystemExit(result.returncode)
log = root / ".experiment" / "finalization.log"
log.write_text("\\n".join(json.dumps(record) for record in records) + "\\n")
for command in (["git", "rev-parse", "HEAD"], ["git", "status", "--short"]):
    result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    record = {"ts": datetime.datetime.now(datetime.timezone.utc).isoformat(), "cwd": str(root), "argv": command, "exit_code": result.returncode, "output": result.stdout}
    with log.open("a") as stream:
        stream.write(json.dumps(record) + "\\n")
    print(result.stdout, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
''')
