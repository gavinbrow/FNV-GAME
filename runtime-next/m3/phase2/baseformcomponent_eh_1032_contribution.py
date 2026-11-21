"""Check unit 1033's independently anchored contribution to a BFC EH extent."""
import copy, hashlib, json, struct, sys
from pathlib import Path
H = Path(__file__).resolve().parent
M = H.parent
RN = M.parent
P = RN.parent
O = M / 'out'
sys.path[:0] = [str(P / 'fnv_decomp/tools'), str(RN)]
from compare import Coff, Pe, compare
from build_and_match import eh_sections, eh_tails, recipe_names
import paths

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    dest = O / 'phase2-bfc-eh-unit1032-contribution.json'
    if dest.exists():
        raise FileExistsError('preserve historical evidence')
    index_path = O / 'phase2-bfc-core-proof-index.json'
    index = json.loads(index_path.read_bytes())
    recipe = O / 'phase2-flags-script-production-before/units.json'
    assert sha(recipe) == index['recipe_sha256']
    units = json.loads(recipe.read_bytes())['units']
    z = next(x for x in index['units'] if x['unit'] == 1032)
    report_path = M / z['report']
    assert sha(report_path) == z['report_sha256']
    report = json.loads(report_path.read_bytes())
    pe = Pe(paths.REF_IMAGE)
    names = recipe_names(units)
    external = RN / 'pinned-build/obj_v3.bak-20261116/1033.obj'
    assert sha(external) == '2d37ac1db50aa3bdb5e3b3e18728fd0f85432ec6b1b75696b3afe7f4226527a5'
    c = Coff(str(external))
    rows = compare(c, pe, units[1033])
    assert len(rows) == 9 and all(x['verdict'] == 'match' for x in rows)
    sections, inferred, errors = eh_sections(c, pe, units[1033], rows, names)
    assert not errors and not inferred
    points = [x for x in sections if x[0] < 0xef3d41 and 0xef3d10 < x[1]]
    assert [(x[0], x[1]) for x in points] == [(0xef3d10, 0xef3d1b), (0xef3d1b, 0xef3d26), (0xef3d26, 0xef3d41)]
    assert all(x[2] and x[3] == '0x0050c000' for x in points)
    assert pe.read(0x0050c006, 4) == struct.pack('<I', 0xef3d26)
    info = struct.unpack('<10I', pe.read(0x1146580, 40))
    assert info[0] == 0x19930522 and info[1] == 2 and info[2] == 0x1146570
    actions = [struct.unpack('<II', pe.read(info[2] + 8*i, 8))[1] for i in range(2)]
    assert actions == [0xef3d10, 0xef3d1b]
    result = []
    for tag, path, digest, changes in [
        ('production', O / 'phase2-bfc-cohort-production-archive/1032.obj', z['production_object_sha256'], []),
        ('original_mirror', report_path.parent / 'original.obj', z['objects']['original'], report['production_to_mirror_literals']),
        ('candidate', report_path.parent / 'candidate.obj', z['objects']['candidate'], report['production_to_mirror_literals'] + report['mirror_to_candidate_literals']),
    ]:
        assert sha(path) == digest
        spec = copy.deepcopy(units[1032])
        for change in changes:
            if 'bound_va' in change:
                spec['symbols'][change['after']] = change['bound_va']
        obj = Coff(str(path))
        rows = compare(obj, pe, spec)
        assert all(x['verdict'] == 'match' for x in rows)
        sec, inf, err = eh_sections(obj, pe, spec, rows, names)
        assert not err
        done = [{'eh_sections': sec, 'eh_inferred': {k: '0x%08x' % v for k, v in inf.items()}}, {'eh_sections': sections, 'eh_inferred': {}}]
        tails, bad, guesses, _, conflicts = eh_tails([units[1032]], done, pe)
        assert len(tails) == 1 and not bad and not conflicts
        result.append({'tag': tag, 'object_sha256': digest, 'strict_functions': len(rows), 'ordinary_tails_passed': len(tails), 'inferred_tails': len(guesses)})
    source = P / 'fnv_decomp' / units[1033]['source']
    out = {'scope': 'outside-cohort unit 1033 source-owned EH contribution; ordinary oracle unchanged',
           'cohort_index_sha256': sha(index_path), 'recipe_sha256': sha(recipe),
           'outside_unit': 1033, 'outside_object': str(external), 'outside_object_sha256': sha(external),
           'outside_source': units[1033]['source'], 'outside_source_sha256': sha(source),
           'outside_strict_functions': 9, 'outside_parent': '0x0050c000',
           'handler': '0x00ef3d26', 'funcinfo': '0x01146580', 'unwind_map': '0x01146570',
           'actions': ['0x%08x' % x for x in actions], 'contribution': ['0x00ef3d10', '0x00ef3d41'],
           'results': result, 'limitations': ['historical Nov 16 outside-cohort object; fresh production capture and final placement remain']}
    dest.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'status': 'PASS ordinary 1032 extent with independently verified 1033 owner', 'results': result}))

if __name__ == '__main__':
    main()
