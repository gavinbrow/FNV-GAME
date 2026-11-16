"""Derive alternate-object literal label bindings from complete physical uses."""
import copy
import hashlib
import re
from collections import defaultdict
from import_plan import require
from relocation_audit import relocation_record
from runtime_bind_plan import section_payload

LABEL = re.compile(r'\$SG[0-9]+\Z')


def uses(coff):
    result = {}
    for section in coff.sections.values():
        for reloc in section['relocs']:
            record = relocation_record(coff,section,reloc)
            key = (section['index'],record['offset'],record['kind'])
            require(key not in result,'duplicate physical use')
            result[key] = dict(record=record,symbol=coff.symbols[record['symbol_index']])
    return result


def contexts(coff, recipe, key):
    section,off,kind = key; result=[]
    for function in recipe['functions']:
        found = [s for s in coff.symbols.values() if s['name'] == function['symbol'] and s['section'] > 0]
        require(len(found) == 1,'literal context function ambiguous')
        symbol=found[0]
        if symbol['section'] == section and symbol['value'] <= off <= symbol['value']+function['size']-4:
            result.append(dict(function_address=function['address'],function_symbol=function['symbol'],
                               offset=off-symbol['value'],kind=kind))
    return sorted(result,key=lambda r:(r['function_address'],r['function_symbol'],r['offset']))


def literal(coff, symbol):
    require(LABEL.fullmatch(symbol['name']) and symbol['section'] > 0 and symbol['type'] == 0 and
            symbol['storage'] == 3 and symbol['aux_count'] == 0,'literal must be a defined static compiler label')
    section=coff.sections[symbol['section']]
    require(section['flags'] & 0x40000000 and not section['flags'] & (0x80000000|0x20000000|0x20) and
            not section['relocs'],'literal container is not readonly/nonpointer')
    start=symbol['value']; ends=[s['value'] for s in coff.symbols.values() if s['section'] == symbol['section'] and s['value'] > start]
    end=min(ends) if ends else section['size']
    require(0 <= start < end <= section['size'] and end-start <= 65536,'literal extent invalid')
    payload=section_payload(coff,symbol['section'])[start:end]
    require(len(payload) == end-start and b'\0' in payload and payload.endswith(b'\0'),'literal extent lacks complete terminator/padding')
    metadata={k:section[k] for k in ('index','name','size','flags','comdat','selection','association','payload_sha256')}
    return payload,dict(symbol=dict(symbol),end=end,extent=end-start,section=metadata,
                       payload_sha256=hashlib.sha256(payload).hexdigest())


def supplement(before, after, recipe, pe, highlows):
    olduses,newuses=uses(before),uses(after)
    renames={}; reverse={}
    for key,new in newuses.items():
        if not LABEL.fullmatch(new['symbol']['name']):continue
        old=olduses.get(key)
        require(old is not None and LABEL.fullmatch(old['symbol']['name']),'literal use has no exact old physical context')
        oldname,newname=old['symbol']['name'],new['symbol']['name']
        if oldname == newname:continue
        require(newname not in renames or renames[newname] == oldname,'one new label has conflicting old identities')
        require(oldname not in reverse or reverse[oldname] == newname,'one old label split across new identities')
        renames[newname]=oldname;reverse[oldname]=newname
    adapted=copy.deepcopy(recipe); witnesses=[]
    for newname,oldname in sorted(renames.items()):
        require(oldname in recipe['symbols'],'old literal lacks original recipe binding')
        olds=[s for s in before.symbols.values() if s['name'] == oldname]
        news=[s for s in after.symbols.values() if s['name'] == newname]
        require(len(olds) == len(news) == 1,'literal label duplicated')
        oldpayload,oldmeta=literal(before,olds[0]);newpayload,newmeta=literal(after,news[0])
        require(oldpayload == newpayload and oldmeta['section'] == newmeta['section'] and
                olds[0]['value'] == news[0]['value'] and oldmeta['end'] == newmeta['end'],
                'literal full payload/container/placement changed')
        oldkeys={k for k,v in olduses.items() if v['symbol']['name'] == oldname}
        newkeys={k for k,v in newuses.items() if v['symbol']['name'] == newname}
        require(bool(oldkeys) and oldkeys == newkeys,'literal complete physical uses differ')
        original=int(recipe['symbols'][oldname],16); extent=len(oldpayload)
        section=pe.section(original-pe.base,extent)
        require(section is not None and section['flags'] & 0x40000000 and
                not section['flags'] & (0x80000000|0x20000000|0x20),'original literal not wholly readonly')
        require(not any(original-3 <= site < original+extent for site in highlows),'original literal has pointer field')
        require(pe.read_rva(original-pe.base,extent) == oldpayload,'original full literal payload differs')
        fields=[]
        for key in sorted(oldkeys):
            old,new=olduses[key],newuses[key]
            require(old['record']['kind'] == new['record']['kind'] == 6 and
                    old['record']['width'] == new['record']['width'] == 4 and
                    old['record']['addend'] == new['record']['addend'] and
                    0 <= old['record']['addend'] < extent,'literal field kind/addend changed')
            oldctx,newctx=contexts(before,recipe,key),contexts(after,recipe,key)
            require(bool(oldctx) and oldctx == newctx,'literal use lacks exact complete original function context')
            for ctx in oldctx:
                fieldva=int(ctx['function_address'],16)+ctx['offset']
                require(int.from_bytes(pe.read_rva(fieldva-pe.base,4,allow_code=True),'little') ==
                        original+old['record']['addend'],'original literal field target conflicts')
            fields.append(dict(physical_section=key[0],physical_offset=key[1],kind=key[2],
                old_record=old['record'],new_record=new['record'],function_contexts=oldctx))
        adapted['symbols'][newname]=recipe['symbols'][oldname]
        witnesses.append(dict(old_name=oldname,new_name=newname,original_binding=recipe['symbols'][oldname],
            previous_new_name_binding=recipe['symbols'].get(newname),old_literal=oldmeta,new_literal=newmeta,
            all_physical_uses=fields,complete_bijective_field_provenance=True,
            original_full_payload_readonly_nonpointer_equal=True,provider_selected=False))
    require(adapted['functions'] == recipe['functions'] and {k:v for k,v in adapted.items() if k != 'symbols'} ==
            {k:v for k,v in recipe.items() if k != 'symbols'},'supplement changed original recipe rows/profile')
    return adapted,dict(kind='fnv-proven-alternate-compiler-literal-bindings',witnesses=witnesses,
        original_recipe_unchanged=True,ordinary_oracle_unchanged=True,provider_selected=False,runtime_eligible=False)
