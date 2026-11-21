"""Inspect already compiled named class metadata; no build or source mutation.

The result is conformance triage, not native-class acceptance. Objects are the
existing pinned pool, whose provenance/currentness must be checked before use.
"""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M3 = HERE.parent
PROJECT = M3.parent.parent
sys.path.insert(0, str(HERE))
from class_metadata_compare import compare_class, unique_global_maps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=M3 / 'out/phase2-class-census/existing-named.json')
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError('refusing to overwrite previous triage')
    units_path = PROJECT / 'fnv_decomp/build/units.json'
    units = json.loads(units_path.read_bytes())['units']
    census_path = M3 / 'out/phase2-class-census/census-v2.json'
    census = json.loads(census_path.read_bytes())
    units_sha = hashlib.sha256(units_path.read_bytes()).hexdigest()
    if census['inputs']['units_sha256'] != units_sha:
        raise ValueError('census recipe is stale')
    candidates = set()
    for table in census['vtables']:
        name = table['locator']['type_name']
        match = re.fullmatch(r'\.\?A[VU]([A-Za-z_]\w*)@@', name)
        if not match:
            continue
        expected = '??_7' + match.group(1) + '@@6B@'
        for symbol in table['unit_symbols']:
            if symbol['symbol'] == expected:
                candidates.add((symbol['unit'], name))
    ordered = sorted(candidates)
    if args.limit is not None:
        if args.limit <= 0:
            raise ValueError('limit must be positive')
        ordered = ordered[:args.limit]
    maps = unique_global_maps(units)
    results = []
    for index, (unit_index, name) in enumerate(ordered):
        object_path = PROJECT / ('runtime-next/pinned-build/obj_v3/%04d.obj' % unit_index)
        try:
            report = compare_class(object_path, units[unit_index], units, census, name, maps)
        except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
            report = dict(type_name=name, error=type(exc).__name__ + ': ' + str(exc))
        report['unit_index'] = unit_index
        report['source'] = units[unit_index]['source']
        results.append(report)
        if (index + 1) % 25 == 0:
            print(json.dumps(dict(inspected=index + 1, total=len(ordered))), flush=True)
    complete = [r for r in results if r.get('emitted_tables') == r.get('reference_tables')
                and r.get('emitted_tables', 0) > 0 and all(
                    t['status'] == 'emitted record fields and slot prefix match' for t in r['tables'])]
    stats = dict(candidate_unit_class_pairs=len(candidates), inspected=len(results),
                 analysis_errors=sum('error' in r for r in results),
                 complete_emitted_fields_and_slot_prefixes=len(complete),
                 full_native_classes_accepted=0)
    result = dict(schema_version=1,
                  scope='Existing named simple-class object record/slot-prefix triage. Not a full native ABI, source-header, current-object, placement or gameplay gate.',
                  inputs=dict(units_sha256=units_sha, census_sha256=hashlib.sha256(census_path.read_bytes()).hexdigest()),
                  stats=stats, conforming_candidates=[dict(unit_index=r['unit_index'], type_name=r['type_name'], source=r['source']) for r in complete],
                  results=results)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(stats), flush=True)


if __name__ == '__main__':
    main()
