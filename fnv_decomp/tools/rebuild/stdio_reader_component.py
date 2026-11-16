"""Project and prepare one actual source-built 39-byte Game read component.

Separate reviewed projection/native stages. There is intentionally no execute API.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gzip
import hashlib
import json
import os
from pathlib import Path
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'runtime/components/stdio_reader_consumer.cpp'
OWNED = ('tools/rebuild/stdio_reader_component.py','tests/rebuild/test_stdio_reader_component.py',
         'runtime/components/stdio_reader_consumer.cpp','docs/rebuild/STDIO-READER-COMPONENT.md')
DEPENDENCIES = tuple('tools/rebuild/'+n+'.py' for n in (
    'coff_code_archive','root_code_closure','scalableordinary_root_collect','runtime_code_inventory',
    'runtime_code_pool','runtime_gaps','data_plan','import_plan','coff_inventory','coff_rewrite',
    'bulk_code_pool','application_entry_projection','crt_bootstrap_contract','crt_provider','toolchain','verify_objects')) + (
    'tools/compare.py','tools/build_and_match.py','tools/function_spans.py','build/image_check.json',
    'tests/rebuild/test_coff_code_archive.py')
PINS = {
    'summary':('fread-ordinary-root-observation-v1.json','231a3cd6cc858264dc8d873072519cf5c5b6d551a98f99d935854df3a8e48068'),
    'details':('fread-ordinary-root-observation-v1.jsonl.gz','cd06640c539276bc6216364453fd086529b66c194fc51a2073643e63d3866738'),
    'request':('fread-ordinary-root-request-v1.json','1bddbf8b18461c3383106b3a9d164e9b088625d30955ee27a37a0a91dd67e91e'),
    'crt_plan':('entry-crt-link-plan-native-v1.json','99e16d2120d7b8249136fde98a78fb2c08f1c268f8cb4d424ab33216dad57082'),
    'doctor':('doctor-all.json','9b24d10209fe0361a5e6b16b11a072e8e0ebc6505cd4b5e1bd782fe23854f29f'),
}
CERTIFICATE = '01a1c3c9161a9a035301ce040251937f48d3ebfb74f34f0dee92ab2402f7a7b2'
RECORD = '57a23a85e203c7ce2cfaf71581ad5f951b3a14aebe6eab75260337180e2ac282'
ADDRESS='0x00d2bcd0'
METHOD='?ReadOrMarkFailed@FUN_00d2bcd0_class@@QAEXPAXI@Z'
EXPORT='_fnv_code_fe18a9a2e35afac66f8df026e1f1b1838be5716b5742b6a1e85b68238119089b'
FREAD='_fnv_undefined_0c4e496a4a88850bf6d891c83171901bbbf2c62066442d845d0fb5bdd4787b0c'
INPUT=b'FNV source-owned reader input.\n'
CHECKS=('actual_source_leaf_only','exact_thiscall_receiver','normal_stream_ownership',
        'normal_fread_functional_contract','complete_certificate_and_omissions',
        'no_game_body_or_original_bytes_in_consumer','separate_stage_gates','private_outputs')
FALSE=dict(runtime_eligible=False,provider_selected=False,ABI_verified=False,
           whole_game_FILE_family_approved=False,execution_performed=False)


def require(ok,message):
    if not ok:raise ValueError(message)


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block)
    return h.hexdigest()


def source_manifest():return {n:sha(ROOT/n)for n in OWNED+DEPENDENCIES}


def bound(path,expected,observed):
    path=Path(path).resolve();require(sha(path)==expected,'input hash differs: '+path.name)
    observed[path]=expected;return json.loads(path.read_text(encoding='utf-8'))


def stable(observed):
    for p,h in observed.items():require(sha(p)==h,'protected input changed: '+p.name)
    require(not(ROOT/'build/function_index.json').exists(),'optional function index appeared')


def private_directory(path):
    private=ROOT/'build/rebuild';out=Path(path).resolve()
    require(private.resolve()==private and out.is_relative_to(private) and out!=private and not out.exists(),
            'new private directory under ignored build/rebuild required')
    return out


def save(path,value):
    with Path(path).open('x',encoding='utf-8')as f:
        json.dump(value,f,sort_keys=True,separators=(',',':'));f.write('\n');f.flush();os.fsync(f.fileno())


def publish_receipt(out,name,result,observed):
    path=out/name
    save(path,result)
    try:stable(observed)
    except BaseException as error:
        path.unlink() # Only this attempt's newly created receipt is removed.
        save(out/'failure.json',dict(status='failed-after-publication',error_type=type(error).__name__))
        raise


def review_gate(path,expected,action,observed):
    review=bound(path,expected,observed)
    require(review.get('schema_version')==1 and review.get('kind')=='stdio-reader-component-source-review'
        and review.get('status')=='approved' and review.get('reviewer')
        and review.get('sources')==source_manifest() and review.get('allow_execute')is False
        and review.get('allow_'+action)is True and all(review.get('checks',{}).get(k)is True for k in CHECKS),
        'missing/stale component source review')
    for name,h in review['sources'].items():observed[ROOT/name]=h
    return review


def pure_projection(raw,certificate):
    """Namespace only root8/reference9; frozen writer keeps certified sets exactly."""
    import coff_code_archive as coff
    require(digest(certificate)==CERTIFICATE,'wrong exact bare certificate')
    require(certificate['closure_observed']is True and certificate['root_closure_candidate']is True
        and certificate['graph_observation_complete']is True and not certificate['blockers']
        and certificate['namespace_approved']is False and certificate['full_serialization_eligible']is False,
        'certificate scope/approval differs')
    require(certificate['provenance']['object_sha256']==hashlib.sha256(raw).hexdigest(),'original object differs')
    require(certificate['retained_section_indices']==[1,3]
        and certificate['retained_primary_indices']==[0,1,2,6,8,9]
        and certificate['retained_runtime_section_indices']==[3]
        and not certificate['omitted_definition_conversions'],'unexpected retained scope')
    obj=coff.parse(raw);root=obj['symbols'][8];ref=obj['symbols'][9]
    require((root['name'],root['section'],root['value'])==(METHOD,3,0)
        and(ref['name'],ref['section'],ref['value'],ref['storage'],ref['aux_count'])==('_fread',0,0,2,0),
        'physical source root/reference differs')
    require(len(obj['sections'][3]['payload'])==39 and obj['sections'][3]['relocs']==[(20,9,20)]
        and obj['sections'][3]['payload'][20:24]==bytes(4),'39-byte leaf field differs')
    named=coff.namespace(raw,[(8,EXPORT),(9,FREAD)])
    output,mapping=coff.serialize(named,[1,3],[0,1,2,6,8,9])
    after=coff.parse(output)
    require(coff.exports(output)==[EXPORT] and
        [s['name']for s in after['symbols'].values()if s['storage']==2 and s['section']==0]==[FREAD],
        'extra game export or unresolved obligation')
    return output,dict(mapping=mapping,original_object_sha256=hashlib.sha256(raw).hexdigest(),
        member_sha256=hashlib.sha256(output).hexdigest(),namespace_plan=[dict(physical_index=i,
            name=EXPORT if i==8 else FREAD if i==9 else obj['symbols'][i]['name'])for i in [0,1,2,6,8,9]],
        canonical_export=EXPORT,canonical_fread=FREAD,certificate_sha256=CERTIFICATE,
        retained_sections=[1,3],code_bytes=39,fields=[dict(offset=20,kind=20,old_symbol_index=9,
            new_symbol_index=mapping['symbol_map'][9],addend=0)],link_alias_applied=False,**FALSE)


def project(args):
    require(args.allow_projection is True,'projection requires explicit root opt-in')
    observed={};review_gate(args.review,args.review_sha256,'projection',observed)
    out=private_directory(args.out);base=Path(args.metadata_dir).resolve()
    import scalableordinary_root_collect as collector
    import runtime_code_inventory as inventory
    import coff_code_archive as coff
    import root_code_closure as ordinary
    import bulk_code_pool as bulk
    import application_entry_projection as independent
    import compare as oracle
    from build_and_match import image_ok
    for module,relative in ((collector,'tools/rebuild/scalableordinary_root_collect.py'),
        (inventory,'tools/rebuild/runtime_code_inventory.py'),(coff,'tools/rebuild/coff_code_archive.py'),
        (ordinary,'tools/rebuild/root_code_closure.py'),(bulk,'tools/rebuild/bulk_code_pool.py'),
        (independent,'tools/rebuild/application_entry_projection.py'),(oracle,'tools/compare.py')):
        require(Path(module.__file__).resolve()==ROOT/relative,'foreign shared helper module')
    meta={k:bound(base/name,h,observed)for k,(name,h)in PINS.items()if k!='details'}
    candidate=[r for r in meta['crt_plan']['provider_candidates']if(r['original_base'],r['role'])==('0x00ecb3a8','code')]
    require(len(candidate)==1 and candidate[0]['expected_canonical_undefined']==FREAD
        and candidate[0]['proposed_provider']['export']=='_fread'
        and candidate[0]['proposed_provider']['compiler_family']=='sp1'
        and candidate[0]['initial_preparation_site_ordinals']==[384166]
        and meta['crt_plan']['source_owned_file_component']['canonical_code_export']==EXPORT,
        'wrong scoped normal fread functional plan')
    detail=base/PINS['details'][0];require(sha(detail)==PINS['details'][1],'ordinary detail differs');observed[detail]=PINS['details'][1]
    with gzip.open(detail,'rt',encoding='utf-8')as stream:
        rows=[json.loads(line)for line in stream]
    require(len(rows)==1 and digest(rows[0])==RECORD and digest(rows[0]['certificate'])==CERTIFICATE,'exact certificate group differs')
    row=rows[0];certificate=row['certificate'];summary=meta['summary']
    require(summary['details_sha256']==PINS['details'][1] and summary['groups'][0]['record_sha256']==RECORD
        and summary['groups'][0]['certificate_sha256']==CERTIFICATE,'ordinary summary/detail join differs')
    names=dict(selection='function-selection-v2.json',manifest='objects.json',retained='retained-verify-full-v3.json',
        binding='runtime-bind-plan-native-v2.json',owners='runtime-data-owners-native-v1.json',
        imports='import-plan-native-v3.json')
    # EH basename is taken from the caller's explicit exact metadata path.
    require(Path(args.eh_name).name==args.eh_name,'EH report must be an explicit metadata basename')
    names['eh']=args.eh_name
    data={k:bound(base/n,summary['inputs'][k],observed)for k,n in names.items()}
    data['recipes']=bound(ROOT/'build/units.json',summary['inputs']['recipes'],observed)
    inventory.validate_headers(data)
    for relative,h in summary['tools_sha256'].items():
        require((ROOT/relative).is_relative_to(ROOT),'foreign observer dependency')
        require(sha(ROOT/relative)==h,'frozen observation helper differs');observed[ROOT/relative]=h
    for relative,h in data['retained']['inputs']['tools_sha256'].items():
        require(sha(ROOT/relative)==h,'original matching helper differs');observed[ROOT/relative]=h
    require(sha(ROOT/'build/image_check.json')==data['retained']['inputs']['image_check_sha256'],'image gate specification differs')
    require(inventory.reconcile_recipes(data['manifest'],ROOT/'build/units.json')['verified'],'authoritative recipes differ')
    owner_detail=base/'runtime-data-owners-native-v1.jsonl.gz'
    require(sha(owner_detail)==summary['owner_details_sha256'],'owner stream differs');observed[owner_detail]=summary['owner_details_sha256']
    with gzip.open(owner_detail,'rt',encoding='utf-8')as stream:
        providers,_=inventory.owner_providers(stream,data['owners'],data['selection']['selections'])
    groups=collector.validate_request(meta['request'],data['selection']['selections'],data['manifest'],data['retained'],providers)
    require(set(groups)=={1821} and len(groups[1821])==1,'not the one FILE leaf')
    unit=next(u for u in data['manifest']['units']if u['recipe_index']==1821)
    proof=next(u for u in data['retained']['units']if u['recipe_index']==1821)
    binding_detail=base/'runtime-bind-plan-native-v2.jsonl.gz'
    require(sha(binding_detail)==summary['binding_details_sha256'],'binding stream differs');observed[binding_detail]=summary['binding_details_sha256']
    buckets=None
    with gzip.open(binding_detail,'rt',encoding='utf-8')as stream:
        reader=inventory.BindingReader(stream,data['binding']['summary'],data['selection']['selections'])
        for u in data['manifest']['units']:
            bucket=reader.take(u['recipe_index'])
            if u['recipe_index']==1821:buckets=bucket
        reader.finish()
    imported=next(r for r in data['imports']['imports']if r['import_id']==175)
    contract=collector.build_contract(unit,proof,groups[1821],buckets,imported,row['provenance'])
    require(digest(contract)==row['contract_identity_sha256'],'reconstructed exact contract differs')
    object_path=(base/data['manifest'].get('object_root_relative','.')/unit['object']).resolve()
    source=(ROOT/unit['source']).resolve()
    require(source.is_relative_to(ROOT) and sha(source)==unit['source_sha256'] and sha(object_path)==unit['object_sha256'],'original source/object differs')
    observed[source]=unit['source_sha256'];observed[object_path]=unit['object_sha256']
    raw=object_path.read_bytes();require(ordinary.assess_object(coff.parse(raw),contract)==certificate,'fresh ordinary certificate differs')
    image=Path(args.image).resolve();reference=data['retained']['inputs']['image_sha256']
    require(sha(image)==reference,'owned reference differs');observed[image]=reference
    selected=dict(groups[1821][0]);contracts=[dict(selected=selected)]
    output,projection=pure_projection(raw,certificate)
    stable(observed)
    with tempfile.TemporaryDirectory(prefix='fnv_stdio_projection_')as temp:
        selected_path=Path(temp)/'selected.obj';selected_path.write_bytes(output)
        view=dict(namespace_plan=projection['namespace_plan'],primary_bijection=sorted([list(x)for x in projection['mapping']['symbol_map'].items()]),
                  auxiliary_bijection=sorted([list(x)for x in projection['mapping']['auxiliary_map'].items()]))
        independent_report=independent.independent_projection(object_path,selected_path,view,projection)
        bulk.strict_reparse(selected_path,output)
        pe=oracle.Pe(image);passed,hits,probes=image_ok(pe);require(passed,'unchanged image gate failed')
        before=bulk.compare_functions(object_path,pe,contracts,unit['recipe'])
        after=bulk.compare_functions(selected_path,pe,contracts,unit['recipe'],dict(bindings=[(8,EXPORT),(9,FREAD)],comparison_base_view={EXPORT:ADDRESS,FREAD:'0x00ecb3a8'}))
    stable(observed);out.mkdir(parents=True)
    with(out/'selected.obj').open('xb')as stream:stream.write(output)
    result=dict(schema_version=1,kind='stdio-reader-projected',status='pending-independent-projection-review',
        inputs={str(p):h for p,h in observed.items()},sources=source_manifest(),projection=projection,
        original_comparison=before,projected_comparison=after,image_gate=dict(hits=hits,probes=probes),
        independent_projection=independent_report,root_certificate=certificate,selected_sha256=sha(out/'selected.obj'),
        source_review_sha256=args.review_sha256,scoped_provider_contract='normal SP1 fread only in the later bounded link',**FALSE)
    require(sha(out/'selected.obj')==projection['member_sha256'],'published selected object differs')
    observed[out/'selected.obj']=projection['member_sha256']
    stable(observed);publish_receipt(out,'projection.json',result,observed);return result


def projection_review(proof,review):
    require(proof.get('kind')=='stdio-reader-projected' and proof.get('selected_sha256')==proof['projection']['member_sha256']
        and proof.get('sources')==source_manifest() and proof['projection']['certificate_sha256']==CERTIFICATE,
        'stale projected component/source')
    require(review.get('kind')=='stdio-reader-projection-review' and review.get('status')=='approved'
        and review.get('reviewer') and review.get('selected_sha256')==proof['selected_sha256']
        and review.get('allow_native_prepare')is True and review.get('allow_execute')is False
        and all(review.get('checks',{}).get(k)is True for k in ('complete_COFF_bijection','exact_root_certificate',
            'unchanged_reference_comparison','one_unresolved_fread','typed_normal_FILE_consumer','normal_fread_functional_contract')),
        'missing/stale independent projected-object review')


def consumer_shape(raw):
    import coff_code_archive as coff
    obj=coff.parse(raw)
    targets=[i for i,s in obj['symbols'].items()if s['name']==METHOD]
    require(len(targets)==1 and obj['symbols'][targets[0]]['section']==0,'typed member boundary absent or source body supplied')
    fields=[dict(section=s,offset=o,symbol_index=i,kind=k)for s,sec in obj['sections'].items()for o,i,k in sec['relocs']if i==targets[0]]
    require(len(fields)==4 and all(f['kind']==20 for f in fields),'four typed actual leaf calls required')
    require(not any(s['name'].startswith('_fnv_')and s['section']>0 for s in obj['symbols'].values()),'consumer supplies a game provider')
    return fields


def validate_consumer_directives(obj):
    # Same actual Windows SDK header pragma pair as the accepted host sources,
    # without the separate bootstrap observer's forced-include directive.
    actual=[token.replace('"','').upper()for token in obj.directives]
    expected=['/DEFAULTLIB:UUID.LIB','/DEFAULTLIB:UUID.LIB',
              '/DEFAULTLIB:LIBCMT','/DEFAULTLIB:OLDNAMES']
    require(Counter(actual)==Counter(expected),'unexpected component consumer directives')
    return actual


def inspect_link(exe,mapfile,selected,consumer,libraries):
    import crt_bootstrap_contract as native
    import coff_code_archive as coff
    from data_plan import Pe
    from import_plan import parse_imports
    mapping=native.map_symbols(Path(mapfile).read_text());require(EXPORT in mapping and '_fread'in mapping,'linked root/fread missing')
    require('selected.obj' in mapping[EXPORT]['owner'].lower() and 'libcmt:'in mapping['_fread']['owner'].lower(),'wrong Game/normal fread provider')
    aliases={METHOD:EXPORT,FREAD:'_fread'};visible={}
    for alias,target in aliases.items():
        if alias in mapping:
            require(mapping[alias]['address']==mapping[target]['address'],'link-only alias resolves incorrectly');visible[alias]=mapping.pop(alias)
    contributors=native.validate_contributors(mapping,[consumer,selected],libraries)
    for name in ('_mainCRTStartup','_fopen','_fread','_fseek','_ftell','_fclose','_exit','___security_cookie','___security_init_cookie'):
        require(name in mapping and 'libcmt:'in mapping[name]['owner'].lower(),'required normal CRT provider absent: '+name)
    require({n for n,r in mapping.items()if 'selected.obj'in r['owner'].lower()}=={EXPORT},'extra Game map definitions')
    obj=coff.parse(Path(selected).read_bytes());root=next(s for s in obj['symbols'].values()if s['name']==EXPORT)
    payload=obj['sections'][root['section']]['payload'];pe=Pe(exe)
    try:
        at=mapping[EXPORT]['address'];section=pe.section(at-pe.base,39,True)
        require(section['flags']&0x20000000 and section['flags']&0x40000000 and not section['flags']&0x80000000,'Game code protection differs')
        actual=pe.read_rva(at-pe.base,39,allow_code=True)
        require(all(a==b for i,(a,b)in enumerate(zip(payload,actual))if not 20<=i<24),'linked Game nonrelocation payload differs')
        target=(at+24+struct.unpack_from('<i',actual,20)[0])&0xffffffff
        require(target==mapping['_fread']['address'],'actual Game call does not target normal fread function')
        target_section=pe.section(target-pe.base,1,True)
        require(target_section['flags']&0x20000000 and target_section['flags']&0x20
                and not target_section['flags']&0x80000000,'normal fread target is not function code')
        require(not any(at-pe.base-3<=p<at-pe.base+39 for p in pe.relocations()),'unexpected Game HIGHLOW field')
        shape=consumer_shape(Path(consumer).read_bytes());consumer_obj=coff.parse(Path(consumer).read_bytes());calls=[]
        for field in shape:
            secid,offset=field['section'],field['offset'];defs=[s for s in consumer_obj['symbols'].values()if s['section']==secid and s['storage']==2 and s['type']==32 and s['value']<=offset]
            require(defs,'typed consumer call lacks named owner');owner=max(defs,key=lambda s:s['value'])
            require(owner['name']in mapping,'typed consumer owner absent from map')
            place=mapping[owner['name']]['address']+offset-owner['value'];disp=struct.unpack('<i',pe.read_rva(place-pe.base,4,allow_code=True))[0]
            require((place+4+disp)&0xffffffff==at,'typed consumer call does not target retained leaf');calls.append(dict(field_va=place,target_va=at))
        imports=parse_imports(pe)
        require(all(r['dll'].lower()=='kernel32.dll' and r['export']['kind']=='name'for r in imports),'unexpected DLL/ordinal import')
        require(len({(r['dll'].lower(),r['export']['name'])for r in imports})==len(imports),'duplicate imports')
        entry=pe.unpack('<I',pe.unpack('<I',0x3c)[0]+24+16)[0]+pe.base
        require(entry==mapping['_mainCRTStartup']['address'],'entry bypasses normal CRT startup')
        return dict(root_va=at,fread_va=target,Game_code_bytes=39,Game_nonrelocation_bytes_equal=True,
            Game_call_targets_normal_function=True,typed_consumer_calls=calls,normal_CRT_entry=entry,
            link_aliases=aliases,map_visible_aliases=visible,map_contributors=contributors,imports=imports)
    finally:pe.close()


def prepare(args):
    require(args.allow_native_prepare is True,'native prepare requires explicit root opt-in')
    observed={};review_gate(args.review,args.review_sha256,'native_prepare',observed)
    require(os.name=='nt','native Windows required')
    require(not any(os.environ.get(n)for n in ('LINK','_LINK_','LIBPATH')),'implicit linker options rejected')
    proof_path=Path(args.projection).resolve();proof=bound(proof_path,args.projection_sha256,observed)
    approval=bound(args.projection_review,args.projection_review_sha256,observed)
    require(approval.get('projection_sha256')==args.projection_sha256,'wrong projected receipt review')
    projection_review(proof,approval)
    for p,h in proof['inputs'].items():require(sha(p)==h,'projection input drift');observed[Path(p)]=h
    selected=proof_path.parent/'selected.obj';require(sha(selected)==proof['selected_sha256'],'selected component drift');observed[selected]=proof['selected_sha256']
    doctor=bound(Path(args.metadata_dir)/PINS['doctor'][0],PINS['doctor'][1],observed)
    import crt_bootstrap_contract as native
    import toolchain
    from coff_inventory import Coff
    require(Path(native.__file__).resolve()==ROOT/'tools/rebuild/crt_bootstrap_contract.py'
        and Path(toolchain.__file__).resolve()==ROOT/'tools/rebuild/toolchain.py','foreign native metadata helper')
    out=private_directory(args.out);root,sdk=toolchain.layout(doctor['toolchains']['sp1']['root']);tc=doctor['toolchains']['sp1']
    require(tc['ready']and tc['version']==toolchain.VERSIONS['sp1']and sha(root/'VC/bin/cl.exe')==tc['cl_sha256']and sha(root/'VC/bin/link.exe')==tc['link_sha256'],'SP1 compiler/linker differs')
    roots=native.capture_include_roots([root/'VC/include',sdk/'Include',SOURCE.parent])
    for p in (root/'VC/bin/cl.exe',root/'VC/bin/c1xx.dll',root/'VC/bin/c2.dll',root/'VC/bin/link.exe',root/'VC/bin/dumpbin.exe',root/'VC/lib/libcmt.lib',root/'VC/lib/oldnames.lib',sdk/'Lib/kernel32.lib',sdk/'Lib/uuid.lib'):
        observed[p.resolve()]=sha(p)
    require(sha(root/'VC/lib/libcmt.lib')=='bd9700d126d378f31f32736abc0c88cb08a8e0f0914acb6e2c8cbfd1ab99f411','normal SP1 library differs')
    for name in ('kernel32.dll','kernelbase.dll','ntdll.dll'):
        p=Path(os.environ['SystemRoot'])/'SysWOW64'/name;observed[p]=sha(p)
    stable(observed);out.mkdir(parents=True);commands=[];artifacts={};report=dict(schema_version=1,kind='stdio-reader-native-preparation',status='error',commands=commands,**FALSE)
    with(out/'progress.jsonl').open('x',encoding='utf-8')as progress:
        def note(state):progress.write(json.dumps(dict(state=state))+'\n');progress.flush();os.fsync(progress.fileno())
        def check():native.verify_include_roots(roots);stable(observed)
        def run(command,label):
            check();commands.append([str(c)for c in command]);rc,text=toolchain.run(command,root,out,timeout=120)
            p=out/(label+'.log');p.write_text(text,encoding='utf-8');artifacts[str(p)]=sha(p);observed[p]=sha(p);check();require(rc==0,'native preparation failed: '+label);return text
        try:
            note('started');input_path=out/'input.bin'
            with input_path.open('xb')as f:f.write(INPUT)
            artifacts[str(input_path)]=sha(input_path);observed[input_path]=sha(input_path)
            local=out/'selected.obj'
            with local.open('xb')as f:f.write(selected.read_bytes())
            artifacts[str(local)]=sha(local);observed[local]=sha(local);require(sha(local)==proof['selected_sha256'],'component staging differs')
            flags=['/nologo','/MT','/Od','/Oy-','/GS','/EHsc','/Gy','/W4','/showIncludes']
            prefix=[root/'VC/bin/cl.exe']+flags
            syntax=run(prefix+['/Zs',SOURCE],'consumer-syntax');headers=native.includes(syntax,[],roots)
            for p in headers:observed[p]=sha(p)
            consumer=out/'consumer.obj';compile_log=run(prefix+['/c',SOURCE,'/Fo'+str(consumer)],'consumer-compile')
            require(native.includes(compile_log,[],roots)==headers,'compile include set changed')
            consumer_directives=validate_consumer_directives(Coff(consumer));consumer_fields=consumer_shape(consumer.read_bytes());artifacts[str(consumer)]=sha(consumer);observed[consumer]=sha(consumer)
            libraries=native.controlled_libraries(out,root/'VC/lib',sdk/'Lib');exe=out/'stdio_reader.exe';mapping=out/'stdio_reader.map'
            aliases=['/alternatename:'+METHOD+'='+EXPORT,'/alternatename:'+FREAD+'=_fread']
            text=run([root/'VC/bin/link.exe','/nologo','/machine:x86','/subsystem:console','/incremental:no','/opt:ref','/opt:noicf','/safeseh','/VERBOSE:LIB','/out:'+str(exe),'/map:'+str(mapping)]+aliases+[consumer,local],'component-link')
            require(native.controlled_libraries(out,root/'VC/lib',sdk/'Lib')==libraries,'library search changed')
            library_log=native.verify_library_log(text,libraries);linked=inspect_link(exe,mapping,local,consumer,libraries)
            for p in(exe,mapping):artifacts[str(p)]=sha(p);observed[p]=sha(p)
            check();require(all(sha(p)==h for p,h in artifacts.items()),'prepared artifact drift')
            report.update(status='prepared-pending-independent-review',sources=source_manifest(),inputs={str(p):h for p,h in observed.items()},artifacts=artifacts,
                source_review_sha256=args.review_sha256,projection_sha256=args.projection_sha256,projection_review_sha256=args.projection_review_sha256,
                include_root_identities=roots,consumer_fields=consumer_fields,consumer_directives=consumer_directives,linked=linked,library_search_evidence=library_log,
                expected_input_sha256=hashlib.sha256(INPUT).hexdigest(),expected_input_bytes=len(INPUT),
                link_only_normal_fread_binding_verified=True,normal_FILE_creation_and_close_owner='source consumer and one normal SP1 static CRT',
                expected_execution=dict(arguments=[str(input_path)],returncode=0,stdout='{"component":"source_stdio_reader","calls":4,"cases":4,"closed":true}\n',stderr=''),
                execution_gate='Independent source/emission/map/ABI/artifact review and separate root go; this tool cannot execute.')
            note('complete')
        except BaseException as error:
            report['error_type']=type(error).__name__;report['error']=str(error);note('failed')
            save(out/'prepare.json',report);raise
    publish_receipt(out,'prepare.json',report,observed);return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    for action in('project','prepare'):
        p=sub.add_parser(action);p.add_argument('--metadata-dir',type=Path,default=ROOT/'build/rebuild');p.add_argument('--out',type=Path,required=True)
        p.add_argument('--review',type=Path,required=True);p.add_argument('--review-sha256',required=True)
        if action=='project':
            p.add_argument('--allow-projection',action='store_true');p.add_argument('--image',type=Path,required=True)
            p.add_argument('--eh-name',required=True,help='exact existing EH roles report basename')
        else:
            p.add_argument('--allow-native-prepare',action='store_true');p.add_argument('--projection',type=Path,required=True);p.add_argument('--projection-sha256',required=True)
            p.add_argument('--projection-review',type=Path,required=True);p.add_argument('--projection-review-sha256',required=True)
    args=parser.parse_args(argv)
    try:result=project(args)if args.action=='project'else prepare(args)
    except(ValueError,OSError,KeyError,TypeError,struct.error)as e:parser.exit(2,'stdio reader rejected: '+str(e)+'\n')
    print(json.dumps(dict(kind=result['kind'],status=result['status'])));return 0


if __name__=='__main__':raise SystemExit(main())
