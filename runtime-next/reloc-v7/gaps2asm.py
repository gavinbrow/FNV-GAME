r"""gaps2asm.py: the .text bytes that no source produces ('failed EH pieces': unwind funclets whose compiled form differs) -> naked asm functions with real instructions.
The strict image of build-v7 marks them 0xCC; the filled image has the reference bytes. Each missing run is widened to whole funclets (a funclet ends with ret or jmp rel32), disassembled,
written as inline asm (call/jmp targets symbolic: SUB_<va>), compiled and compared with the reference (relocation fields masked). Output: gaps_out\gaps.cpp + report.json.
usage: python -I gaps2asm.py"""
import bisect
import collections
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
sys.path.insert(0, r'C:\Projects\Decompilation\FNV\scripts')
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\coverage-v3')
import local_targets as LT
import assemble_v3 as A
import numpy as np
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

B = Path(r'C:\Projects\Decompilation\runtime-next\build-v7')
OUT = Path(r'C:\Projects\Decompilation\runtime-next\reloc-v7\gaps_out'); OUT.mkdir(exist_ok=True)
md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
s = np.fromfile(B / 'FalloutNV_v7_strict.exe', np.uint8); r = np.fromfile(B / 'FalloutNV_v7_filled.exe', np.uint8)
LO = 0x400; N = 0xbdd600; VA0 = 0x401000
S = s[LO:LO + N]; R = r[LO:LO + N]
units = json.loads((A.FN / 'build/units.json').read_text())['units']
fr = sorted((int(f['address'], 16), int(f['address'], 16) + f['size']) for u in units for f in u['functions'])
fks = [x[0] for x in fr]
def in_recipe_fn(va0, va1):
    j = bisect.bisect_left(fks, va1)
    return any(fr[k][1] > va0 for k in range(max(0, j - 3), j))
m = (S == 0xcc) & (R != 0xcc) & (R != 0)
idx = np.flatnonzero(m).tolist(); runs = []; st = idx[0]; p = idx[0]
for i in idx[1:]:
    if i > p + 1: runs.append((int(st), int(p - st + 1))); st = i
    p = i
runs.append((int(st), int(p - st + 1)))
data = bytes(R)


def term_end(off, limit):
    """disassemble from off; return end offset after the first terminator (ret, jmp rel32) or None"""
    pos = off
    while pos < limit:
        ins = next(md.disasm(data[pos:pos + 16], VA0 + pos), None)
        if ins is None: return None
        pos += ins.size
        if ins.mnemonic in ('ret', 'jmp'): return pos
    return None


def extent(st, n):
    en = st + n
    best = None
    for k in range(0, 24):
        a = st - k
        # a must be an instruction boundary reaching st, and the previous byte must end a funclet (ret / end of jmp rel32) or be a placed-gap boundary
        pos = a; ok = True
        while pos < st:
            ins = next(md.disasm(data[pos:pos + 16], VA0 + pos), None)
            if ins is None: ok = False; break
            pos += ins.size
        if not ok or pos != st: continue
        prev_ret = data[a - 1] == 0xc3 or (a >= 5 and data[a - 5] == 0xe9)
        if k == 0 or prev_ret: best = a; break
    if best is None: return None
    pos = st; endpos = None
    while pos < en + 24 and pos < N:
        ins = next(md.disasm(data[pos:pos + 16], VA0 + pos), None)
        if ins is None: return None
        pos += ins.size
        if pos >= en and ins.mnemonic in ('ret', 'jmp'): endpos = pos; break
    if endpos is None: return None
    return best, endpos


ext = []
for st, n in runs:
    e = extent(st, n)
    ext.append(e)
merged = []
for e in sorted(x for x in ext if x):
    if merged and e[0] <= merged[-1][1]: merged[-1] = (merged[-1][0], max(merged[-1][1], e[1]))
    else: merged.append(e)
print('runs', len(runs), 'extents ok', sum(1 for e in ext if e), 'merged functions', len(merged))


def compile_src(text, compiler='sp1', flags=('/MT', '/O2', '/GS', '/EHsc', '/Gy')):
    cl, env = LT._env_for(compiler)
    w = Path(tempfile.mkdtemp(prefix='g2a_')); env = dict(env); env['TMP'] = env['TEMP'] = str(w)
    sp = w / 'a.cpp'; sp.write_bytes(text.replace('\n', '\r\n').encode('latin1')); op = w / 'a.obj'
    rr = subprocess.run([str(cl), '/c', '/nologo'] + list(flags) + ['/I' + str(LT.FN / 'include'), str(sp), '/Fo' + str(op)], cwd=str(LT.FN), env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    if rr.returncode != 0: return None, rr.stdout[-300:]
    c = A.Coff(op); shutil.rmtree(w, ignore_errors=True); return c, ''


results = []; good = []
for a, e in merged:
    va = VA0 + a; code = data[a:e]; size = e - a
    if in_recipe_fn(va, va + size): results.append(dict(va=hex(va), size=size, status='overlaps-recipe-function')); continue
    insts = []; pos = 0
    while pos < size:
        ins = next(md.disasm(code[pos:pos + 16], va + pos), None); insts.append(ins); pos += ins.size
    targets = {i.operands[0].imm for i in insts if i.group(1) and i.mnemonic.startswith('j') and i.operands and i.operands[0].type == X86_OP_IMM and va <= i.operands[0].imm < va + size}
    force = set(); okc = False; decls = set()
    for attempt in range(8):
        items = []; decls = set(); nemit = 0
        for ins in insts:
            off = ins.address - va
            if ins.address in targets: items.append('L%04x:' % off)
            mn = ins.mnemonic
            if ins.address in force: txt = None
            elif mn in ('call', 'jmp') and ins.size == 5 and ins.operands[0].type == X86_OP_IMM:
                t = ins.operands[0].imm
                if va <= t < va + size: txt = '%s L%04x' % (mn, t - va)
                else: nm = 'SUB_%08x' % t; decls.add('void %s();' % nm); txt = '%s %s' % (mn, nm)
            elif ins.group(1) and mn.startswith('j') and ins.operands[0].type == X86_OP_IMM and ins.operands[0].imm in targets: txt = '%s L%04x' % (mn, ins.operands[0].imm - va)
            else: txt = (mn + ' ' + ins.op_str).strip()
            if txt is None:
                items += ['_emit 0x%02x' % x for x in bytes(ins.bytes)]; nemit += ins.size
            else: items.append(txt)
        fname = 'FUN_%08x' % va
        src = '\n'.join(sorted(decls) + ['__declspec(naked) void %s()' % fname, '{', '    __asm {'] + ['        ' + t for t in items] + ['    }', '}', ''])
        c, err = compile_src('// @fnv 0x%08x\n' % va + src)
        if c is None:
            nf = [i.address for i in insts if i.address not in force]
            if nf and attempt < 7: force.add(nf[0]); continue
            break
        sy = [x for x in c.symbols.values() if x['section'] > 0 and x['name'].startswith('?' + fname)][0]
        sec = c.sections[sy['section']]; got = bytes(sec['data']); rel = sorted(o for o, ri, k in sec['relocs'])
        mask = bytearray(b'\x01' * size)
        for o in rel:
            for q in range(o, min(o + 4, size)): mask[q] = 0
        diff = [i for i in range(min(size, len(got))) if mask[i] and got[i] != code[i]]
        if len(got) == size and not diff:
            # relocation targets: rel32 field = target - (field+4); compare after applying symbol addresses
            okc = True; break
        i0 = diff[0] if diff else min(len(got), size)
        cand = [ins.address for ins in insts if ins.address - va <= i0 < ins.address - va + ins.size]
        if not cand or cand[0] in force: break
        force.add(cand[0])
    if okc: good.append(dict(va=va, size=size, src=src, emit=nemit)); results.append(dict(va=hex(va), size=size, status='ok', emit=nemit))
    else: results.append(dict(va=hex(va), size=size, status='fail'))
json.dump(results, open(OUT / 'report.json', 'w'), indent=0)
(OUT / 'gaps.cpp').write_text('\n'.join('// @fnv 0x%08x\n%s' % (g['va'], g['src']) for g in good), encoding='latin1')
json.dump([dict(va=g['va'], size=g['size']) for g in good], open(OUT / 'good.json', 'w'))
print(collections.Counter(x['status'] for x in results), 'bytes ok', sum(g['size'] for g in good), 'emit', sum(g['emit'] for g in good))
