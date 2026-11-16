"""Regenerate FalloutNV_direct.exe from build-v7 outputs (M1: direct start, no SteamStub wrapper).
Usage: python make_direct.py [src.exe] [out.exe]
Steps: copy build-v7 filled exe, entry -> WinMainCRTStartup (0xECC4DB), drop .bind section
(and the Authenticode cert dir that lived inside it), fix SizeOfImage/SizeOfCode/checksum.
Import dir/IAT, TLS, .rsrc, data sections are still the reference's (borrowed)."""
import sys, struct, shutil, os
import pefile
here = os.path.dirname(os.path.abspath(__file__))
import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--src', default=os.path.join(here, '..', 'build-v7', 'FalloutNV_v7_filled.exe'))
ap.add_argument('--out', default=None)
ap.add_argument('--borrowed', action='store_true', help='keep the reference import tables and .rsrc (variant FalloutNV_direct_borrowed.exe)')
a = ap.parse_args()
src = a.src
out = a.out or os.path.join(here, 'FalloutNV_direct_borrowed.exe' if a.borrowed else 'FalloutNV_direct.exe')
OEP_VA = 0xECC4DB  # WinMainCRTStartup: call __security_init_cookie; jmp __tmainCRTStartup
d = bytearray(open(src, 'rb').read())
pe = pefile.PE(data=bytes(d))
e_lfanew = struct.unpack_from('<I', d, 0x3c)[0]
fh = e_lfanew + 4
opt = fh + 20
nsec = struct.unpack_from('<H', d, fh + 2)[0]
secoff = opt + struct.unpack_from('<H', d, fh + 16)[0]
secs = [(bytes(d[secoff+i*40:secoff+i*40+8]).rstrip(b'\0'), secoff+i*40) for i in range(nsec)]
assert secs[-1][0] == b'.bind', secs
bind_hdr = secs[-1][1]
bind_raw = struct.unpack_from('<I', d, bind_hdr + 20)[0]
bind_va = struct.unpack_from('<I', d, bind_hdr + 12)[0]
d[bind_hdr:bind_hdr+40] = b'\0' * 40
struct.pack_into('<H', d, fh + 2, nsec - 1)
struct.pack_into('<I', d, opt + 16, OEP_VA - 0x400000)         # AddressOfEntryPoint
struct.pack_into('<I', d, opt + 56, bind_va)                    # SizeOfImage
# data dirs: security (4) -> 0
dd = opt + 96
struct.pack_into('<II', d, dd + 4*8, 0, 0)
del d[bind_raw:]
# own import tables + own .rsrc (byte-compared against the reference when --borrowed is not given)
if not a.borrowed:
    sys.path.insert(0, here)
    import json, build_imports, build_rsrc
    def foff(rva):
        for sec in pe.sections:
            if sec.VirtualAddress <= rva < sec.VirtualAddress + sec.SizeOfRawData: return sec.PointerToRawData + rva - sec.VirtualAddress
        raise ValueError(hex(rva))
    r = build_imports.build(json.load(open(build_imports.SPEC)))
    o = foff(r['region_rva']); assert pe.get_data(r['region_rva'], len(r['region'])) is not None
    d[o:o+len(r['region'])] = r['region']
    o = foff(r['iat_rva']); d[o:o+len(r['iat'])] = r['iat']
    rs = pe.OPTIONAL_HEADER.DATA_DIRECTORY[2]
    img = build_rsrc.build(rs.VirtualAddress); assert len(img) <= rs.Size + 0x200, 'rsrc grew; section relayout needed'
    o = foff(rs.VirtualAddress); d[o:o+len(img)] = img
    struct.pack_into('<II', d, dd + 1*8, r['region_rva'], r['dir_size'])
    struct.pack_into('<II', d, dd + 2*8, rs.VirtualAddress, len(img))
# checksum
struct.pack_into('<I', d, opt + 64, 0)
p2 = pefile.PE(data=bytes(d))
cs = p2.generate_checksum()
struct.pack_into('<I', d, opt + 64, cs)
open(out, 'wb').write(d)
print('wrote', out, len(d), 'checksum', hex(cs))
