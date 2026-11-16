"""Positive compiler-local LABEL bookkeeping proof; no symbol rebinding."""
import hashlib
import re
from import_plan import require
from literal_symbol_migration import uses
from runtime_bind_plan import section_payload


def source_span(raw,address):
    marker=('// @fnv '+address+'\r\n').encode()
    require(raw.count(marker) == 1,'local-label source owner ambiguous')
    start=raw.index(marker);end=raw.find(b'// @fnv ',start+len(marker))
    return raw[start:len(raw) if end<0 else end]


def prove(before,after,recipe,original_source,generated_source,pe,highlows,allowed):
    olduses,newuses=uses(before),uses(after);witnesses=[]
    for spec in allowed:
        oldname,newname=spec['old_name'],spec['new_name']
        pattern=r'\$'+re.escape(spec['source_label'])+r'\$[0-9]+\Z'
        require(re.fullmatch(pattern,oldname) and re.fullmatch(pattern,newname) and oldname != newname,'unknown label spelling/stem')
        old=[s for s in before.symbols.values() if s['name'] == oldname]
        new=[s for s in after.symbols.values() if s['name'] == newname]
        require(len(old) == len(new) == 1,'local label absent/duplicated');old,new=old[0],new[0]
        require(all(s['storage'] == 6 and s['type'] == 0 and s['aux_count'] == 0 and s['section'] > 0 for s in (old,new)),'not a compiler-local LABEL')
        require({k:v for k,v in old.items() if k not in ('name','index')} ==
                {k:v for k,v in new.items() if k not in ('name','index')},'local label physical placement differs')
        functions=[f for f in recipe['functions'] if f['address'] == spec['function_address'] and f['symbol'] == spec['function_symbol']]
        require(len(functions) == 1 and functions[0]['size'] == spec['function_size'],'local-label parent recipe differs');function=functions[0]
        parents=[]
        for coff,symbol in ((before,old),(after,new)):
            found=[s for s in coff.symbols.values() if s['name'] == function['symbol'] and s['section'] > 0]
            require(len(found) == 1,'local-label native parent ambiguous');parent=found[0]
            require(parent['section'] == symbol['section'] and parent['value'] <= symbol['value'] < parent['value']+function['size'],'label outside exact parent')
            parents.append(parent)
        require({k:v for k,v in parents[0].items() if k != 'index'} ==
                {k:v for k,v in parents[1].items() if k != 'index'},'local-label parent native identity differs')
        oldsection=before.sections[old['section']];newsection=after.sections[new['section']]
        require({k:v for k,v in oldsection.items() if k != 'relocs'} ==
                {k:v for k,v in newsection.items() if k != 'relocs'} and
                section_payload(before,old['section']) == section_payload(after,new['section']),'local-label parent section bytes/metadata differ')
        old_parent={k:v for k,v in olduses.items() if k[0] == old['section']}
        new_parent={k:v for k,v in newuses.items() if k[0] == new['section']}
        require(old_parent.keys() == new_parent.keys(),'other parent relocation geometry differs')
        facts=[]
        for key,a in sorted(old_parent.items()):
            b=new_parent[key]
            record=lambda r:{k:v for k,v in r.items() if k not in ('symbol_index','symbol')}
            target=lambda s:{k:s[k] for k in ('name','section','value','type','storage','aux_count')}
            at,bt=target(a['symbol']),target(b['symbol'])
            if bt['name'] == newname:bt['name']=oldname
            require(record(a['record']) == record(b['record']) and at == bt and
                    a['symbol'].get('weak') == b['symbol'].get('weak'),'other parent relocation identity differs')
            facts.append(dict(field=key,record=record(a['record']),target=at))
        original=source_span(original_source,function['address']);generated=source_span(generated_source,function['address'])
        require(original == generated and hashlib.sha256(original).hexdigest() == spec['source_span_sha256'],'local-label source body differs')
        require(len(re.findall(rb'(?m)^\s*'+spec['source_label'].encode()+rb'\s*:',original)) == 1,'source label absent/ambiguous')
        oldkeys={k for k,v in olduses.items() if v['symbol']['index'] == old['index']}
        newkeys={k for k,v in newuses.items() if v['symbol']['index'] == new['index']}
        require(oldkeys == newkeys and len(oldkeys) == spec['physical_use_count'],'local-label complete physical uses differ')
        fields=[];parent=parents[0]
        for key in sorted(oldkeys):
            a,b=olduses[key]['record'],newuses[key]['record']
            require(key[0] == parent['section'] and parent['value'] <= key[1] <= parent['value']+function['size']-4,
                    'local-label use outside exact parent span')
            require(a['kind'] == b['kind'] == 6 and a['width'] == b['width'] == 4 and a['addend'] == b['addend'] == 0,'local-label field kind/addend differs')
            offset=key[1]-parent['value'];require(offset in spec['field_offsets'],'unexpected local-label field context')
            fieldva=int(function['address'],16)+offset;target=int(function['address'],16)+old['value']-parent['value']
            require(fieldva in highlows and int.from_bytes(pe.read_rva(fieldva-pe.base,4,allow_code=True),'little') == target,'original local-label HIGHLOW/interior target differs')
            fields.append(dict(physical_section=key[0],physical_offset=key[1],function_offset=offset,
                original_field_va='0x%08x'%fieldva,original_interior_target_va='0x%08x'%target,
                old_relocation=a,new_relocation=b))
        require({f['function_offset'] for f in fields} == set(spec['field_offsets']),'local-label field coverage differs')
        witnesses.append(dict(old_name=oldname,new_name=newname,source_label=spec['source_label'],old_symbol=old,new_symbol=new,
            parent_function=function,old_native_parent=parents[0],new_native_parent=parents[1],source_span_sha256=spec['source_span_sha256'],
            parent_section_sha256=oldsection['payload_sha256'],complete_physical_uses=fields,
            complete_parent_relocation_count=len(facts),all_other_parent_relocation_facts_equal=True,
            function_source_and_code_bytes_unchanged=True,complete_bijective_field_provenance=True,
            namespace_effect='compiler-local bookkeeping only; not an external provider or resolver alias',provider_selected=False))
    return dict(kind='fnv-proven-compiler-local-label-names',witnesses=witnesses,
                resolver_recipe_unchanged=True,provider_selected=False,runtime_eligible=False)
