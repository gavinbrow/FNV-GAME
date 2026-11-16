"""w2: diagnose why EH pieces are not-ok. non-writing. usage: ehdiag.py unit_idx..."""
import sys, os, json, inspect, collections
sys.dont_write_bytecode = True
sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
from pathlib import Path
PB = Path(r'C:\Projects\Decompilation\runtime-next\pinned-build')
sys.path.insert(0, str(PB)); sys.path.insert(0, r'C:\Projects\Decompilation\runtime-next\coverage-v3')
import assemble_v3 as A
WHY = []
W2OBJ = Path(__file__).resolve().parent / 'obj_v3'
_Coff = A.Coff
def _CoffOv(path, *a, **k):
    p = Path(path)
    if os.environ.get('W2OBJ', '1') == '1' and (W2OBJ / p.name).exists(): p = W2OBJ / p.name
    return _Coff(p, *a, **k)
A.Coff = _CoffOv
def setup():
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    pe = A.Pe(A.IMG)
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnn = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    sym = A.BAM.recipe_names(units)
    imp, th = A.parse_imports(pe)
    A.init(fnn, sym, imp, th)
    src = inspect.getsource(A.BAM.eh_sections)
    src = src.replace('out.append([at, at + s1 - s0, ok, parent, sorted(guessed)])', 'out.append([at, at + s1 - s0, ok, parent, sorted(guessed), bytes(data[s0:s1]), index, s0])')
    src = src.replace('return out, inferred, errors', 'return out, inferred, errors, dict(data_bases), dict(anchors)')
    a = "mask, ok, guessed = set(), parent in matched, set()"
    assert a in src
    src = src.replace(a, a + "\n            if not ok: WHY.append((at, 'parent-unmatched', parent))")
    b = "                if expected is None or expected & 0xffffffff != observed:\n                    ok = False"
    assert b in src
    src = src.replace(b, b + "\n                    WHY.append((at, 'reloc', target['name'][:90], kind, expected, observed, target['section']))")
    c = "            if any(piece[i] != original[i] for i in range(len(piece)) if i not in mask):\n                ok = False"
    assert c in src
    src = src.replace(c, c + "\n                WHY.append((at, 'bytes'))")
    d = "ok = False; errors.append('%s: relocation kind %d in a tail' % (parent, kind)); continue"
    assert d in src
    src = src.replace(d, "WHY.append((at,'kind',kind)); " + d)
    ns = dict(A.BAM.__dict__); ns['WHY'] = WHY; exec(src, ns)
    A.G['eh'] = ns['eh_sections']
    return units
if __name__ == '__main__':
    units = setup()
    idxs = [int(x) for x in sys.argv[1:]]
    for i in idxs:
        WHY.clear()
        if not units[i].get('eh_tails'): units[i]['eh_tails'] = [{'address': '0x0', 'size': 0, 'dummy': True}]
        r = A.process((i, units[i]))
        for t in r['tails']:
            if not t['ok']:
                w = [x for x in WHY if x[0] == t['address']]
                print(i, hex(t['address']), len(t['data']) if t['data'] else None, hex(t['parent']) if isinstance(t['parent'], int) else t['parent'], w[:4])
