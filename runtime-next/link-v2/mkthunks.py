"""link-v2 mkthunks.py: code targets that no linked object defines and whose original bytes are a bare `jmp dword ptr [abs]` (function-pointer thunks outside the IAT) are
emitted as real assembler thunks C_<va>: jmp [D_<abs>] (the D_ label is data-v3's). usage: python -I mkthunks.py (after a link that produced link1.log)"""
import json, re, struct, subprocess, sys, os
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent / 'data-v3'))
from common import ref, SEC, TLO
T = ref[SEC['.text']['off']:SEC['.text']['off'] + SEC['.text']['raw']]
need = sorted(set(int(m, 16) for m in re.findall(r'unresolved external symbol C_([0-9a-f]{8})', (HERE / 'link1.log').read_text(errors='replace'))))
lines = ['.686', '.model flat', '']; ext = set(); body = []; extra = json.load(open(HERE / 'extra_labels.json')); n = 0
for va in need:
    o = va - TLO
    if T[o:o + 2] == bytes([0xff, 0x25]):
        tgt = struct.unpack_from('<I', T, o + 2)[0]; ext.add(tgt); n += 1
        body.append('PUBLIC C_%08x\nC_%08x PROC\n  jmp dword ptr [D_%08x]\nC_%08x ENDP\n' % (va, va, tgt, va))
        if tgt not in extra: extra.append(tgt)
if n:
    asm = ['.686', '.model flat', '']
    asm += ['EXTRN D_%08x:DWORD' % t for t in sorted(ext)]
    asm += ['.code'] + body + ['END']
    out = HERE / 'thunk_asm'; out.mkdir(exist_ok=True)
    (out / 'thunks.asm').write_text('\n'.join(asm) + '\n')
    env = dict(os.environ); env['PATH'] = 'C:/Projects/Decompilation/FNV/tools/vc2008/VC/bin;' + env['PATH']
    r = subprocess.run(['C:/Projects/Decompilation/FNV/tools/vc2008/VC/bin/ml.exe', '/c', '/coff', '/nologo', '/Cp', '/Fo', str(HERE / 'crt_obj' / 'zthunks.obj'), str(out / 'thunks.asm')], env=env, capture_output=True, text=True)
    print(r.stdout[-300:], r.stderr[-300:]); json.dump(sorted(extra), open(HERE / 'extra_labels.json', 'w'))
print('thunks', n, 'of', len(need), 'unresolved C_ targets')
