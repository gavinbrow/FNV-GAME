"""Read-only independent section/weak-symbol review of a finished kind cohort."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import struct
import sys

H = Path(__file__).resolve().parent
M = H.parent
F = M.parent.parent / 'fnv_decomp'
sys.path.insert(0, str(F / 'tools'))
from compare import Coff

OLD = '??_R0?AVNiMemObject@@@8'
NEW = '??_R0?AUNiMemObject@@@8'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def norm(name):
    return NEW if name == OLD else name


def records(c):
    """Keep section characteristics and complete relocation identity/addends."""
    out = Counter()
    grouped = defaultdict(list)
    for s in c.symbols.values():
        grouped[s['section']].append(s)
    for index, sec in enumerate(c.sections[1:], 1):
        if sec['name'].startswith('.debug'):
            continue
        names = tuple(sorted((norm(s['name']), s['value'], s['type'], s['storage'])
                             for s in grouped[index] if s['name'] != sec['name']))
        data = bytearray(sec['data'])
        for s in grouped[index]:
            if s['name'] in (OLD, NEW):
                start = s['value'] + 8
                before = b'.?AVNiMemObject@@\0' if s['name'] == OLD else b'.?AUNiMemObject@@\0'
                if data[start:start + len(before)] != before:
                    raise ValueError('NiMemObject descriptor bytes disagree with symbol')
                data[start:start + len(before)] = b'.?AUNiMemObject@@\0'
        rel = tuple(sorted((off, kind, norm(c.symbols[target]['name']),
                            c.symbols[target]['section'], c.symbols[target]['value'],
                            c.symbols[target]['type'], c.symbols[target]['storage'])
                           for off, target, kind in sec['relocs']))
        out[(index, sec['name'], sec['flags'], bytes(data), names, rel)] += 1
    return out


def aux(c):
    """Read selection/association and weak lookup; never compare raw indices."""
    _, _, _, start, count, _, _ = struct.unpack_from('<HHIIIHH', c.data)
    rows = []
    identities = defaultdict(list)
    for s in c.symbols.values():
        if s['section'] > 0 and s['name'] != c.sections[s['section']]['name']:
            identities[s['section']].append((norm(s['name']), s['value'], s['type'], s['storage']))
    identities = {k: tuple(sorted(v)) for k, v in identities.items()}
    index = 0
    while index < count:
        s = c.symbols[index]
        at = start + index * 18
        n = c.data[at + 17]
        if n and s['storage'] == 3 and s['section'] > 0 and s['value'] == 0:
            length, reloc, lines, checksum, assoc, selection = struct.unpack_from('<IHHIhB', c.data, at + 18)
            if s['name'] == c.sections[s['section']]['name'] and not s['name'].startswith('.debug'):
                # Checksums vary with the intentionally changed type-name byte.
                partner = None
                if selection == 5:
                    if not 0 < assoc < len(c.sections):
                        raise ValueError('invalid associative COMDAT target')
                    partner = (assoc, identities.get(assoc, ()))
                rows.append(('section', s['section'], s['name'], identities.get(s['section'], ()), length, reloc, lines, selection, partner))
        elif n and s['storage'] == 105:
            target, mode = struct.unpack_from('<II', c.data, at + 18)
            t = c.symbols[target]
            rows.append(('weak', norm(s['name']), norm(t['name']), t['section'], t['value'], t['type'], t['storage'], mode))
        index += 1 + n
    return Counter(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    run, output = a.run.resolve(), a.out.resolve()
    if not run.is_relative_to((M / 'out').resolve()) or not output.is_relative_to((M / 'out').resolve()):
        raise ValueError('private paths required')
    if output.exists():
        raise FileExistsError(output)
    p = run / 'progress.json'
    raw = p.read_bytes()
    progress = json.loads(raw)
    if progress['status'] not in ('complete-review-required', 'function-and-eh-pass-metadata-review-required') or len(progress['units']) != progress['total_units']:
        raise ValueError('finished complete cohort required')
    if progress['total_units'] != 750 or len({x['unit'] for x in progress['units']}) != 750 or any(x['status'] not in ('pass', 'review-required') for x in progress['units']):
        raise ValueError('invalid or failed cohort scope')
    if sha(F / 'build/units.json') != progress['recipe_sha256']:
        raise ValueError('live recipe changed')
    watched = {F / 'build/units.json': progress['recipe_sha256']}
    for name, digest in progress['tools_sha256'].items():
        watched[H / name] = digest
    watched[M / 'out/phase2-nimemobject-coherent-kind-consumers.json'] = progress['scope_sha256']
    watched[M / 'out/phase2-nimemobject-coherent-kind/manifest.json'] = progress['kind_manifest_sha256']
    for path, digest in watched.items():
        if sha(path) != digest:
            raise ValueError('cohort dependency changed: ' + str(path))
    scope = json.loads((M / 'out/phase2-nimemobject-coherent-kind-consumers.json').read_bytes())
    if (scope['recipe_sha256'] != progress['recipe_sha256'] or scope['affected_units'] != 750
            or scope['fixture_manifest_sha256'] != progress['kind_manifest_sha256']
            or len(scope['units']) != 750
            or {x['unit'] for x in scope['units']} != {x['unit'] for x in progress['units']}):
        raise ValueError('progress unit set differs from pinned cohort')
    rows = []
    for row in progress['units']:
        i = row['unit']
        d = run / ('unit-%04d' % i)
        cp = d / 'comparison.json'
        if not cp.exists() or sha(cp) != row.get('comparison_sha256'):
            raise ValueError('comparison identity missing or changed: %d' % i)
        comparison = json.loads(cp.read_bytes())
        if comparison['unit'] != i or comparison['recipe_sha256'] != progress['recipe_sha256']:
            raise ValueError('comparison scope changed')
        watched[cp] = row['comparison_sha256']
        cr = d / 'compile-result.json'
        if sha(cr) != comparison['compile_result_sha256']:
            raise ValueError('compile identity changed: %d' % i)
        compile_result = json.loads(cr.read_bytes())
        watched[cr] = comparison['compile_result_sha256']
        mm = d / 'mirror-manifest.json'
        if sha(mm) != comparison['mirror_manifest_sha256'] or compile_result['mirror_manifest_sha256'] != comparison['mirror_manifest_sha256'] or compile_result['unit_index'] != i:
            raise ValueError('mirror scope changed')
        watched[mm] = comparison['mirror_manifest_sha256']
        mirror = json.loads(mm.read_bytes())
        for tag in ('original', 'candidate'):
            for name, digest in mirror[tag]['files'].items():
                watched[d / tag / name] = digest
        if len(compile_result['outcomes']) != 2 or {x['tag'] for x in compile_result['outcomes']} != {'original', 'candidate'}:
            raise ValueError('original/candidate pair required')
        objs = {}
        for x in compile_result['outcomes']:
            path = d / (x['tag'] + '.obj')
            if x['rc'] or not x['trace_valid'] or sha(path) != x['object_sha256']:
                raise ValueError('unverified object: %d' % i)
            watched[path] = x['object_sha256']
            watched[d / (x['tag'] + '.log')] = x['show_includes_log_sha256']
            objs[x['tag']] = Coff(str(path))
        left, right = (records(objs[t]) for t in ('original', 'candidate'))
        al, ar = (aux(objs[t]) for t in ('original', 'candidate'))
        rows.append({'unit': i, 'comparison_sha256': sha(cp),
                     'normalized_nondebug_sections_equal': left == right,
                     'original_only_sections': sum((left - right).values()),
                     'candidate_only_sections': sum((right - left).values()),
                     'comdat_selection_and_weak_lookup_equal': al == ar,
                     'normalized_section_count': sum(left.values())})
    if p.read_bytes() != raw:
        raise ValueError('cohort changed during review')
    for path, digest in watched.items():
        if sha(path) != digest:
            raise ValueError('review input changed: ' + str(path))
    result = {'scope': 'Independent original/candidate nondebug section and COFF auxiliary comparison',
              'progress_sha256': hashlib.sha256(raw).hexdigest(),
              'units': rows, 'unit_count': len(rows),
              'nondebug_section_mismatches': sum(not x['normalized_nondebug_sections_equal'] for x in rows),
              'auxiliary_mismatches': sum(not x['comdat_selection_and_weak_lookup_equal'] for x in rows),
              'watched_file_count': len(watched),
              'reference_eh_acceptance': False,
              'normalization': {'symbol': [OLD, NEW], 'type_name': ['.?AVNiMemObject@@', '.?AUNiMemObject@@']},
              'limits': ['Only the exact NiMemObject class-key type descriptor name and bytes are normalized.',
                         'Debug sections and section checksums are excluded; section indices are deliberately retained.',
                         'This preserves emitted selection modes; final provider/placement ownership is separate.',
                         'Ordinary function/EH reference checks and source identity remain separate gates.']}
    output.write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps({k: result[k] for k in ('unit_count', 'nondebug_section_mismatches', 'auxiliary_mismatches')}))


if __name__ == '__main__':
    main()
