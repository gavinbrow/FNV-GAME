r"""M3 batch 9 stage 3: reference-free data production support (opt-in FNV_M3_NOREF=1).
  python -I b9_freeze.py --freeze        reads the reference image ONCE (FNV_REF_IMAGE) and writes the frozen inputs to m3\frozen\
  python -I b9_freeze.py --synth OUT     builds the data-stage stand-in image OUT from m3\frozen\ + the strict .text of OUR build (build-v7\FalloutNV_v7_strict.exe); never opens the reference
  python -I b9_freeze.py --verify        (oracle, needs the reference) frozen inputs == reference; synthesized image == reference everywhere the data stages read
Frozen inputs (original game values: m3\frozen\ is not exported, see export_repo.py BAN_PREFIX):
  ref_headers.bin      PE headers (first SizeOfHeaders bytes)
  ref_data.bin.z       zlib: raw bytes of .rdata .data .tls CONST (contiguous in the image)
  ref_reloc.bin.z      zlib: raw bytes of .reloc (original relocation table: the data-v3 field set / original .reloc sites)
  ref_meta.json        section table (offsets/sizes), file size, sha256 of every frozen piece and of the whole reference (provenance only)
The stand-in image keeps every file offset of the reference: .text from our strict build, headers/data/.reloc from the frozen files, .rsrc/.bind zero-filled (no data-stage script reads them)."""
import os, sys, json, zlib, struct, hashlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); FZ = os.path.join(HERE, 'frozen')
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
RN = os.path.join(PROJ, 'runtime-next')
sha = lambda b: hashlib.sha256(b).hexdigest()
DATA = ('.rdata', '.data', '.tls', 'CONST')


def sections(img):
    peo = struct.unpack_from('<I', img, 0x3c)[0]; n = struct.unpack_from('<H', img, peo + 6)[0]; osz = struct.unpack_from('<H', img, peo + 20)[0]
    out = {}
    for i in range(n):
        o = peo + 24 + osz + 40 * i; nm = img[o:o + 8].rstrip(b'\0').decode(); vs, va, rs, rp = struct.unpack_from('<IIII', img, o + 8)
        out[nm] = dict(va=va, vs=vs, raw=rs, off=rp)
    return out, struct.unpack_from('<I', img, peo + 24 + 60)[0]


def freeze():
    ref = open(os.environ.get('FNV_REF_IMAGE') or r'C:\path\to\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe', 'rb').read()
    secs, hdr = sections(ref); os.makedirs(FZ, exist_ok=True)
    lo = secs['.rdata']['off']; hi = max(secs[n]['off'] + secs[n]['raw'] for n in DATA)
    assert all(secs[a]['off'] + secs[a]['raw'] == secs[b]['off'] for a, b in zip(DATA, DATA[1:])), 'data sections must be contiguous in the file'
    r = secs['.reloc']
    pieces = {'ref_headers.bin': ref[:hdr], 'ref_data.bin.z': zlib.compress(ref[lo:hi], 9), 'ref_reloc.bin.z': zlib.compress(ref[r['off']:r['off'] + r['raw']], 9)}
    for k, v in pieces.items(): open(os.path.join(FZ, k), 'wb').write(v)
    meta = dict(note='frozen reference-derived inputs of the data stages (b9_freeze.py --freeze); original game values, not exported', file_size=len(ref), headers=hdr, sections=secs, data_off=lo, data_end=hi,
                reloc_off=r['off'], reloc_raw=r['raw'], reference_sha256=sha(ref), pieces_sha256={k: sha(v) for k, v in pieces.items()}, data_sha256=sha(ref[lo:hi]), reloc_sha256=sha(ref[r['off']:r['off'] + r['raw']]))
    json.dump(meta, open(os.path.join(FZ, 'ref_meta.json'), 'w'), indent=1)
    print('frozen', {k: len(v) for k, v in pieces.items()})


def synth(out):
    meta = json.load(open(os.path.join(FZ, 'ref_meta.json')))
    for k, h in meta['pieces_sha256'].items():
        if sha(open(os.path.join(FZ, k), 'rb').read()) != h: raise SystemExit('frozen input changed: ' + k)
    img = bytearray(meta['file_size']); hd = open(os.path.join(FZ, 'ref_headers.bin'), 'rb').read(); img[:len(hd)] = hd
    t = meta['sections']['.text']; strict = open(os.path.join(RN, 'build-v7', 'FalloutNV_v7_strict.exe'), 'rb').read(); img[t['off']:t['off'] + t['raw']] = strict[t['off']:t['off'] + t['raw']]
    d = zlib.decompress(open(os.path.join(FZ, 'ref_data.bin.z'), 'rb').read()); assert len(d) == meta['data_end'] - meta['data_off']; img[meta['data_off']:meta['data_end']] = d
    r = zlib.decompress(open(os.path.join(FZ, 'ref_reloc.bin.z'), 'rb').read()); assert len(r) == meta['reloc_raw']; img[meta['reloc_off']:meta['reloc_off'] + len(r)] = r
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); open(out, 'wb').write(img)
    print('synthesized', out, len(img), sha(bytes(img)))


def verify():
    meta = json.load(open(os.path.join(FZ, 'ref_meta.json')))
    ref = open(os.environ.get('FNV_REF_IMAGE') or r'C:\path\to\Decompilation\FNV\work\worker1\FalloutNV.runtime-text.exe', 'rb').read()
    assert sha(ref) == meta['reference_sha256'], 'reference differs from the one that was frozen'
    out = os.path.join(HERE, 'gen', 'ref-synth-verify.exe'); synth(out); s = open(out, 'rb').read(); t = meta['sections']['.text']
    ok = s[:meta['headers']] == ref[:meta['headers']] and s[t['off']:t['off'] + t['raw']] == ref[t['off']:t['off'] + t['raw']] and s[meta['data_off']:meta['data_end']] == ref[meta['data_off']:meta['data_end']] \
        and s[meta['reloc_off']:meta['reloc_off'] + meta['reloc_raw']] == ref[meta['reloc_off']:meta['reloc_off'] + meta['reloc_raw']]
    os.remove(out); print('VERIFY', 'OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--freeze' in a: freeze()
    elif '--synth' in a: synth(a[a.index('--synth') + 1])
    elif '--verify' in a: verify()
    else: print(__doc__)
