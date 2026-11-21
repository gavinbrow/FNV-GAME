"""Inventory observed x86 RTTI graphs without asserting recovered source classes.

Output is private reference-derived analysis, under m3/out by default. No source,
selection, compiler or shared build output is changed. A valid RTTI record is
evidence of a record, not evidence of a C++ signature, access rule or vtable extent.
"""
import argparse
import collections
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M3 = HERE.parent
PROJECT = M3.parent.parent


class InvalidRecord(ValueError):
    pass


class Records:
    def __init__(self, image, sections, relocations):
        self.image = image
        self.sections = sections
        self.relocations = set(relocations)
        self.names = {}
        self.hierarchies = {}

    def section(self, va, size=1):
        if size < 0:
            raise InvalidRecord('negative size')
        for name, sec in self.sections.items():
            if sec['va'] <= va and va + size <= sec['va'] + sec['raw']:
                return name
        raise InvalidRecord('record has no complete file backing')

    def read(self, va, size, section=None):
        name = self.section(va, size)
        if section is not None and name != section:
            raise InvalidRecord('record in unexpected section')
        sec = self.sections[name]
        offset = sec['off'] + va - sec['va']
        result = self.image[offset:offset + size]
        if len(result) != size:
            raise InvalidRecord('truncated image')
        return result

    def pointer(self, va):
        if va not in self.relocations:
            raise InvalidRecord('pointer has no original relocation')
        return struct.unpack('<I', self.read(va, 4))[0]

    def type_name(self, va):
        if va in self.names:
            return self.names[va]
        header = self.read(va, 8, '.data')
        type_info = self.pointer(va)
        if self.section(type_info, 4) != '.rdata' or header[4:] != bytes(4):
            raise InvalidRecord('invalid type descriptor header')
        remaining = self.sections['.data']['va'] + self.sections['.data']['raw'] - va - 8
        raw = self.read(va + 8, min(remaining, 4096), '.data')
        end = raw.find(bytes(1))
        if end < 0:
            raise InvalidRecord('unterminated type name')
        try:
            name = raw[:end].decode('ascii')
        except UnicodeDecodeError as exc:
            raise InvalidRecord('non-ASCII type name') from exc
        if not name.startswith(('.?AV', '.?AU')) or not name.endswith('@@'):
            raise InvalidRecord('unrecognized class type name')
        self.names[va] = name
        return name

    @staticmethod
    def preorder_parents(counts):
        """Validate subtree intervals; do not interpret access or virtual bases."""
        if not counts or counts[0] != len(counts) - 1:
            raise InvalidRecord('root subtree does not cover the base array')
        stack = []
        parents = []
        for index, count in enumerate(counts):
            while stack and stack[-1][1] < index:
                stack.pop()
            end = index + count
            if count < 0 or end >= len(counts):
                raise InvalidRecord('base subtree outside array')
            if stack and end > stack[-1][1]:
                raise InvalidRecord('crossing base subtrees')
            if index and not stack:
                raise InvalidRecord('disconnected base subtree')
            parents.append(stack[-1][0] if stack else None)
            stack.append((index, end))
        return parents

    def hierarchy(self, va):
        if va in self.hierarchies:
            return self.hierarchies[va]
        sig, attrs, count, array = struct.unpack('<IIII', self.read(va, 16, '.rdata'))
        if sig != 0 or attrs & ~7 or not 1 <= count <= 16384:
            raise InvalidRecord('unrecognized hierarchy header')
        if self.pointer(va + 12) != array:
            raise InvalidRecord('invalid base array pointer')
        self.read(array, 4 * count, '.rdata')
        bases = []
        for index in range(count):
            descriptor = self.pointer(array + 4 * index)
            td, contained, mdisp, pdisp, vdisp, flags = struct.unpack(
                '<IIiiiI', self.read(descriptor, 24, '.rdata'))
            if self.pointer(descriptor) != td:
                raise InvalidRecord('invalid base type pointer')
            name = self.type_name(td)
            base = dict(index=index, descriptor_va=descriptor, type_descriptor_va=td,
                        type_name=name, contained_bases=contained,
                        pmd=[mdisp, pdisp, vdisp], attributes=flags)
            if flags & 0x40:
                base['hierarchy_va'] = self.pointer(descriptor + 24)
                self.read(base['hierarchy_va'], 16, '.rdata')
            bases.append(base)
        parents = self.preorder_parents([b['contained_bases'] for b in bases])
        for base, parent in zip(bases, parents):
            base['preorder_parent_index'] = parent
        result = dict(va=va, attributes=attrs, base_array_va=array, bases=bases)
        self.hierarchies[va] = result
        return result

    def locator(self, va):
        sig, offset, cd, td, chd = struct.unpack('<IIIII', self.read(va, 20, '.rdata'))
        if sig != 0 or offset > 0x1000000 or cd > 0x1000000:
            raise InvalidRecord('unrecognized complete object locator')
        self.pointer(va + 12)
        self.pointer(va + 16)
        name = self.type_name(td)
        graph = self.hierarchy(chd)
        if graph['bases'][0]['type_descriptor_va'] != td:
            raise InvalidRecord('locator and root base identities disagree')
        return dict(va=va, subobject_offset=offset, constructor_displacement=cd,
                    type_descriptor_va=td, type_name=name, hierarchy_va=chd)

    def code_pointer_prefix(self, va):
        targets = []
        for index in range(4096):
            cell = va + 4 * index
            try:
                if self.section(cell, 4) != '.rdata':
                    break
                target = self.pointer(cell)
                if self.section(target) != '.text':
                    break
            except InvalidRecord:
                break
            targets.append(target)
        return targets


def collect():
    sys.path.insert(0, str(PROJECT / 'runtime-next/data-v3'))
    import common
    records = Records(common.ref, common.SEC, common.orig_reloc_sites())
    units_path = PROJECT / 'fnv_decomp/build/units.json'
    units = json.loads(units_path.read_bytes())['units']
    labels = collections.defaultdict(list)
    for index, unit in enumerate(units):
        for name, addr in unit.get('symbols', {}).items():
            if name.startswith('??_7'):
                labels[int(addr, 0)].append(dict(unit=index, source=unit['source'], symbol=name))
    tables = []
    rejected_named = []
    for cell in sorted(records.relocations):
        try:
            if records.section(cell, 4) != '.rdata':
                continue
            locator = records.locator(records.pointer(cell))
            targets = records.code_pointer_prefix(cell + 4)
            if not targets:
                raise InvalidRecord('no contiguous relocated code-pointer prefix')
        except InvalidRecord as exc:
            if cell + 4 in labels:
                rejected_named.append(dict(vtable_va=cell + 4, reason=str(exc),
                                           unit_symbols=labels[cell + 4]))
            continue
        tables.append(dict(vtable_va=cell + 4, locator=locator,
                           contiguous_code_pointer_prefix_targets=targets,
                           unit_symbols=labels.get(cell + 4, [])))
    locator_hierarchies = {r['locator']['hierarchy_va'] for r in tables}
    # Independently discover complete hierarchy headers. Some types have no
    # surviving vtable with a nonempty contiguous code-pointer prefix.
    for cell in sorted(records.relocations):
        try:
            records.read(cell - 12, 16, '.rdata')
            records.hierarchy(cell - 12)
        except InvalidRecord:
            pass
    used_hierarchies = set(records.hierarchies)
    used_types = {b['type_descriptor_va'] for va in used_hierarchies
                  for b in records.hierarchies[va]['bases']}
    type_info_targets = {records.pointer(td) for td in used_types}
    for cell in sorted(records.relocations):
        try:
            if records.section(cell, 8) != '.data' or records.pointer(cell) not in type_info_targets:
                continue
            records.type_name(cell)
            used_types.add(cell)
        except InvalidRecord:
            pass
    grouped = collections.defaultdict(list)
    for table in tables:
        grouped[table['locator']['type_descriptor_va']].append(table['vtable_va'])
    simple = re.compile(r'^\.\?A[VU]([A-Za-z_][A-Za-z_0-9]*)@@$')
    source_root = PROJECT / 'fnv_decomp'
    source_files = {source_root / u['source'] for u in units}
    source_files.update((source_root / 'include').rglob('*.h'))
    declared_in = collections.defaultdict(set)
    # Lexical discovery only. Comments/literals are removed; preprocessing,
    # namespace semantics and full declaration/layout parsing remain unproved.
    scrub = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)
    declaration = re.compile(r'\b(?:class|struct)\s+([A-Za-z_]\w*)\s*(?:\{|:[^;{]*\{)')
    for path in sorted(source_files):
        if not path.is_file():
            continue
        text = scrub.sub(' ', path.read_text(encoding='utf-8-sig', errors='replace'))
        for name in declaration.findall(text):
            declared_in[name].add(path.relative_to(source_root).as_posix())
    classes = []
    for td in sorted(used_types):
        name = records.type_name(td)
        match = simple.fullmatch(name)
        classes.append(dict(type_descriptor_va=td, type_name=name,
                            simple_identifier=match.group(1) if match else None,
                            lexical_definition_files=sorted(declared_in.get(match.group(1), [])) if match else [],
                            observed_vtables=grouped.get(td, []),
                            native_class_verified=False))
    stats = dict(observed_vtables=len(tables), observed_locator_type_descriptors=len(grouped),
                 observed_class_type_descriptors=len(classes), observed_hierarchies=len(used_hierarchies),
                 hierarchies_reached_from_vtables=len(locator_hierarchies),
                 tables_with_unit_vtable_symbols=sum(bool(t['unit_symbols']) for t in tables),
                 named_symbol_addresses_rejected=len(rejected_named),
                 code_pointer_prefix_cells=sum(len(t['contiguous_code_pointer_prefix_targets']) for t in tables),
                 simple_names_with_lexical_definition=sum(bool(c['lexical_definition_files']) for c in classes),
                 native_classes_verified=0)
    return dict(schema_version=1,
                scope='Observed relocated RTTI graph census and lexical definition leads. Not recovered classes, complete virtual slot extents, native ABI proof, or a whole-phase completion percentage.',
                inputs=dict(reference_sha256=hashlib.sha256(common.ref).hexdigest(),
                            units_sha256=hashlib.sha256(units_path.read_bytes()).hexdigest()),
                stats=stats, classes=classes, vtables=tables,
                hierarchies=[records.hierarchies[va] for va in sorted(used_hierarchies)],
                rejected_named_symbol_addresses=rejected_named)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=M3 / 'out/phase2-class-census/census.json')
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError('refusing to replace an existing census')
    data = collect()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2)
    print(json.dumps(data['stats'], sort_keys=True))


if __name__ == '__main__':
    main()
