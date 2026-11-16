"""Build-time extraction of binary resources from the user's installed exe (read-only) into build/res/ (NOT source):
FalloutNV.ico (icon group 101 + icons 1-12 re-wrapped as .ico), bitmap180.bmp, spafile.bin (RCDATA SPAFILE), manifest.xml check."""
import pefile, struct, os, sys
here = os.path.dirname(os.path.abspath(__file__))
SRC = (__import__('os').environ.get('FNV_GAME_DIR', r'C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas') + r'\FalloutNV.exe')
out = os.path.join(here, 'build', 'res'); os.makedirs(out, exist_ok=True)
pe = pefile.PE(SRC, fast_load=True); pe.parse_data_directories([2])
R = {}
for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    tn = t.name.decode() if t.name else t.id
    for n in t.directory.entries:
        nn = n.name.decode() if n.name else n.id
        for l in n.directory.entries:
            R[(tn, nn)] = pe.get_data(l.data.struct.OffsetToData, l.data.struct.Size)
grp = R[(14, 101)]
_, _, cnt = struct.unpack_from('<HHH', grp, 0)
ents = [struct.unpack_from('<BBBBHHIH', grp, 6 + 14 * i) for i in range(cnt)]
ico = bytearray(struct.pack('<HHH', 0, 1, cnt)); data = bytearray(); off = 6 + 16 * cnt
for (w, h, c, r, pl, bpp, sz, iid) in ents:
    img = R[(3, iid)]; assert len(img) == sz
    ico += struct.pack('<BBBBHHII', w, h, c, r, pl, bpp, sz, off + len(data)); data += img
    assert iid == ents.index((w, h, c, r, pl, bpp, sz, iid)) + 1
open(os.path.join(out, 'FalloutNV.ico'), 'wb').write(bytes(ico) + bytes(data))
dib = R[(2, 180)]
# DIB -> .bmp (file header needs pixel offset)
hdr = struct.unpack_from('<I', dib, 0)[0]; bpp = struct.unpack_from('<H', dib, 14)[0]; clr = struct.unpack_from('<I', dib, 32)[0]
ncol = clr if clr else ((1 << bpp) if bpp <= 8 else 0)
open(os.path.join(out, 'bitmap180.bmp'), 'wb').write(b'BM' + struct.pack('<IHHI', 14 + len(dib), 0, 0, 14 + hdr + 4 * ncol) + dib)
open(os.path.join(out, 'spafile.bin'), 'wb').write(R[('RT_RCDATA', 'SPAFILE')])
man = os.path.join(here, 'res-src', 'manifest.xml')
if not os.path.exists(man): open(man, 'wb').write(R[(24, 1)])
assert open(man, 'rb').read() == R[(24, 1)], 'manifest.xml differs from installed exe'
print('extracted', len(ents), 'icons, dib', len(dib), 'spafile', len(R[('RT_RCDATA', 'SPAFILE')]))
