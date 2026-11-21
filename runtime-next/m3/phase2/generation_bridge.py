"""Revalidate selector authorization before excluding three heuristic name dwords.

This module is staged privately. Production callers must provide the current
fresh build context, not diagnostic paths or a prior run's proof.
"""
import copy,hashlib,json
from pathlib import Path
from selector_bridge import prepare_selector,finish,sha

def exclude_literals(*,fields,symbol_at,st,SEC,original_sites,read_ref,chunks,m3_claims,object_dir,proof,pieces_path,recipe_path,reference_path,placement_path):
    """Return a new field map and the canonical heuristic rows for later selectors."""
    original=dict(fields)
    rows=[]
    for va,(target,evidence) in sorted(original.items()):
        sections=[(name,s) for name,s in SEC.items() if s['va']<=va<s['va']+s['raw']]
        if len(sections)!=1:raise ValueError('field has no unique raw section')
        name,s=sections[0]
        rows.append([name,va-s['va'],symbol_at(target),0,evidence,'canonical-discovery','function'])
    proven,objects=prepare_selector(st,{'fields':rows},SEC,original_sites,read_ref,chunks,m3_claims,object_dir)
    raw=Path(pieces_path).read_bytes();doc=json.loads(raw)
    expected=finish(proven,objects,doc['pieces'],hashlib.sha256(raw).hexdigest(),recipe_path,reference_path,placement_path)
    if proof!=expected:raise ValueError('selector proof is stale, changed or detached from actual compiler/pieces')
    removed=proof['removed_value_fields']
    if len(removed)!=3 or len(set(removed))!=3:raise ValueError('exact three literal fields required')
    canonical=[];result=dict(original)
    for f in removed:
        if f in original_sites or result.get(f)!=(0x00404040,'value-rule') or read_ref(f,4)!=b'@@@\0':raise ValueError('not an exact unrelocated heuristic name tail')
        matching=[r for r in rows if SEC[r[0]]['va']+r[1]==f]
        if len(matching)!=1:raise ValueError('canonical field ambiguity')
        canonical.append(matching[0]);del result[f]
    if any(result.get(f)!=v for f,v in original.items() if f not in removed):raise ValueError('unapproved field change')
    if any(result.get(f)!=original[f] for f in original_sites if f in original):raise ValueError('original PE relocation changed')
    meta={'schema':1,'proof_sha256':hashlib.sha256(json.dumps(proof,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'canonical_heuristic_rows':canonical,'removed_value_fields':removed,'note':'These three canonical heuristic matches are typed name bytes, not runtime pointers. Restore rows only for conservative selector rejection before current-epoch authorization.'}
    return result,meta

def restore_selector_heuristics(sj,SEC,read_ref,original_sites):
    """Preserve conservative selector behavior after a prior filtered generation.

    The restored entries only add rejection checks. Current typed authorization
    must independently validate COFF/reference/placement before excluding them.
    """
    meta=sj.get('rtti_name_literals')
    if meta is None:return sj
    if not isinstance(meta,dict) or meta.get('schema')!=1:raise ValueError('invalid literal metadata')
    rows=meta.get('canonical_heuristic_rows');fields=meta.get('removed_value_fields')
    if not isinstance(rows,list) or len(rows)!=3 or not isinstance(fields,list) or len(set(fields))!=3:raise ValueError('invalid canonical heuristic metadata')
    actual={SEC[r[0]]['va']+r[1] for r in sj['fields']};restored=[]
    for row in rows:
        if not isinstance(row,list) or len(row)!=7 or row[0]!='.data' or row[2:5]!=['?FUN_00404040@@YAMM@Z',0,'value-rule']:raise ValueError('invalid canonical heuristic row')
        f=SEC[row[0]]['va']+row[1]
        if f not in fields or f in actual or any(f+d in original_sites for d in range(-3,4)) or read_ref(f,4)!=b'@@@\0':raise ValueError('not a canonical unrelocated dword')
        restored.append(row)
    if {SEC[r[0]]['va']+r[1] for r in restored}!=set(fields):raise ValueError('heuristic identity mismatch')
    out=copy.deepcopy(sj);out['fields'].extend(restored);out['fields'].sort(key=lambda r:SEC[r[0]]['va']+r[1]);return out
