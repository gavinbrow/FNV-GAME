r"""data-v2 rename_apply.py: rename classes in source to their original (RTTI) names, recompile the units, and update the recipe (fnv_decomp\build\units.json) so every
function/symbol binding follows the rename. A class is renamed only if it passes all checks; otherwise its source file is restored.
usage: python -I rename_apply.py cands.json        cands: [{old,new,file(rel to src),units:[...]}]
Checks per class: keyword (class/struct) of our definition equals the original's RTTI (V/U); `new` appears nowhere in src; after recompile every symbol of each unit equals the
textually renamed old symbol (so the rename is pure and units.json can follow). Backups: <file>.bak-20261116-wB (source), units.json.bak-20261116-wB (once),
pinned-build\obj_v3.bak-20261116-pilot (objects before the rename batch, once per run, in addition to obj_v3.bak-20261116)."""
import json
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\pinned-build')
sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\coverage-v3')
import assemble_v3 as A
import compile_units_v3 as CU

SRC = 'C:/Projects/Decompilation/fnv_decomp/src/'
UJ = 'C:/Projects/Decompilation/fnv_decomp/build/units.json'
OBJ = r'C:\Projects\Decompilation\runtime-next\pinned-build' + chr(92)
cands = json.load(open(sys.argv[1]))
tag = sys.argv[2] if len(sys.argv) > 2 else 'pilot'
if not os.path.exists(UJ + '.bak-20261116-wB'):
    shutil.copy(UJ, UJ + '.bak-20261116-wB')
bakdir = OBJ + 'obj_v3.bak-20261116-' + tag
if not os.path.exists(bakdir):
    shutil.copytree(OBJ + 'obj_v3', bakdir)
udoc = json.load(open(UJ))
units = udoc['units']
tc = CU.find_toolchains()


sys.path.insert(0, "C:/Projects/Decompilation/runtime-next/data-v2")
from kwswap import swap_keyword
from msub import mangle_sub2

done = []
snapdir = os.environ.get('TEMP', '.') + chr(92) + 'rename_snap'
os.makedirs(snapdir, exist_ok=True)
for c in cands:
    old, new, rel, uids = c['old'], c['new'], c['file'], c['units']
    p = SRC + rel
    raw = open(p, 'rb').read().decode('latin1'); orig_raw = raw
    m = re.search(r'\b(class|struct)\s+' + re.escape(old) + r'\b(?!\s*;)', raw)
    kw_orig = c.get('kw'); kw_from = None
    if not m:
        print('SKIP', old, 'no definition'); continue
    if kw_orig and m.group(1) != kw_orig:
        kw_from = m.group(1)
        raw2 = swap_keyword(raw, old, m.group(1), kw_orig)
        if raw2 is None: print('SKIP', old, 'keyword swap not possible', m.group(1), kw_orig); continue
        raw = raw2
    if re.search(r'\b' + re.escape(new) + r'\b', raw):
        print('SKIP', old, 'new name already in file'); continue
    new_raw = re.sub(r'\b' + re.escape(old) + r'\b', new, raw)
    if not os.path.exists(p + '.bak-20261116-wB'): shutil.copy(p, p + '.bak-20261116-wB')
    prev_raw = orig_raw
    open(p, 'wb').write(new_raw.encode('latin1'))
    ok = True; pairs = {}
    for ui in uids:
        u = units[ui]
        shutil.copy(OBJ + 'obj_v3' + chr(92) + '%04d.obj' % ui, snapdir + chr(92) + '%04d.obj' % ui)
        old_obj = A.Coff(__import__('pathlib').Path(snapdir) / ('%04d.obj' % ui))
        r = CU.one((ui, u, tc))
        if r['status'] != 'ok': print('COMPILE FAIL', ui, r['error'][:150]); ok = False; break
        new_obj = A.Coff(__import__('pathlib').Path(OBJ + 'obj_v3') / ('%04d.obj' % ui))
        on = [old_obj.symbols[i]['name'] for i in sorted(old_obj.symbols)]
        nn = [new_obj.symbols[i]['name'] for i in sorted(new_obj.symbols)]
        if len(on) != len(nn): print('SYMBOL COUNT DIFF', ui, len(on), len(nn)); ok = False; break
        bad = [(a, b) for a, b in zip(on, nn) if mangle_sub2(a, old, new, kw_from, kw_orig) != b]
        if bad: print('SYMBOL MISMATCH', ui, bad[:3]); ok = False; break
    if not ok:
        open(p, 'wb').write(prev_raw.encode('latin1'))
        for ui in uids:
            shutil.copy(snapdir + chr(92) + '%04d.obj' % ui, OBJ + 'obj_v3' + chr(92) + '%04d.obj' % ui)
        continue
    for ui in uids:
        s = json.dumps(units[ui]); s2 = mangle_sub2(s, old, new, kw_from, kw_orig)
        units[ui] = json.loads(s2)
    done.append((old, new, rel, uids)); print('RENAMED', old, '->', new, rel, uids)
open(UJ, 'w', newline='').write(json.dumps(udoc, indent=1).replace(chr(10), chr(13) + chr(10)) + chr(13) + chr(10))
json.dump(done, open(r'C:\Projects\Decompilation\runtime-next\data-v2\renamed_' + tag + '.json', 'w'))
print('renamed', len(done), 'of', len(cands))
