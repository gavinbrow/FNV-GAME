"""Stage Phase 2 promotion files and patch without modifying build inputs."""
import difflib,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;OUT=H/'promotion-staged-v5';S=M/'out/phase2-w-arrays-expanded/selection.json';L=H/'library_candidates.json';SEL='2dc3eb28083648d0d701268d8aa858a4d90fddd45e6ffb2613073cbb83672045';LIB='da19c0a782f6ba4ac986e992daf4af7ed67c282d0b70f35e8804a22227bce645'
def sha(b):return hashlib.sha256(b).hexdigest()
def replace(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor missing or ambiguous '+a[:50])
 return s.replace(a,b,1)
def config(s):
 s=replace(s,"DEFAULT_SELECTION = 'batch8_final_selection.json'\nDEFAULT_SELECTION_SHA256 = '42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7'", """import os

DEFAULT_SELECTION = 'phase2/selection.json'
DEFAULT_SELECTION_SHA256 = '"""+SEL+"""'
DEFAULT_LIBRARY_SELECTION = 'phase2/library_candidates.json'
DEFAULT_LIBRARY_SHA256 = '"""+LIB+"""'
_M3_ROOT = os.path.dirname(os.path.abspath(__file__))


def _selection_path(value):
    return os.path.normcase(os.path.abspath(os.path.join(_M3_ROOT, value)))""")
 s=replace(s,"    return env\n\n\ndef validate_driver_options", """    toggle = env.get('FNV_M3_LIB')
    explicit_library = ('FNV_M3_LIB_SELECTION' in environment or 'FNV_M3_LIB_SHA256' in environment)
    default_selected = _selection_path(env.get('FNV_M3_SEL', DEFAULT_SELECTION)) == _selection_path(DEFAULT_SELECTION)
    if (promoted or toggle == '1') and env.get('FNV_M3_DV1') == '1' and toggle != '0' and not explicit_library and (toggle == '1' or default_selected):
        env['FNV_M3_LIB_SELECTION'] = os.path.abspath(os.path.join(_M3_ROOT, DEFAULT_LIBRARY_SELECTION))
        env['FNV_M3_LIB_SHA256'] = DEFAULT_LIBRARY_SHA256
    return env


def validate_driver_options""")
 s=replace(s,"    selection, digest = raw.get('FNV_M3_LIB_SELECTION'), raw.get('FNV_M3_LIB_SHA256')\n", """    toggle = raw.get('FNV_M3_LIB') or None
    if toggle not in (None, '0', '1'):
        raise ValueError('FNV_M3_LIB must be 0 or 1')
    selection, digest = raw.get('FNV_M3_LIB_SELECTION'), raw.get('FNV_M3_LIB_SHA256')
    if toggle == '0' and (selection is not None or digest is not None):
        raise ValueError('FNV_M3_LIB=0 conflicts with explicit library selection')
    if toggle == '1' and (env.get('FNV_M3') != '1' or env.get('FNV_M3_DV1') != '1' or skip_data_v1):
        raise ValueError('library overlay requires active M3/DV1 and fresh data-v1')
""")
 return s
def driver(s):
 s=replace(s,'from m3.config import configure, validate_driver_options, validate_library_result, DEFAULT_SELECTION, DEFAULT_SELECTION_SHA256\n','from m3.config import configure, validate_driver_options, validate_library_result, DEFAULT_SELECTION, DEFAULT_SELECTION_SHA256, DEFAULT_LIBRARY_SELECTION, DEFAULT_LIBRARY_SHA256\n')
 s=replace(s,"        if library_digest != env['FNV_M3_LIB_SHA256'].lower():\n", "        if os.path.normcase(os.path.abspath(env['FNV_M3_LIB_SELECTION'])) == os.path.normcase(os.path.abspath(J(RN, 'm3', DEFAULT_LIBRARY_SELECTION))) and library_digest != DEFAULT_LIBRARY_SHA256:\n            finish('failed', 'default library selection SHA-256 does not match pinned digest')\n        if library_digest != env['FNV_M3_LIB_SHA256'].lower():\n")
 old="""# ---- 1..4 compile and rebuild
step(1, 'compile-units', [PY, '-I', J(RN, 'pinned-build', 'compile_units_v3.py'), '30'])
if M3:
    try:
        selection = J(RN, 'm3', env.get('FNV_M3_SEL') or 'pilot_selection.json')
        with open(selection, 'rb') as f: digest = hashlib.sha256(f.read()).hexdigest()
        summary['provenance']['m3_config']['selection_sha256'] = digest
        if os.path.normcase(os.path.abspath(selection)) == os.path.normcase(os.path.abspath(J(RN, 'm3', DEFAULT_SELECTION))) and digest != DEFAULT_SELECTION_SHA256:
            finish('failed', 'default M3 selection SHA-256 does not match pinned digest')
    except (OSError, ValueError) as exc:
        finish('failed', 'cannot read M3 selection for SHA-256: ' + str(exc))
    step(1, 'm3-gen', [PY, '-I', J(RN, 'm3', 'gen_m3.py')])
"""
 new="""# Validate the selected input before compiling or mutating build outputs.
if M3:
    try:
        selection = J(RN, 'm3', env.get('FNV_M3_SEL') or 'pilot_selection.json')
        with open(selection, 'rb') as f: digest = hashlib.sha256(f.read()).hexdigest()
        summary['provenance']['m3_config']['selection_sha256'] = digest
        if os.path.normcase(os.path.abspath(selection)) == os.path.normcase(os.path.abspath(J(RN, 'm3', DEFAULT_SELECTION))) and digest != DEFAULT_SELECTION_SHA256:
            finish('failed', 'default M3 selection SHA-256 does not match pinned digest')
    except (OSError, ValueError) as exc:
        finish('failed', 'cannot read M3 selection for SHA-256: ' + str(exc))
# ---- 1..4 compile and rebuild
step(1, 'compile-units', [PY, '-I', J(RN, 'pinned-build', 'compile_units_v3.py'), '30'])
if M3:
    step(1, 'm3-gen', [PY, '-I', J(RN, 'm3', 'gen_m3.py')])
"""
 return replace(s,old,new)
def tests(s):
 s=replace(s,'from config import configure, validate_driver_options, DEFAULT_SELECTION, DEFAULT_SELECTION_SHA256\n','from config import configure, validate_driver_options, DEFAULT_SELECTION, DEFAULT_SELECTION_SHA256, DEFAULT_LIBRARY_SELECTION, DEFAULT_LIBRARY_SHA256\n')
 s=replace(s,"        'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '1'}", "        'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '1',\n        'FNV_M3_LIB_SELECTION': str(Path(__file__).resolve().parents[1] / DEFAULT_LIBRARY_SELECTION),\n        'FNV_M3_LIB_SHA256': DEFAULT_LIBRARY_SHA256}")
 s=replace(s,"        'FNV_M3': '1', 'FNV_M3_SEL': DEFAULT_SELECTION, 'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '0'}", "        'FNV_M3': '1', 'FNV_M3_SEL': DEFAULT_SELECTION, 'FNV_M3_DV1': '1', 'FNV_M3_DV1_EXT': '0',\n        'FNV_M3_LIB_SELECTION': str(Path(__file__).resolve().parents[1] / DEFAULT_LIBRARY_SELECTION),\n        'FNV_M3_LIB_SHA256': DEFAULT_LIBRARY_SHA256}")
 return s
def main():
 if sha(S.read_bytes())!=SEL or sha(L.read_bytes())!=LIB:raise ValueError('reviewed selection digest changed')
 paths=[(M/'config.py',config,'runtime-next/m3/config.py'),(RN/'build_all.py',driver,'runtime-next/build_all.py'),(M/'tools/test_m3_config.py',tests,'runtime-next/m3/tools/test_m3_config.py')];changes=[];inputs={}
 if OUT.exists():raise FileExistsError('refusing overwrite')
 OUT.mkdir();(OUT/'selection.json').write_bytes(S.read_bytes())
 for p,func,rel in paths:
  original=p.read_text(encoding='utf8');modified=func(original);inputs[rel]=sha(p.read_bytes());(OUT/p.name).write_text(modified,encoding='utf8',newline='\n');changes.extend(difflib.unified_diff(original.splitlines(True),modified.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
 (OUT/'promotion.patch').write_text(''.join(changes),encoding='utf8',newline='\n');(OUT/'manifest.json').write_text(json.dumps({'input_sha256':inputs,'selection_sha256':SEL,'selection_staged':'selection.json','selection_destination':'runtime-next/m3/phase2/selection.json','library_sha256':LIB,'patch_sha256':sha((OUT/'promotion.patch').read_bytes()),'scope':'private staged patch; canonical selection file is a separate exact-copy operation; no protected inputs changed'},indent=2));print('staged',OUT)
if __name__=='__main__':main()
