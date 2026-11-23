r"""data-v3 gen_zero.py (batch 10 step C, opt-in via build_all FNV_M3_NOREF2=1): the zero-filled data base.  No reference image, no reference section bytes.
Every initialised byte of .rdata/.data/.tls/CONST is supplied by our overlays (M3 datasrc objects, data-v1 pieces, library pieces) or built by make_image.py (import directory, IAT,
TLS directory), so the base is zero.  Frozen metadata only (m3\frozen\dv3_meta.json: section sizes, bss extent, chunk boundaries and the few pointer fields of the base that no overlay
produces); no section bytes.  Writes the same files as gen.py: out\*.asm, manifest.json, symbolic.json (no fields), code_symbols.json, data_labels.json."""
import json, os, sys, collections
H = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
RN = os.path.join(PROJ, 'runtime-next')
OUT = os.environ.get('DV3_OUT') or os.path.join(H, 'out')
os.makedirs(OUT, exist_ok=True)
meta = json.load(open(os.path.join(RN, 'm3', 'frozen', 'dv3_meta.json')))
SEGDEF = {'.rdata': ("CONST", "SEGMENT DWORD READONLY PUBLIC 'CONST'"), '.data': ('_DATA', "SEGMENT DWORD PUBLIC 'DATA'"),
          '.tls': ('_TLS', "SEGMENT DWORD PUBLIC 'DATA'"), 'CONST': ('_CONSTPE', "SEGMENT DWORD READONLY PUBLIC 'CONST'")}
OBJSEC = {'.rdata': '.rdata', '.data': '.data', '.tls': '_TLS (rename to .tls)', 'CONST': '_CONSTPE (rename to CONST)'}
for f in os.listdir(OUT):
    if f.endswith(('.asm', '.obj')): os.remove(os.path.join(OUT, f))
bss = meta['bss']; secs = meta['sections']
base_fields = collections.defaultdict(list)       # file -> [(offset in chunk, symbol)]  pointer fields of the base that no overlay produces
for bf in meta.get('base_fields', []): base_fields[bf['file']].append(bf)
lits = json.load(open(os.path.join(RN, 'm3', 'datasrc', 'section_literals.json')))
import struct
def literal_bytes(section, size):
    buf = bytearray(size)
    for l in lits.get(section, []):
        b = l['string'].encode() + bytes(1) if 'string' in l else struct.pack('<I', l['dword'])
        buf[l['offset']:l['offset'] + len(b)] = b
    return buf
manifest = []
for m in meta['chunks']:
    seg, defn = SEGDEF[m['section']]; asm = ['.386', '.model flat', 'option casemap:none']
    flds = sorted(base_fields.get(m['file'], []), key=lambda x: x['offset'])
    for f in flds: f['symbol'] = 'B_%08x' % f['target']; f['addend'] = 0
    ext = sorted({f['symbol'] for f in flds})
    for e in ext: asm.append('EXTERNDEF %s:%s' % (e, 'NEAR'))
    asm.append('%s %s' % (seg, defn))
    pos = 0
    for f in flds:
        if f['offset'] > pos: asm.append('db %d dup(0)' % (f['offset'] - pos))
        asm.append('dd offset %s%s' % (f['symbol'], ('%+d' % f['addend']) if f.get('addend') else '')); pos = f['offset'] + 4
    if m['size'] > pos:
        lb = literal_bytes(m['section'], m['size']) if m['section'] in lits and m['va'] == secs[m['section']]['va'] else bytearray(m['size'])
        i = pos
        while i < m['size']:
            if lb[i] == 0:
                j = i
                while j < m['size'] and lb[j] == 0: j += 1
                asm.append('db %d dup(0)' % (j - i)); i = j
            else:
                j = i
                while j < m['size'] and lb[j] != 0 and j - i < 16: j += 1
                asm.append('db ' + ','.join('0%02Xh' % x for x in lb[i:j])); i = j
    asm.append('%s ENDS' % seg)
    if m['section'] == '.data' and m['va'] + m['size'] >= secs['.data']['va'] + secs['.data']['raw']:
        tail = secs['.data']['virt'] - secs['.data']['raw']
        asm += ["_BSS SEGMENT DWORD PUBLIC 'BSS'", 'db %d dup(?)' % tail, '_BSS ENDS']
    asm.append('END')
    open(os.path.join(OUT, m['file'] + '.asm'), 'w').write('\n'.join(asm) + '\n')
    manifest.append(dict(file=m['file'], section=m['section'], va=m['va'], size=m['size'], object_section=OBJSEC[m['section']]))
json.dump(manifest, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=0)
sj = dict(note='zero base (gen_zero.py): no fields; every field comes from the overlays', sections={k: dict(v) for k, v in secs.items()}, bss=dict(bss), fields=[])
json.dump(sj, open(os.path.join(OUT, 'symbolic.json'), 'w'), separators=(',', ':'))
json.dump({'B_%08x' % f['target']: dict(va=f['target'], kind='base-field') for v in base_fields.values() for f in v}, open(os.path.join(OUT, 'code_symbols.json'), 'w'))
json.dump(dict(data_labels={}, ext_targets={}), open(os.path.join(OUT, 'data_labels.json'), 'w'))
print('zero base: %d chunks, %d base pointer fields, reference reads 0' % (len(manifest), sum(len(v) for v in base_fields.values())))
