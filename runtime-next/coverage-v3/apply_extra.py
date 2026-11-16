"""apply_extra.py <in.exe> <out.exe> [extra_pieces.json]  -- write each piece's bytes at its VA (PE32, section table lookup).
Only bytes that the piece list names are changed; a piece whose VA is not file-backed is skipped and reported."""
import sys, json, struct
from pathlib import Path
src, dst = sys.argv[1], sys.argv[2]
pj = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).resolve().parent / 'extra_pieces.json'
b = bytearray(Path(src).read_bytes())
pe = struct.unpack_from('<I', b, 0x3c)[0]
nsec = struct.unpack_from('<H', b, pe + 6)[0]; osz = struct.unpack_from('<H', b, pe + 20)[0]
base = struct.unpack_from('<I', b, pe + 52)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + osz + 40 * i
    vs, rva, rs, raw = struct.unpack_from('<IIII', b, o + 8)
    secs.append((rva, rs, raw))
n = nb = skipped = 0
for p in json.loads(pj.read_text())['pieces']:
    data = bytes.fromhex(p['data']); r = p['address'] - base
    for rva, rs, raw in secs:
        if rva <= r and r + len(data) <= rva + rs:
            o = raw + r - rva; b[o:o + len(data)] = data; n += 1; nb += len(data); break
    else: skipped += 1
Path(dst).write_bytes(b)
print('pieces applied', n, 'bytes', nb, 'skipped', skipped)
