#!/usr/bin/env python3
"""Inventory address-labelled symbol spellings without inferring C/C++ types.

Explicit input files only. Results retain declaration text as evidence; they are
not a selection or a claim that a symbol has a particular size or type.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

SYMBOL = re.compile(r'(?<![A-Za-z0-9_])(?P<name>(?:DAT|PTR|OFF|_DAT)_[0-9a-fA-F]{8})(?![A-Za-z0-9_])')
# Keep strings and comments from introducing spurious symbols. Preserve newlines
# and character offsets so declaration evidence remains attributable to its line.
LEX = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
DECL = re.compile(r'^\s*extern\b')


def mask_noncode(text):
    return LEX.sub(lambda m: ''.join('\n' if c == '\n' else ' ' for c in m.group()), text)


def inventory_files(files):
    records = defaultdict(lambda: {'references': 0, 'files': set(), 'declarations': set()})
    for path in files:
        path = Path(path)
        text = path.read_text(encoding='utf-8', errors='replace')
        originals = text.splitlines()
        codes = mask_noncode(text).splitlines()
        for code in codes:
            for match in SYMBOL.finditer(code):
                name = match.group('name')
                # Normalize only the hexadecimal address, preserving the spelling prefix.
                prefix, address = name.rsplit('_', 1)
                name = prefix + '_' + address.lower()
                record = records[name]
                record['references'] += 1
                record['files'].add(str(path))

        # Capture only straightforward extern statements. Braces and preprocessor
        # directives make a multiline construct ambiguous, so leave it pending.
        start = None
        for index, code in enumerate(codes):
            if start is None:
                if not DECL.match(code):
                    continue
                start = index
            if re.search(r'[{}]|^\s*#', code):
                start = None
                continue
            if ';' not in code:
                continue
            # Preserve historical single-line evidence, including trailing comments.
            # For multiline statements retain the exact source lines through the
            # terminating line, without claiming a parsed C/C++ declaration.
            statement_code = '\n'.join(codes[start:index + 1])
            if code.rstrip().endswith(';') and (start == index or statement_code.count(';') == 1):
                evidence = '\n'.join(originals[start:index + 1]).strip()
                for match in SYMBOL.finditer(statement_code):
                    prefix, address = match.group('name').rsplit('_', 1)
                    name = prefix + '_' + address.lower()
                    records[name]['declarations'].add((str(path), start + 1, evidence))
            start = None
    result = []
    for name, rec in sorted(records.items(), key=lambda item: (int(item[0][-8:], 16), item[0])):
        result.append({'name': name, 'address': '0x' + name[-8:],
                       'references': rec['references'], 'files': sorted(rec['files']),
                       'declarations': [{'file': f, 'line': n, 'text': s}
                                        for f, n, s in sorted(rec['declarations'])]})
    return result


def annotate_sections(rows, metadata):
    """Annotate from saved section bounds, without inspecting image contents."""
    sections = metadata['meta']['sections']
    for row in rows:
        addr = int(row['address'], 16)
        matches = [s for s in sections if int(s['va'], 0) <= addr < int(s['end'], 0)]
        if len(matches) > 1:
            raise ValueError('overlapping saved sections at %s' % row['address'])
        if matches:
            section = matches[0]
            row['section'] = section['name']
            row['storage'] = 'file_resident' if addr < int(section['raw_end'], 0) else 'memory_only'
        else:
            row['section'] = None
            row['storage'] = 'unmapped'
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', type=Path, help='explicit source files; directories are not scanned')
    parser.add_argument('--files-from', type=Path, help='UTF-8 file listing one source path per line')
    parser.add_argument('--section-metadata', type=Path, help='existing inventory JSON with saved section bounds')
    args = parser.parse_args()
    if args.files_from:
        with args.files_from.open(encoding='utf-8-sig') as fh:
            args.files.extend(Path(line.strip()) for line in fh if line.strip())
    if not args.files:
        parser.error('provide source files or --files-from')
    for path in args.files:
        if not path.is_file():
            parser.error('not a file: %s' % path)
    # A file named both explicitly and in a list must not be counted twice.
    files = list(dict.fromkeys(path.resolve() for path in args.files))
    rows = inventory_files(files)
    if args.section_metadata:
        with args.section_metadata.open(encoding='utf-8') as fh:
            annotate_sections(rows, json.load(fh))
    print(json.dumps({'section_metadata': str(args.section_metadata) if args.section_metadata else None,
                      'symbols': rows}, indent=2))


if __name__ == '__main__':
    main()
