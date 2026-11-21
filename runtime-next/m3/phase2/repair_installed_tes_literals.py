"""Derive production compiler literal-label bindings without altering code/oracle.

prepare reads the frozen full-build unit object; apply is a hash-guarded recipe
generator action for the coordinator's released build lane. Historical private
fixture evidence is preserved. No address is taken from the failing image.
"""
import argparse
import copy
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import tescontainer_experiment as pilot
import tescontainer_install as transaction
from rtti_hkp_viewer_compare import relocated
from compare import Coff, Pe, compare
import paths

PROJECT = pilot.PROJECT
OUT = pilot.M3 / 'out/phase2-tescontainer-production-labels'
INSTALL = transaction.OUT


def prepare():
    units_path = pilot.FN / 'build/units.json'
    for index, target in enumerate([pilot.FN / pilot.SOURCE, pilot.FN / 'include/TESContainer.h', units_path]):
        if target.read_bytes() != (INSTALL / ('%d.generated' % index)).read_bytes():
            raise ValueError('installed source/header/recipe differs from reviewed transaction')
    before = json.loads((INSTALL / '2.original').read_bytes())['units'][980]
    current = json.loads(units_path.read_bytes())['units'][980]
    if len(before['functions']) != 31 or len(current['functions']) != 31:
        raise ValueError('unexpected function scope')
    OUT.mkdir(parents=False, exist_ok=False)
    original_path = pilot.OUT / '0980.original.obj'
    production_path = PROJECT / 'runtime-next/pinned-build/obj_v3/0980.obj'
    shutil.copy2(original_path, OUT / '0980.original.obj')
    shutil.copy2(production_path, OUT / '0980.production.obj')
    original = Coff(OUT / '0980.original.obj')
    production = Coff(OUT / '0980.production.obj')
    facts = []
    normal = {pilot.NEW: pilot.OLD}
    labels = {}
    for old, new in zip(before['functions'], current['functions']):
        a, ar = relocated(original, old['symbol'], old['size'], {})
        b, br = relocated(production, new['symbol'], new['size'], normal)
        if a != b or len(ar) != len(br):
            raise ValueError('production code bytes/relocation counts changed')
        for x, y in zip(ar, br):
            if x == y:
                continue
            if (x[0], x[1], x[3]) != (y[0], y[1], y[3]) or not all(re.fullmatch(r'\$SG\d+', z[2]) for z in (x, y)):
                raise ValueError('difference exceeds compiler literal-label identity')
            pools = []
            for coff, name in [(original, x[2]), (production, y[2])]:
                symbol = coff.named(name)
                section = coff.sections[symbol['section']]
                if section['name'] != '.rdata' or section['relocs']:
                    raise ValueError('literal pool section must be nonrelocated rdata')
                pools.append((symbol['value'], section['data']))
            if pools[0] != pools[1] or not pools[0][1] or x[2] not in before['symbols']:
                raise ValueError('literal pool/symbol offset/source binding changed')
            if y[2] in labels and labels[y[2]] != x[2]:
                raise ValueError('ambiguous production label')
            labels[y[2]] = x[2]
            facts.append(dict(function_address=old['address'], field_offset=x[0], old_label=x[2], production_label=y[2],
                              source_bound_va=before['symbols'][x[2]], pool_symbol_offset=pools[0][0],
                              pool_size=len(pools[0][1]), pool_sha256=hashlib.sha256(pools[0][1]).hexdigest()))
    if len(facts) != 4 or len(labels) != 4:
        raise ValueError('requires exactly four independently paired literal labels')
    corrected = copy.deepcopy(current)
    private = json.loads((pilot.OUT / 'literal-remap.json').read_bytes())['normalization']
    old_to_production = {old: name for name, old in labels.items()}
    symbols = {}
    changes = []
    for name, value in corrected['symbols'].items():
        original_name = private.get(name, name)
        new = old_to_production.get(original_name, name) if name in private else name
        if new in symbols and symbols[new] != value:
            raise ValueError('production literal binding collision')
        symbols[new] = value
        if new != name:
            changes.append(dict(before=name, after=new, value=value))
    if len(changes) != 4:
        raise ValueError('recipe correction must change exactly four keys')
    corrected['symbols'] = symbols
    normal.update(labels)
    checks = []
    for old, new in zip(before['functions'], corrected['functions']):
        a, ar = relocated(original, old['symbol'], old['size'], {})
        b, br = relocated(production, new['symbol'], new['size'], normal)
        checks.append(dict(address=old['address'], bytes_equal=a == b, normalized_relocations_equal=ar == br))
    reference = compare(production, Pe(paths.REF_IMAGE), corrected)
    if len(checks) != 31 or not all(x['bytes_equal'] and x['normalized_relocations_equal'] for x in checks) or len(reference) != 31 or any(x['verdict'] != 'match' for x in reference):
        raise ValueError('all 31 production code/relocation/reference checks must pass')
    generated = transaction.replace_unit(units_path.read_bytes(), 980, corrected)
    (OUT / 'units.original').write_bytes(units_path.read_bytes())
    (OUT / 'units.generated').write_bytes(generated)
    with (OUT / 'manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(unit_index=980, old_units_sha256=pilot.digest(units_path), new_units_sha256=hashlib.sha256(generated).hexdigest(),
                       original_object_sha256=pilot.digest(OUT / '0980.original.obj'), production_object_sha256=pilot.digest(OUT / '0980.production.obj'),
                       source_sha256=pilot.digest(pilot.FN / pilot.SOURCE), header_sha256=pilot.digest(pilot.FN / 'include/TESContainer.h'),
                       literal_facts=facts, recipe_key_changes=changes, checks=checks,
                       reference_matches=31, scope='Only four compiler-local literal keys change; source addresses, code bytes, compiler flags and original matching gates remain unchanged.'), stream, indent=2)
    print(json.dumps(dict(functions=31, reference_matches=31, literal_key_changes=4, generated_units_sha256=hashlib.sha256(generated).hexdigest())))


def apply(restore=False):
    if (PROJECT / 'runtime-next/build.lock').exists():
        raise ValueError('source recipe correction requires released build lane')
    meta = json.loads((OUT / 'manifest.json').read_bytes())
    target = pilot.FN / 'build/units.json'
    expected = meta['new_units_sha256'] if restore else meta['old_units_sha256']
    payload = OUT / ('units.original' if restore else 'units.generated')
    desired = meta['old_units_sha256'] if restore else meta['new_units_sha256']
    if pilot.digest(target) != expected or pilot.digest(payload) != desired:
        raise ValueError('recipe or generated payload changed')
    if pilot.digest(pilot.FN / pilot.SOURCE) != meta['source_sha256'] or pilot.digest(pilot.FN / 'include/TESContainer.h') != meta['header_sha256']:
        raise ValueError('production source or header changed')
    marker = OUT / ('restored.json' if restore else 'applied.json')
    if marker.exists():
        raise FileExistsError('recipe correction action already recorded')
    previous = target.read_bytes()
    marker_owned = False
    try:
        transaction.atomic_write(target, payload.read_bytes())
        with marker.open('x', encoding='utf-8') as stream:
            marker_owned = True
            json.dump(dict(units_sha256=pilot.digest(target), manifest_sha256=pilot.digest(OUT / 'manifest.json')), stream, indent=2)
    except BaseException:
        transaction.atomic_write(target, previous)
        if marker_owned and marker.exists():
            marker.unlink()
        raise
    print(json.dumps(dict(units_sha256=pilot.digest(target), action='restored fixture recipe' if restore else 'applied production literal labels')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'apply', 'restore'])
    {'prepare': prepare, 'apply': apply, 'restore': lambda: apply(True)}[parser.parse_args().action]()
