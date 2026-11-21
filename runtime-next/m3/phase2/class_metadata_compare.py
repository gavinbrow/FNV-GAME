"""Read-only structural RTTI and virtual-slot comparison for one private COFF.

Uses native COFF references, exact names and normal source-unit mappings. Never
invents an address alias from the reference target. Output belongs under m3/out.
This checks emitted records, not C++ source/ABI correctness or runtime behavior.
"""
import argparse
import collections
import hashlib
import json
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M3 = HERE.parent
PROJECT = M3.parent.parent
sys.path[:0] = [str(HERE), str(PROJECT / 'fnv_decomp/tools'), str(PROJECT / 'runtime-next/pinned-build')]
from compare import Coff
import assemble_v3 as assembler
from native_class_inventory import InvalidRecord, Records


class ObjectRecords:
    def __init__(self, coff):
        self.coff = coff

    def read(self, location, size):
        section, offset = location
        if not 0 < section < len(self.coff.sections) or offset < 0:
            raise InvalidRecord('invalid COFF location')
        data = self.coff.sections[section]['data'][offset:offset + size]
        if len(data) != size:
            raise InvalidRecord('COFF record crosses section')
        return data

    def location(self, symbol):
        if symbol['section'] > 0:
            return symbol['section'], symbol['value']
        try:
            defined = self.coff.named(symbol['name'])
        except ValueError as exc:
            raise InvalidRecord('unresolved or ambiguous local metadata symbol') from exc
        return defined['section'], defined['value']

    def relocation(self, location):
        section, offset = location
        rows = [r for r in self.coff.sections[section]['relocs']
                if r[0] < offset + 4 and offset < r[0] + 4]
        if len(rows) != 1 or rows[0][0] != offset or rows[0][2] != 6:
            raise InvalidRecord('metadata pointer requires one exact DIR32 relocation')
        symbol = self.coff.symbols.get(rows[0][1])
        if symbol is None:
            raise InvalidRecord('relocation references a missing symbol')
        addend = struct.unpack('<I', self.read(location, 4))[0]
        return symbol, addend

    def pointer(self, location):
        symbol, addend = self.relocation(location)
        section, offset = self.location(symbol)
        self.read((section, offset + addend), 1)
        return section, offset + addend

    def check_fields(self, location, size, expected_offsets):
        section, start = location
        self.read(location, size)
        rows = [r for r in self.coff.sections[section]['relocs']
                if r[0] < start + size and start < r[0] + 4]
        if sorted((r[0] - start, r[2]) for r in rows) != [(o, 6) for o in expected_offsets]:
            raise InvalidRecord('unexpected metadata relocation field set')

    def type_name(self, location):
        section, offset = location
        symbol, addend = self.relocation(location)
        if symbol['name'] != '??_7type_info@@6B@' or addend != 0:
            raise InvalidRecord('unexpected type-info identity or addend')
        if self.read((section, offset + 4), 4) != bytes(4):
            raise InvalidRecord('nonzero type descriptor spare')
        raw = self.coff.sections[section]['data'][offset + 8:offset + 4104]
        end = raw.find(bytes(1))
        if end < 0:
            raise InvalidRecord('unterminated COFF type name')
        try:
            name = raw[:end].decode('ascii')
        except UnicodeDecodeError as exc:
            raise InvalidRecord('non-ASCII COFF type name') from exc
        if not name.startswith(('.?AV', '.?AU')) or not name.endswith('@@'):
            raise InvalidRecord('unrecognized COFF class type name')
        self.check_fields(location, 9 + end, [0])
        return name

    def hierarchy(self, location):
        section, start = location
        sig, attrs, count, _ = struct.unpack('<IIII', self.read(location, 16))
        if sig != 0 or attrs & ~7 or not 1 <= count <= 16384:
            raise InvalidRecord('unrecognized COFF hierarchy header')
        self.check_fields(location, 16, [12])
        array = self.pointer((section, start + 12))
        self.check_fields(array, count * 4, list(range(0, count * 4, 4)))
        bases = []
        for index in range(count):
            b = self.pointer((array[0], array[1] + index * 4))
            _, contained, m, p, v, flags = struct.unpack('<IIiiiI', self.read(b, 24))
            self.check_fields(b, 28 if flags & 0x40 else 24, [0, 24] if flags & 0x40 else [0])
            name = self.type_name(self.pointer(b))
            if flags & 0x40:
                self.read(self.pointer((b[0], b[1] + 24)), 16)
            bases.append(dict(type_name=name, contained_bases=contained,
                              pmd=[m, p, v], attributes=flags))
        parents = Records.preorder_parents([b['contained_bases'] for b in bases])
        for b, parent in zip(bases, parents):
            b['preorder_parent_index'] = parent
        return dict(attributes=attrs, bases=bases)

    def locator(self, location):
        section, start = location
        sig, offset, cd, _, _ = struct.unpack('<IIIII', self.read(location, 20))
        if sig != 0:
            raise InvalidRecord('unexpected COFF locator signature')
        self.check_fields(location, 20, [12, 16])
        name = self.type_name(self.pointer((section, start + 12)))
        graph = self.hierarchy(self.pointer((section, start + 16)))
        if graph['bases'][0]['type_name'] != name:
            raise InvalidRecord('COFF locator and root type disagree')
        return dict(type_name=name, subobject_offset=offset,
                    constructor_displacement=cd, graph=graph)

    def tables(self, type_name):
        seen = set()
        result = []
        for symbol in self.coff.symbols.values():
            if not symbol['name'].startswith('??_7') or symbol['section'] <= 0:
                continue
            loc = self.location(symbol)
            if loc in seen or loc[1] < 4:
                continue
            seen.add(loc)
            try:
                col = self.locator(self.pointer((loc[0], loc[1] - 4)))
            except InvalidRecord:
                continue
            if col['type_name'] != type_name:
                continue
            end = len(self.coff.sections[loc[0]]['data'])
            next_tables = [s['value'] - 4 for s in self.coff.symbols.values()
                           if s['name'].startswith('??_7') and s['section'] == loc[0] and s['value'] > loc[1]]
            if next_tables:
                end = min(end, min(next_tables))
            if end < loc[1] or (end - loc[1]) % 4:
                raise InvalidRecord('ambiguous emitted vtable extent')
            self.check_fields(loc, end - loc[1], list(range(0, end - loc[1], 4)))
            slots = []
            for offset in range(loc[1], end, 4):
                target, addend = self.relocation((loc[0], offset))
                slots.append(dict(symbol=target, addend=addend))
            result.append(dict(symbol=symbol['name'], locator=col, slots=slots))
        return result


def unique_global_maps(units):
    functions = collections.defaultdict(set)
    symbols = collections.defaultdict(set)
    for unit in units:
        for f in unit.get('functions', []):
            for name in [f['symbol']] + f.get('fold_aliases', []):
                functions[name].add(int(f['address'], 0))
        for name, value in unit.get('symbols', {}).items():
            symbols[name].add(int(value, 0))
    return ({k: next(iter(v)) for k, v in functions.items() if len(v) == 1},
            {k: next(iter(v)) for k, v in symbols.items() if len(v) == 1})


def compare_class(object_path, unit, units, census, type_name, global_maps=None):
    coff = Coff(object_path)
    emitted = ObjectRecords(coff).tables(type_name)
    refs = [t for t in census['vtables'] if t['locator']['type_name'] == type_name]
    graphs = {g['va']: g for g in census['hierarchies']}
    fn, sym = global_maps if global_maps is not None else unique_global_maps(units)
    # No original pointer value is supplied to the field resolver. This uses its
    # direct source mappings only, excluding name-embedded-address heuristics.
    assembler.G.update(pe=None, fn=fn, sym=sym, imp={}, thunks={})
    mapped = dict(unit)
    mapped['_fnmap'] = {name: int(f['address'], 0) for f in unit.get('functions', [])
                        for name in [f['symbol']] + f.get('fold_aliases', [])}
    locals_ = []
    for f in unit.get('functions', []):
        for name in [f['symbol']] + f.get('fold_aliases', []):
            for s in coff.by_name.get(name, []):
                if s['section'] > 0:
                    locals_.append((s['section'], s['value'], int(f['address'], 0), int(f['size'])))
    rows = []
    for table in emitted:
        locator = table['locator']
        candidates = [r for r in refs if r['locator']['subobject_offset'] == locator['subobject_offset']
                      and r['locator']['constructor_displacement'] == locator['constructor_displacement']]
        row = dict(symbol=table['symbol'], subobject_offset=locator['subobject_offset'],
                   emitted_slot_count=len(table['slots']), original_candidate_count=len(candidates))
        if len(candidates) != 1:
            row['status'] = 'ambiguous or missing original locator'
            rows.append(row)
            continue
        ref = candidates[0]
        graph = graphs[ref['locator']['hierarchy_va']]
        reference_bases = [{k: b[k] for k in ('type_name', 'contained_bases', 'pmd', 'attributes', 'preorder_parent_index')}
                           for b in graph['bases']]
        row.update(reference_vtable_va=ref['vtable_va'],
                   graph_fields_equal=(locator['graph'] == dict(attributes=graph['attributes'], bases=reference_bases)),
                   original_code_pointer_prefix_count=len(ref['contiguous_code_pointer_prefix_targets']))
        slots = []
        for index, slot in enumerate(table['slots']):
            src, target = assembler._resolve_field_direct(coff, mapped, locals_, 6, slot['symbol'], slot['addend'], 0, bytes(4))
            if src == 'b':
                src, target = None, None
            prefix = ref['contiguous_code_pointer_prefix_targets']
            expected = prefix[index] if index < len(prefix) else None
            slots.append(dict(index=index, symbol=slot['symbol']['name'], addend=slot['addend'],
                              resolution_source=src, resolved_target=target, reference_target=expected,
                              match=target is not None and target == expected))
        row.update(slots=slots, slot_prefix_count_equal=len(slots) == len(ref['contiguous_code_pointer_prefix_targets']))
        row['status'] = ('emitted record fields and slot prefix match' if row['graph_fields_equal']
                         and row['slot_prefix_count_equal'] and all(s['match'] for s in slots)
                         else 'incomplete or mismatched emitted metadata')
        rows.append(row)
    return dict(schema_version=1, scope='Emitted COFF graph fields and virtual slot prefix conformance only; full source ABI, ODR, record placement/ownership, whole vtable extent and gameplay remain separate gates.',
                object_sha256=hashlib.sha256(Path(object_path).read_bytes()).hexdigest(),
                type_name=type_name, emitted_tables=len(emitted), reference_tables=len(refs), tables=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--object', type=Path, required=True)
    parser.add_argument('--unit-index', type=int, required=True)
    parser.add_argument('--unit-overlay', type=Path)
    parser.add_argument('--type-name', required=True)
    parser.add_argument('--census', type=Path, default=M3 / 'out/phase2-class-census/census-v2.json')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError('refusing to overwrite prior comparison')
    units_path = PROJECT / 'fnv_decomp/build/units.json'
    units = json.loads(units_path.read_bytes())['units']
    census = json.loads(args.census.read_bytes())
    if census['inputs']['units_sha256'] != hashlib.sha256(units_path.read_bytes()).hexdigest():
        raise ValueError('census unit recipe is stale')
    unit = json.loads(args.unit_overlay.read_bytes()) if args.unit_overlay else units[args.unit_index]
    result = compare_class(args.object, unit, units, census, args.type_name)
    result['inputs'] = dict(unit_index=args.unit_index, units_sha256=census['inputs']['units_sha256'],
                            census_sha256=hashlib.sha256(args.census.read_bytes()).hexdigest())
    if args.unit_overlay:
        result['inputs']['unit_overlay_sha256'] = hashlib.sha256(args.unit_overlay.read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(dict(emitted_tables=result['emitted_tables'], reference_tables=result['reference_tables'],
                          graph_matches=sum(t.get('graph_fields_equal', False) for t in result['tables']),
                          slot_count_matches=sum(t.get('slot_prefix_count_equal', False) for t in result['tables']),
                          statuses=dict(collections.Counter(t['status'] for t in result['tables'])))))


if __name__ == '__main__':
    main()
