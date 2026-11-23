r"""Batch 10 step C one-shot: freeze the data-v3 METADATA the zero-filled base needs (section sizes, bss extent, chunk boundaries and the few pointer fields of the base that no
overlay produces) from a normal build's data-v3\out.  No section bytes are frozen.  usage: python -I b10_freeze_dv3.py [data-v3 dir] [out json]"""
import os, sys, json, re
sys.dont_write_bytecode = True
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
RN = os.path.join(PROJ, 'runtime-next')
sys.path.insert(0, os.path.join(PROJ, 'fnv_decomp', 'tools'))
from compare import Coff
D3 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RN, 'data-v3')
OUTJ = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RN, 'm3', 'frozen', 'dv3_meta.json')
OBJSEC = {'.rdata': '.rdata', '.data': '.data', '.tls': '_TLS', 'CONST': '_CONSTPE'}
man = json.load(open(os.path.join(D3, 'out', 'manifest.json'))); sj = json.load(open(os.path.join(D3, 'out', 'symbolic.json')))
cs = json.load(open(os.path.join(D3, 'out', 'code_symbols.json')))
base = []
for m in man:
    c = Coff(os.path.join(D3, 'out', m['file'] + '.obj'))
    for i_, s in enumerate(c.sections):
        if s and s['name'] == OBJSEC[m['section']]:
            for off, ri, kind in s['relocs']:
                assert kind == 6
                nm = c.symbols[ri]['name']; mm = re.fullmatch(r'D_([0-9a-f]{8})', nm)
                va = int(mm.group(1), 16) if mm else cs[nm]['va']
                fva = m['va'] + off
                if any(lo <= fva < hi for lo, hi in ((0xfdf000, 0xfdf4a4), (0x118062c, 0x118204c))): continue      # import directory / IAT: built by make_image.py (build_imports), not relocations of the image
                base.append(dict(file=m['file'], offset=off, target=va))
meta = dict(note='batch 10 step C: metadata for the zero-filled data-v3 base (no bytes). chunks = boundaries of the normal run; base_fields = pointer fields of the base that no overlay produces',
            sections=sj['sections'], bss=sj['bss'], chunks=[dict(file=m['file'], section=m['section'], va=m['va'], size=m['size']) for m in man], base_fields=base)
os.makedirs(os.path.dirname(OUTJ), exist_ok=True)
json.dump(meta, open(OUTJ, 'w'), indent=0)
print('frozen dv3 meta:', len(man), 'chunks,', len(base), 'base pointer fields ->', OUTJ)
for b in base: print('  %s +%d -> %08x' % (b['file'], b['offset'], b['target']))
