"""Check saved seven-unit source-batch image/data/freeze artifacts, read-only."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

H = Path(__file__).resolve().parent
M = H.parent
R = M.parent.parent
sys.path[:0] = [str(H), str(M / 'tools'), str(R / 'fnv_decomp/tools'), str(R / 'runtime-next')]
import audit_native_methods_acceptance as common
from compare import Pe
from harness_evidence import accepted_verdict
import paths

RECIPE = '825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
CANONICAL = 'c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f'
SEL = 'a0a8e8d2c9818f777f6e07ae18b5cc7d55ff94ca0bd6ccd952ff98ab836d9c3a'
LIB = '74e3815454a8926ee3d8f70abf939e8d61eadd7173a7514c93e66fee92589700'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_bytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', required=True, type=Path)
    a = ap.parse_args()
    run = a.run.resolve()
    if not run.is_relative_to((M / 'out').resolve()):
        raise ValueError('private saved run required')
    e = run / 'evidence'
    output = e / 'root-data-image-freeze-review.json'
    if output.exists():
        raise FileExistsError(output)
    freeze_dir = Path(str(run) + '-freeze')
    summary, freeze, command = (load(p) for p in (run / 'build-summary.json', freeze_dir / 'result.json', freeze_dir / 'command.json'))
    assert summary['status'] == 'ok' and all(x['rc'] == 0 for x in summary['steps'])
    assert freeze['command_rc'] == 0 and freeze['input_freeze_passed']
    assert not freeze['final_digest_changes'] and not freeze['observed_metadata_changes']
    assert command['build_environment'] == {}
    assert sha(e / 'units.json') == RECIPE and sha(e / 'selection.json') == SEL and sha(e / 'library_candidates.json') == LIB
    before = {str(Path(k).resolve()).casefold(): v for k, v in load(freeze_dir / 'inputs-before.json').items()}
    transaction = load(M / 'out/phase2-source-integration6757-transaction-v2/manifest.json')
    for x in transaction['files']:
        assert before[str((R / 'fnv_decomp' / x['path']).resolve()).casefold()]['sha256'] == x['new_sha256']
    preflight = load(Path(str(run) + '-preflight.json'))
    assert len(preflight['required']) == 10 and preflight['recipe_sha256'] == RECIPE
    assert all(before[str(Path(x['path']).resolve()).casefold()]['sha256'] == x['sha256'] for x in preflight['required'])
    source_count = sum('/fnv_decomp/src/' in k.replace('\\', '/') or '/fnv_decomp/include/' in k.replace('\\', '/') for k in before)
    assert len(before) == 12710 and source_count == 5497
    image = run / 'FalloutNV_selfbuilt.exe'
    assert sha(image) == summary['exe']['sha256'] == CANONICAL
    reloc = common.reloc(image)
    assert len(reloc) == 734884 and hashlib.sha256(reloc).hexdigest() == '364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057'
    verdict = load(run / 'harness-verdict.json')
    assert accepted_verdict(summary['harness']['rc'], verdict, summary['exe']['path'], summary['harness']['tag'])
    v = verdict['steps']
    assert v['extended_ok'] and v['extended']['new_save_written'] and v['extended']['cell_changed'] and v['extended']['cell_restored'] and v['exited_cleanly'] and v['exit_code'] == 0
    pe = Pe(paths.REF_IMAGE)
    assert sha(Path(paths.REF_IMAGE)) == 'df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'
    entries = load(e / 'm3_manifest.json')['entries']
    pieces = load(e / 'dv1_pieces.json')['pieces']
    assert len(entries) == 8268 and summary['provenance']['m3']['dropped'] == 0
    libs = [x for x in pieces if x.get('library_opt_in')]
    assert len(libs) == 405 and sum(x['size'] for x in libs) == 16730
    ranges, total, tls = [], 0, 0
    for x in entries + pieces:
        data = bytearray.fromhex(x['ref'] if 'ref' in x else x['data'])
        assert len(data) == x['size'] and len(data) > 0
        sites = set()
        for off, target, addend in x.get('relocs', []):
            assert 0 <= off <= len(data) - 4 and not sites.intersection(range(off, off + 4))
            sites.update(range(off, off + 4))
            struct.pack_into('<I', data, off, target)
        assert data == pe.read(x['va'], len(data))
        ranges.append((x['va'], x['va'] + len(data)))
        if x['section'] in ('.data', '.rdata'):
            total += len(data)
        else:
            assert x['section'] == '.tls'
            tls += len(data)
    ranges.sort()
    assert all(x[1] <= y[0] for x, y in zip(ranges, ranges[1:]))
    assert total == 1613018 and tls == 5
    for filename, digest in summary['provenance']['data_v1_scratch_sha256'].items():
        assert sha(e / 'data-v1-scratch' / filename) == digest
    assert summary['provenance']['weak_coff']['enabled'] is False
    result = {'status': 'PASS positive artifact replay; controls/repeat still required',
              'whole_phase2_complete': False, 'recipe_sha256': RECIPE, 'selection_sha256': SEL,
              'library_sha256': LIB, 'summary_sha256': sha(run / 'build-summary.json'),
              'actual_image_sha256': sha(image), 'relocation_sha256': hashlib.sha256(reloc).hexdigest(),
              'initialized_data_bytes': total, 'tls_bytes_separate': tls, 'frozen_inputs': len(before),
              'source_inputs': source_count, 'required_production_pins': 10,
              'play_seconds': v['play_secs'],
              'limits': ['This is a positive artifact check, not a controls/repeat acceptance gate.',
                         'Ordinary production function/EH and native metadata/ownership audits remain separate.']}
    output.write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps({k: result[k] for k in ('status', 'initialized_data_bytes', 'tls_bytes_separate', 'frozen_inputs')}))


if __name__ == '__main__':
    main()
