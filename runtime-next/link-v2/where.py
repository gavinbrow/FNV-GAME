"""link-v2 where.py: map a VA of the linked exe to the nearest map symbol and disassemble. usage: python -I where.py <hexva> [ninstr]"""
import re, struct, sys, bisect, capstone
va = int(sys.argv[1], 16); nin = int(sys.argv[2]) if len(sys.argv) > 2 else 12
rows = []
for l in open('linked.map', errors='replace'):
    m = re.match(r'\s*([0-9a-f]{4}):([0-9a-f]{8})\s+(\S+)\s+([0-9a-f]{8})\s+(?:f\s+)?(?:i\s+)?(\S+)', l)
    if m: rows.append((int(m.group(4), 16), m.group(3), m.group(5)))
rows.sort(); i = bisect.bisect(rows, (va, '~', '')) - 1; print(hex(rows[i][0]), rows[i][1], rows[i][2], '+', hex(va - rows[i][0]))
b = open('FalloutNV_linked.exe', 'rb').read(); pe = struct.unpack_from('<I', b, 0x3c)[0]; so = pe + 24 + struct.unpack_from('<H', b, pe + 20)[0]
for k in range(struct.unpack_from('<H', b, pe + 6)[0]):
    n, vs, sva, rs, rp = struct.unpack_from('<8sIIII', b, so + 40 * k)
    if 0x400000 + sva <= va < 0x400000 + sva + max(vs, rs):
        s0 = max(rows[i][0], va - 0x30); o = rp + (s0 - 0x400000 - sva)
        for ins in capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32).disasm(b[o:o + 0x80], s0):
            print(('=> ' if ins.address == va else '   ') + hex(ins.address), ins.mnemonic, ins.op_str)
            if ins.address > va + 24: break
        break
