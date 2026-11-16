r"""emit2asm.py: turn `_emit` byte contributions (EH unwind funclets) into naked-asm functions written with real instructions and symbolic call targets.
For each accepted contribution in an address range: compile the current source (the reference object), disassemble its code with the relocations known, write the instructions as
MSVC inline asm, recompile and compare code bytes + relocation table with the reference object. A mismatching instruction is kept as `_emit` bytes (counted) and the loop retries.
usage: python -I emit2asm.py LO HI outdir      -> writes outdir\<addr>.cpp for every converted target and outdir\report.json"""
import collections
import json
import os
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
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

LO, HI, OUTD = int(sys.argv[1], 16), int(sys.argv[2], 16), Path(sys.argv[3])
OUTD.mkdir(parents=True, exist_ok=True)
md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
state = json.loads(LT.STATE.read_text(encoding='utf-8')); acc = state['accepted']
cat = LT.catalog(); by_addr = {t['address']: t for t in cat.values()}


def compile_src(src_text, compiler, flags, tag):
    cl, env = LT._env_for(compiler)
    w = Path(tempfile.mkdtemp(prefix='e2a_'))
    try:
        env = dict(env); env['TMP'] = env['TEMP'] = str(w)
        sp = w / 'a.cpp'; sp.write_bytes(src_text.replace('\r\n', '\n').replace('\n', '\r\n').encode('latin1'))
        op = w / 'a.obj'
        r = subprocess.run([str(cl), '/c', '/nologo'] + flags + ['/I' + str(LT.FN / 'include'), str(sp), '/Fo' + str(op)], cwd=str(LT.FN), env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, timeout=120)
        if r.returncode != 0 or not op.exists(): return None, (r.stdout + r.stderr)[-300:]
        c = A.Coff(op)
        return c, ''
    finally:
        shutil.rmtree(w, ignore_errors=True)


def code_of(c, name):
    """(bytes, [(offset, targetname, kind)]) of the function section in a Coff"""
    sy = c.named(name)
    s = c.sections[sy['section']]
    data = bytes(s['data'])
    rel = sorted((off, c.symbols[ri]['name'], kind) for off, ri, kind in s['relocs'])
    return data, rel


def build_source(hdr_lines, fname, addr, items):
    out = ['// @fnv 0x%08x' % addr] + hdr_lines + ['__declspec(naked) void %s()' % fname, '{', '    __asm {']
    for it in items:
        out.append('        ' + it)
    out += ['    }', '}', '']
    return '\n'.join(out)


results = {}
for a_str, a in sorted(acc.items()):
    addr = int(a_str, 16)
    if not (LO <= addr < HI): continue
    srcp = LT.CONTRIB / ('FUN_%s.cpp' % a_str[2:])
    if not srcp.exists(): results[a_str] = dict(status='no-source'); continue
    t = by_addr.get(a_str)
    compiler = a.get('compiler') or t['compiler']
    flags = list(a['flags']) if a.get('flags') else t['flags']
    old = srcp.read_text(encoding='latin1')
    fname = 'FUN_%s' % a_str[2:]
    if '_emit' not in old: results[a_str] = dict(status='no-emit'); continue
    _ol = old.splitlines()
    if not any(l.startswith('__declspec') for l in _ol): results[a_str] = dict(status='no-naked-decl'); continue
    hdr = [l for l in _ol[:next(k for k, l in enumerate(_ol) if l.startswith('__declspec'))] if l.strip() and not l.startswith('// @fnv')]
    c0, err = compile_src(old, compiler, flags, 'old')
    if c0 is None: results[a_str] = dict(status='old-compile-fail', err=err); continue
    mangled = [sy['name'] for sy in c0.symbols.values() if sy['section'] > 0 and sy['name'].startswith('?' + fname)]
    if not mangled: results[a_str] = dict(status='no-func-symbol'); continue
    code0, rel0 = code_of(c0, mangled[0])
    relmap = {off: (nm, k) for off, nm, k in rel0}
    # disassemble
    insts = []; pos = 0
    while pos < len(code0):
        ins = next(md.disasm(code0[pos:pos + 16], pos), None)
        if ins is None: insts.append(('bytes', pos, code0[pos:pos + 1], None)); pos += 1; continue
        insts.append(('ins', pos, bytes(ins.bytes), ins)); pos += ins.size
    targets = set()
    for kind, p, b, ins in insts:
        if kind == 'ins' and ins.group(1) and (ins.mnemonic.startswith('j') or ins.mnemonic in ('loop',)) and ins.operands and ins.operands[0].type == X86_OP_IMM:
            tgt = ins.operands[0].imm
            if tgt < len(code0): targets.add(tgt)
    force_emit = set()
    ok = False
    for attempt in range(40):
        items = []
        nemit = 0
        for kind, p, b, ins in insts:
            if p in targets: items.append('L%04x:' % p)
            relhere = [o for o in relmap if p <= o < p + len(b)]
            if kind == 'bytes' or p in force_emit:
                if relhere: items.append('// reloc inside raw bytes');
                for x in b: items.append('_emit 0x%02x' % x)
                nemit += len(b); continue
            txt = None
            mn = ins.mnemonic
            if relhere:
                o = relhere[0]; nm, k = relmap[o]
                sym = re.sub(r'^\?(\w+)@@.*$', r'\1', nm) if nm.startswith('?') else nm.lstrip('_')
                if mn in ('call', 'jmp') and o == p + 1 and len(b) == 5: txt = '%s %s' % (mn, sym)
                elif o == p + len(b) - 4 and k == 6 and mn in ('push', 'mov') and ins.operands and ins.operands[-1].type == X86_OP_IMM:
                    txt = ins.mnemonic + ' ' + ins.op_str.rsplit(',', 1)[0] + ', offset ' + sym if mn == 'mov' else 'push offset ' + sym
                if txt is None:
                    items.append('// reloc inside raw bytes: %s' % nm)
                    for x in b: items.append('_emit 0x%02x' % x)
                    nemit += len(b); continue
            else:
                if ins.group(1) and (mn.startswith('j') or mn == 'loop') and ins.operands[0].type == X86_OP_IMM and ins.operands[0].imm in targets:
                    txt = '%s L%04x' % (mn, ins.operands[0].imm)
                else:
                    txt = (mn + ' ' + ins.op_str).strip()
            items.append(txt)
        new_src = build_source(hdr, fname, addr, items)
        c1, err = compile_src(new_src, compiler, flags, 'new')
        if c1 is None:
            # find an instruction that fails to assemble: force the last non-forced instruction mentioned? fall back to emitting everything non-trivial
            nf = [p for kind, p, b, ins in insts if p not in force_emit and kind == 'ins']
            if attempt < 6 and nf: force_emit.add(nf[0]); continue
            results[a_str] = dict(status='new-compile-fail', err=err[:300], dbg=new_src[:900]); break
        m1 = [sy['name'] for sy in c1.symbols.values() if sy['section'] > 0 and sy['name'].startswith('?' + fname)]
        code1, rel1 = code_of(c1, m1[0])
        if code1 == code0 and rel1 == rel0: ok = True; break
        # first differing instruction
        n = min(len(code0), len(code1)); d = next((i for i in range(n) if code0[i] != code1[i]), n)
        cand = [p for kind, p, b, ins in insts if p <= d < p + len(b)]
        if not cand or cand[0] in force_emit: results[a_str] = dict(status='cannot-match', at=d); break
        force_emit.add(cand[0])
    if ok:
        (OUTD / ('%s.cpp' % a_str[2:])).write_text(new_src, encoding='latin1')
        results[a_str] = dict(status='ok', size=len(code0), emit_bytes=nemit, compiler=compiler, flags=flags, hdr=hdr)
json.dump(results, open(OUTD / 'report.json', 'w'), indent=0)
c = collections.Counter(r['status'] for r in results.values())
print(dict(c), 'bytes ok', sum(r.get('size', 0) for r in results.values() if r['status'] == 'ok'), 'emit bytes left', sum(r.get('emit_bytes', 0) for r in results.values() if r['status'] == 'ok'))
