import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
label, *command = sys.argv[1:]
result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = root / '.experiment' / f'{label}.txt'
output.write_text(result.stdout)
with (root / '.experiment' / 'commands.jsonl').open('a') as log:
    log.write(json.dumps({'ts': datetime.now(timezone.utc).isoformat(), 'cwd': str(root), 'argv': command, 'exit_code': result.returncode, 'output': str(output.relative_to(root))}) + '\n')
print(result.stdout, end='')
print(f'Exit code: {result.returncode}; output: {output.relative_to(root)}')
sys.exit(result.returncode)
