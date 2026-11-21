"""Independently replay actual W103 source COFF and final-image mutation effects."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import pefile

if sys.flags.optimize:
    raise RuntimeError('Evidence audits require assertions enabled')

HERE = Path(__file__).resolve().parent
M3 = HERE.parent
ROOT = M3.parents[1]
sys.path[:0] = [str(ROOT / 'fnv_decomp/tools'), str(HERE), str(M3 / 'tools')]
from compare import Coff
from next_data_artifact_audit import pe_sections
from verify_saved_runs import check_control_logs
import w103_frozen_proof

def load(path):
    return json.loads(path.read_bytes())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('control', choices=('p2rv', 'p2rp'))
    ap.add_argument('--suite', choices=('v3', 'v4'), default='v3')
    args = ap.parse_args()
    runs = [M3 / ('out/phase2-psa-w103-' + args.suite + '-positive'), M3 / ('out/phase2-psa-w103-' + args.suite + '-' + args.control)]
    output = runs[1] / 'evidence' / ('root-' + args.control + '-actual-proof.json')
    if output.exists():
        raise FileExistsError(output)
    target = 0x1196e20 if args.control == 'p2rv' else 0x110fbe8
    snapshots, records, images, results, offsets, fixed_inputs = [], [], [], [], [], []
    for run in runs:
        evidence = run / 'evidence'
        freeze = Path(str(run) + '-freeze')
        f = load(freeze / 'result.json')
        assert f['command_rc'] == 0 and f['input_freeze_passed']
        assert not f['final_digest_changes'] and not f['observed_metadata_changes']
        snapshots.append(load(freeze / 'inputs-before.json'))
        fixed_inputs.append(w103_frozen_proof.check(run, snapshots[-1]))
        summary = load(run / 'build-summary.json')
        assert all(step['rc'] == 0 for step in summary['steps'])
        if run == runs[0]:
            assert summary['status'] == 'ok'
        else:
            assert summary['status'] == 'ok-harness-skipped'
            assert summary['harness'] == 'skipped (--no-harness)'
            assert '--no-harness' in load(freeze / 'command.json')['command']
            assert all(step['name'] != 'harness' for step in summary['steps'])
        pieces = load(evidence / 'dv1_pieces.json')['pieces']
        candidates = [p for p in pieces if p['va'] == target]
        assert len(candidates) == 1
        piece = candidates[0]
        assert piece['unit'] == 620 and piece['nunits'] == 1
        assert piece['size'] == (26 if args.control == 'p2rv' else 20)
        records.append(piece)
        obj = evidence / '0620.obj'
        coff = Coff(str(obj))
        symbol = coff.named(piece['names'][0])
        section = coff.sections[symbol['section']]
        start = symbol['value']
        raw_size, raw_ptr = struct.unpack_from('<II', coff.data, 20 + (symbol['section'] - 1) * 40 + 16)
        assert raw_ptr > 0 and start + piece['size'] <= raw_size
        assert bytes(section['data'][start:start + piece['size']]).hex() == piece['data']
        relocs = [(off-start, coff.symbols[i]['name'], k) for off, i, k in section['relocs'] if start <= off < start+piece['size']]
        assert sorted(x[0] for x in relocs) == sorted(x[0] for x in piece['relocs'])
        assert all(x[2] == 6 for x in relocs)
        expected_relocs = [(0, '??_7type_info@@6B@', 6)] if args.control == 'p2rv' else [(12, '??_R0?AVTESModelPSA@@@8', 6), (16, '??_R3TESModelPSA@@8', 6)]
        assert sorted(relocs) == expected_relocs
        image, base, sections = pe_sections(run / 'FalloutNV_selfbuilt.exe')
        images.append(image)
        chunks = {x['file']: x for x in load(evidence / 'data-v3-manifest.json')}
        pos, chunk_offsets = 0, {}
        for name in ('rdata_03', 'rdata_02', 'rdata_01', 'rdata_00'):
            chunk = chunks[name]
            pos += (chunk['va'] - pos) % 16
            chunk_offsets[name] = pos
            pos += chunk['size']
        def translate(va):
            found = [c for c in chunks.values() if c['section'] in ('.data', '.rdata') and c['va'] <= va < c['va'] + c['size']]
            assert len(found) == 1
            c = found[0]
            return sections[c['section']]['va'] + chunk_offsets.get(c['file'], 0) + va - c['va']
        new_va = translate(target)
        file_offset = sections[piece['section']]['offset'] + new_va - sections[piece['section']]['va']
        expected = bytearray.fromhex(piece['data'])
        for off, original_target, addend in piece['relocs']:
            if run == runs[1] and args.control == 'p2rp' and off == 12:
                original_target = 0x11831e8
            struct.pack_into('<I', expected, off, translate(original_target))
        if run == runs[1] and args.control == 'p2rv':
            expected[8] ^= 1
        assert image[file_offset:file_offset+piece['size']] == expected
        offsets.append(file_offset)
        results.append({'object_sha256': sha(obj), 'image_sha256': sha(run / 'FalloutNV_selfbuilt.exe'), 'final_va': new_va, 'actual_payload': expected.hex(), 'coff_relocations': relocs, 'coff_native_record': {'data': bytes(section['data']).hex(), 'name': section['name'], 'flags': section['flags'], 'symbol_value': start, 'storage': symbol['storage']}})
    assert records[0] == records[1], 'source DV1 records must remain unmodified'
    assert results[0]['coff_native_record'] == results[1]['coff_native_record'] and results[0]['coff_relocations'] == results[1]['coff_relocations'], 'native COFF record must remain unmodified'
    assert results[0]['image_sha256'] == 'c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f'
    assert results[0]['image_sha256'] != results[1]['image_sha256'] and offsets[0] == offsets[1]
    assert len(images[0]) == len(images[1])
    differences = [i for i, (a, b) in enumerate(zip(*images)) if a != b]
    field = offsets[0] + (8 if args.control == 'p2rv' else 12)
    payload_fields = set(range(field, field + (1 if args.control == 'p2rv' else 4)))
    checksum_proofs = []
    for raw in images:
        pe = pefile.PE(data=raw, fast_load=True)
        checksum_offset = pe.OPTIONAL_HEADER.get_field_absolute_offset('CheckSum')
        computed = pe.generate_checksum()
        assert pe.OPTIONAL_HEADER.CheckSum == computed, 'independent PE checksum verification failed'
        checksum_proofs.append({'file_offset': checksum_offset, 'stored': pe.OPTIONAL_HEADER.CheckSum, 'computed': computed})
        pe.close()
    assert checksum_proofs[0]['file_offset'] == checksum_proofs[1]['file_offset']
    checksum_fields = set(range(checksum_proofs[0]['file_offset'], checksum_proofs[0]['file_offset'] + 4))
    assert not payload_fields & checksum_fields
    payload_differences = set(differences) & payload_fields
    assert payload_differences and set(differences) <= payload_fields | checksum_fields
    source = lambda snap: {k: v['sha256'] for k, v in snap.items() if '/fnv_decomp/src/' in k.lower().replace('\\', '/') or '/fnv_decomp/include/' in k.lower().replace('\\', '/')}
    assert source(snapshots[0]) == source(snapshots[1]) and len(source(snapshots[0])) == 5497
    manifest = load(M3 / 'out/phase2-psa-w103-control-patch/manifest.json')
    for row in manifest['files']:
        key = str((ROOT / row['path']).resolve())
        assert all(s[key]['sha256'] == row['new_sha256'] for s in snapshots)
    package = M3 / 'out/phase2-psa-w103-optin-package'
    package_manifest = load(package / 'manifest.json')
    required = {
        package / 'selection.json': package_manifest['selection_sha256'],
        package / 'manifest.json': sha(package / 'manifest.json'),
        ROOT / 'fnv_decomp/build/units.json': package_manifest['recipe_sha256'],
        M3 / 'phase2/library_candidates.json': package_manifest['library_selection_sha256'],
        ROOT / 'FNV/work/worker1/FalloutNV.runtime-text.exe': 'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7',
    }
    for path, digest in required.items():
        assert all(s[str(path.resolve())]['sha256'] == digest for s in snapshots)
    for run, snapshot in zip(runs, snapshots):
        preflight = load(Path(str(run) + '-preflight.json'))
        assert preflight['recipe_sha256'] == package_manifest['recipe_sha256']
        for row in preflight['required']:
            assert snapshot[str(Path(row['path']).resolve())]['sha256'] == row['sha256']
    assert check_control_logs(runs[1] / 'build-summary.json', load(runs[1] / 'build-summary.json')) == ('value' if args.control == 'p2rv' else 'pointer')
    proof = {'status': 'PASS actual native COFF, unchanged DV1 input, exact final PE mutation', 'control': args.control, 'runs': results, 'fixed_input_proofs': fixed_inputs, 'source_inputs_equal': 5497, 'different_image_bytes': len(differences), 'payload_difference_bytes': len(payload_differences), 'checksum_difference_bytes': len(set(differences) & checksum_fields), 'checksum_proofs': checksum_proofs, 'checksum_verifier_sha256': sha(Path(pefile.__file__)), 'mutation_scope': 'only intended payload field and independently verified derived PE checksum; mutation occurs after selected source records are validated', 'whole_phase2_complete': False}
    output.write_text(json.dumps(proof, indent=2), encoding='utf-8')
    print(json.dumps({'status': proof['status'], 'control': args.control, 'different_image_bytes': len(differences)}))

if __name__ == '__main__':
    main()
