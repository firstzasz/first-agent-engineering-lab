"""Capture local public command evidence; no shell or network helpers."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
label, *command = sys.argv[1:]
result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = root / '.experiment' / f'{label}.txt'
output.write_text(result.stdout)
with (root / '.experiment' / 'commands.jsonl').open('a') as log:
    log.write(json.dumps({'label': label, 'command': command, 'cwd': str(root), 'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'exit_code': result.returncode, 'outputpath': str(output.relative_to(root))}) + '\n')
print(result.stdout, end='')
print(f'Captured {label}: exit {result.returncode}')
sys.exit(result.returncode)
