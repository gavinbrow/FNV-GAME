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
if os.environ.get('FNV_M3_RTTI_NAME_LITERAL') not in (None, '0', '1'): raise ValueError('invalid FNV_M3_RTTI_NAME_LITERAL')
if os.environ.get('FNV_M3_RTTI_NAME_LITERAL') == '1':
    import pickle, hashlib
    sys.path[:0] = [os.path.join(RN, 'm3', 'phase2'), os.path.join(RN, 'data-v1')]
    import place
    from generation_bridge import exclude_literals
    _placement = os.path.join(os.environ['TEMP'], 'dv1_placed.pkl')
    _proof_path = os.path.join(os.environ['TEMP'], 'rtti-name-field-proof.json')
    _proof = json.load(open(_proof_path))
    _fields = {SEC[r[0]]['va'] + r[1]:(int.from_bytes(read_ref(SEC[r[0]]['va'] + r[1],4),'little'),r[4]) for r in sj['fields']}
    _symbols = {int.from_bytes(read_ref(SEC[r[0]]['va'] + r[1],4),'little'):r[2] for r in sj['fields']}
    _chunks = [(r['va'],r['va']+r['size'],r['section'],r['file']) for r in manifest]
    _claims = [(a,a+n) for a,n in json.load(open(os.path.join(RN,'m3','gen','skip_ranges.json')))]
    _expected,_meta = exclude_literals(fields=_fields,symbol_at=lambda t:_symbols[t],st=pickle.load(open(_placement,'rb')),SEC=SEC,original_sites=set(orig_reloc_sites()),read_ref=read_ref,chunks=_chunks,m3_claims=_claims,object_dir=os.path.join(RN,'pinned-build','obj_v3'),proof=_proof,pieces_path=os.path.join(RN,'m3','gen','dv1_pieces.json'),recipe_path=os.path.join(os.path.dirname(RN),'fnv_decomp','build','units.json'),reference_path=REF,placement_path=_placement)
    for _f in _meta['removed_value_fields']:
        _sec=next(k for k,s in SEC.items() if s['va']<=_f<s['va']+s['raw'])
        del want[(_sec,_f-SEC[_sec]['va'])]
    print('AUTHENTICATED NATIVE NAME LITERALS',len(_meta['removed_value_fields']),'original PE relocations preserved',len(orig_reloc_sites()),'proof',_meta['proof_sha256'])
import bisect
VRVA = sorted(SEC[_s]['va'] + _o for _s, _o, _sym, _add, _ev, _og, _kd in sj['fields'] if _ev == 'value-rule' and (_s, _o) in want)      # batch 9 stage 2: value-rule fields (no .reloc site) that an M3 object may hold as plain bytes
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
    splice.validate_records(M3SPL)
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
                    for _vf in VRVA[bisect.bisect_left(VRVA, _r['va']):bisect.bisect_left(VRVA, _r['va'] + len(_r['data']))]:      # value-rule field inside our object: plain value equal to the reference, counted as the field's relocation
                        if bytes(data[_o + _vf - _r['va']:_o + _vf - _r['va'] + 4]) != read_ref(_vf, 4): print('M3 VALUE-RULE FIELD VALUE MISMATCH', hex(_vf)); ok_all = False
                        nrel += 1; stats['relocs'] += 1; stats['m3-overlay-value-rule'] += 1
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
print('relocs total', stats['relocs'], 'canonical fields in symbolic.json', len(sj['fields']), 'expected relocations', nf)
if stats['relocs'] != nf: ok_all = False      # nf includes our pointer fields (gen.py keeps them as ghost fields under DV_M3)
print('ROUND TRIP', 'OK' if ok_all else 'FAILED', dict(stats))
if not ok_all:
    if os.environ.get('FNV_M3_NEGCTL') in ('1', 'ptr', 'b4v', 'b4p', 'b5v', 'b5p', 'b6v', 'b6p', 'b7v', 'b7p', 'b8v', 'b8p', 'b9v', 'b9p', 'dsv', 'dsp', 'p2sv', 'p2av', 'p2wp', 'p2lv', 'p2rv', 'p2rp', 'p2tv', 'p2tp', 'p2nv', 'p2np', 'p2bv', 'p2bp', 'p2bw', 'p2cv', 'p2cp', 'p2cw'): print('(negative control: failure is expected, exit code 0 so the build continues to the image)')
    else: sys.exit(1)
