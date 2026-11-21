"""Stage a private NiMem kind/API composition and its exact retest scope."""
import hashlib, json
from pathlib import Path
import baseformcomponent_core_stage as core

M = Path(__file__).resolve().parent.parent
F = M.parent.parent / 'fnv_decomp'
OUT = M / 'out'
K = OUT / 'phase2-nimemobject-coherent-kind'
A = OUT / 'phase2-nimem-operators-825d'
T = OUT / 'phase2-source-integration6757-transaction-v2'
DEST = OUT / 'phase2-nimem-combined-825d'
BASE = '825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
OLD = '6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
PINS = {
    K / 'manifest.json': '5e4610cd17372885861964b9e25238925b5d69f8c0f2287065107fee7ac445d6',
    OUT / 'phase2-nimemobject-coherent-kind-consumers.json': 'c45dad435c9c172c149afa1fb4054ae5844f59299e1a1dcb6ffaa1e3ca2bc67f',
    A / 'manifest.json': '7689a05cc64e094a726f8d8261378e4cdcbad790f7b05a73295a4439d01da4bf',
    T / 'manifest.json': '9422dd1642f66ddca78a1b161b040cdb55847afd3ad447fbf66e86a6ed47e9da',
}
def digest(data): return hashlib.sha256(data).hexdigest()
def read(path): return json.loads(path.read_bytes())
def main():
    if DEST.exists(): raise FileExistsError('preserve previous combined evidence')
    for path, expected in PINS.items():
        if digest(path.read_bytes()) != expected: raise ValueError('changed pinned input: ' + str(path))
    raw = (F / 'build/units.json').read_bytes()
    oldraw = (T / '0.original').read_bytes()
    if digest(raw) != BASE or digest(oldraw) != OLD or raw != (T / '0.candidate').read_bytes():
        raise ValueError('unreviewed recipe transition')
    old, current = json.loads(oldraw), json.loads(raw)
    if [i for i,(a,b) in enumerate(zip(old['units'],current['units'])) if a != b] != [253,370,425,620,2909]:
        raise ValueError('unexpected unit transition')
    tx = read(T / 'manifest.json')
    touched = {x['path']: x for x in tx['files'] if x['path'] != 'build/units.json'}
    for rel, x in touched.items():
        if digest((F / rel).read_bytes()) != x['new_sha256']: raise ValueError('changed transition file ' + rel)
    kind, api = read(K / 'manifest.json'), read(A / 'manifest.json')
    scope = read(OUT / 'phase2-nimemobject-coherent-kind-consumers.json')
    review_path = OUT / 'phase2-nimem-kind-root-section-review.json'
    review = read(review_path)
    reviews = {r['unit']:r for r in review['units']}
    if len(reviews) != 750 or any(not r['normalized_nondebug_sections_equal'] or not r['comdat_selection_and_weak_lookup_equal'] for r in reviews.values()):
        raise ValueError('archived pair evidence incomplete')
    kind_overrides = {}
    for item in kind['files']:
        rel = item['path']; data = (K / item['generated']).read_bytes()
        if digest((F / rel).read_bytes()) != item['before_sha256'] or digest(data) != item['after_sha256']:
            raise ValueError('kind preimage/payload differs ' + rel)
        kind_overrides[rel] = data
    if len(kind_overrides) != 27: raise ValueError('kind scope changed')
    combined = dict(kind_overrides)
    for rel, h in api['source_payload_sha256'].items():
        data = (A / 'payload' / rel).read_bytes()
        if digest(data) != h: raise ValueError('API payload changed ' + rel)
        if rel == 'include/NiMemObject.h':
            if data.count(b'class NiMemObject\r\n') != 1: raise ValueError('header composition ambiguous')
            data = data.replace(b'class NiMemObject\r\n', b'struct NiMemObject\r\n')
        combined[rel] = data
    if len(combined) != 29: raise ValueError('combined source scope changed')
    candidate_recipe = (A / 'units.generated').read_bytes()
    if digest(candidate_recipe) != api['candidate_recipe_sha256']: raise ValueError('API recipe changed')
    api_rows = []
    for row in api['units']:
        i = row['unit']; u = current['units'][i]
        original = core.walk(F, u['source'], {})
        if original != row['original'] or u['functions'] != row['functions'] or u.get('eh_tails',[]) != row['eh_tails'] or u['flags'] != row['flags'] or u['compiler'] != row['compiler']:
            raise ValueError('API baseline drift for unit %d' % i)
        candidate = core.walk(F, u['source'], combined)
        api_rows.append(dict(unit=i, source=u['source'], compiler=u['compiler'], flags=u['flags'], functions=u['functions'], eh_tails=u.get('eh_tails',[]), original=original, candidate=candidate))
    if len(api_rows) != 128: raise ValueError('API cohort changed')
    unchanged, overlap, fresh = [], [], []
    api_ids = {r['unit'] for r in api_rows}
    for row in scope['units']:
        i = row['unit']; u = current['units'][i]; original = core.walk(F,u['source'],{})
        previous = row['quoted_project_closure']; now = original['files']
        changes = sorted(k for k in set(now) | set(previous) if now.get(k) != previous.get(k))
        recipe_changed = old['units'][i] != u
        if changes or recipe_changed:
            if any(k in now and k in previous and k not in touched for k in changes): raise ValueError('unreviewed changed preexisting input unit %d' % i)
            if not any(k in touched for k in changes): raise ValueError('closure transition lacks reviewed source cause unit %d' % i)
            fresh.append(dict(unit=i, source=u['source'], compiler=u['compiler'], flags=u['flags'], functions=u['functions'], eh_tails=u.get('eh_tails',[]), original=original, candidate=core.walk(F,u['source'],kind_overrides), closure_changes=changes, recipe_changed=recipe_changed))
        else:
            (overlap if i in api_ids else unchanged).append(dict(unit=i, archived_comparison_sha256=reviews[i]['comparison_sha256']))
    if [x['unit'] for x in fresh] != [253,370,621,2909,2910] or len(unchanged)!=618 or len(overlap)!=127:
        raise ValueError('unexpected kind recheck scope')
    if set(x['unit'] for x in fresh) & set(x['unit'] for x in api_rows): raise ValueError('cohort overlap changed')
    DEST.mkdir()
    (DEST / 'units.original').write_bytes(raw); (DEST / 'units.generated').write_bytes(candidate_recipe)
    for rel,data in combined.items():
        path=DEST/'payload'/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    result = dict(base_recipe_sha256=BASE,old_recipe_sha256=OLD,candidate_recipe_sha256=digest(candidate_recipe), input_sha256={str(p.relative_to(OUT)):digest(p.read_bytes()) for p in PINS}, archived_section_review_sha256=digest(review_path.read_bytes()), source_payload_sha256={p:digest(b) for p,b in combined.items()}, combined_api_units=api_rows, fresh_kind_only_units=fresh, unchanged_kind_only_units=unchanged, api_kind_overlap_prior_evidence=overlap, limitations=['private source proposal only; no compilation or live changes', 'lexical closure is not compiler include-trace proof', '618 reused unit pairs establish section equivalence only, not clean reference EH or global ODR', '128 combined pairs and five separate kind-only pairs require fresh compiled proof', 'legacy operator symbol resolution and full image/runtime gates remain open'])
    (DEST/'manifest.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(api_units=len(api_rows), fresh_kind_only=[r['unit'] for r in fresh], unchanged_kind_units=len(unchanged), files=len(combined), manifest_sha256=digest((DEST/'manifest.json').read_bytes()))))
if __name__ == '__main__': main()
