r"""merge_fix.py: the last `_emit` bytes in the funclet units. (1) jz rel32 to a target outside the function -> `je SUB_<va>`; (2) functions that start in the middle of an instruction (their first
bytes are the tail of the previous function's last instruction) are merged with the previous function into one function written with real instructions.
usage: python -I merge_fix.py"""
import json
import re
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
import compile_units_v3 as CU
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM

md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
ref = open(r'C:\Projects\Decompilation\runtime-next\build-v7\FalloutNV_v7_filled.exe', 'rb').read()
def rb(va, n): o = 0x400 + va - 0x401000; return ref[o:o + n]
UP = A.FN / 'build' / 'units.json'
shutil.copy(UP, str(UP) + '.bak6-20261116-wB')
doc = json.loads(UP.read_text()); units = doc['units']
FL = ['/MT', '/O2', '/GS', '/EHsc', '/Gy']


def compile_src(text):
    cl, env = LT._env_for('sp1')
    w = Path(tempfile.mkdtemp(prefix='mf_')); env = dict(env); env['TMP'] = env['TEMP'] = str(w)
    sp = w / 'a.cpp'; sp.write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('latin1')); op = w / 'a.obj'
    r = subprocess.run([str(cl), '/c', '/nologo'] + FL + ['/I' + str(LT.FN / 'include'), str(sp), '/Fo' + str(op)], cwd=str(LT.FN), env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL)
    if r.returncode != 0: print(r.stdout[-400:]); return None
    c = A.Coff(op); shutil.rmtree(w, ignore_errors=True); return c


def convert(va, code, fname):
    insts = []; pos = 0
    while pos < len(code):
        ins = next(md.disasm(code[pos:pos + 16], va + pos), None)
        if ins is None: print('DISASM FAIL', hex(va), pos, code[pos:pos + 8].hex()); return None
        insts.append(ins); pos += ins.size
    items = []; decls = set()
    for ins in insts:
        mn = ins.mnemonic; t = None
        if ins.operands and ins.operands[0].type == X86_OP_IMM and (mn == 'call' or mn == 'jmp' or (mn.startswith('j') and ins.group(1))):
            tg = ins.operands[0].imm; nm = 'SUB_%08x' % tg; decls.add('void %s();' % nm); t = '%s %s' % (mn, nm)
        else: t = (mn + ' ' + ins.op_str).strip()
        items.append(t)
    src = '\n'.join(sorted(decls) + ['__declspec(naked) void %s()' % fname, '{', '    __asm {'] + ['        ' + t for t in items] + ['    }', '}', ''])
    c = compile_src(src)
    if c is None: return None
    sy = [x for x in c.symbols.values() if x['section'] > 0 and x['name'].startswith('?' + fname)][0]
    sec = c.sections[sy['section']]; got = bytes(sec['data']); mask = bytearray(b'\x01' * len(code))
    for o, ri, k in sec['relocs']:
        for q in range(o, min(o + 4, len(code))): mask[q] = 0
    if len(got) != len(code) or any(mask[i] and got[i] != code[i] for i in range(len(code))): print('MISMATCH', fname); return None
    return src


def fix_in_unit(path_rel, old_va):
    """returns the functions list entry etc."""


# --- the 5 functions
cases = {0x00f2954e: 'merge'}
funcs = {}   # va -> (unit idx, entry)
for ui, u in enumerate(units):
    if u['source'].startswith('src/funclets/'):
        for f in u['functions']: funcs[int(f['address'], 16)] = (ui, f)
byend = {va + f['size']: va for va, (ui, f) in funcs.items()}
newfuncs = []     # (ui, remove vas, new va, size, src)
for va, kind in cases.items():
    ui, f = funcs[va]; size = f['size']
    if kind == 'jz':
        code = rb(va, size); fname = 'FUN_%08x' % va
        src = convert(va, code, fname)
        if src: newfuncs.append((ui, [va], va, size, src))
    else:      # starts one byte early: its first byte is the last byte of the previous jmp rel32
        size = {0x00f2954e: 27}.get(va, size)
        code = rb(va + 1, size - 1); fname = 'FUN_%08x' % (va + 1)
        src = convert(va + 1, code, fname)
        if src: newfuncs.append((ui, [va], va + 1, size - 1, src))
print('converted', len(newfuncs), 'of', len(cases))
byunit = {}
for t in newfuncs: byunit.setdefault(t[0], []).append(t)
touched = set()
for ui, lst in byunit.items():
    path = A.FN / units[ui]['source']; txt = path.read_bytes().decode('latin1')
    for t in lst:
        remove = t[1]; new_va = t[2]; size = t[3]; src = t[4]; pui = t[5] if len(t) > 5 else ui
        for rv in remove:
            fui = funcs[rv][0]; fp = A.FN / units[fui]['source']
            body = fp.read_bytes().decode('latin1') if fp != path else txt
            m = re.search(r'// @fnv 0x%08x\r?\n__declspec\(naked\) void FUN_%08x\(\)\r?\n\{.*?\r?\n\}\r?\n' % (rv, rv), body, re.S)
            assert m, hex(rv)
            body = body[:m.start()] + body[m.end():]
            if fp == path: txt = body
            else: fp.write_bytes(body.encode('latin1')); touched.add(fui)
            units[fui]['functions'] = [x for x in units[fui]['functions'] if int(x['address'], 16) != rv]
        txt = txt.rstrip('\r\n') + '\r\n\r\n// @fnv 0x%08x\r\n' % new_va + src.replace('\n', '\r\n')
        units[ui]['functions'].append(dict(address='0x%08x' % new_va, symbol='?FUN_%08x@@YAXXZ' % new_va, size=size))
    path.write_bytes(txt.encode('latin1')); touched.add(ui)
UP.write_text(json.dumps(doc, indent=1).replace('\n', '\r\n') + '\r\n')
tc = CU.find_toolchains()
for ui in sorted(touched):
    r = CU.one((ui, units[ui], tc)); print('compile', ui, r['status'], r['error'][:150])
