"""Private proposal to replace an exact duplicate with the canonical class header."""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tescontainer_experiment as pilot


def main():
    units_path = pilot.FN / 'build/units.json'
    units_raw = units_path.read_bytes()
    installed = pilot.M3 / 'out/phase2-tescontainer-install-v1'
    if units_raw != (installed / '2.generated').read_bytes():
        raise ValueError('requires exact reviewed recipe transition')
    units = json.loads(units_raw)['units']
    unit = units[981]
    if unit['source'] != 'src/fallout_shared/tescontainer_rtti2_variant.cpp' or len(unit['functions']) != 1:
        raise ValueError('unexpected one-function sibling unit')
    source_path = pilot.FN / unit['source']
    source = source_path.read_text(encoding='utf-8')
    original = (installed / '0.original').read_text(encoding='utf-8')
    pattern = re.compile(r'^class TESContainer : public BaseFormComponent\n\{.*?^\};', re.M | re.S)
    blocks = pattern.findall(source)
    prior = pattern.findall(original)
    if len(blocks) != 1 or len(prior) != 1 or re.sub(r'\s+', '', blocks[0]) != re.sub(r'\s+', '', prior[0]):
        raise ValueError('sibling class declaration differs from reviewed pre-pilot class')
    header = pilot.FN / 'include/TESContainer.h'
    if pilot.digest(header) != json.loads((pilot.OUT / 'manifest.json').read_bytes())['header_sha256']:
        raise ValueError('canonical header changed')
    transformed = source.replace(blocks[0], '#include "TESContainer.h"', 1)
    out = pilot.M3 / 'out/phase2-tescontainer-sibling'
    out.mkdir(parents=False, exist_ok=False)
    with (out / 'tescontainer_rtti2_variant.cpp').open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(transformed)
    with (out / 'manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(unit_index=981, source=unit['source'], source_sha256=pilot.digest(source_path),
                       units_sha256=hashlib.sha256(units_raw).hexdigest(), canonical_header_sha256=pilot.digest(header),
                       overlay_sha256=pilot.digest(out / 'tescontainer_rtti2_variant.cpp'),
                       original_include_closure=pilot.closure(source_path),
                       status='private uncompiled one-function header consolidation; exact literal-label and reference comparison still required; all other class views remain open'), stream, indent=2)
    print(json.dumps(dict(unit_index=981, functions=1, overlay_sha256=pilot.digest(out / 'tescontainer_rtti2_variant.cpp'))))


if __name__ == '__main__':
    main()
