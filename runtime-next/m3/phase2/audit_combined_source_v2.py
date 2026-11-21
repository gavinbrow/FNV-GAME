"""Independent read-only ordinary oracle replay for the seven-unit source batch."""
import hashlib
import json
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
M = H.parent
R = M.parent.parent
F = R / 'fnv_decomp'
V = M / 'out/phase2-source-integration6757-v2'
L = M / 'out/phase2-source-integration6757-lane'
sys.path[:0] = [str(H), str(R / 'runtime-next'), str(F / 'tools')]
from compare import Coff, Pe, compare
from build_and_match import eh_sections, eh_tails, recipe_names
import paths

IDS = (253, 370, 425, 620, 621, 2909, 2910)
BASE = '6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
NEW = '825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
PIN = 'e2b8c9590ef174448f1898c3168b37846ade5af85a74ba5cef03731cc9b237d9'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    output = V / 'root-ordinary-review.json'
    if output.exists():
        raise FileExistsError(output)
    if sha(F / 'build/units.json') != BASE or sha(V / 'manifest.json') != PIN or sha(V / 'units.generated') != NEW:
        raise ValueError('source or proposal identity changed')
    m = json.loads((V / 'manifest.json').read_bytes())
    units = json.loads((V / 'units.generated').read_bytes())['units']
    pe = Pe(paths.REF_IMAGE)
    if sha(Path(paths.REF_IMAGE)) != 'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':
        raise ValueError('reference changed')
    rows, details, watched = {}, [], {}
    names = recipe_names(units)
    for i in IDS:
        d = L / str(i)
        cr = d / 'compile-result.json'
        run = json.loads(cr.read_bytes())
        mm = d / 'mirror-manifest.json'
        if run['mirror_manifest_sha256'] != sha(mm):
            raise ValueError('mirror identity changed')
        if len(run['outcomes']) != 2 or {x['tag'] for x in run['outcomes']} != {'original', 'candidate'}:
            raise ValueError('missing compiled pair')
        record = next(x for x in run['outcomes'] if x['tag'] == 'candidate')
        p = d / 'candidate.obj'
        if record['rc'] or not record['trace_valid'] or sha(p) != record['object_sha256'] or sha(p) != m['function_and_eh_replay'][str(i)]['object_sha256']:
            raise ValueError('candidate compiler/trace/object changed')
        watched.update({cr: sha(cr), mm: sha(mm), p: sha(p)})
        c = Coff(str(p))
        r = compare(c, pe, units[i])
        if len(r) != len(units[i]['functions']) or any(x['verdict'] != 'match' for x in r):
            raise ValueError('strict functions failed: %d' % i)
        sec, inferred, errors = eh_sections(c, pe, units[i], r, names)
        if errors or any(not x[2] for x in sec):
            raise ValueError('ordinary EH failed: %d' % i)
        detail = {'eh_sections': sec, 'eh_inferred': inferred, 'errors': errors}
        details.append(detail)
        rows[str(i)] = {'functions': len(r), 'ordinary_eh_sections': len(sec), 'ordinary_eh': detail,
                        'object_sha256': sha(p), 'compile_result_sha256': sha(cr)}
    tails, bad, inferred, _, conflicts = eh_tails([units[i] for i in IDS], details, pe)
    if bad or conflicts:
        raise ValueError('recipe EH tail union failed')
    for p, digest in watched.items():
        if sha(p) != digest:
            raise ValueError('input changed while auditing')
    result = {'status': 'strict functions, all located ordinary EH and requested tail union pass',
              'base_recipe_sha256': BASE, 'candidate_recipe_sha256': NEW, 'proposal_sha256': PIN,
              'units': rows, 'function_count': sum(x['functions'] for x in rows.values()),
              'ordinary_eh_sections': sum(x['ordinary_eh_sections'] for x in rows.values()),
              'recipe_eh_tails': len(tails), 'bad_tails': bad, 'tail_conflicts': conflicts,
              'limits': ['No live source change, final-image or gameplay verification.',
                         'Weak PSA E binding remains excluded; final metadata/provider ownership is separate.']}
    output.write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps({k: result[k] for k in ('function_count', 'ordinary_eh_sections', 'recipe_eh_tails')}))


if __name__ == '__main__':
    main()
