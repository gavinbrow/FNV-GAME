"""Own import tables. Spec (iat_spec.json) = per-DLL descriptor order, IAT RVA (slots must match what code uses),
entry order, hints, hint/name stream order. Generator emits: descriptors, ILT blocks (in IAT order), hint/name stream
(per descriptor: hint/names in stream order, then DLL name, even padded) and the initial IAT (== ILT, unbound).
usage: build_imports.py --extract <exe>   (one-time: derive spec from a reference image; writes iat_spec.json)
       build_imports.py --verify <exe>    (compare generated tables with those in <exe>)"""
import struct, json, sys, os
here = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(here, 'iat_spec.json')
IMPORT_DIR_RVA = 0xd8062c

def extract(exe):
    sys.argv = [sys.argv[0], exe]
    import importlib, impdump
    importlib.reload(impdump)
    out = []
    tail_start = max(d['name_rva'] for d in impdump.dl)
    for d in impdump.dl:
        hn = sorted((e[3], k) for k, e in enumerate(d['ents']) if e[0] == 'name')
        rank = {k: v for v, k in hn}  # reference hint/name RVA = global stream order key
        ents = []
        for k, e in enumerate(d['ents']):
            ents.append({'ord': e[1]} if e[0] == 'ord' else {'name': e[2], 'hint': e[1], 'rank': rank[k], 'phase': 2 if rank[k] > tail_start else 1})
        out.append({'dll': d['dll'], 'iat': d['iat'], 'ents': ents})
    json.dump({'import_dir_rva': IMPORT_DIR_RVA, 'dlls': out}, open(SPEC, 'w'), indent=1)

def build(spec):
    dlls = spec['dlls']; base = spec['import_dir_rva']
    desc_size = 20 * (len(dlls) + 1)
    ilt_rva = base + desc_size
    byiat = sorted(range(len(dlls)), key=lambda i: dlls[i]['iat'])
    ilt = {}; p = ilt_rva
    for i in byiat:
        ilt[i] = p; p += 4 * (len(dlls[i]['ents']) + 1)
    hn_rva = {}; name_rva = {}
    stream = bytearray(); sbase = p
    Z = bytes([0])
    def pad(b):
        return b + Z if len(b) & 1 else b
    def emit_hn(i, k):
        e = dlls[i]['ents'][k]
        hn_rva[(i, k)] = sbase + len(stream)
        stream.extend(pad(struct.pack('<H', e['hint']) + e['name'].encode() + Z))
    for i, d in enumerate(dlls):
        for r, k in sorted((e['rank'], k) for k, e in enumerate(d['ents']) if 'name' in e and e['phase'] == 1):
            emit_hn(i, k)
        name_rva[i] = sbase + len(stream)
        stream.extend(pad(d['dll'].encode() + Z))
    # phase 2: hint/name members pulled in later (CRT/lib order), no DLL name between them
    for r, i, k in sorted((e['rank'], i, k) for i, d in enumerate(dlls) for k, e in enumerate(d['ents']) if 'name' in e and e['phase'] == 2):
        emit_hn(i, k)
    desc = bytearray()
    for i, d in enumerate(dlls):
        desc += struct.pack('<5I', ilt[i], 0, 0, name_rva[i], d['iat'])
    desc += bytes(20)
    iltb = bytearray()
    for i in byiat:
        for k, e in enumerate(dlls[i]['ents']):
            iltb += struct.pack('<I', (0x80000000 | e['ord']) if 'ord' in e else hn_rva[(i, k)])
        iltb += bytes(4)
    region = bytes(desc + iltb + stream)
    return dict(region_rva=base, region=region, iat_rva=dlls[byiat[0]]['iat'], iat=bytes(iltb), dir_size=desc_size)

if __name__ == '__main__':
    if sys.argv[1] == '--extract': extract(sys.argv[2])
    elif sys.argv[1] == '--verify':
        import pefile
        pe = pefile.PE(sys.argv[2]); r = build(json.load(open(SPEC)))
        ref = pe.get_data(r['region_rva'], len(r['region'])); print('import region identical:', ref == r['region'], len(r['region']))
        ri = pe.get_data(r['iat_rva'], len(r['iat'])); print('IAT identical:', ri == r['iat'], len(r['iat']))
        if ref != r['region']:
            d = [i for i in range(len(ref)) if ref[i] != r['region'][i]]; print('first diffs', [hex(x) for x in d[:10]], len(d))
