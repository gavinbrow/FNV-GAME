"""Record the accepted native-source range partition from audited archives."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile

H = Path(__file__).resolve().parent
O = H.parent / 'out'
TARGET = H / 'accepted_range_partition.json'
BACKUP = H / 'accepted_range_partition.before-native-source.json'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_bytes())


def main():
    if BACKUP.exists():
        raise FileExistsError(BACKUP)
    if sha(TARGET) != 'e1422da7c8e0cb54283043e681b9e7d712a5c3d45bd0b8c2e9151c38dcd7abcc':
        raise ValueError('prior accepted partition changed')
    cpath = O / 'phase2-native-source-positive/evidence/candidate-disjoint-partition.json'
    if sha(cpath) != '7f5de3f5e1bf5207466e6fc4a7b316c627e1a9fc926ff7410095773f987e4141':
        raise ValueError('independent candidate partition changed')
    acceptance_path = O / 'phase2-native-source-acceptance.json'
    acceptance = load(acceptance_path)
    if (acceptance['status'] != 'PASS complete native-source positive/two-controls/repeat suite'
            or acceptance['recipe_sha256'] != '825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
            or acceptance['initialized_data_bytes'] != 1613018):
        raise ValueError('complete source suite not accepted')
    previous, candidate = load(TARGET), load(cpath)
    for name, digest in candidate['inputs'].items():
        if name == 'accepted_partition_sha256' and digest != sha(TARGET):
            raise ValueError('candidate partition lineage changed')
    positive = O / 'phase2-native-source-positive/evidence'
    repeat = O / 'phase2-native-source-repeat/evidence'
    for name, key in (('dv1_pieces.json', 'new_dv1_sha256'), ('m3_manifest.json', 'new_m3_sha256')):
        if sha(positive / name) != candidate['inputs'][key] or sha(repeat / name) != candidate['inputs'][key]:
            raise ValueError('accepted archive range input changed')
    if candidate['candidate']['total'] != 1613018 or candidate['candidate']['tls_excluded'] != 5 or candidate['remaining']['total'] != 366374:
        raise ValueError('partition totals changed')
    result = copy.deepcopy(previous)
    result['accepted'] = candidate['candidate']
    result['remaining'] = candidate['remaining']
    for key, count in candidate['delta_from_accepted_by_prior_bucket'].items():
        result['delta_since_batch8'][key] += count
    result['input_sha256'].update({'old_partition': sha(TARGET), 'new_dv1': sha(repeat / 'dv1_pieces.json'),
                                   'new_m3': sha(repeat / 'm3_manifest.json'), 'acceptance': sha(acceptance_path),
                                   'candidate_partition': sha(cpath)})
    result['accepted_run'] = 'phase2-native-source-repeat'
    result['accepted_recipe_sha256'] = acceptance['recipe_sha256']
    result['note'] = ('Computed disjoint archived M3/DV1 range partition. Native-source batch adds eight BGSBodyPart '
                      'vtable bytes from produced/unspliced; M3 union and W tails are unchanged. Five physical TLS '
                      'bytes remain separate. Kind labels such as tls do not identify physical PE sections.')
    raw = TARGET.read_bytes()
    with BACKUP.open('xb') as f:
        f.write(raw)
    fd, name = tempfile.mkstemp(prefix='native-partition-', dir=H)
    tmp = Path(name)
    try:
        with os.fdopen(fd, 'w', encoding='utf8') as f:
            json.dump(result, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, TARGET)
    finally:
        tmp.unlink(missing_ok=True)
    print(json.dumps({'covered': result['accepted']['total'], 'remaining': result['remaining'], 'sha256': sha(TARGET)}))


if __name__ == '__main__':
    main()
