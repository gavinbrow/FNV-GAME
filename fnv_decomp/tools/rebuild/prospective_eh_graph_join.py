"""Pure, bounded seven-root join of a future saved singleton graph certificate.

Inputs are already-decoded dictionaries; this module reads no files. Caller pins
are comparison expectations, not evidence of acceptance. Output is observation
only and cannot discharge EH obligations or authorize any projection.
"""
import copy
import hashlib
import json
import re

ROOTS={'0x00c546c0':(1445,'907aac8edb6d761e6222e10a55e028531e07eb48c5b82147440123f9eb585561'),
 '0x00c55200':(2769,'9ca7f847097b668d7c18c8a69ea7106f50c28f4c8d91a12fba56aa9f8260881e'),
 '0x00c5f240':(2770,'1472295d24c9d76827b5e6f7e2c5f941860198bd0a10548714438100571e4152'),
 '0x00c43500':(2770,'1472295d24c9d76827b5e6f7e2c5f941860198bd0a10548714438100571e4152'),
 '0x00c65530':(2779,'23605df56549207f482c5ca4f776627eee73a7dd47190fe542463a25595babb2'),
 '0x00c618f0':(2779,'23605df56549207f482c5ca4f776627eee73a7dd47190fe542463a25595babb2'),
 '0x00c616c0':(2779,'23605df56549207f482c5ca4f776627eee73a7dd47190fe542463a25595babb2')}
FALSE=dict(runtime_eligible=False,provider_selected=False,ABI_verified=False,frame_execution_verified=False,projection_authorized=False,full_closure_verified=False)
class JoinError(ValueError): pass
def require(v,msg):
    if not v: raise JoinError(msg)
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def sha(v): return type(v) is str and re.fullmatch('[0-9a-f]{64}',v) is not None
def integer(v,lo,hi): return type(v) is int and lo<=v<=hi
def typed_equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(typed_equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def join_saved_singleton(record,root_address,*,expected_record_sha256,expected_certificate_sha256):
    """Join one unmodified singleton. Hash expectations do not authenticate review."""
    try: return _join(record,root_address,expected_record_sha256,expected_certificate_sha256)
    except (KeyError,TypeError,IndexError,AttributeError) as e: raise JoinError('malformed graph record') from e

def _join(record,address,record_sha,cert_sha):
    require(address in ROOTS and sha(record_sha) and sha(cert_sha),'root/hash input')
    require(digest(record)==record_sha,'stale record')
    require(record['kind']=='fresh-root-observation-from-qualified-contract' and record['event']=='SINGLE_ROOT_OBSERVATION' and record['native_parse_performed'] is True and record['fresh_certificate_created'] is True,'not a fresh singleton')
    recipe,obj=ROOTS[address];roots=record['requested_roots'];require(type(roots) is list and len(roots)==1,'exact singleton')
    root=roots[0];require(root['original_address']==address and type(record['recipe_index']) is int and record['recipe_index']==recipe and root['recipe_index']==recipe and record['native_object_sha256']==obj and root['object_sha256']==obj,'root/object identity')
    require(integer(root['symbol_index'],0,0xffffffff) and integer(root['section'],1,0x7fff) and type(root['value']) is int and root['value']==0 and type(root['size']) is int and root['size']==157,'root physical span')
    cert=record['certificate'];require(digest(cert)==cert_sha==record['certificate_sha256'],'stale certificate')
    require(cert['provenance']['object_sha256']==obj and len(cert['roots'])==1 and typed_equal(cert['roots'][0],{k:root[k] for k in ('original_address','symbol','symbol_index','section','value','size')}),'certificate root/object')
    contract=record['contract'];native={k:root[k] for k in ('original_address','symbol','symbol_index','section','value','size')}
    require(cert['contract_identity_sha256']==record['contract_identity_sha256']==digest(contract),'contract identity')
    require(type(root['recipe_id']) is str and root['recipe_id'] and record['recipe_id']==root['recipe_id']==cert['recipe_id']==contract['recipe_id'] and typed_equal(contract['roots'],[native]) and contract['provenance']['object_sha256']==obj,'contract root/recipe/object')
    sub=cert['omission_subcertificate'];scope=sub['scope']
    require(digest(scope)==sub['scope_sha256'] and scope['object_sha256']==obj and scope['contract_identity_sha256']==record['contract_identity_sha256'] and scope['edges_sha256']==digest(cert['edges']),'graph scope binding')
    require(sub['disposition_sha256']==digest(dict(sections=cert['sections'],symbols=cert['symbols'])),'physical inventory binding')
    sections=cert['sections'];symbols=cert['symbols'];edges=cert['edges'];safe=cert['safeseh']
    require(all(type(x) is list for x in (sections,symbols,edges,safe)),'physical inventories')
    require(all(integer(x['index'],1,0x7fff) for x in sections) and len({x['index'] for x in sections})==len(sections),'section identity')
    require(all(integer(x['index'],0,0xffffffff) and integer(x['section'],-2,0x7fff) and integer(x['value'],0,0xffffffff) and integer(x['type'],0,0xffff) and integer(x['storage'],0,0xff) and integer(x['aux_count'],0,0xff) for x in symbols) and len({x['index'] for x in symbols})==len(symbols),'symbol identity')
    sm={x['index']:x for x in sections};ym={x['index']:x for x in symbols};parent=root['section'];idx=root['symbol_index']
    require(parent in sm and idx in ym,'missing physical parent')
    sym=ym[idx];require(sym['section']==parent and sym['value']==0 and sym['name']==root['symbol'] and sym['type']==32 and sym['storage']==2 and sym['aux_count']==0 and type(sm[parent]['extent']) is int and sm[parent]['extent']==157,'parent symbol mismatch')
    # Association edges are candidates only. No transitive or sibling borrowing.
    assoc=[]
    for e in edges:
        if e.get('kind')=='ASSOCIATION_CHILD':
            require(integer(e['source'],1,0x7fff) and integer(e['target'],1,0x7fff),'association physical types')
            if e['source']==parent:assoc.append(e)
    children=[]
    for e in assoc:
        child=e['target'];require(integer(child,1,0x7fff) and child in sm and child!=parent and child not in children,'invalid direct association');children.append(child)
    scopes={parent,*children};physical=[]
    for e in edges:
        if e.get('kind')!='PHYSICAL_SECTION_RELOCATION':continue
        src=e['source'];sn=src['section'];require(integer(sn,1,0x7fff),'relocation section type')
        if sn not in scopes:continue
        ti=e['target'];require(integer(ti,0,0xffffffff) and ti in ym and integer(src['offset'],0,0xffffffff) and integer(src['kind'],0,0xffff),'invalid physical edge')
        physical.append(dict(edge=copy.deepcopy(e),target=copy.deepcopy(ym[ti])))
    # Whole table is reported by physical index, without treating omissions as proved.
    safe_join=[]
    for entry in safe:
        ti=entry['symbol_index'];require(integer(ti,0,0xffffffff) and ti in ym and integer(entry['target_section'],1,0x7fff) and integer(entry['target_value'],0,0xffffffff) and entry['target_section']==ym[ti]['section'] and entry['target_value']==ym[ti]['value'],'SafeSEH index join')
        safe_join.append(dict(entry=copy.deepcopy(entry),target=copy.deepcopy(ym[ti])))
    return dict(kind='prospective-eh-seven-saved-graph-join-v1',root_address=address,recipe_index=recipe,object_sha256=obj,
      record_sha256=record_sha,certificate_sha256=cert_sha,hash_expectations_are_not_review_authority=True,
      recipe_id_and_physical_descriptor_authenticity_require_external_review=True,
      parent=copy.deepcopy(root),direct_association_candidates=[copy.deepcopy(sm[i]) for i in children],physical_relocation_candidates=physical,
      reported_safeseh_entries=safe_join,graph_blockers=copy.deepcopy(cert['blockers']),
      missing=['14_METADATA_HIGHLOW_AND_RAW_OPERANDS','OWN_HANDLER_COOKIE_CLEANUP_SEMANTICS','FRAME_NO_CATCH','HISTORICAL_AND_CURRENT_SOURCE_LINEAGE','EXPANDED_OMISSION_AND_NAMESPACE_PROOF'],
      discharged=[],real_evidence_replay_performed=False,**FALSE)
