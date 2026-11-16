"""Lay out a cvtres .obj (.rsrc$01 + .rsrc$02) as a PE .rsrc section image at a given RVA (what link.exe does)."""
import struct, sys
def layout(objpath, rva):
    d = open(objpath, 'rb').read()
    ns = struct.unpack_from('<H', d, 2)[0]; secs = {}; symptr = struct.unpack_from('<I', d, 8)[0]
    relkind = lambda x: False
    for i in range(ns):
        o = 20 + 40 * i; nm = d[o:o+8].rstrip(b'\0'); vs, va, sz, rp, rl, lp, nr, nl, fl = struct.unpack_from('<IIIIIIHHI', d, o + 8)
        secs[nm] = (sz, rp, rl, nr)
    s1, p1, r1, n1 = secs[b'.rsrc$01']; s2, p2, _, _ = secs[b'.rsrc$02']
    a = bytearray(d[p1:p1+s1]); off2 = (s1 + 3) & ~3  # reference has .rsrc$02 at 4-byte alignment (cvtres 9 objects carry no explicit alignment); a += bytes(off2 - s1)
    for k in range(n1):
        vaddr, sym, typ = struct.unpack_from('<IIH', d, r1 + 10 * k); assert typ == 7  # DIR32NB
        v = struct.unpack_from('<I', a, vaddr)[0]
        symval = struct.unpack_from('<I', d, symptr + 18 * sym + 8)[0]   # $R00000N symbol: offset inside .rsrc$02
        struct.pack_into('<I', a, vaddr, v + symval + rva + off2)
        if relkind(vaddr): pass
    img = bytearray(a) + d[p2:p2+s2]
    # the reference's resource directory headers carry MajorVersion=4 (older cvtres); patch all directory headers
    def walk(off):
        struct.pack_into('<H', img, off + 8, 4)
        nn, ni = struct.unpack_from('<HH', img, off + 12)
        for i in range(nn + ni):
            _, o = struct.unpack_from('<II', img, off + 16 + 8 * i)
            if o & 0x80000000: walk(o & 0x7fffffff)
    walk(0)
    # data entries carry CodePage 1252 in the reference (cvtres 9 leaves 0); patch the data-entry records
    def walk2(off):
        nn, ni = struct.unpack_from('<HH', img, off + 12)
        for i in range(nn + ni):
            _, o = struct.unpack_from('<II', img, off + 16 + 8 * i)
            if o & 0x80000000: walk2(o & 0x7fffffff)
            else: struct.pack_into('<I', img, o + 8, 1252)
    walk2(0)
    # repack raw data at 4-byte alignment (cvtres 9 uses 8); data order is the .res order = ascending cvtres offset
    ents = []
    def walk3(off):
        nn, ni = struct.unpack_from('<HH', img, off + 12)
        for i in range(nn + ni):
            _, o = struct.unpack_from('<II', img, off + 16 + 8 * i)
            if o & 0x80000000: walk3(o & 0x7fffffff)
            else: ents.append(o)
    walk3(0)
    ents.sort(key=lambda o: struct.unpack_from('<I', img, o)[0])
    head = bytes(img[:off2]); raw = bytearray(); newrva = {}
    for o in ents:
        r, sz = struct.unpack_from('<II', img, o)
        newrva[o] = rva + off2 + len(raw)
        raw += bytes(img[r - rva:r - rva + sz]); raw += b'PADDING'[:(-len(raw)) % 4]  # rc.exe pads resource data with 'PADDING'
    head = bytearray(head)
    for o, v in newrva.items(): struct.pack_into('<I', head, o, v)
    return bytes(head) + bytes(raw)
if __name__ == '__main__':
    import pefile
    img = layout(sys.argv[1], 0xe74000); pe = pefile.PE(sys.argv[2]); ref = pe.get_data(0xe74000, len(img))
    print(len(img), 'identical to reference:', img == ref)
    if img != ref:
        diffs = [i for i in range(len(img)) if img[i] != ref[i]]; print(len(diffs), [hex(x) for x in diffs[:20]])
