"""Independently audit the bounded native-method source batch's saved artifacts."""
import hashlib
import json
from pathlib import Path
import struct
import sys

M = Path(__file__).resolve().parent.parent
RN = M.parent
P = RN.parent
sys.path[:0] = [str(P / 'fnv_decomp/tools'), str(RN), str(M / 'tools')]
from compare import Coff, Pe, compare
from build_and_match import recipe_names, eh_sections, eh_tails
from harness_evidence import accepted_verdict
import paths
import verify_saved_runs as checker


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reloc(path):
    data = path.read_bytes()
    header = struct.unpack_from('<I', data, 0x3c)[0]
    optional = header + 24
    count = struct.unpack_from('<H', data, header + 6)[0]
    size = struct.unpack_from('<H', data, header + 20)[0]
    assert data[header:header + 4] == b'PE\0\0'
    assert struct.unpack_from('<H', data, optional)[0] == 0x10b
    rva, length = struct.unpack_from('<II', data, optional + 96 + 5 * 8)
    chunks = []
    for index in range(count):
        va, raw_size, offset = struct.unpack_from('<III', data, optional + size + index * 40 + 12)
        if va <= rva and rva + length <= va + raw_size:
            chunks.append(data[offset + rva - va:offset + rva - va + length])
    assert len(chunks) == 1 and len(chunks[0]) == length
    return chunks[0]


def main():
    directory = M / 'out/phase2-native-methods-repeat'
    evidence = directory / 'evidence'
    run = load(directory / 'build-summary.json')
    verdict = load(directory / 'harness-verdict.json')
    baseline = load(M / 'out/batch8-baseline/build-summary.json')
    controls = [load(M / ('out/phase2-native-methods-' + identity + '/build-summary.json'))
                for identity in ('p2av', 'p2wp')]
    assert not checker.check(run, baseline, controls, verdict)
    assert not checker.check_cell_state(verdict)
    assert accepted_verdict(run['harness']['rc'], verdict, run['exe']['path'], run['harness']['tag'])
    canonical = 'c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f'
    assert sha(Path(run['exe']['path'])) == run['exe']['sha256'] == canonical
    freeze_root = M / 'out/phase2-native-methods-repeat-freeze'
    freeze = load(freeze_root / 'result.json')
    assert freeze['command_rc'] == 0 and freeze['input_freeze_passed'] is True
    assert not freeze['final_digest_changes'] and not freeze['observed_metadata_changes']
    environment = load(freeze_root / 'command.json')['build_environment']
    assert environment in ({}, {'FNV_COFF_WEAK': '0'})
    relocation = reloc(Path(run['exe']['path']))
    assert relocation == reloc(Path(baseline['exe']['path'])) and len(relocation) == 734884
    relocation_hash = hashlib.sha256(relocation).hexdigest()
    assert relocation_hash == '364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057'
    for name, digest in run['provenance']['data_v1_scratch_sha256'].items():
        assert sha(evidence / 'data-v1-scratch' / name) == digest
    recipe = evidence / 'units.json'
    assert sha(recipe) == 'd5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
    units = load(recipe)['units']
    late = evidence / 'late-production-objects'
    archival = load(late / 'manifest.json')
    for item in archival['files']:
        assert sha(Path(item['archived'])) == item['sha256']
    assert sha(late / 'units.json') == sha(recipe)
    pe = Pe(paths.REF_IMAGE)
    names = recipe_names(units)
    facts, completed = [], []
    for index in (2, 651, 980, 998):
        unit = units[index]
        spec = dict(unit, symbols=dict(unit['symbols']))
        if index == 2:
            symbol = '??1TESForm@@UAE@XZ'
            assert units[658]['symbols'][symbol] == units[973]['symbols'][symbol] == '0x00483630'
            spec['symbols'][symbol] = '0x00483630'
        obj = late / ('%04d.obj' % index)
        coff = Coff(str(obj))
        rows = compare(coff, pe, spec)
        assert all(row['verdict'] == 'match' for row in rows), (index, rows)
        sections, inferred, errors = eh_sections(coff, pe, unit, rows, names)
        assert not errors, (index, errors)
        completed.append(dict(eh_sections=sections,
                              eh_inferred={key: '0x%08x' % value for key, value in inferred.items()}))
        facts.append(dict(unit=index, functions=len(rows), strict_matches=len(rows),
                          eh_sections=len(sections), object_sha256=sha(obj)))
    tails, bad, inferred, _, conflicts = eh_tails([units[i] for i in (2, 651, 980, 998)], completed, pe)
    assert not bad and not conflicts
    report = dict(status='PASS bounded native-methods source batch accepted',
                  scope='11 TESForm and 9 BGSE source remaps, typed contracts, no-op folding and TESContainer consolidation. Whole Phase 2 remains open.',
                  recipe_sha256=sha(recipe), actual_executable_sha256=canonical,
                  actual_relocation_bytes=len(relocation), actual_relocation_sha256=relocation_hash,
                  units=facts, ordinary_eh_tails_passed=len(tails), inferred_eh_tails=inferred,
                  play_seconds=verdict['steps']['play_secs'],
                  cells=[verdict['steps']['extended'][key] for key in ('cell_before_save', 'cell_after_coc', 'cell_after_load')],
                  harness_tag=run['harness']['tag'], frozen_files=freeze['watched_files'],
                  recorded_build_environment=environment,
                  controls_actual_hashes=[sha(Path(control['exe']['path'])) for control in controls],
                  object_archival_attribution=archival['attribution'],
                  object_archival_manifest_sha256=sha(late / 'manifest.json'),
                  initialized_data_bytes=1602654, new_raw_coverage_bytes=0)
    (evidence / 'root-acceptance-review.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('status', 'ordinary_eh_tails_passed', 'play_seconds', 'cells')}))


if __name__ == '__main__':
    main()
