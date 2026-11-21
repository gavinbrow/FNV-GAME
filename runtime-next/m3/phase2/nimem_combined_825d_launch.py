"""Launch the reviewed pinned combined runner on an explicitly granted lane."""
import hashlib, subprocess, sys
from pathlib import Path
EXPECTED='9a04d1d9f477ebc7d5989ab2147a39e3025d94c8ab431284a64bac40778ef2d7'
runner=Path(__file__).with_name('nimem_combined_825d_run.py')
if any(x=='--runner-sha256' or x.startswith('--runner-sha256=') for x in sys.argv[1:]):raise ValueError('runner pin cannot be overridden')
if hashlib.sha256(runner.read_bytes()).hexdigest()!=EXPECTED:raise ValueError('reviewed runner changed')
raise SystemExit(subprocess.call([sys.executable,str(runner),'--runner-sha256',EXPECTED]+sys.argv[1:]))
