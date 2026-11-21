r"""Shared path configuration for every build script (environment first, today's local paths as defaults).
  FNV_PROJ_ROOT         project root holding fnv_decomp/, runtime-next/ (and FNV/ for the MCP-era inputs). Default: C:\path\to\Decompilation
  FNV_GAME_DIR          installed Fallout New Vegas folder (read only, never modified)
  FNV_MSVC9_RTM_ROOT    VC 2008 RTM toolchain root;   FNV_MSVC9_ROOT  VC 2008 SP1 toolchain root (FNV/tools/vc2008)
  FNV_REF_IMAGE         the decrypted reference image (FalloutNV.runtime-text.exe): READ ONLY, never copied; the matcher/assembler use it as oracle
  FNV_PY_SITE           extra site-packages dir (numpy etc.)
Scripts that cannot import this module (python -I runs) use the same variables inline through os.environ.get (see layout-v2/ci/relocate_paths.py)."""
import os
J = os.path.join
_DEF_PROJ = 'C:' + chr(92) + 'Projects' + chr(92) + 'Decompilation'
PROJ = os.environ.get('FNV_PROJ_ROOT') or _DEF_PROJ
RN = J(PROJ, 'runtime-next')
FN = J(PROJ, 'fnv_decomp')
FNV = J(PROJ, 'FNV')
GAME_DIR = os.environ.get('FNV_GAME_DIR') or J('C:' + chr(92), 'Program Files (x86)', 'Steam', 'steamapps', 'common', 'Fallout New Vegas')
MSVC9_SP1 = os.environ.get('FNV_MSVC9_ROOT') or J(_DEF_PROJ, 'FNV', 'tools', 'vc2008')
MSVC8 = os.environ.get('FNV_MSVC8_ROOT') or J(_DEF_PROJ, 'FNV', 'tools', 'vc8sp1')
MSVC9_RTM = os.environ.get('FNV_MSVC9_RTM_ROOT') or J(_DEF_PROJ, 'FNV', 'tools', 'vc2008rtm')
REF_IMAGE = os.environ.get('FNV_REF_IMAGE') or J(_DEF_PROJ, 'FNV', 'work', 'worker1', 'FalloutNV.runtime-text.exe')
PY_SITE = os.environ.get('FNV_PY_SITE') or J(os.environ.get('APPDATA', ''), 'Python', 'Python312', 'site-packages')
def sub(*p): return J(PROJ, *p)
