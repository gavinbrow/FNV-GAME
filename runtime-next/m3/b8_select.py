"""Freeze reviewed Batch 8 storage definitions; never infer interval extents.

Run from any directory with python -I.  Source linkage/alias identity remains
in the evidence files.  New M3 names explicitly describe separate storage
definitions, and the sphere array is only a source-accessed prefix.
"""
import bisect
import hashlib
import json
from pathlib import Path
import sys
import argparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_m3 as G


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8-sig'))


def size(entry):
    return 4 if entry['tc'] == 'P' else G.TYPES[entry['tc']][1] if entry['tc'] in G.TYPES else entry['size']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', action='store_true', help='include reviewed command and string prefixes')
    args = parser.parse_args()
    base = read('batch7_selection.json')['entries']
    inputs = ['inventory/b8_other_names_accepted.json', 'inventory/b8_types_accepted.json',
              'inventory/b8_types_pointer_candidates.json', 'inventory/b8_zeros_accepted.json',
              'inventory/b8_sphere_prefix.json']
    added = []
    for row in read(inputs[0])['entries']:
        added.append(dict(row['selection'], evidence=inputs[0]))
    for row in read(inputs[1])['entries']:
        added.append(dict(va=row['va'], tc={1: 'E', 2: 'G', 4: 'I'}[row['size']], evidence=inputs[1]))
    for row in read(inputs[2])['entries']:
        added.append(dict(va=row['va'], tc='P', ptr=row['ptr'], evidence=inputs[2]))
    for entry in read(inputs[3])['selection_entries']:
        added.append(dict(entry, evidence=inputs[3]))
    sphere = read(inputs[4])
    added += [dict(entry, evidence=inputs[4]) for entry in sphere['entries']]
    if args.final:
        inputs += ['inventory/b8_command_prefix_selection.json', 'inventory/b8_string_prefixes.json']
        strings = read(inputs[-1])['selection_entries']
        replacements = {e['va'] for e in strings}
        added = [e for e in added if e['va'] not in replacements]
        added += [dict(e, evidence=inputs[-1]) for e in strings]
        added += [dict(e, evidence=inputs[-2]) for e in read(inputs[-2])['entries']]

    covered = [(e['va'], e['va'] + size(e)) for e in base]
    for name in ('inventory/b7_dv1_ranges.json', 'inventory/b7_produced.json'):
        covered += [(a, a + n) for a, n in read(name)]
    # Audited by BATCH8-verification.md: imports and IAT are post-overlay writes;
    # TLS is conservatively retained from the Batch 7 exclusions.
    rewritten = [(0xfdf000, 0xfdf000 + 1188), (0x118062c, 0x118062c + 6688), (0x110147c, 0x110147c + 24)]
    covered += rewritten
    sj = json.loads((Path(G.RN) / 'data-v3/symbolic.json').read_text())
    fields = sorted({G.SEC[r[0]]['va'] + r[1] for r in sj['fields']} | G.ORIG_SET)
    chunks = [(c['va'], c['va'] + c['size']) for c in json.loads((Path(G.RN) / 'data-v3/out/manifest.json').read_text())]
    claims = G.splice.RangeClaims()
    zeros = nonzeros = 0
    for e in sorted(added, key=lambda e: e['va']):
        a = e['va']; n = size(e); b = a + n; section = G.sec_of(a)
        assert section in ('.data', '.rdata')
        assert b <= G.SEC[section]['va'] + G.SEC[section]['raw']
        assert any(x <= a and b <= y for x, y in chunks), ('chunk boundary', hex(a))
        assert not any(x < b and a < y for x, y in covered), ('existing coverage', hex(a))
        claims.add(a, n)
        near = fields[bisect.bisect_left(fields, a - 3):bisect.bisect_left(fields, b)]
        if e['tc'] == 'P':
            assert near == [a] and a in G.ORIG_SET
            assert int.from_bytes(G.refbytes(a, 4), 'little') == e['ptr']
        elif e['tc'] == 'R':
            assert near == [x for x in G.ORIG_SITES if a <= x < b]
            assert all(a <= x and x + 4 <= b for x in near)
            G.build_entries([e])  # enforces the reviewed source record schema
        else:
            assert not near, ('scalar/array field overlap', hex(a))
        e.update(generated_name='M3_%08x' % a, batch=8, align=e.get('align', 4 if e['tc'] == 'R' else min(a & -a, n if n in (1, 2, 4, 8) else 8)))
        raw = G.refbytes(a, n)
        if not any(raw): e['file_backed'] = True
        zeros += raw.count(0); nonzeros += sum(bool(x) for x in raw)
    added.sort(key=lambda e: e['va'])
    result = dict(note='Batch 7 plus reviewed Batch 8 definitions; M3 storage names do not resolve native aliases. Array/record/string prefixes do not claim complete original object extents. Opaque command fields retain unresolved semantics.',
                  evidence_sha256={name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in inputs},
                  added=dict(entries=len(added), bytes=zeros + nonzeros, zeros=zeros, nonzeros=nonzeros),
                  entries=base + added)
    dest = HERE / ('batch8_final_selection.json' if args.final else 'batch8_selection.json')
    dest.write_text(json.dumps(result, indent=0) + '\n', encoding='utf-8')
    print(json.dumps(result['added']), hashlib.sha256(dest.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
