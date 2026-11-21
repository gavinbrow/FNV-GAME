"""Launch the reviewed private NiRef cohort only on a granted lane."""
import hashlib,subprocess,sys
from pathlib import Path
EXPECTED='5c61bf44aad00a3b2041f47d0d87f7937eec04ff8174edc0f34cd6c82c85d708';runner=Path(__file__).with_name('niref_inline_cohort_run.py')
if any(x=='--runner-sha256' or x.startswith('--runner-sha256=') for x in sys.argv[1:]):raise ValueError('runner pin cannot be overridden')
if hashlib.sha256(runner.read_bytes()).hexdigest()!=EXPECTED:raise ValueError('reviewed runner changed')
raise SystemExit(subprocess.call([sys.executable,str(runner),'--runner-sha256',EXPECTED]+sys.argv[1:]))
