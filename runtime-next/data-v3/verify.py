r"""data-v3 verify.py: round trip. Assemble result (out\*.obj) laid out at the ORIGINAL section addresses, relocations resolved from the object's own symbols + code_symbols.json,
must equal the reference .rdata/.data/.tls/CONST bytes; every relocation must be a field of symbolic.json with the same target symbol and addend; every D_ label must sit at its VA."""
import collections
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
sys.path.insert(0, RN + r'\pinned-build'); sys.path.insert(0, RN + r'\coverage-v3')
import assemble_v3 as A

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
sj = json.load(open(OUT + r'\symbolic.json'))
csym = json.load(open(OUT + r'\code_symbols.json'))
dl = json.load(open(OUT + r'\data_labels.json'))
bss_lo = sj['bss']['va']
want = {}
for sec, off, sym, add, ev, og, kind in sj['fields']:
    want[(sec, off)] = (sym, add)
manifest = json.load(open(OUT + r'\manifest.json'))
OBJSEC = {'.rdata': '.rdata', '.data': '.data', '.tls': '_TLS', 'CONST': '_CONSTPE'}
base = {'.rdata': SEC['.rdata']['va'], '.data': SEC['.data']['va'], '.tls': SEC['.tls']['va'], 'CONST': SEC['CONST']['va'], '.bss': bss_lo}
objs = []
alladdr = {}
for m in manifest:
    c = A.Coff(OUT + chr(92) + m['file'] + '.obj')
    secs = {}
    for i, s in enumerate(c.sections):
        if not s: continue
        if s['name'] == OBJSEC[m['section']]: secs[i] = (m['section'], m['va'] - SEC[m['section']]['va'], s)
        elif s['name'] == '.bss': secs[i] = ('.bss', 0, s)
    for si, sy in c.symbols.items():
        if sy['section'] in secs and sy['storage'] == 2:
            sn, start, s = secs[sy['section']]
            a = (m['va'] + sy['value']) if sn != '.bss' else bss_lo + sy['value']
            if sy['name'] in alladdr: print('DUPLICATE SYMBOL', sy['name']); ok_all = False
            alladdr[sy['name']] = a
    objs.append((m, c, secs))
ok_all = True; stats = collections.Counter()
M3SPL = []; M3SITES = set()
if os.environ.get('DV_M3') == '1':
    sys.path.insert(0, RN + r'\m3'); import splice; M3SPL = splice.load(); M3SITES = set(orig_reloc_sites())
    if os.environ.get('FNV_M3_DV1') == '1': M3SPL += splice.load_dv1()      # batch 5: data-v1 placed pieces of our unit objects, same overlay + same relocation checks
for nm, a in alladdr.items():
    if nm.startswith('D_') and int(nm[2:], 16) != a: print('LABEL MISPLACED', nm, hex(a)); ok_all = False
    stats['labels'] += 1
for nm in dl['data_labels']:
    if nm not in alladdr: print('LABEL MISSING', nm); ok_all = False
tot_rel = 0
for m, c, secs in objs:
    for i, (pn, start, s) in secs.items():
        data = bytearray(s['data']); nrel = 0
        for off, ri, kind in s['relocs']:
            sy = c.symbols[ri]; nm = sy['name']; add, = struct.unpack_from('<i', data, off)
            if kind != 6: print('UNEXPECTED RELOC KIND', kind); ok_all = False; continue
            if nm in alladdr: v = alladdr[nm]
            elif nm in csym: v = csym[nm]['va']
            else: print('UNRESOLVED', nm); ok_all = False; continue
            struct.pack_into('<I', data, off, (v + add) & 0xffffffff)
            w = want.get((pn, start + off))
            if w is None: print('RELOC NOT IN symbolic.json', pn, start + off, nm); ok_all = False
            elif w != (nm, add): print('MISMATCH', pn, start + off, w, (nm, add)); ok_all = False
            nrel += 1
        stats['relocs'] += nrel
        if M3SPL and pn != '.bss':      # FNV_M3=1: bytes of the generated definitions overlay the zeroed (DV3_SKIP) ranges
            for _r in M3SPL:
                _o = _r['va'] - SEC[pn]['va'] - start
                if sec_of(_r['va']) == pn and 0 <= _o and _o + len(_r['data']) <= m['size']:
                    data[_o:_o + len(_r['data'])] = _r['data']; stats['m3-overlay-bytes'] += len(_r['data'])
                    for (_ro, _rn, _ra), _tv in zip(_r['relocs'], _r['reloc_va']):      # phase 1b: our pointer fields: install the relocation and check it against symbolic.json
                        # out\symbolic.json is written after DV3_SKIP, so it has no entry for our fields: check them against the ORIGINAL .reloc sites and the reference value instead
                        _fva = SEC[pn]['va'] + start + _o + _ro; struct.pack_into('<I', data, _o + _ro, (_tv + _ra) & 0xffffffff)
                        if _fva not in M3SITES: print('M3 RELOC NOT AN ORIGINAL .reloc SITE', hex(_fva), _rn); ok_all = False
                        elif struct.unpack('<I', read_ref(_fva))[0] != (_tv + _ra) & 0xffffffff: print('M3 RELOC VALUE MISMATCH', hex(_fva), _rn, hex(_tv), _ra); ok_all = False
                        nrel += 1; stats['relocs'] += 1; stats['m3-overlay-relocs'] += 1
        if pn != '.bss':
            S = SEC[pn]; refb = ref[S['off'] + start:S['off'] + start + m['size']]
            same = bytes(data) == refb
            print(m['file'], pn, 'bytes', len(data), 'equal' if same else 'DIFFERENT', 'relocs', nrel)
            if not same:
                ok_all = False
                d = [k for k in range(min(len(data), len(refb))) if data[k] != refb[k]][:10]; print('  first diffs', d)
        else:
            print(m['file'], '.bss bytes', len(data), 'expected', SEC['.data']['vs'] - SEC['.data']['raw'])
nf = len(want)
print('relocs total', stats['relocs'], 'fields in symbolic.json', nf)
if stats['relocs'] != nf: ok_all = False      # nf includes our pointer fields (gen.py keeps them as ghost fields under DV_M3)
print('ROUND TRIP', 'OK' if ok_all else 'FAILED', dict(stats))
if not ok_all:
    if os.environ.get('FNV_M3_NEGCTL') in ('1', 'ptr', 'b4v', 'b4p', 'b5v', 'b5p', 'b6v', 'b6p', 'b7v', 'b7p'): print('(negative control: failure is expected, exit code 0 so the build continues to the image)')
    else: sys.exit(1)
