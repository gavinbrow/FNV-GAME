"""fix2.py: the last two `_emit` contributions (0x00ec408c `rep ret`, 0x00fde581 static-init stub + 117 data bytes) as real source (rep ret, db data); compile-compare against the
accepted object, write src\funclets\tail_stubs.cpp, add the unit, retire the contributions. usage: python -I fix2.py [--apply]"""
import json
import re
import shutil
import sys
import tempfile
import subprocess
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
sys.path.insert(0, r'C:\Projects\Decompilation\FNV\scripts')
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\coverage-v3')
import local_targets as LT
import assemble_v3 as A
import compile_units_v3 as CU

state = json.loads(LT.STATE.read_text(encoding='utf-8')); acc = state['accepted']


def compile_src(text, compiler, flags):
    cl, env = LT._env_for(compiler)
    w = Path(tempfile.mkdtemp(prefix='fx2_'))
    env = dict(env); env['TMP'] = env['TEMP'] = str(w)
    sp = w / 'a.cpp'; sp.write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('latin1')); op = w / 'a.obj'
    r = subprocess.run([str(cl), '/c', '/nologo'] + flags + ['/I' + str(LT.FN / 'include'), str(sp), '/Fo' + str(op)], cwd=str(LT.FN), env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    if r.returncode != 0: print(r.stdout[-400:]); return None
    c = A.Coff(op); shutil.rmtree(w, ignore_errors=True); return c


def code(c, fname):
    sy = [s for s in c.symbols.values() if s['section'] > 0 and s['name'].startswith('?' + fname)][0]
    s = c.sections[sy['section']]
    return bytes(s['data']), sorted((o, c.symbols[ri]['name'], k) for o, ri, k in s['relocs'])


out = {}
# 1. 0xec408c
new1 = """// @fnv 0x00ec408c
void FUN_00ed159c();
extern unsigned int DAT_011c16bc;
__declspec(naked) void FUN_00ec408c()
{
    __asm {
        cmp ecx, DAT_011c16bc
        jne L1
        rep ret
    L1:
        jmp FUN_00ed159c
    }
}
"""
# 2. 0xfde581
old2 = (LT.CONTRIB / 'FUN_00fde581.cpp').read_text()
b = bytes(int(x, 16) for x in re.findall(r'_emit (0x[0-9a-fA-F]+)', old2))
rows = ['        db ' + ', '.join('0x%02x' % x for x in b[i:i + 16]) for i in range(0, len(b), 16)]
new2 = """// @fnv 0x00fde581
extern char DAT_0126fc95;
void FUN_00ec3b35();
__declspec(naked) void FUN_00fde581()
{
    __asm {
        mov ecx, offset DAT_0126fc95
        jmp FUN_00ec3b35
        // 117 bytes of data stored in .text after the stub
""" + '\n'.join(rows) + "\n    }\n}\n"
good = []
for a, new in (('0x00ec408c', new1), ('0x00fde581', new2)):
    old = (LT.CONTRIB / ('FUN_%s.cpp' % a[2:])).read_text()
    t = acc[a]; comp = t.get('compiler'); flags = t.get('flags')
    cat = {x['address']: x for x in LT.catalog().values()}
    comp = comp or cat[a]['compiler']; flags = flags or cat[a]['flags']
    c0 = compile_src(old, comp, flags); c1 = compile_src(new, comp, flags)
    if not c0 or not c1: print(a, 'compile fail'); continue
    f = 'FUN_%s' % a[2:]
    d0, r0 = code(c0, f); d1, r1 = code(c1, f)
    print(a, 'bytes equal', d0 == d1, 'relocs equal', r0 == r1, len(d0))
    if d0 == d1 and r0 == r1: good.append((a, new, comp, flags, len(d0)))
if '--apply' in sys.argv and good:
    FN = CU.FN
    parts = ['// funclets/tail_stubs.cpp: two stubs that were _emit contributions', '']
    decl = set(); body = []
    for a, new, comp, flags, n in good:
        ls = new.splitlines(); i = next(k for k, l in enumerate(ls) if l.startswith('__declspec'))
        decl.update(l for l in ls[1:i] if l.strip()); body += ['// @fnv %s' % a] + ls[i:] + ['']
    parts += sorted(decl) + [''] + body
    rel = 'src/funclets/tail_stubs.cpp'
    (FN / rel).write_bytes('\r\n'.join(parts).encode('latin1'))
    comp, flags = good[0][2], good[0][3]
    udoc_path = FN / 'build' / 'units.json'; shutil.copy(udoc_path, str(udoc_path) + '.bak3-20261116-wB')
    udoc = json.loads(udoc_path.read_text()); units = udoc['units']
    u = dict(source=rel, compiler=comp, flags=list(flags), functions=[dict(address=a, symbol='?FUN_%s@@YAXXZ' % a[2:], size=n) for a, _, _, _, n in good], symbols={})
    idx = len(units); units.append(u)
    r = CU.one((idx, u, CU.find_toolchains())); print(rel, idx, r['status'], r['error'][:200])
    assert r['status'] == 'ok'
    udoc_path.write_text(json.dumps(udoc, indent=1).replace('\n', '\r\n') + '\r\n')
    with open(r'C:\Projects\Decompilation\runtime-next\pinned-build\logs\compile_v3.jsonl', 'a') as f:
        f.write(json.dumps(dict(index=idx, source=rel, compiler=comp, status='ok', rc=0, error='', seconds=r['seconds'])) + '\n')
    cat = json.loads(LT.CATALOG.read_text(encoding='utf-8'))
    for a, *_ in good:
        state['accepted'].pop(a, None)
        for k in [k for k, t in cat['targets'].items() if t['address'] == a]: cat['targets'].pop(k)
        shutil.move(str(LT.CONTRIB / ('FUN_%s.cpp' % a[2:])), r'C:\Projects\Decompilation\FNV\local\contributions-replaced\FUN_%s.cpp.emit2asm-20261116' % a[2:])
    LT.STATE.write_text(json.dumps(state, indent=1), encoding='utf-8'); LT.CATALOG.write_text(json.dumps(cat, indent=1), encoding='utf-8')
    print('retired', [g[0] for g in good])
