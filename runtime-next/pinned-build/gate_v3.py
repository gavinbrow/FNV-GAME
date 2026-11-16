"""Greedy per-class gate for the sized-delete edits of one unit: keep a class edit only if it gains tails and loses nothing."""
import sys, json, subprocess, os
from pathlib import Path
HERE = Path(__file__).resolve().parent; FN = Path(r'C:\Projects\Decompilation\fnv_decomp')
U = json.load(open(FN / 'build/units.json'))['units']; plan = json.load(open(HERE / 'logs/sized_plan_v3.json'))
base = json.load(open(HERE / 'logs/base_v3.json'))
def run(args, env=None): return subprocess.run([sys.executable, '-I'] + args, cwd=HERE, capture_output=True, text=True, env={**os.environ, **(env or {})})
def check(u):
    run(['check_units_v3.py', 'logs/gate_tmp.json', str(u)]); return json.load(open(HERE / 'logs/gate_tmp.json'))[str(u)]
for u in map(int, sys.argv[1:]):
    src = U[u]['source']
    subprocess.run(['git', 'checkout', '--', src], cwd=FN)
    classes = list(dict.fromkeys(c for o in plan if o['unit'] == u for c in o['cands']))
    acc = []; cur = base[str(u)]
    for c in classes:
        subprocess.run(['git', 'checkout', '--', src], cwd=FN)
        run(['tail_fix_v3.py', 'apply', str(u)], {'TF_ONLY': ','.join(acc + [c])})
        r = check(u)
        lost = set(cur['matched']) - set(r['matched']) if r['status'] == 'ok' else {1}
        tl = set(cur['tails_ok']) - set(r.get('tails_ok', []))
        gain = len(r.get('tails_ok', [])) - len(cur['tails_ok'])
        ok = r['status'] == 'ok' and not lost and not tl and gain > 0
        print(u, c, 'ACCEPT' if ok else 'reject', 'gain', gain, 'lost fn', len(lost), 'lost tails', len(tl), flush=True)
        if ok: acc.append(c); cur = r
    subprocess.run(['git', 'checkout', '--', src], cwd=FN)
    run(['tail_fix_v3.py', 'apply', str(u)], {'TF_ONLY': ','.join(acc)})
    print(u, 'accepted', acc, 'tails_ok', len(cur['tails_ok']), flush=True)
