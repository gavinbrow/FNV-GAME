"""Freeze every input of make_image.py into layout-v2/snapshot (other workers rebuild build-v7/data-v3 at any time; a mixed set of inputs produces broken images)."""
import os, shutil, hashlib, json
import numpy as np
J = os.path.join
HERE = os.path.dirname(os.path.abspath(__file__)); S = J(HERE, 'snapshot'); os.makedirs(J(S, 'data-v3', 'out'), exist_ok=True)
RN = (__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next'); B7 = J(RN, 'build-v7'); D3 = J(RN, 'data-v3')
def text(p): return np.frombuffer(open(p, 'rb').read(), np.uint8)[0x400:0x400 + 0xbdd600]
open(J(S, 'strict_text.bin'), 'wb').write(text(J(B7, 'FalloutNV_v7_strict.exe')).tobytes())
open(J(S, 'filled_text.bin'), 'wb').write(text(J(B7, 'FalloutNV_v7_filled.exe')).tobytes())
for f in ('relocs_v7.tsv.gz', 'inferred_literals_v7.json', 'contrib_pieces.json'): shutil.copy2(J(B7, f), J(S, f))
shutil.copy2((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\fnv_decomp\build\units.json'), J(S, 'units.json'))
for f in os.listdir(J(D3, 'out')):
    if f.endswith('.obj') or f in ('code_symbols.json', 'manifest.json'): shutil.copy2(J(D3, 'out', f), J(S, 'data-v3', 'out', f))
shutil.copy2(J(D3, 'symbolic.json'), J(S, 'data-v3', 'symbolic.json'))
shutil.rmtree(J(S, 'm3'), ignore_errors=True)     # M3 phase 1 (opt-in): the generated globals' object + manifest; make_image reads them only when FNV_M3=1
if os.environ.get('FNV_M3') == '1':
    os.makedirs(J(S, 'm3'), exist_ok=True)
    for f in ['m3_manifest.json'] + sorted(x for x in os.listdir(J(RN, 'm3', 'gen')) if x.startswith('m3_data') and x.endswith('.obj')): shutil.copy2(J(RN, 'm3', 'gen', f), J(S, 'm3', f))      # m3_data.obj (+ m3_data_<k>.obj, batch 7)
    if os.environ.get('FNV_M3_DV1') == '1': shutil.copy2(J(RN, 'm3', 'gen', 'dv1_pieces.json'), J(S, 'm3', 'dv1_pieces.json'))      # batch 5
man = {}
for r, d, fs in os.walk(S):
    for f in fs: man[os.path.relpath(J(r, f), S)] = hashlib.sha256(open(J(r, f), 'rb').read()).hexdigest()[:16]
json.dump(man, open(J(S, 'manifest.json'), 'w'), indent=1); print('snapshot of', len(man), 'files')
