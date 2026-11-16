"""Prospective parent-owned EH observations, never eligibility or providers.

Pure inventory/comparison functions. Callers authenticate inputs and authorize reads.
The comparison input contains only explicitly requested parents, not a unit scan.
"""
from __future__ import annotations
import hashlib
import struct
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build_and_match as oracle
import coff_code_archive as coff

FALSE=dict(runtime_eligible=False,provider_selected=False,ABI_verified=False,
           frame_contract_verified=False,no_catch_family_approved=False,
           full_closure_verified=False,emission_performed=False)
def need(ok,why):
    if not ok:raise ValueError(why)
def sha(data):return hashlib.sha256(data).hexdigest()
def aux(obj,sn):
    sec=obj['sections'][sn]
    found=[(i,s) for i,s in obj['symbols'].items() if (s['section'],s['name'],s['storage'],s['type'],s['value'],s['aux_count'])==(sn,sec['name'],3,0,0,1)]
    need(len(found)==1,'missing/ambiguous section definition')
    index,s=found[0];a=struct.unpack('<IHHIhBBH',s['aux'])
    need(a[0]==sec['size'] and a[1]==len(sec['relocs']) and not a[2] and not a[6] and not a[7],'unknown section aux layout')
    return dict(symbol_index=index,length=a[0],relocations=a[1],checksum=a[3],association=a[4],selection=a[5])
def chain(obj,sn):
    seen=set();edges=[]
    while True:
        need(sn in obj['sections'] and sn not in seen,'invalid/cyclic association');seen.add(sn)
        a=aux(obj,sn)
        if a['selection']!=5:return edges,sn
        parent=a['association'];need(parent>0 and parent!=sn,'invalid associative parent');edges.append([sn,parent]);sn=parent
def cuts(obj,sn):
    length=obj['sections'][sn]['size'];points=sorted({0,length}|{s['value'] for s in obj['symbols'].values() if s['section']==sn and 0<s['value']<length})
    return [dict(section=sn,start=a,end=b) for a,b in zip(points,points[1:]) if b>a]
def inventory_parent(obj,root):
    """Report own physical graph, including unknown/catch forms without approval."""
    syms=obj['symbols'];sections=obj['sections'];sn=root['section'];s=syms.get(root['symbol_index'])
    need(s is not None and (s['name'],s['section'],s['value'],s['type'],s['storage'],s['aux_count'])==(root['symbol'],sn,root['value'],32,2,0),'selected physical identity differs')
    need(0<root['size']<=65536 and root['value']+root['size']<=sections[sn]['size'],'parent extent')
    result=dict(root=root,parent_section_aux=aux(obj,sn),parent_section=dict(section=sn,name=sections[sn]['name'],flags=sections[sn]['flags'],extent=sections[sn]['size'],payload_sha256=sha(sections[sn]['payload'])),owned_sections=[],named_roles={},pieces=[],safeseh=[],unsupported=[],**FALSE)
    if not sections[sn]['flags']&0x20000000 or not sections[sn]['flags']&0x20 or len(sections[sn]['payload'])!=sections[sn]['size']:result['unsupported'].append('NATIVE_PARENT_DOMAIN_OR_BACKING')
    if root['value']!=0 or sections[sn]['size']!=root['size']:result['unsupported'].append('PARTIAL_OR_SHARED_PARENT_SECTION')
    for child,sec in sections.items():
        if sec['name'] not in ('.text$x','.xdata$x'):continue
        try:edges,parent=chain(obj,child)
        except ValueError as e:
            result['unsupported'].append('ASSOCIATION_UNRESOLVED:'+str(child)+':'+str(e));continue
        if parent!=sn:continue
        need(sec['size']<=65536,'owned EH extent cap')
        domain=bool(sec['flags']&0x20000000) if sec['name']=='.text$x' else not bool(sec['flags']&0x20000000)
        if not domain or len(sec['payload'])!=sec['size']:result['unsupported'].append('NATIVE_OWNED_DOMAIN_OR_BACKING:'+str(child))
        record=dict(section=child,name=sec['name'],flags=sec['flags'],extent=sec['size'],payload_sha256=sha(sec['payload']),association_chain=edges,section_aux=aux(obj,child),relocations=[dict(offset=o,target=i,kind=k) for o,i,k in sec['relocs']])
        result['owned_sections'].append(record)
        if sec['name']=='.text$x':result['pieces'].extend(cuts(obj,child))
    owned={r['section'] for r in result['owned_sections']}
    for role,prefix in (('handler','__ehhandler$'),('funcinfo','__ehfuncinfo$'),('unwind','__unwindtable$')):
        found=[dict(index=i,**s) for i,s in syms.items() if s['name']==prefix+root['symbol'] and s['section']>0]
        # Exclude auxiliary payloads from public metadata; preserve their identity separately.
        for row in found:row['aux_sha256']=sha(row.pop('aux'))
        result['named_roles'][role]=found
        if len(found)!=1 or found[0]['section'] not in owned:result['unsupported'].append('MISSING_AMBIGUOUS_OR_FOREIGN_'+role.upper())
        elif (found[0]['storage'],found[0]['type'],found[0]['aux_count'])!=(3,32 if role=='handler' else 0,0):result['unsupported'].append('UNKNOWN_'+role.upper()+'_SYMBOL_RECORD')
    handler=result['named_roles']['handler']
    result['parent_to_handler_fields']=[dict(offset=o,target=i,kind=k) for o,i,k in sections[sn]['relocs'] if root['value']<=o<=root['value']+root['size']-4 and handler and i in {r['index'] for r in handler}]
    if handler and not result['parent_to_handler_fields']:result['unsupported'].append('UNANCHORED_HANDLER')
    for sx,sec in sections.items():
        if sec['name']!='.sxdata':continue
        need(not sec['relocs'] and len(sec['payload'])==sec['size'] and sec['size']%4==0 and sec['size']<=16384,'unknown SafeSEH table')
        for offset in range(0,sec['size'],4):
            index=struct.unpack_from('<I',sec['payload'],offset)[0];target=syms.get(index)
            need(target is not None,'SafeSEH auxiliary/missing index')
            result['safeseh'].append(dict(section=sx,offset=offset,symbol_index=index,target_section=target['section'],target_value=target['value'],owned_handler=bool(handler and index in {r['index'] for r in handler})))
    if handler and sum(r['owned_handler'] for r in result['safeseh'])!=1:result['unsupported'].append('MISSING_OR_DUPLICATE_OWN_SAFESEH')
    infos=result['named_roles']['funcinfo'];unwinds=result['named_roles']['unwind']
    result['funcinfo']=None;result['states']=[]
    if len(infos)==len(unwinds)==1 and infos[0]['section'] in owned and infos[0]['section']==unwinds[0]['section']:
        info,unwind=infos[0],unwinds[0];sec=sections[info['section']];at=info['value']
        if 0<=at<=len(sec['payload'])-36:
            values=struct.unpack_from('<9I',sec['payload'],at)
            result['funcinfo']=dict(section=info['section'],offset=at,magic=values[0],max_state=values[1],unwind_addend=values[2],try_count=values[3],try_map_addend=values[4],ip_count=values[5],ip_map_addend=values[6],type_list_addend=values[7],flags=values[8])
            if values[0]!=0x19930522:result['unsupported'].append('UNKNOWN_FUNCINFO_MAGIC')
            elif values[1]>256 or unwind['value']+8*values[1]>len(sec['payload']):result['unsupported'].append('UNKNOWN_UNWIND_EXTENT')
            else:
                for state in range(values[1]):
                    pos=unwind['value']+8*state;to,action=struct.unpack_from('<iI',sec['payload'],pos);refs=[r for r in sec['relocs'] if r[0]==pos+4]
                    targets=[dict(index=i,name=syms[i]['name'],section=syms[i]['section'],value=syms[i]['value'],kind=k) for _,i,k in refs]
                    result['states'].append(dict(state=state,to_state=to,action_addend=action,action_fields=targets))
                    if to < -1 or to>=state:result['unsupported'].append('UNKNOWN_STATE_TRANSITION:'+str(state))
                    if len(refs)>1 or (not refs and action):result['unsupported'].append('UNKNOWN_ACTION_FIELD:'+str(state))
                    if refs and any(t['kind']!=6 or not any(p['section']==t['section'] and p['start']==t['value']+action for p in result['pieces']) for t in targets):result['unsupported'].append('FOREIGN_OR_INTERIOR_ACTION:'+str(state))
                if any(values[i] for i in (3,4,5,6,7)):result['unsupported'].append('CATCH_IP_OR_TYPELIST_FAMILY_REQUIRES_ADAPTER')
                if values[8]!=1:result['unsupported'].append('UNKNOWN_FUNCINFO_FLAGS')
                if values[1]==0:result['unsupported'].append('ZERO_STATE_FAMILY_REQUIRES_REVIEW')
        else:result['unsupported'].append('TRUNCATED_FUNCINFO')
    # Presence of names is not evidence that a section is actually parent-owned.
    result['native_graph_observed']=True
    result['comparison_status']='NOT_RUN'
    return result

class ScopedReference:
    """Allow only parent and native-field-derived owned code/metadata spans."""
    def __init__(self,backend,executable_ranges):
        self.backend=backend;self.base=getattr(backend,'base',0);self.executable_ranges=executable_ranges;self.spans=[];self.reads=[];self.total=0
    def secrel(self,address):return self.backend.secrel(address)
    def allow(self,start,size,kind,basis):
        need(type(start)is int and 0<start<=0xffffffff and 0<size<=65536 and start+size<=0x100000000,'derived scope bounds')
        executable=any(a<=start and start+size<=b for a,b in self.executable_ranges)
        need(executable if kind=='code' else not any(a<start+size and start<b for a,b in self.executable_ranges),'derived scope execution domain')
        self.spans.append(dict(start=start,size=size,kind=kind,basis=basis))
    def read(self,address,size):
        need(type(address)is int and type(size)is int and 0<=size<=65536,'reference read geometry')
        need(any(r['start']<=address and address+size<=r['start']+r['size'] for r in self.spans),'OUTSIDE_SELECTED_DERIVED_SCOPE')
        need(len(self.reads)<8192 and self.total+size<=1024**2,'reference read budget')
        self.total+=size;record=dict(address=address,size=size,completed=False);self.reads.append(record)
        value=self.backend.read(address,size);need(len(value)==size,'short original read');record['completed']=True;return value

def prepare_scope(obj,view,backend,executable_ranges,reference=None):
    root=view['root'];reference=reference or ScopedReference(backend,executable_ranges)
    for sn in [root['section']]+[r['section'] for r in view['owned_sections']]:
        sec=obj['sections'][sn];is_code=sn==root['section'] or sec['name']=='.text$x';need(len(sec['payload'])==sec['size'] and (bool(sec['flags']&0x20000000) if is_code else not bool(sec['flags']&0x20000000)),'native domain/backing unsupported')
    address=int(root['original_address'],16);reference.allow(address,root['size'],'code','explicit selected parent')
    original=reference.read(address,root['size']);sections=obj['sections'];syms=obj['symbols'];code={r['section'] for r in view['owned_sections'] if r['name']=='.text$x'};data={r['section'] for r in view['owned_sections'] if r['name']=='.xdata$x'};bases={};dbases={};cut_origins={}
    for offset,index,kind in sections[root['section']]['relocs']:
        target=syms[index]
        if target['section'] not in code or not root['value']<=offset<=root['value']+root['size']-4:continue
        rel=offset-root['value'];need(kind in (6,20),'unsupported parent EH relocation')
        addend=struct.unpack_from('<i' if kind==20 else '<I',sections[root['section']]['payload'],offset)[0];operand=struct.unpack_from('<i' if kind==20 else '<I',original,rel)[0]
        observed=(address+rel+4+operand if kind==20 else operand)&0xffffffff;base=(observed-addend-target['value'])&0xffffffff
        need(bases.setdefault(target['section'],base)==base,'conflicting own anchor')
        native=target['value']+addend;pieces=[p for p in view['pieces'] if p['section']==target['section'] and p['start']==native];need(len(pieces)==1,'parent target not complete native cut')
        key=(target['section'],native);need(cut_origins.setdefault(key,observed)==observed,'conflicting parent cut');reference.allow(observed,pieces[0]['end']-native,'code','exact parent-targeted native cut')
    need(set(bases)==code,'unanchored owned code section')
    for sn,base in bases.items():
        for offset,index,kind in sections[sn]['relocs']:
            target=syms[index]
            if kind!=6 or target['section'] not in data:continue
            owners=[p for p in view['pieces'] if p['section']==sn and p['start']<=offset<=p['end']-4 and (sn,p['start']) in cut_origins]
            if not owners:continue
            need(len(owners)==1,'metadata anchor field ambiguous cut');owner=owners[0];field_va=cut_origins[(sn,owner['start'])]+offset-owner['start']
            observed=struct.unpack('<I',reference.read(field_va,4))[0];addend=struct.unpack_from('<I',sections[sn]['payload'],offset)[0];at=(observed-target['value']-addend)&0xffffffff
            need(dbases.setdefault(target['section'],at)==at,'conflicting metadata anchors')
    need(set(dbases)==data,'unanchored owned metadata section')
    for sn,base in dbases.items():
        reference.allow(base,sections[sn]['size'],'data','own handler metadata field')
        for offset,index,kind in sections[sn]['relocs']:
            target=syms[index]
            if kind!=6 or target['section'] not in code:continue
            native=target['value']+struct.unpack_from('<I',sections[sn]['payload'],offset)[0];pieces=[p for p in view['pieces'] if p['section']==target['section'] and p['start']==native]
            need(len(pieces)==1,'metadata action not complete native cut');observed=struct.unpack('<I',reference.read(base+offset,4))[0]
            key=(target['section'],native);need(cut_origins.setdefault(key,observed)==observed,'conflicting metadata/parent cut')
            reference.allow(observed,pieces[0]['end']-native,'code','owned metadata action pointer to complete native cut')
    reference.native_cut_origins=cut_origins
    return reference,dbases

def _compare_parent(core,obj,view,recipe,all_recipes,backend,executable_ranges,global_names,reference):
    """Explicitly invoke unchanged core for ONE root, even without eh_tails.

    Inference observations remain labelled; they do not become external providers.
    Caller records exceptions as unsupported/missing, never a successful graph.
    """
    root=view['root'];selected=[f for f in recipe['functions'] if f['symbol']==root['symbol'] and f['address']==root['original_address']]
    need(len(selected)==1,'selected comparison function missing/ambiguous')
    reference,metadata_bases=prepare_scope(obj,view,backend,executable_ranges,reference)
    comparison=dict(recipe,functions=selected)
    ordinary=oracle.compare(core,reference,comparison,None)
    reference.partial_ordinary=[dict(address=r['address'],symbol=r['symbol'],size=r['size'],compiled_extent=r['compiled_extent'],verdict=r['verdict'],errors=r['errors'],relocations=r['relocations'],byte_difference_count=len(r['byte_differences'])) for r in ordinary]
    need(len(ordinary)==1 and ordinary[0]['address']==root['original_address'],'comparison escaped selected parent')
    if global_names is None:global_names=oracle.recipe_names(all_recipes)
    pieces,inferred,errors=oracle.eh_sections(core,reference,comparison,ordinary,global_names)
    need(all(p[3]==root['original_address'] for p in pieces),'EH comparison escaped selected parent')
    native=sorted(view['pieces'],key=lambda p:(p['section'],p['start']));need(len(native)==len(pieces),'MISSING_NATIVE_OR_ORIGINAL_PIECE_ROWS')
    rows=[]
    for n,p in zip(native,pieces):
        need(n['end']-n['start']==p[1]-p[0],'native/original piece extent differs')
        need(reference.native_cut_origins.get((n['section'],n['start']))==p[0],'native/original piece placement identity differs')
        rows.append(dict(native=n,original=p,local_MATCH=p[2],inferred_names=p[4]))
    names=dict(global_names);names.update({k:int(v,0) for k,v in recipe.get('symbols',{}).items()});metadata=[]
    for sn,base in metadata_bases.items():
        sec=obj['sections'][sn];original=reference.read(base,sec['size']);masked=set();fields=[]
        for offset,index,kind in sec['relocs']:
            need(kind in (6,20) and offset+4<=sec['size'],'unsupported metadata field');need(not masked.intersection(range(offset,offset+4)),'overlapping metadata fields');masked.update(range(offset,offset+4))
            target=obj['symbols'][index];addend=struct.unpack_from('<i' if kind==20 else '<I',sec['payload'],offset)[0];operand=struct.unpack_from('<i' if kind==20 else '<I',original,offset)[0];observed=(base+offset+4+operand if kind==20 else operand)&0xffffffff;expected=None
            if target['section'] in metadata_bases:expected=metadata_bases[target['section']]+target['value']+addend
            else:
                effective=target['value']+addend
                owners=[r for r in rows if r['native']['section']==target['section'] and r['native']['start']<=effective<r['native']['end']]
                if len(owners)==1:expected=owners[0]['original'][0]+effective-owners[0]['native']['start']
                elif target['name'] in names:expected=names[target['name']]+addend
            fields.append(dict(offset=offset,symbol_index=index,kind=kind,addend=addend,original_target=observed,expected_target=expected,comparison_MATCH=None if expected is None else (expected&0xffffffff)==observed))
        nonfields=all(a==b for i,(a,b) in enumerate(zip(sec['payload'],original)) if i not in masked)
        metadata.append(dict(section=sn,original_base=base,size=sec['size'],native_sha256=sha(sec['payload']),original_sha256=sha(original),nonrelocation_MATCH=nonfields,fields=fields,all_field_identities_resolved=all(f['comparison_MATCH'] is not None for f in fields),full_MATCH=nonfields and all(f['comparison_MATCH'] is True for f in fields),HIGHLOW_validated=False))
    ordinary_safe=[]
    for r in ordinary:
        saved={k:r[k] for k in ('address','symbol','size','compiled_extent','verdict','errors','relocations','fold_aliases')};saved['byte_difference_count']=len(r['byte_differences']);saved['byte_difference_offsets']=[d['offset'] for d in r['byte_differences']]
        fields=[]
        for offset,index,kind in obj['sections'][root['section']]['relocs']:
            if not root['value']<=offset<=root['value']+root['size']-4:continue
            target=obj['symbols'][index];fields.append(dict(offset=offset,relative_offset=offset-root['value'],symbol_index=index,symbol=target['name'],target_section=target['section'],target_value=target['value'],target_storage=target['storage'],target_type=target['type'],target_aux_count=target['aux_count'],kind=kind))
        saved['native_fields']=fields;ordinary_safe.append(saved)
    return dict(ordinary=ordinary_safe,pieces=rows,errors=errors,inferred_comparison_bindings={k:hex(v) for k,v in inferred.items()},inferred_bindings_are_provider_proof=False,metadata_original_bases=metadata_bases,metadata_comparisons=metadata,reference_scope=reference.spans,reference_reads=reference.reads,comparison_status='OBSERVED_NOT_ELIGIBILITY',**FALSE)

def compare_parent(core,obj,view,recipe,all_recipes,backend,executable_ranges,global_names=None):
    reference=ScopedReference(backend,executable_ranges)
    try:return _compare_parent(core,obj,view,recipe,all_recipes,backend,executable_ranges,global_names,reference)
    except (ValueError,KeyError,struct.error) as error:
        error.scope_snapshot=dict(reference_scope=reference.spans,reference_reads=reference.reads,partial_ordinary=getattr(reference,'partial_ordinary',None))
        raise
