"""Private lexical inventory of assignments referring to observed vtable VAs.

This identifies manual-vptr-write leads for the Phase 2 constructor gate; a
matched assignment/inline-assembly line is not itself proof of an object write.
"""
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
M3 = HERE.parent
PROJECT = M3.parent.parent
TOKEN = re.compile(r'(?<![A-Za-z_0-9])(?:DAT_|PTR_|0x)([0-9a-fA-F]{8})(?![A-Za-z_0-9])')
ANNOTATION = re.compile(r'//\s*@fnv\s+(0x[0-9a-fA-F]{8})')
SCRUB = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)


def masked(source):
    return SCRUB.sub(lambda m: ''.join('\n' if c == '\n' else ' ' for c in m.group()), source)


def annotated_bodies(source, clean):
    annotations = list(ANNOTATION.finditer(source))
    result = []
    for index, annotation in enumerate(annotations):
        limit = annotations[index + 1].start() if index + 1 < len(annotations) else len(source)
        start = clean.find('{', annotation.end(), limit)
        if start < 0:
            continue
        # A declaration before the opening brace makes function attribution
        # ambiguous; keep the assignment lead unassociated in that case.
        if ';' in clean[annotation.end():start]:
            continue
        depth = 1
        end = start + 1
        while end < limit and depth:
            depth += (clean[end] == '{') - (clean[end] == '}')
            end += 1
        if depth == 0:
            result.append((start, end, annotation.group(1).lower()))
    return result


def scan_source(source, addresses):
    clean = masked(source)
    functions = annotated_bodies(source, clean)
    result = []
    for match in TOKEN.finditer(clean):
        address = int(match.group(1), 16)
        if address not in addresses:
            continue
        # Bound a lead by the previous statement/body delimiter; this does not
        # resolve the type of the assignment's destination expression.
        begin = max(clean.rfind(';', 0, match.start()), clean.rfind('{', 0, match.start()),
                    clean.rfind('}', 0, match.start()), match.start() - 400) + 1
        prefix = clean[begin:match.start()]
        if re.search(r'(?<![=!<>])=(?!=)[^;]*$', prefix):
            kind = 'assignment_referring_to_vtable'
        else:
            line_start = clean.rfind('\n', 0, match.start()) + 1
            if not re.search(r'\b(?:mov|lea)\b', clean[line_start:match.start()], re.I):
                continue
            kind = 'inline_assembly_reference_to_vtable'
        containing = [addr for start, end, addr in functions if start < match.start() < end]
        result.append(dict(line=source.count('\n', 0, match.start()) + 1,
                           vtable_va=address, syntax=kind,
                           annotated_function_address=containing[0] if len(containing) == 1 else None,
                           destination_is_object_vptr_proven=False))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--census', type=Path, default=M3 / 'out/phase2-class-census/census-current.json')
    parser.add_argument('--out', type=Path, default=M3 / 'out/phase2-vptr-writes/inventory.json')
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError('refusing to overwrite previous inventory')
    census = json.loads(args.census.read_bytes())
    units_path = PROJECT / 'fnv_decomp/build/units.json'
    units_raw = units_path.read_bytes()
    if hashlib.sha256(units_raw).hexdigest() != census['inputs']['units_sha256']:
        raise ValueError('census and current recipe differ')
    units = json.loads(units_raw)['units']
    addresses = {t['vtable_va'] for t in census['vtables']}
    addresses.update(int(addr, 0) for unit in units for name, addr in unit.get('symbols', {}).items()
                     if name.startswith('??_7'))
    rows = []
    source_counts = collections.Counter()
    for relative in sorted({u['source'] for u in units}):
        path = PROJECT / 'fnv_decomp' / relative
        raw = path.read_bytes()
        # Keep CR/LF characters when deriving byte-independent line metadata.
        source = raw.decode('utf-8-sig', errors='replace')
        matches = scan_source(source, addresses)
        if matches:
            source_counts[relative] = len(matches)
            rows.append(dict(source=relative, source_sha256=hashlib.sha256(raw).hexdigest(), leads=matches))
    stats = dict(sources_with_leads=len(rows), leads=sum(source_counts.values()),
                 annotated_function_leads=sum(r['annotated_function_address'] is not None for s in rows for r in s['leads']),
                 proven_manual_vptr_writes=0)
    result = dict(schema_version=1, scope=__doc__, inputs=dict(units_sha256=hashlib.sha256(units_raw).hexdigest(),
                  census_sha256=hashlib.sha256(args.census.read_bytes()).hexdigest()), stats=stats,
                  source_counts=dict(source_counts), sources=rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(stats))


if __name__ == '__main__':
    main()
