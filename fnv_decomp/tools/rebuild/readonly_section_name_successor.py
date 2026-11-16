"""Fixed, review-gated section-name successor for two accepted private COFF objects."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct

RECEIPT_SHA = 'b1a6554ad8170f06f7367a21d5b6ecd6b8b6c910e3fa3241ef8a3bde039db792'
INPUTS = (
    ('cb8d58d939251b22cc7429f62751a51e83d1c6f11abeef2489d3b96a973b7c1a', '2243cf180e35988042c930514b7b3ae54cdab4cafa951c179312537e4000e67e', 219, 11),
    ('a80a7435d3665b08022dc0a36be353e4ffafa56da5fd9b4337224164f96aedeb', '1b786bd7a6fbef349327851bbc8ebc350b3deabb9ca190144bf7b33f2a26f686', 227, 9),
)
OLD = b'.data\0\0\0'
NEW = b'.rdata\0\0'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def transform(data, size, symbols):
    """Change exactly the sole COFF section's eight-byte name field."""
    if len(data) < 60:
        raise ValueError('truncated COFF header')
    machine, sections, _, symptr, count, optional, flags = struct.unpack_from('<HHIIIHH', data)
    if (machine, sections, count, optional, flags) != (0x14c, 1, symbols, 0, 0):
        raise ValueError('unexpected COFF shape')
    rawsize, rawptr, relocptr, lineptr, reloccount, linecount, characteristics = struct.unpack_from('<IIIIHHI', data, 36)
    if (data[20:28] != OLD or rawsize != size or rawptr < 60 or rawptr + size > len(data)
            or relocptr != 0 or lineptr != 0 or reloccount != 0 or linecount != 0
            or characteristics != 0x40100040 or symptr < rawptr + size or symptr + count * 18 + 4 > len(data)):
        raise ValueError('unexpected section geometry or protection')
    result = data[:20] + NEW + data[28:]
    if result[:20] != data[:20] or result[28:] != data[28:]:
        raise ValueError('unexpected change outside section name')
    return result


def project(input_dir, review_path, output_dir):
    """Exact immutable inputs and source review; output directory must be new."""
    source = Path(__file__).resolve()
    input_dir, review_path, output_dir = map(lambda p: Path(p).resolve(), (input_dir, review_path, output_dir))
    review_bytes = review_path.read_bytes()
    review = json.loads(review_bytes)
    if not (review.get('kind') == 'readonly-section-name-successor-review'
            and review.get('approved') is True and review.get('root_authorized') is True
            and isinstance(review.get('reviewer'), str) and review['reviewer'].strip()
            and review.get('source_sha256') == digest(source.read_bytes())
            and review.get('input_receipt_sha256') == RECEIPT_SHA):
        raise ValueError('exact independent review and root authorization required')
    receipt_path = input_dir / 'projection.json'
    receipt_bytes = receipt_path.read_bytes()
    if digest(receipt_bytes) != RECEIPT_SHA:
        raise ValueError('input receipt hash differs')
    receipt = json.loads(receipt_bytes)
    if (receipt.get('kind'), receipt.get('initialized_bytes'), receipt.get('aliases'), receipt.get('entry_fields'), receipt.get('relocations')) != ('private-entry-raw-alias-projection', 446, 16, 20, 0):
        raise ValueError('input receipt scope differs')
    if output_dir.exists() or output_dir == input_dir or input_dir in output_dir.parents or output_dir in input_dir.parents or output_dir == review_path or output_dir in review_path.parents or output_dir == source or output_dir in source.parents:
        raise ValueError('output exists or overlaps protected inputs')
    records = receipt.get('objects', [])
    if len(records) != 2:
        raise ValueError('expected two receipt objects')
    staged = []
    for record, (identity, expected, size, symbols) in zip(records, INPUTS):
        path = input_dir / (identity + '.obj')
        data = path.read_bytes()
        if record.get('fragment_id') != identity or record.get('object_sha256') != expected or digest(data) != expected:
            raise ValueError('input object identity differs')
        result = transform(data, size, symbols)
        staged.append((path, data, result, identity, expected))
    def stable():
        if (receipt_path.read_bytes() != receipt_bytes or review_path.read_bytes() != review_bytes
                or digest(source.read_bytes()) != review['source_sha256']
                or any(path.read_bytes() != data for path, data, _, _, _ in staged)):
            raise ValueError('protected input changed')
    stable()
    output_dir.mkdir()
    created = []
    try:
        outputs = []
        for _, _, result, identity, expected in staged:
            dest = output_dir / (identity + '.obj')
            with dest.open('xb') as f:
                created.append(dest)
                f.write(result)
            if dest.read_bytes() != result:
                raise ValueError('output differs')
            outputs.append(dict(fragment_id=identity, input_sha256=expected, output_sha256=digest(result), section_name_offset=20))
        stable()
        report = dict(kind='private-readonly-section-name-successor', schema_version=1,
                      input_receipt_sha256=RECEIPT_SHA, review_sha256=digest(review_bytes),
                      source_sha256=review['source_sha256'], objects=outputs,
                      old_section_name='.data', new_section_name='.rdata', changed_field_bytes=8,
                      initialized_bytes=446, aliases=16, entry_fields=20, relocations=0,
                      runtime_eligible=False, provider_selected=False, materialization_approved=False,
                      link_ready=False, game_fixups_approved=False)
        dest = output_dir / 'projection.json'
        with dest.open('x', encoding='utf-8', newline='\n') as f:
            created.append(dest)
            json.dump(report, f, indent=2)
            f.write('\n')
        stable()
        return report
    except Exception:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        output_dir.rmdir()
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--review', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    project(args.input_dir, args.review, args.output_dir)
