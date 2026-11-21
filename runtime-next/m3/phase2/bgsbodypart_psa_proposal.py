"""Prepare a private, uncompiled two-unit PSA identity experiment."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
M3 = HERE.parent
ROOT = M3.parent.parent
FN = ROOT / 'fnv_decomp'
OUT = M3 / 'out/phase2-bgsbodypart-psa-proposal'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    paths = {
        '620.cpp': FN / 'src/fallout_shared/bgsbodypart.cpp',
        '620.h': FN / 'src/fallout_shared/bgsbodypart_decls.h',
        '621.cpp': FN / 'src/fallout_shared/bgsbodypartdata.cpp',
        '621.h': FN / 'src/fallout_shared/bgsbodypartdata.h',
        'units': FN / 'build/units.json',
    }
    data = {name: path.read_bytes() for name, path in paths.items()}
    units = json.loads(data['units'])['units']
    for index, source, count in ((620, 'src/fallout_shared/bgsbodypart.cpp', 15),
                                  (621, 'src/fallout_shared/bgsbodypartdata.cpp', 10)):
        if units[index]['source'] != source or len(units[index]['functions']) != count:
            raise ValueError('unexpected unit recipe')
    if units[620]['symbols'].get('??0FUN_005e3be0@@QAE@XZ') != '0x005e3be0':
        raise ValueError('surrogate constructor mapping changed')
    header = data['620.h']
    old = (b'class FUN_005e3be0\r\n{\r\n  public:\r\n    unsigned char storage[24];\r\n'
           b'    FUN_005e3be0();\r\n    ~FUN_005e3be0();\r\n};')
    new = (b'class TESModelPSA : public TESModel\r\n{\r\n  public:\r\n'
           b'    TESModelPSA();\r\n    ~TESModelPSA();\r\n};')
    member = b'    FUN_005e3be0 m_kRagdollModel;'
    if header.count(old) != 1 or header.count(member) != 1:
        raise ValueError('unexpected surrogate declaration')
    candidate = header.replace(old, new, 1).replace(member, b'    TESModelPSA m_kRagdollModel;', 1)
    OUT.mkdir(exist_ok=False)
    for directory, source, header_name, contents in (
        ('620', 'bgsbodypart.cpp', 'bgsbodypart_decls.h', candidate),
        ('621', 'bgsbodypartdata.cpp', 'bgsbodypartdata.h', data['621.h']),
    ):
        dest = OUT / directory
        dest.mkdir()
        (dest / source).write_bytes(data[directory + '.cpp'])
        (dest / header_name).write_bytes(contents)
    manifest = {
        'status': 'private hypothesis only; not compiled, no destructor alias approved',
        'input_sha256': {name: digest(value) for name, value in data.items()},
        'candidate_header_sha256': digest(candidate),
        'units': {str(i): {'source': units[i]['source'], 'compiler': units[i]['compiler'],
                           'flags': units[i]['flags'], 'function_count': len(units[i]['functions'])}
                  for i in (620, 621)},
        'candidate_constructor': {'symbol': '??0TESModelPSA@@QAE@XZ', 'address': '0x005e3be0',
                                  'status': 'requires emitted COFF verification'},
        'candidate_destructor': {'symbol': '??1TESModelPSA@@QAE@XZ', 'address': None,
                                 'status': 'unresolved; do not map from same-address aliases'},
        'limitations': ['unit 621 is a byte-identical control, not a canonical header merge',
                        'virtual-slot reconciliation is a separate experiment',
                        'include closure and compiler inputs must be frozen by verification lane'],
    }
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'output': str(OUT), 'candidate_header_sha256': digest(candidate)}))


if __name__ == '__main__':
    main()
