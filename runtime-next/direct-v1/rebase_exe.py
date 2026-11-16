"""Statically rebase a PE32 using its own .reloc (all HIGHLOW entries += delta) and set the new ImageBase.
usage: rebase_exe.py in.exe out.exe 0x1000000"""
import sys, struct, pefile
src, dst, nb = sys.argv[1], sys.argv[2], int(sys.argv[3], 0)
d = bytearray(open(src, 'rb').read()); pe = pefile.PE(src); pe.parse_data_directories([5])
old = pe.OPTIONAL_HEADER.ImageBase; delta = (nb - old) & 0xffffffff
def foff(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + max(s.SizeOfRawData, 0): return s.PointerToRawData + rva - s.VirtualAddress
    raise ValueError(hex(rva))
n = 0; skipped = 0
for blk in pe.DIRECTORY_ENTRY_BASERELOC:
    for e in blk.entries:
        if e.type == 0: continue
        assert e.type == 3, e.type
        o = foff(e.rva); v = struct.unpack_from('<I', d, o)[0]; struct.pack_into('<I', d, o, (v + delta) & 0xffffffff); n += 1
opt = pe.DOS_HEADER.e_lfanew + 24
struct.pack_into('<I', d, opt + 28, nb)
if '--aslr' in sys.argv:  # DYNAMIC_BASE: loader must pick another base and apply .reloc itself
    struct.pack_into('<H', d, opt + 70, struct.unpack_from('<H', d, opt + 70)[0] | 0x40)
struct.pack_into('<I', d, opt + 64, 0); struct.pack_into('<I', d, opt + 64, pefile.PE(data=bytes(d)).generate_checksum())
open(dst, 'wb').write(d); print('rebased', n, 'fields', hex(old), '->', hex(nb))
