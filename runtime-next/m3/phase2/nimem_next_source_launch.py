"""Launch the pinned ten-unit private experiment on an explicitly granted lane."""
import hashlib,subprocess,sys
from pathlib import Path
EXPECTED='14d2b02f9cac25b95a39607bbe63f1dd12e74c0de01c26d86347f830d6b09748'
p=Path(__file__).with_name('nimem_next_source_run.py')
if any(x=='--runner-sha256' or x.startswith('--runner-sha256=') for x in sys.argv[1:]):raise ValueError('runner pin cannot be overridden')
if hashlib.sha256(p.read_bytes()).hexdigest()!=EXPECTED:raise ValueError('runner changed')
raise SystemExit(subprocess.call([sys.executable,str(p),'--runner-sha256',EXPECTED]+sys.argv[1:]))
