"""Fixed whole-RAW DATA projection; every address remains an undefined demand.

No CODE payload, source provider choice, bridge, compiler, link or execution.
"""
from __future__ import annotations
import bisect
import gzip
import hashlib
import json
from pathlib import Path
import struct
import tempfile

from coff_rewrite import strict_object
from data_plan import Pe

POLICY='whole-raw-address-demands-v1'
FRAGMENT='374b2034599e26fb66895c38ed20cdebd079783c94fde6c9ba470cacb54e88b4'
START,SIZE,COUNT=0x1183000,255676,13869
DATA_ROLE='original-nonexec-storage-address-v1'
CODE_ROLE='original-executable-address-v1'
FALSE=dict(runtime_eligible=False,provider_selected=False,materialization_approved=False,link_ready=False,game_fixups_approved=0)


def require(ok,message):
    if not ok:raise ValueError(message)


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk:=stream.read(1048576):h.update(chunk)
    return h.hexdigest()


def stable(bindings):require(bindings and all(sha(p)==h for p,h in bindings.items()),'protected input changed')


def coordinate(policy):
    return digest({k:policy[k] for k in ('owned_sha256','reference_sha256','nonexec_identity_sha256','recipes_sha256')})


def demand_identity(space,target,role):
    require(isinstance(space,str) and len(space)==64 and all(c in '0123456789abcdef' for c in space) and
        type(target) is int and 0<=target<=0xffffffff and role in (DATA_ROLE,CODE_ROLE),'invalid exact address identity')
    identity=dict(version=1,address_space=space,original_target='0x%08x'%target,representation='absolute32',role=role)
    return '_fnv_address_v1_'+digest(identity),identity


def policy_contract(p):
    require(p.get('schema_version')==1 and p.get('policy_id')==POLICY and p.get('fields')==COUNT,'unsupported whole fragment policy')
    require(all(p.get(k)==v for k,v in FALSE.items()),'runtime/provider approval forbidden')
    f=p['fragment'];require((f['fragment_id'],f['start'],f['size'],f['flags'],f['alignment'])==
        (FRAGMENT,START,SIZE,0xc0000040,4096),'fixed raw fragment geometry differs')
    require(p['roles']==sorted((CODE_ROLE,DATA_ROLE)) and p['identity_bridges']==[] and p['target_provider_definitions']==[] and
        p['default_action']=='verify-only' and p['private_projection_requires_exact_review'] is True,'role/bridge/provider action unsupported')
    require(p['protected_source_intervals']==[dict(start=0x101de30,size=8),dict(start=0x1051680,size=8)],'selected source exclusions differ')
    for key in ('owned_sha256','reference_sha256','nonexec_identity_sha256','recipes_sha256','legacy_field_sequence_sha256'):
        require(isinstance(p.get(key),str) and len(p[key])==64,'missing input identity')
    require(set(p['input_pins'])=={'candidate_fields','owner_details','data_plan','data_details','binding_details','address_evidence'},'metadata pin set differs')
    require(set(p.get('implementation_pins',{}))=={'tools/rebuild/coff_rewrite.py','tools/rebuild/coff_inventory.py','tools/rebuild/data_plan.py'} and
        all(isinstance(h,str) and len(h)==64 for h in p['implementation_pins'].values()),'implementation pins incomplete')


class Domains:
    def __init__(self,rows):
        self.rows=sorted(rows,key=lambda r:(r['start'],r['end']));self.starts=[];self.ends=[];end=-1
        for r in self.rows:
            require(0<=r['start']<r['end']<=0x100000000,'invalid domain extent')
            self.starts.append(r['start']);end=max(end,r['end']);self.ends.append(end)
    def overlap(self,lo,hi):
        i=bisect.bisect_left(self.starts,hi)-1;result=[]
        while i>=0 and self.ends[i]>lo:
            r=self.rows[i]
            if r['start']<hi and lo<r['end']:result.append(r)
            i-=1
        return result


def classify_target(target,sections,domains,protected):
    hits=[s for s in sections if s['start']<=target<s['end']]
    require(len(hits)==1,'unmapped/ambiguous target section')
    s=hits[0];claims=domains.overlap(target,target+1)
    require(not any(p['start']<=target<p['start']+p['size'] for p in protected),'selected source owner target excluded')
    if s['executable']:
        require(s['name']=='.text' and not claims,'unsupported executable/metadata domain')
        return CODE_ROLE,dict(section=s['name'],backing='source-built provider required; no code bytes read',
            ownership_selected=False,callable_ABI_approved=False,claims=[])
    require(s['name'] in ('.rdata','.data','CONST') and s['flags'] & 0x40000000 and not s['flags'] & 0x20000020,
        'unsupported nonexec/resource/TLS target')
    # All claims must be unselected source alternatives. Known special state is
    # never flattened into a generic DATA role or silently copied.
    for r in claims:
        require(r['family']=='SOURCE_PROJECTION_CANDIDATE' and r.get('provider_selected') is False and
            r.get('materialization_approved') is False,'special/selected/conflicting target domain')
    return DATA_ROLE,dict(section=s['name'],backing='raw' if target<s['raw_end'] else 'virtual-zero',
        ownership_selected=False,source_owner_alternatives=claims,object_extent=None,object_type=None)


def assess_fields(original_rows,sections,domain_rows,space,protected,source_start,source_size):
    """Pure metadata core. Unknown site/target/domain blocks the entire plan."""
    domains=Domains(domain_rows);require(not domains.overlap(source_start,source_start+source_size),'source span intersects reserved/source-owned storage')
    result=[];seen=set();sites=[];target_roles={};image_base=None
    for row in original_rows:
        values=row['original_record'];require(isinstance(values,list) and len(values)==7,'malformed original field')
        site=int(row['original_site_va'],16);target=int(row['original_target_va'],16)
        require(row['site_identity']==digest(values) and values[4]==4 and values[5]=='raw' and
            source_start<=site<=source_start+source_size-4 and 0<=target<=0xffffffff,'field identity/width/raw bounds differ')
        base=site-values[0]
        require(0<=base<=0xffffffff and (image_base is None or image_base==base) and target==base+values[1],
            'original site/target coordinate identity differs')
        image_base=base
        require(row['original_symbol_base_identity'] is None and row['original_symbol_addend'] is None,
            'unreviewed source-base/addend bridge')
        require(site not in seen,'duplicate source field');seen.add(site);sites.append((site,site+4))
        role,evidence=classify_target(target,sections,domains,protected)
        require(target not in target_roles or target_roles[target]==role,'same address incompatible roles');target_roles[target]=role
        symbol,identity=demand_identity(space,target,role)
        result.append(dict(field_id=row['site_identity'],site=site,offset=site-source_start,original_target=target,
            symbol=symbol,identity=identity,addend=0,source_symbol_base=None,representation='DIR32',
            target_evidence=evidence,original_ledger_record=row,provider_obligations_unresolved=True,**FALSE))
    sites.sort();require(all(a[1]<=b[0] for a,b in zip(sites,sites[1:])),'overlapping HIGHLOW fields')
    return sorted(result,key=lambda r:r['offset'])


def metadata(paths,policy,root):
    """Only exact saved inputs; never consume the 1GB observation."""
    policy_contract(policy);root=Path(root).resolve();require(set(paths)==set(policy['input_pins']),'exact metadata paths required')
    paths={n:Path(p).resolve() for n,p in paths.items()};require(len(set(paths.values()))==len(paths),'metadata input alias')
    bindings={str(paths[n]):h for n,h in policy['input_pins'].items()};stable(bindings)
    saved=json.loads(paths['candidate_fields'].read_text());candidates=[r for r in saved['candidates'] if r['fragment']['fragment_id']==FRAGMENT]
    require(len(candidates)==1,'large source fragment missing/duplicate');candidate=candidates[0];fragment=candidate['fragment']
    require(all(fragment[k]==policy['fragment'][k] for k in ('start','size','flags','alignment')) and
        fragment['admitted'] is True and fragment['backing']=='raw' and fragment['original_domain']['families']==['ORDINARY_UNCLASSIFIED'] and
        fragment['original_domain']['overlap'] is False,'reserved/changed source fragment')
    legacy=candidate['fields'];require(len(legacy)==COUNT and hashlib.sha256(b''.join(canonical(r)+b'\n' for r in legacy)).hexdigest()==
        policy['legacy_field_sequence_sha256'],'complete legacy field sequence differs')
    by_site={r['site']:r for r in legacy};require(len(by_site)==COUNT,'duplicate legacy field')
    owner=[];domains=[];source_domains=[];geometry=[];ordinal_records={}
    with gzip.open(paths['owner_details'],'rt',encoding='utf-8') as stream:
        for ordinal,line in enumerate(stream,1):
            require(ordinal<=1000000 and len(line)<=16*1024*1024,'owner stream resource bound')
            r=json.loads(line)
            if r['event']=='STORAGE_DOMAIN_EVIDENCE':domains.append(r)
            elif r['event']=='ARENA_GEOMETRY':geometry.append(r)
            elif r['event']=='DISJOINT_ARENA_DOMAIN' and r['domain_id']==fragment['original_domain']['domain_id']:source_domains.append((ordinal,r))
            elif r['event']=='DATA_HIGHLOW_FIELD':
                site=int(r['original_site_va'],16)
                if START<=site<START+SIZE:
                    require(site in by_site and by_site[site]['original']['original']['record']==r and
                        by_site[site]['original']['original']['ordinal']==ordinal,'source ledger original/ordinal join differs')
                    owner.append(r);ordinal_records[r['site_identity']]=ordinal
    require(len(owner)==COUNT and len(source_domains)==1 and source_domains[0][0]==policy['fragment']['domain_ordinal'],
        'complete source domain/field closure differs')
    require(next(r for r in geometry if r['section']=='.data')==policy['fragment']['arena_geometry'],'source arena geometry changed')
    dp=json.loads(paths['data_plan'].read_text());require(dp['image']['base']==0x400000 and dp['provenance']['nonexec_digest']==policy['nonexec_identity_sha256'] and
        dp['recipe_sha256']==policy['recipes_sha256'] and dp['detail_sha256']==policy['input_pins']['data_details'],'data plan/image/recipe join differs')
    expected={r['site_identity']:r for r in owner};seen=set()
    with gzip.open(paths['data_details'],'rt',encoding='utf-8') as stream:
        for number,line in enumerate(stream,1):
            require(number<=1000000 and len(line)<=65536,'v4 stream bound')
            values=json.loads(line);site=dp['image']['base']+values[0]
            if START<=site<START+SIZE:
                key=digest(values);require(key in expected and values==expected[key]['original_record'] and key not in seen and
                    int(expected[key]['original_target_va'],16)==dp['image']['base']+values[1], 'v4 exact field closure differs')
                seen.add(key)
    require(seen==set(expected),'missing v4 field')
    stable(bindings);return owner,domains,ordinal_records,bindings


def coff_bytes(payload,fields,anchor,alignment=4096):
    """DATA records only; field values are zero before any COFF publication."""
    require(len(payload)>0 and alignment in [1<<i for i in range(14)] and len(fields)<65535,'unsupported DATA geometry')
    normalized=bytearray(payload);names=sorted({r['symbol'] for r in fields});symbols=[(anchor,0,1,2),('@feat.00',1,-1,3)]+[(n,0,0,2) for n in names]
    name_index={n:i+2 for i,n in enumerate(names)};seen=[];relocations=bytearray()
    for r in fields:
        off=r['offset'];require(0<=off<=len(payload)-4 and r['addend']==0 and
            demand_identity(r['identity']['address_space'],r['original_target'],r['identity']['role'])==(r['symbol'],r['identity']), 'wrong demand/addend/bounds')
        require(struct.unpack_from('<I',payload,off)[0]==r['original_target'],'original field word differs')
        seen.append((off,off+4));struct.pack_into('<I',normalized,off,0);relocations+=struct.pack('<IIH',off,name_index[r['symbol']],6)
    seen.sort();require(all(a[1]<=b[0] for a,b in zip(seen,seen[1:])),'overlapping serialized fields')
    strings=bytearray(bytes(4));symbol_bytes=bytearray()
    for name,value,section,storage in symbols:
        require(name.startswith('_fnv_') or name=='@feat.00','foreign symbol')
        enc=name.encode('ascii');raw=struct.pack('<II',0,len(strings)) if len(enc)>8 else enc.ljust(8,b'\0')
        if len(enc)>8:strings+=enc+b'\0'
        symbol_bytes+=struct.pack('<8sIhHBB',raw,value,section,0,storage,0)
    struct.pack_into('<I',strings,0,len(strings));relptr=60+len(payload);symptr=relptr+len(relocations)
    flags=0xc0000040|(alignment.bit_length()<<20)
    section=struct.pack('<8sIIIIIIHHI',b'.data',0,0,len(payload),60,relptr if fields else 0,0,len(fields),0,flags)
    return struct.pack('<HHIIIHH',0x14c,1,0,symptr,len(symbols),0,0)+section+normalized+relocations+symbol_bytes+strings


def validate_object(path,payload,fields,anchor,alignment=4096):
    coff,_,_,_=strict_object(path);require(len(coff.sections)==1 and not coff.directives,'extra section/directive')
    sec=coff.sections[1];require((sec['name'],sec['size'],sec['flags'])==('.data',len(payload),0xc0000040|(alignment.bit_length()<<20)),
        'DATA geometry/protection changed')
    expected={anchor:(1,0,2),'@feat.00':(-1,1,3)};expected.update({r['symbol']:(0,0,2) for r in fields})
    require(len(coff.symbols)==len(expected) and {r['name']:(r['section'],r['value'],r['storage']) for r in coff.symbols.values()}==expected and
        all(r['aux_count']==0 and r['type']==0 for r in coff.symbols.values()),'extra/defined/typed demand symbol')
    raw=struct.unpack_from('<I',coff.data,40)[0];require(raw>0,'initialized storage lost');data=bytearray(coff.data[raw:raw+len(payload)])
    actual=[];physical=[]
    for off,index,kind in sec['relocs']:
        require(kind==6 and 0<=off<=len(data)-4 and coff.symbols[index]['section']==0,'unsupported relocation/target')
        actual.append((off,coff.symbols[index]['name'],struct.unpack_from('<I',data,off)[0]))
        physical.append(dict(section=1,offset=off,kind=6,serialized_symbol_index=index,symbol=coff.symbols[index]['name'],addend=struct.unpack_from('<I',data,off)[0]))
    require(sorted(actual)==sorted((r['offset'],r['symbol'],0) for r in fields),'full field/symbol/zero-addend bijection differs')
    for r in fields:struct.pack_into('<I',data,r['offset'],r['original_target'])
    require(bytes(data)==payload,'non-field bytes changed')
    return dict(object_sha256=sha(path),payload_sha256=hashlib.sha256(payload).hexdigest(),initialized_bytes=len(payload),
        fields=len(fields),undefined_demands=len(expected)-2,code_sections=0,physical_field_map=physical,
        undefined_symbols=[dict(symbol=s['name'],serialized_index=s['index']) for s in coff.symbols.values() if s['section']==0],**FALSE)


def project(paths,policy_path,owned,reference,root,review_path,out):
    """Separate exact source review/root go is required before actual reads."""
    policy_path,review_path,out=[Path(p).resolve() for p in (policy_path,review_path,out)];p=json.loads(policy_path.read_text());policy_contract(p)
    review=json.loads(review_path.read_text());rh=sha(review_path)
    require(review.get('kind')=='whole-raw-address-projection-review' and review.get('phase')=='private-whole-fragment-projection' and
        review.get('approved') is True and review.get('root_authorized') is True and review.get('reviewer') and
        review.get('source_sha256')==sha(__file__) and review.get('policy_sha256')==sha(policy_path),'source/root projection gate absent/stale')
    rows,domain_rows,ordinals,bindings=metadata(paths,p,root)
    require(sha(owned)==p['owned_sha256'] and sha(reference)==p['reference_sha256'],'owned/reference identity changed')
    for path,h in [(policy_path,sha(policy_path)),(review_path,rh),(Path(__file__),review['source_sha256']),
                   (Path(owned).resolve(),p['owned_sha256']),(Path(reference).resolve(),p['reference_sha256'])]:bindings[str(path)]=h
    for relative,h in p['implementation_pins'].items():
        path=(Path(root)/relative).resolve();require(path.is_relative_to(Path(root).resolve()),'implementation path escapes root');bindings[str(path)]=h
    stable(bindings);require(not out.exists() and all(out!=Path(k) and out not in Path(k).parents for k in bindings),'output/input collision')
    pe,ref=Pe(owned),Pe(reference)
    try:
        require(pe.base==ref.base==0x400000 and pe.section_headers==ref.section_headers,'input PE geometry differs')
        sec=pe.section(START-pe.base,SIZE,required=True);require(sec['name']=='.data' and sec['flags']==0xc0000040 and not sec['executable'] and
            START-pe.base-sec['rva']+SIZE<=sec['raw_size'],'fixed whole RAW source extent differs')
        a=p['fragment']['arena_geometry'];require(pe.base+sec['rva']==a['original_start'] and sec['extent']==a['logical_extent'] and
            min(sec['raw_size'],sec['extent'])==a['raw_backed_extent'],'original arena geometry changed')
        sections=[dict(name=s['name'],start=pe.base+s['rva'],end=pe.base+s['rva']+s['extent'],raw_end=pe.base+s['rva']+min(s['extent'],s['raw_size']),
            executable=s['executable'],flags=s['flags']) for s in pe.sections]
        fields=assess_fields(rows,sections,domain_rows,coordinate(p),p['protected_source_intervals'],START,SIZE)
        require(len(fields)==COUNT,'incomplete positive field classification')
        actual=[]
        for site in pe.relocations():
            if START<site+pe.base+4 and site+pe.base<START+SIZE:
                require(START<=site+pe.base<=START+SIZE-4,'crossing original HIGHLOW');actual.append(site+pe.base)
        require(sorted(actual)==[r['site'] for r in fields],'actual PE HIGHLOW closure differs')
        payload=pe.read_rva(START-pe.base,SIZE);other=ref.read_rva(START-ref.base,SIZE)
        require(payload==other,'owned/reference raw payload differs')
    finally:pe.close();ref.close()
    anchor='_fnv_address_arena_v1_'+digest(dict(space=coordinate(p),fragment=FRAGMENT));stable(bindings)
    with tempfile.TemporaryDirectory(prefix='fnv_data_address_') as tmp:
        obj=Path(tmp)/'whole-data.obj';obj.write_bytes(coff_bytes(payload,fields,anchor));proof=validate_object(obj,payload,fields,anchor)
        stable(bindings);out.mkdir();created=[]
        try:
            dest=out/'whole-data.obj'
            with dest.open('xb') as stream:created.append(dest);stream.write(obj.read_bytes())
            require(sha(dest)==proof['object_sha256'],'published DATA object differs')
            report=dict(schema_version=1,kind='private-whole-raw-address-projection',policy_sha256=sha(policy_path),review_sha256=rh,
                fragment=p['fragment'],coordinate_space=coordinate(p),anchor=anchor,proof=proof,protected_inputs=bindings,
                fields=fields,source_ledger_ordinals=ordinals,unresolved_provider_bridge_applied=False,**FALSE)
            stable(bindings);receipt=out/'projection.json'
            with receipt.open('x') as stream:created.append(receipt);json.dump(report,stream,separators=(',',':'));stream.write('\n')
            stable(bindings);return report
        except Exception:
            for path in created:path.unlink()
            out.rmdir();raise
