import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
label, *command = sys.argv[1:]
result = subprocess.run(command, capture_output=True, text=True)
output = result.stdout + result.stderr
(root / f'{label}.txt').write_text(output)
entry = {'label': label, 'command': command, 'cwd': str(Path.cwd()), 'exit_code': result.returncode, 'outputpath': f'.experiment/{label}.txt'}
with (root / 'commands.jsonl').open('a') as log:
    log.write(json.dumps(entry) + '\n')
print(json.dumps(entry))
print(output, end='')
sys.exit(result.returncode)
