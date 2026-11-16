"""icf_v7: emulate linker identical-COMDAT folding (/OPT:ICF) to resolve borrowed relocation targets from our OWN compiled objects.
For every referenced name that no map resolves (borrowed 'tail:...:None' fields), find its COMDAT body in our compiled objects (obj_v3, the same
objects the build uses) and fold it onto a placed recipe function whose compiled bytes are identical (relocation fields masked) and whose
relocation targets are the same after folding (same name+addend, or same resolved address, or a name already folded to that address).
Iterates to a fixpoint (leaf destructors first). No reference bytes/addresses are read; tail_alias_candidates.json is read only at the end, as a check.
Writes icf_map.json (name -> address), icf_report.json. usage: python -I icf_v7.py [workers]"""
import sys, os, json, struct, gzip, hashlib, collections, re, time
sys.dont_write_bytecode = True
sys.path.append((__import__('os').environ.get('FNV_PY_SITE', r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')))
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
HERE = Path(__file__).resolve().parent
PB = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next\pinned-build')); CV = Path((__import__('os').environ.get('FNV_PROJ_ROOT', r'C:\Projects\Decompilation') + r'\runtime-next\coverage-v3'))
sys.path.insert(0, str(PB)); sys.path.insert(0, str(CV)); sys.path.insert(0, str(HERE))
import assemble_v3 as A
M32 = 0xffffffff
SKIP = ('__catch$', '__unwind', '__ehhandler')


def scan(task):
    idx, unit = task
    out = []
    try: coff = A.Coff(PB / 'obj_v3' / ('%04d.obj' % idx))
    except Exception: return idx, out
    recipe = {}
    for f in unit['functions']:
        for nm in [f['symbol']] + f.get('fold_aliases', []): recipe[nm] = (int(f['address'], 16), f['size'])
    secsig = {}
    def sig(i):
        if i not in secsig: secsig[i] = hashlib.md5(coff.sections[i]['data']).hexdigest()[:12]
        return secsig[i]
    for s in list(coff.symbols.values()):
        if s['section'] <= 0 or not s['type'] & 0x20 or s['storage'] != 2 or s['name'].startswith(SKIP): continue
        sec = coff.sections[s['section']]; start = s['value']
        if sec['name'].startswith('.text$x'): continue
        nm = s['name']
        if nm in recipe: addr, size = recipe[nm]; end = start + size
        else:
            addr = None
            nxt = [x['value'] for x in coff.symbols.values() if x['section'] == s['section'] and x['type'] & 0x20 and x['value'] > start and not x['name'].startswith('__catch$')]
            end = min(nxt) if nxt else len(sec['data'])
        body = bytearray(sec['data'][start:end])
        if addr is None:
            while body and body[-1] in (0xcc,): body.pop()
            end = start + len(body)
        rl = []; bad = False
        for off, ti, kind in sec['relocs']:
            if not start <= off < end: continue
            if kind not in (6, 7, 0x14) or off + 4 > end: bad = True; continue
            t = coff.symbols[ti]; ad, = struct.unpack_from('<i' if kind == 0x14 else '<I', sec['data'], off)
            loc = sig(t['section']) if (t['section'] > 0 and not t['type'] & 0x20) else None
            rl.append((off - start, kind, t['name'], ad, loc, t['storage']))
            body[off - start:off - start + 4] = bytes(4)
        out.append((nm, addr, len(body), hashlib.md5(bytes(body)).hexdigest(), tuple(rl), bad))
    return idx, out


def main():
    T0 = time.time(); W = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    units = json.loads((A.FN / 'build/units.json').read_text())['units']
    comp = {}
    for line in (PB / 'logs' / 'compile_v3.jsonl').read_text().splitlines():
        r = json.loads(line); comp[r['index']] = r
    pe = A.Pe(A.IMG)
    seen = collections.defaultdict(set)
    for u in units:
        for f in u['functions']:
            for n in [f['symbol']] + f.get('fold_aliases', []): seen[n].add(int(f['address'], 16))
    fnnames = {k: next(iter(v)) for k, v in seen.items() if len(v) == 1}
    symnames = A.BAM.recipe_names(units)
    imports, thunks = A.parse_imports(pe); A.G['imp'], A.G['thunks'] = imports, thunks
    tasks = [(i, u) for i, u in enumerate(units) if comp[i]['status'] == 'ok']
    bodies = collections.defaultdict(set)     # name -> {(size, hash, relocs, bad)}   (non-recipe definitions)
    recipe_fns = {}                            # addr -> (name, size, hash, relocs)
    with ProcessPoolExecutor(W) as ex:
        for idx, out in ex.map(scan, tasks, chunksize=16):
            for nm, addr, size, h, rl, bad in out:
                if addr is None: bodies[nm].add((size, h, rl, bad))
                elif addr not in recipe_fns: recipe_fns[addr] = (nm, size, h, rl, bad)
    print('scan', round(time.time() - T0), 's; recipe fns', len(recipe_fns), 'non-recipe names', len(bodies), flush=True)

    # wanted names = targets of borrowed fields with no source
    wanted = collections.Counter()
    for l in gzip.open(HERE / 'borrowed_v7.tsv.gz', 'rt').read().splitlines()[1:]:
        f = l.split('\t')
        if f[2] == 'None': wanted[f[6]] += 1
    print('wanted names', len(wanted), 'fields', sum(wanted.values()))

    def base(name):
        if name in fnnames: return fnnames[name]
        if name in symnames: return symnames[name]
        if not name.startswith(A.NOADDR_PREFIX):
            m = A.ADDR_RE.search(name)
            if m:
                a = int(m.group(1), 16)
                if 0x400000 <= a < 0x400000 + 0x107b000: return a
        a = A.import_target(name)
        return a
    R = {}                                    # folded name -> address
    def addr_of(name):
        v = R.get(name)
        return v if v is not None else base(name)
    # closure: names reachable from wanted bodies that nothing resolves
    todo = list(wanted); Q = set()
    while todo:
        n = todo.pop()
        if n in Q or base(n) is not None: continue
        Q.add(n)
        for (size, h, rl, bad) in bodies.get(n, ()):
            for r_ in rl: todo.append(r_[2])
    print('names to fold (incl. closure)', len(Q), 'of which with a body in our objects', sum(1 for n in Q if n in bodies))
    index = collections.defaultdict(list)
    for a, (nm, size, h, rl, bad) in recipe_fns.items():
        if not bad: index[(size, h)].append((a, nm, rl))
    def same_target(c, f):
        # c, f: reloc tuples (off, kind, tname, addend, loc, storage)
        if c[0] != f[0] or c[1] != f[1]: return False
        if c[4] is not None or f[4] is not None: return c[4] == f[4] and c[3] == f[3]
        if c[2] == f[2] and c[3] == f[3]: return True
        ca, fa = addr_of(c[2]), addr_of(f[2])
        return ca is not None and fa is not None and ca + c[3] == fa + f[3]
    cands = {}; rounds = 0
    while True:
        rounds += 1; changed = 0
        for n in sorted(Q):
            if n in R or n not in bodies: continue
            hits = set()
            for (size, h, rl, bad) in bodies[n]:
                if bad: continue
                for a, fnm, frl in index.get((size, h), ()):
                    if len(frl) == len(rl) and all(same_target(c, f) for c, f in zip(rl, frl)): hits.add(a)
            if hits:
                cands[n] = sorted(hits)
                if len(hits) == 1: R[n] = next(iter(hits)); changed += 1
        if not changed: break
    # ambiguous: several identical placed functions. ICF keeps the first one in link order: use the lowest address (reported separately)
    amb = {n: c for n, c in cands.items() if n not in R}
    for n, c in amb.items(): R[n] = c[0]
    print('rounds', rounds, 'folded unique', len(cands) - len(amb), 'ambiguous (lowest taken)', len(amb), flush=True)
    nobody = [n for n in Q if n not in bodies]; nohit = [n for n in Q if n in bodies and n not in cands]
    (HERE / 'icf_map.json').write_text(json.dumps({n: a for n, a in R.items() if n not in amb}))
    (HERE / 'icf_ambiguous_lowest.json').write_text(json.dumps({n: [R[n], cands[n]] for n in amb}))
    rep = dict(wanted_names=len(wanted), wanted_fields=sum(wanted.values()), names_to_fold_incl_closure=len(Q), no_body_in_our_objects=len(nobody),
               body_but_no_identical_placed_function=len(nohit), folded_unique=len(cands) - len(amb), folded_ambiguous_lowest=len(amb), rounds=rounds,
               wanted_resolved_names=sum(1 for n in wanted if n in R), wanted_resolved_fields=sum(c for n, c in wanted.items() if n in R),
               ambiguity_sizes=dict(collections.Counter(len(c) for c in amb.values())), seconds=round(time.time() - T0))
    # check against the reference-derived candidate file (only now)
    tc = json.loads((PB.parent / 'reloc-v5' / 'tail_alias_candidates.json').read_text())
    agree = dis = nocand = multi = 0; dis_ex = []; diag = collections.Counter()
    for n, a in R.items():
        c = tc.get(n)
        if not c: nocand += 1; continue
        tg = {int(k, 16) for k in c['targets']}
        if len(tg) > 1: multi += 1
        if a in tg: agree += 1
        else:
            dis += 1; dis_ex.append((n, hex(a), sorted(hex(x) for x in tg)[:3], n in amb))
            if n not in amb:
                t0 = next(iter(tg)); rf = recipe_fns.get(t0)
                k = 'ref-target-not-a-recipe-fn' if rf is None else ('ref-target-same-bytes-in-index' if (rf[1], rf[2]) == (recipe_fns[a][1], recipe_fns[a][2]) else 'ref-target-different-bytes')
                diag[k] += 1
    rep['check_vs_tail_alias_candidates'] = dict(agree=agree, disagree=dis, folded_names_not_in_candidates=nocand, candidates_with_multiple_targets=multi,
                                                 disagree_ambiguous=sum(1 for e in dis_ex if e[3]), unique_disagree_diag=dict(diag), disagree_examples=dis_ex[:8])
    (HERE / 'icf_report.json').write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))

if __name__ == '__main__':
    main()
