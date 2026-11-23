r"""Batch 10 step C: the image phase0 (data-v1 front end, code comparison) needs, built WITHOUT the reference image.
  --freeze-meta <reference exe>   one-shot (reads only the PE headers): m3\frozen\pe_meta.json = image base, section table, data directory entries (header constants as JSON fields)
  <out.exe>                       builds the stand-in: headers from pe_meta.json, .text = the strict .text of OUR earlier build (build-v7\FalloutNV_v7_strict.exe, code side output reused as in
                                  batch 9 stage 3), the import directory + IAT generated from the committed direct-v1\iat_spec.json (tool-built), every other byte zero (no .rdata/.data/.rsrc/.reloc bytes)."""
import os, sys, json, struct
sys.dont_write_bytecode = True
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
RN = os.path.join(PROJ, 'runtime-next')
META = os.path.join(RN, 'm3', 'frozen', 'pe_meta.json')


def freeze_meta(exe):
    d = open(exe, 'rb').read(0x1000)
    pe = struct.unpack_from('<I', d, 0x3c)[0]; n = struct.unpack_from('<H', d, pe + 6)[0]; osz = struct.unpack_from('<H', d, pe + 20)[0]
    base = struct.unpack_from('<I', d, pe + 24 + 28)[0]; dd = [list(struct.unpack_from('<II', d, pe + 24 + 96 + 8 * i)) for i in range(16)]
    secs = []
    for i in range(n):
        o = pe + 24 + osz + 40 * i; nm = d[o:o + 8].rstrip(b'\0').decode(); vs, va, rs, rp = struct.unpack_from('<IIII', d, o + 8); fl = struct.unpack_from('<I', d, o + 36)[0]
        secs.append(dict(name=nm, vs=vs, rva=va, rs=rs, raw=rp, flags=fl))
    meta = dict(note='batch 10 step C: PE header constants (no section bytes)', e_lfanew=pe, nsec=n, opt_size=osz, base=base, entry=struct.unpack_from('<I', d, pe + 24 + 16)[0], datadirs=dd, sections=secs)
    json.dump(meta, open(META, 'w'), indent=1); print('wrote', META)


def build(out):
    sys.path.insert(0, os.path.join(RN, 'direct-v1')); import build_imports
    m = json.load(open(META)); spec = json.load(open(build_imports.SPEC)); r = build_imports.build(spec)
    size = max(s['raw'] + s['rs'] for s in m['sections']); img = bytearray(size)
    pe = m['e_lfanew']; img[0:2] = b'MZ'; struct.pack_into('<I', img, 0x3c, pe); img[pe:pe + 4] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', img, pe + 4, 0x14c, m['nsec'], 0, 0, 0, m['opt_size'], 0x102)
    o = pe + 24; struct.pack_into('<H', img, o, 0x10b); struct.pack_into('<I', img, o + 16, m['entry']); struct.pack_into('<I', img, o + 28, m['base'])
    for i, (a, b) in enumerate(m['datadirs']): struct.pack_into('<II', img, o + 96 + 8 * i, a, b)
    for i, s in enumerate(m['sections']):
        q = o + m['opt_size'] + 40 * i; img[q:q + 8] = s['name'].encode().ljust(8, b'\0'); struct.pack_into('<IIIIIIHHI', img, q + 8, s['vs'], s['rva'], s['rs'], s['raw'], 0, 0, 0, 0, s['flags'])
    sec = {s['name']: s for s in m['sections']}
    st = open(os.path.join(RN, 'build-v7', 'FalloutNV_v7_strict.exe'), 'rb').read()
    t = sec['.text']; img[t['raw']:t['raw'] + t['rs']] = st[t['raw']:t['raw'] + t['rs']]
    for blob, rva in ((r['region'], r['region_rva']), (r['iat'], r['iat_rva'])):
        s = next(x for x in m['sections'] if x['rva'] <= rva < x['rva'] + x['rs']); a = s['raw'] + rva - s['rva']; img[a:a + len(blob)] = blob
    open(out, 'wb').write(img); print('stand-in for phase0:', out, len(img), 'bytes; no reference bytes (headers: json; .text: our strict build; imports: iat_spec.json)')


if __name__ == '__main__':
    if sys.argv[1] == '--freeze-meta': freeze_meta(sys.argv[2])
    else: build(sys.argv[1])
