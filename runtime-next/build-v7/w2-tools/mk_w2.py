"""generate asm_w2.py (non-writing copy of build-v7/assemble_v7.py with obj overlay from w2/obj_v3) """
SP='C:/Users/cjhub/AppData/Local/Temp/claude/d3df7c44bb2dc2c7/66f6aa78-253b-4179-a20c-dce805948bed/scratchpad/w2'
s=open('C:/Projects/Decompilation/runtime-next/build-v7/assemble_v7.py').read()
s=s.replace("HERE = Path(__file__).resolve().parent","HERE = Path('C:/Projects/Decompilation/runtime-next/build-v7')\nOUT = Path('%s')"%SP)
s=s.replace("def init4(*a):\n    A.init(*a)\n","""def init4(*a):
    A.init(*a)
    _C = A.Coff
    def _Cov(path, *x, **k):
        p = Path(path); q = OUT / 'obj_v3' / p.name
        if os.environ.get('W2OBJ', '1') == '1' and q.exists(): p = q
        return _C(p, *x, **k)
    A.Coff = _Cov
""")
a=s.index("    (HERE / 'FalloutNV_v7_strict.exe')")
b=s.index("    # ---- progress (same")
s=s[:a]+s[b:]
k=s.index("    # ---- relocation statistics")
tail='''    import pickle
    fnm = {}
    for i, r in results.items():
        for rec in r['fn']:
            if rec['data'] is not None and Wm[rec['address']-TEXT_VA] == 1: fnm.setdefault(i, []).append(rec['address'])
    prog['seconds'] = round(time.time() - T0)
    (OUT / os.environ.get('W2OUT', 'progress_w2.json')).write_text(json.dumps(prog, indent=1))
    pickle.dump(dict(Wm=Wm, S=S, B=B, rej=rej, cover=cover, cB=np.flatnonzero(cB), fnm=fnm), open(OUT / os.environ.get('W2OUT', 'progress_w2.json').replace('.json', '.pkl'), 'wb'))
    print(json.dumps({k: prog[k] for k in ('ours_bytes','coverage_pct_of_nonpadding_text','missing_b_failed_pieces','missing_c_undecompiled','borrowed_relocation_field_bytes')}), prog['pieces']['eh'])
    return
'''
s=s[:k]+tail+s[k:]
W1='C:/Users/cjhub/AppData/Local/Temp/claude/d3df7c44bb2dc2c7/66f6aa78-253b-4179-a20c-dce805948bed/scratchpad/w1/'
helper='''
def _cpf():
    import json as _j
    d = _j.loads((HERE / 'contrib_pieces.json').read_text())
    ids = set()
    for f in ('eh_targets_add.json', 'eh2_targets_add.json'):
        try: ids |= set(_j.loads(open(W1B + f).read()))
        except Exception: pass
    if os.environ.get('W2EXCL', '1') == '1':
        d = dict(d, pieces=[p for p in d['pieces'] if p.get('target_id') not in ids], eh=[p for p in d.get('eh', []) if p.get('target_id') not in ids])
    return d
'''.replace('W1B', repr(W1))
s=s.replace("json.loads((HERE / 'contrib_pieces.json').read_text())", "_cpf()")
s=s.replace("# ------------------------------------------------------------ worker", helper+"# ------------------------------------------------------------ worker",1)
old="        if not (arr[P] == ref[o:o + L][P]).all(): eh_stat['bytes-differ-from-reference'] += 1;"
assert old in s
s=s.replace(old,"        if not (arr[P] == ref[o:o + L][P]).all(): RJ.append((at, i, data.hex(), t['parent'], notok)); eh_stat['bytes-differ-from-reference'] += 1;")
s=s.replace("    eh_stat = collections.Counter(); rlcache = {}","    eh_stat = collections.Counter(); rlcache = {}; RJ = []")
s=s.replace("rej=rej, cover=cover,","rej=rej, RJ=RJ, cover=cover,")
open(SP+'/asm_w2.py','w').write(s)
