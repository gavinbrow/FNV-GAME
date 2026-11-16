"""link-v2 mk_xcu.py: the C++ static-initializer table. The decompiled sources bind it to the original data (their objects carry only 17 .CRT$XCU entries), so the linked exe's
__xc_a..__xc_z range (libcmt crt0init markers) would be nearly empty. This emits the original table (reference [__xc_a, __xc_z) = 0x00fdf4a4..0x010113c0) as a real `.CRT$XCU` section of
`dd C_<va>` entries so _initterm runs every initializer in the original order, and zeroes that range in data-v3 (skip_ranges.json). usage: python -I mk_xcu.py"""
import json, os, struct, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent / 'data-v3'))
from common import ref, SEC, sec_of, TLO, THI
A, Z = 0x00fdf4a4, 0x010113c0
S = SEC['.rdata']; raw = ref[S['off'] + A - S['va']:S['off'] + Z - S['va']]
vals = struct.unpack('<%dI' % ((Z - A) // 4), raw)
LIM = int(os.environ.get('XCU_LIMIT', '-1'))
if LIM >= 0:
    seen = 0; nv = []
    for v in vals:
        if v: seen += 1
        nv.append(v if (v and seen <= LIM) else 0)
    vals = tuple(nv)
bad = [v for v in vals if v and not (TLO <= v < THI)]
print('entries', len(vals), 'non-zero', sum(1 for v in vals if v), 'outside text', len(bad))
asm = ['.386', '.model flat', 'option casemap:none']
tg = sorted({v for v in vals if v and TLO <= v < THI})
asm += ['EXTERNDEF C_%08x:PROC' % t for t in tg]
asm += ['_XCU SEGMENT DWORD USE32 READONLY PUBLIC \'DATA\'']
for v in vals: asm.append('dd C_%08x' % v if v and TLO <= v < THI else 'dd 0')
asm += ['_XCU ENDS', 'END']
d = HERE / 'xcu_asm'; d.mkdir(exist_ok=True); (d / 'xcu.asm').write_text('\n'.join(asm) + '\n')
VC = 'C:/Projects/Decompilation/FNV/tools/vc2008/VC'; env = dict(os.environ); env['PATH'] = VC + '/bin;C:/Projects/Decompilation/FNV/tools/vc2008/Common7/IDE;' + env['PATH']
r = subprocess.run([VC + '/bin/ml.exe', '/c', '/coff', '/nologo', '/Cp', '/Fo', str(HERE / 'supp_obj' / 'zxcu.obj'), str(d / 'xcu.asm')], env=env, capture_output=True, text=True); print(r.stdout[-300:], r.stderr[-300:])
sys.path.insert(0, str(HERE)); import coffrw
pth = HERE / 'supp_obj' / 'zxcu.obj'; bb = bytearray(pth.read_bytes())
for s_ in coffrw.sections(bytes(bb)):
    if s_['name'] == '_XCU': bb[s_['hdr']:s_['hdr'] + 8] = '.CRT$XCU'.encode()
for i_, nm_, v_, sec_, ty_, sc_, na_, o_ in coffrw.symbols(bytes(bb)):
    if nm_ == '_XCU' and sc_ == 3: bb[o_:o_ + 8] = '.CRT$XCU'.encode()
pth.write_bytes(bytes(bb))
sk = json.load(open(HERE / 'skip_ranges.json')); sk = [x for x in sk if x != [A, Z - A]] + [[A, Z - A]]; json.dump(sk, open(HERE / 'skip_ranges.json', 'w'))
json.dump(tg, open(HERE / 'xcu_targets.json', 'w'))
