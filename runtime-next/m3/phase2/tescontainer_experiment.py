"""Hash-pinned native TESContainer header/override experiment, private outputs only.

prepare changes no protected input. compile requires the exclusive compiler lane.
compare checks all original mapped functions and graph/slot metadata independently.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M3 = HERE.parent
RN = M3.parent
PROJECT = RN.parent
FN = PROJECT / 'fnv_decomp'
SOURCE = 'src/fallout_shared/tescontainer.cpp'
SOURCE_SHA = '8deede13d9a7e9e7263aebcd8dfa8ac55e6d2a3f402e2ff6a4d014807d0fd955'
UNITS_SHA = 'ae4182c8062cf566210935d284b6663a83ab63e077b41d8e147fa66cb7aca70e'
OLD = '?FUN_00481d10@FUN_00481d10_shell@@QAE_NPAVBaseFormComponent@@@Z'
NEW = '?CompareWithBase@TESContainer@@UAE_NPAVBaseFormComponent@@@Z'
OUT = M3 / 'out/phase2-tescontainer-v1'
sys.path[:0] = [str(HERE), str(FN / 'tools'), str(RN / 'pinned-build')]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transform(source):
    pattern = re.compile(r'^class TESContainer : public BaseFormComponent\n\{.*?^\};', re.M | re.S)
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise ValueError('expected one native class declaration')
    block = matches[0].group()
    anchor = '    virtual void CopyFromBase(BaseFormComponent* component);'
    if block.count(anchor) != 1 or 'CompareWithBase' in block:
        raise ValueError('original class interface changed')
    header_block = block.replace(anchor, anchor + '\n    virtual bool CompareWithBase(BaseFormComponent* other);')
    shell = re.compile(r'^struct FUN_00481d10_shell : TESContainer\n\{\n    bool FUN_00481d10\(BaseFormComponent\* other\);\n\};\n', re.M)
    if len(shell.findall(source)) != 1:
        raise ValueError('expected one comparison shell')
    source = source[:matches[0].start()] + '#include "TESContainer.h"' + source[matches[0].end():]
    source = shell.sub('', source, count=1)
    old = 'bool FUN_00481d10_shell::FUN_00481d10(BaseFormComponent* other)'
    if source.count(old) != 1 or 'TESContainer::CompareWithBase' in source:
        raise ValueError('comparison definition changed')
    source = source.replace(old, 'bool TESContainer::CompareWithBase(BaseFormComponent* other)', 1)
    if 'FUN_00481d10_shell' in source:
        raise ValueError('unhandled shell reference')
    header = ('#ifndef FNV_PHASE2_TESCONTAINER_H\n#define FNV_PHASE2_TESCONTAINER_H\n'
              '#include "BaseFormComponent.h"\nclass InventoryStackRecord;\nclass InventoryItemEntry;\n'
              '#pragma pack(push, 4)\n' + header_block + '\n#pragma pack(pop)\n'
              'FNV_STATIC_ASSERT(sizeof(TESContainer) == 0xC);\n#endif\n')
    return source, header


def closure(path):
    todo = [path]
    seen = {}
    while todo:
        current = todo.pop().resolve()
        if current in seen:
            continue
        if not current.is_relative_to(FN.resolve()):
            raise ValueError('source include escapes protected tree')
        seen[current] = digest(current)
        for name in re.findall(rb'^\s*#\s*include\s*"([^"\r\n]+)"', current.read_bytes(), re.M):
            include = name.decode('ascii')
            found = next((p for p in (current.parent / include, FN / 'include' / include) if p.is_file()), None)
            if found is None:
                raise ValueError('unresolved quoted include')
            todo.append(found)
    return [dict(path=p.relative_to(FN.resolve()).as_posix(), sha256=sha) for p, sha in sorted(seen.items())]


def prepare():
    source_path = FN / SOURCE
    units_path = FN / 'build/units.json'
    if digest(source_path) != SOURCE_SHA or digest(units_path) != UNITS_SHA:
        raise ValueError('source or unit recipe has changed')
    units = json.loads(units_path.read_bytes())['units']
    unit = units[980]
    if unit['source'] != SOURCE or unit['compiler'] != 'sp1' or len(unit['functions']) != 31:
        raise ValueError('unexpected unit recipe')
    # Existing native spelling collisions remain in other source views; this
    # isolated result is not an ODR-equivalence claim about those declarations.
    source, header = transform(source_path.read_text(encoding='utf-8'))
    original = [f for f in unit['functions'] if f['symbol'] == OLD]
    if len(original) != 1 or original[0]['address'] != '0x00481d10':
        raise ValueError('source-backed comparison mapping changed')
    mapped = copy.deepcopy(unit)
    for f in mapped['functions']:
        if f['symbol'] == OLD:
            f['symbol'] = NEW
    if OLD in mapped['symbols']:
        mapped['symbols'][NEW] = mapped['symbols'].pop(OLD)
    OUT.mkdir(parents=False, exist_ok=False)
    for name, text in [('tescontainer.cpp', source), ('TESContainer.h', header)]:
        with (OUT / name).open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(text)
    with (OUT / 'unit-overlay.json').open('x', encoding='utf-8') as stream:
        json.dump(mapped, stream, indent=2)
    manifest = dict(unit_index=980, source=SOURCE, source_sha256=SOURCE_SHA, units_sha256=UNITS_SHA,
                    source_overlay_sha256=digest(OUT / 'tescontainer.cpp'), header_sha256=digest(OUT / 'TESContainer.h'),
                    unit_overlay_sha256=digest(OUT / 'unit-overlay.json'), original_include_closure=closure(source_path),
                    function_remap={OLD: NEW}, status='private uncompiled experiment; source/header ownership and other TU definitions remain unresolved')
    with (OUT / 'manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2)
    print(json.dumps(dict(unit_index=980, source_overlay_sha256=manifest['source_overlay_sha256'],
                          header_sha256=manifest['header_sha256'])))


def check_inputs():
    meta = json.loads((OUT / 'manifest.json').read_bytes())
    paths = [(FN / SOURCE, SOURCE_SHA), (FN / 'build/units.json', UNITS_SHA),
             (OUT / 'tescontainer.cpp', meta['source_overlay_sha256']),
             (OUT / 'TESContainer.h', meta['header_sha256']),
             (OUT / 'unit-overlay.json', meta['unit_overlay_sha256'])]
    paths += [(FN / item['path'], item['sha256']) for item in meta['original_include_closure']]
    if any(digest(p) != expected for p, expected in paths):
        raise ValueError('experiment input digest mismatch')
    source, header = transform((FN / SOURCE).read_text(encoding='utf-8'))
    if (OUT / 'tescontainer.cpp').read_text(encoding='utf-8') != source or (OUT / 'TESContainer.h').read_text(encoding='utf-8') != header:
        raise ValueError('private source differs from deterministic transform')
    return meta


def compile_experiment():
    check_inputs()
    import compile_units_v3 as compiler
    unit = json.loads((OUT / 'unit-overlay.json').read_bytes())
    toolchain = compiler.find_toolchains()['sp1']
    if not toolchain.get('ok'):
        raise ValueError('exact SP1 compiler unavailable')
    temporary = OUT / 'compiler-tmp'
    temporary.mkdir(exist_ok=False)
    env = compiler.make_env(Path(toolchain['vc']), Path(toolchain['sdk']) if toolchain['sdk'] != 'None' else None)
    env['TMP'] = env['TEMP'] = str(temporary)
    rows = []
    for label, source in [('original', FN / SOURCE), ('overlay', OUT / 'tescontainer.cpp')]:
        obj = OUT / ('0980.%s.obj' % label)
        log = OUT / ('0980.%s.log' % label)
        if obj.exists() or log.exists():
            raise FileExistsError('refusing to overwrite experiment')
        cmd = [str(Path(toolchain['vc']) / 'bin/cl.exe'), '/c', '/nologo'] + unit['flags']
        if label == 'overlay':
            cmd += ['/I' + str((FN / SOURCE).parent)]
        cmd += ['/I' + str(FN / 'include'), str(source), '/Fo' + str(obj)]
        result = subprocess.run(cmd, cwd=OUT, env=env, capture_output=True, text=True,
                                errors='replace', stdin=subprocess.DEVNULL, timeout=900)
        with log.open('x', encoding='utf-8') as stream:
            stream.write(result.stdout + '\n' + result.stderr)
        rows.append(dict(source=label, rc=result.returncode,
                         object_sha256=digest(obj) if obj.is_file() else None))
        if result.returncode:
            break
    with (OUT / 'compile-result.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(compiler_version=toolchain['version'], outcomes=rows,
                       manifest_sha256=digest(OUT / 'manifest.json'),
                       census_sha256=digest(M3 / 'out/phase2-class-census/census-v2.json')), stream, indent=2)
    print(json.dumps(rows))
    if len(rows) != 2 or any(row['rc'] or row['object_sha256'] is None for row in rows):
        raise SystemExit(1)


def repair_literals():
    """Remap compiler labels by paired code relocations and exact object bytes."""
    check_inputs()
    from compare import Coff
    from rtti_hkp_viewer_compare import relocated
    units = json.loads((FN / 'build/units.json').read_bytes())['units']
    original = units[980]
    mapped = json.loads((OUT / 'unit-overlay.json').read_bytes())
    compiled = json.loads((OUT / 'compile-result.json').read_bytes())
    coffs = {}
    for row in compiled['outcomes']:
        path = OUT / ('0980.%s.obj' % row['source'])
        if row['rc'] or digest(path) != row['object_sha256']:
            raise ValueError('compiled object changed')
        coffs[row['source']] = Coff(path)
    mappings = {}
    facts = []
    for before, after in zip(original['functions'], mapped['functions']):
        raw_a, rel_a = relocated(coffs['original'], before['symbol'], before['size'], {})
        raw_b, rel_b = relocated(coffs['overlay'], after['symbol'], after['size'], {NEW: OLD})
        if raw_a != raw_b or len(rel_a) != len(rel_b):
            raise ValueError('literal repair cannot change code or relocation count')
        for a, b in zip(rel_a, rel_b):
            if a == b:
                continue
            if (a[0], a[1], a[3]) != (b[0], b[1], b[3]) or not all(re.fullmatch(r'\$SG\d+', row[2]) for row in (a, b)):
                raise ValueError('difference is not a compiler string-label rename')
            old_name, new_name = a[2], b[2]
            sections = []
            for tag, name in [('original', old_name), ('overlay', new_name)]:
                s = coffs[tag].named(name)
                sec = coffs[tag].sections[s['section']]
                if sec['name'] != '.rdata' or sec['relocs']:
                    raise ValueError('literal requires a nonrelocated rdata pool')
                sections.append((s['value'], sec['data']))
            if not sections[0][1] or sections[0] != sections[1] or old_name not in original['symbols']:
                raise ValueError('literal object values or source binding differ')
            if new_name in mappings and mappings[new_name] != old_name:
                raise ValueError('ambiguous compiler-label rename')
            mappings[new_name] = old_name
            facts.append(dict(function_address=before['address'], relocation_offset=a[0], old_name=old_name,
                              new_name=new_name, source_mapped_va=original['symbols'][old_name],
                              object_symbol_offset=sections[0][0], object_pool_bytes=len(sections[0][1]),
                              object_pool_sha256=hashlib.sha256(sections[0][1]).hexdigest()))
    if len(mappings) != 4 or len(facts) != 4:
        raise ValueError('expected exactly four compiler string-label changes')
    old_to_new = {old: new for new, old in mappings.items()}
    updated = {}
    for name, addr in mapped['symbols'].items():
        renamed = old_to_new.get(name, name)
        if renamed in updated and updated[renamed] != addr:
            raise ValueError('new label conflicts with another source mapping')
        updated[renamed] = addr
    mapped['symbols'] = updated
    with (OUT / 'unit-overlay-v2.json').open('x', encoding='utf-8') as stream:
        json.dump(mapped, stream, indent=2)
    with (OUT / 'literal-remap.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(unit_overlay_sha256=digest(OUT / 'unit-overlay-v2.json'), normalization=mappings, facts=facts,
                       scope='paired relocation positions and identical complete nonrelocated pool sections/symbol offsets; no new reference-derived address alias'), stream, indent=2)
    print(json.dumps(dict(remapped_literals=len(mappings))))


def compare_experiment(repaired=False):
    check_inputs()
    from compare import Coff, Pe, compare
    from rtti_hkp_viewer_compare import relocated
    from class_metadata_compare import compare_class
    units = json.loads((FN / 'build/units.json').read_bytes())['units']
    mapped_path = OUT / ('unit-overlay-v2.json' if repaired else 'unit-overlay.json')
    mapped = json.loads(mapped_path.read_bytes())
    normalization = {NEW: OLD}
    if repaired:
        labels = json.loads((OUT / 'literal-remap.json').read_bytes())
        if labels['unit_overlay_sha256'] != digest(mapped_path):
            raise ValueError('repaired literal recipe changed')
        normalization.update(labels['normalization'])
    result = json.loads((OUT / 'compile-result.json').read_bytes())
    if result['manifest_sha256'] != digest(OUT / 'manifest.json') or result['census_sha256'] != digest(M3 / 'out/phase2-class-census/census-v2.json'):
        raise ValueError('manifest or census differs from compile-time inputs')
    coffs = {}
    for row in result['outcomes']:
        path = OUT / ('0980.%s.obj' % row['source'])
        if row['rc'] or digest(path) != row['object_sha256']:
            raise ValueError('compiled object does not match result')
        coffs[row['source']] = Coff(path)
    if set(coffs) != {'original', 'overlay'}:
        raise ValueError('both compiler outcomes required')
    original = units[980]
    if len(original['functions']) != 31 or len(mapped['functions']) != 31:
        raise ValueError('exact 31-function scope required')
    comparisons = []
    for before, after in zip(original['functions'], mapped['functions']):
        a, ar = relocated(coffs['original'], before['symbol'], before['size'], {})
        b, br = relocated(coffs['overlay'], after['symbol'], after['size'], normalization)
        comparisons.append(dict(address=before['address'], code_bytes_equal=a == b, normalized_relocations_equal=ar == br))
    import paths
    reports = {}
    for label, unit in [('original', original), ('overlay', mapped)]:
        reports[label] = [dict(address=row['address'], verdict=row['verdict'],
                               errors=row['errors'], failed_relocations=sum(not x.get('match') for x in row['relocations']))
                          for row in compare(coffs[label], Pe(paths.REF_IMAGE), unit)]
    census = json.loads((M3 / 'out/phase2-class-census/census-v2.json').read_bytes())
    metadata = compare_class(OUT / '0980.overlay.obj', mapped, units, census, '.?AVTESContainer@@')
    data = dict(functions=comparisons, reference_comparator=reports, metadata=metadata,
                unit_overlay_sha256=digest(mapped_path),
                scope='isolated exact function and emitted metadata check; not global ODR, placement, or gameplay acceptance')
    passed = (len(comparisons) == 31 and all(r['code_bytes_equal'] and r['normalized_relocations_equal'] for r in comparisons)
              and all(len(rows) == 31 and all(r['verdict'] == 'match' for r in rows) for rows in reports.values())
              and metadata['emitted_tables'] == metadata['reference_tables'] == len(metadata['tables']) == 1
              and metadata['tables'][0].get('reference_vtable_va') == 0x0101c130
              and metadata['tables'][0].get('emitted_slot_count') == 4
              and metadata['tables'][0]['status'] == 'emitted record fields and slot prefix match')
    data['isolated_checks_passed'] = passed
    with (OUT / ('comparison-v2.json' if repaired else 'comparison.json')).open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2)
    print(json.dumps(dict(functions=len(comparisons), bytes_equal=sum(r['code_bytes_equal'] for r in comparisons),
                          normalized_relocations_equal=sum(r['normalized_relocations_equal'] for r in comparisons),
                          reference_matches={k: sum(x['verdict'] == 'match' for x in rows) for k, rows in reports.items()},
                          metadata_statuses=[t['status'] for t in metadata['tables']])))
    if not passed:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'compile', 'compare', 'repair-labels', 'compare-labels'])
    action = parser.parse_args().action
    {'prepare': prepare, 'compile': compile_experiment, 'compare': compare_experiment,
     'repair-labels': repair_literals, 'compare-labels': lambda: compare_experiment(True)}[action]()


if __name__ == '__main__':
    main()
