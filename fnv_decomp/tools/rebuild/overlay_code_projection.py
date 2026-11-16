"""Separate overlay CODE collector/projector with original logical caller names."""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import gzip
import itertools
import json
import os
from pathlib import Path
import struct
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
import coff_code_archive as coff
import root_code_closure as ordinary
import runtime_code_pool as pool
import runtime_overlay_inputs_v2 as registry_tool
import entry_relocation_batch as batch
from data_plan import file_hash
from coff_inventory import peak_memory_bytes
from relocation_audit import WIDTHS
from import_plan import ImagePe, image_ok, require
from compare import Coff as CompareCoff, compare as plain_compare

ROOT=batch.ROOT
POLICY=ROOT/'runtime/code-pools/overlay-repaired-code-v1.json'
POLICY_SHA='ba5c84ef938baa12c05dc27a17b880f73592118e3869526d43f8fc7266050b79'
REGISTRY='build/rebuild/runtime-overlay-inputs-native-v2/registry.json'
CONTEXTS='build/rebuild/runtime-overlay-inputs-native-v2/root-observer-inputs.jsonl.gz'
INVENTORY='build/rebuild/runtime-code-inventory-native-v1.jsonl.gz'
COVERAGE='build/rebuild/bulk-code-pool-all-current-v1/production/coverage.jsonl.gz'
MEMBERS='build/rebuild/bulk-code-pool-all-current-v1/production/members.jsonl'
IMPORTS='build/rebuild/import-plan-native-v1.json'
FALSE=dict(provider_selected=False,runtime_eligible=False,ABI_verified=False,link_ready=False,game_execution=False,compiler_performed=False)


def digest(value):return registry_tool.identity(value)


def records(path):
    opener=gzip.open if str(path).endswith('.gz') else open
    with opener(path,'rt',encoding='utf-8') as stream:
        for ordinal,line in enumerate(stream,1):
            require(ordinal <= 1000000 and len(line) <= 16*1024*1024,'metadata stream bound')
            yield ordinal,json.loads(line)


def logical_providers(rows,selections,manifest):
    providers={}
    for row in rows:
        if 'original_address' not in row or 'physical_identity' not in row:continue
        address=row['original_address'];native=row['selected_native'];identity=row['physical_identity'];choice=selections.get(address)
        require(choice is not None and address not in providers,'duplicate/unknown logical provider')
        unit=manifest['units'][choice['recipe_index']]
        require(identity['recipe_id'] == choice['recipe_id'] == unit['recipe_id'] and identity['object_sha256'] == unit['object_sha256'] and
                all(native[k] == choice[k] for k in ('symbol','section','value','size')) and native['symbol_index'] == identity['symbol_index'],
                'baseline logical provider selection/native lineage differs')
        providers[address]=identity
    require(set(providers) == set(selections),'incomplete baseline logical provider universe')
    return providers


def no_competing_exports(roots,providers,coverage,exports):
    require(len(exports) == len(set(exports)),'baseline duplicate strong exports')
    for root in roots:
        address=root['original_address'];identity=providers[address];row=coverage[address]
        require(row['physical_identity'] == identity and row['status'] != 'EMITTED','baseline physical provider already emitted')
        require(pool.canonical(identity) not in exports,'baseline logical name already exported')


def fresh_frame_facts(obj,functions,roots,original_lineage):
    """Native anchors/associations are observations, never new EH byte proofs."""
    root_addresses={r['original_address'] for r in roots};root_sections={r['section']:r for r in roots};facts=[]
    for f in functions:
        if f['address'] not in root_addresses:continue
        for off,si,kind in obj['sections'][f['section']]['relocs']:
            if not f['value'] <= off < f['value']+f['size']:continue
            target=obj['symbols'][si];section=obj['sections'].get(target['section'])
            if (section and section['name'].startswith(('.text$x','.xdata','.pdata'))) or target['name'].startswith(('__eh','__unwind','__catch')):
                facts.append(dict(kind='FRESH_NATIVE_PARENT_FRAME_REFERENCE',parent=f['address'],section=f['section'],offset=off,target_index=si,relocation_kind=kind,frame_contract_verified=False))
    for si,s in obj['symbols'].items():
        if s['aux_count'] != 1 or s['storage'] != 3 or s['section'] <= 0 or s['name'] != obj['sections'][s['section']]['name']:continue
        aux=struct.unpack('<IHHIhBBH',s['aux'])
        if aux[5] == 5 and aux[4] in root_sections and not obj['sections'][s['section']]['name'].startswith('.debug'):
            facts.append(dict(kind='FRESH_NATIVE_PARENT_ASSOCIATIVE_OBLIGATION',parent=root_sections[aux[4]]['original_address'],section=s['section'],association=aux[4],frame_contract_verified=False))
    old=original_lineage.get('original_retained_unit',{})
    for piece in old.get('eh_sections',[]):
        if piece[3] in root_addresses:facts.append(dict(kind='ORIGINAL_PARENT_EH_LINEAGE_NOT_REVALIDATED',parent=piece[3],original_piece=piece,fresh_overlay_EH_proof=False))
    return facts


def closure_contract(context,unit,bindings,roots,imports):
    addresses={r['original_address'] for r in roots};fields=[];missing=[]
    for row in bindings:
        if row['function_va'] not in addresses:continue
        (fields if row.get('coff_relocation') is not None else missing).append(row)
    functions=[dict(address=r['address'],symbol=r['symbol'],size=r['size'],section=r['overlay_native']['section'],
                    value=r['overlay_native']['value'],verdict='match') for r in unit['scope']]
    frame=fresh_frame_facts(unit['parsed'],functions,roots,context['original_eh_proof_lineage'])
    provenance=dict(object_sha256=context['actual_object']['sha256'],source_sha256=context['actual_source_proof']['generated_source_sha256'],
        overlay_unit_id=context['overlay_unit_id'],original_ancestry=context['original_ancestry'],
        function_proof_kind='fresh-overlay-registry-complete-ordinary-comparison',registry_sha256=unit['registry_sha256'],
        unit_proof_scope='complete fresh function rows/native fields; not an overlay EH byte proof',
        root_context_sha256=digest(context),source_proof=context['actual_source_proof'],fresh_EH_byte_proof=False,
        optional_function_index_present=False,observer_sha256=unit['observer_sha256'],parser_sha256=unit['parser_sha256'])
    return dict(recipe_id=context['original_ancestry']['recipe_id'],roots=roots,export_policy=ordinary.EXPORT_POLICY,
        verified_match=True,fields_complete=True,missing_fields_complete=True,unit_proofs_complete=True,
        fields=fields,missing_fields=missing,parent_eh=frame,
        omission_field_proofs=[r for r in bindings if r.get('coff_relocation') and
            (r['coff_relocation']['symbol_storage'] == 6 or r['coff_relocation']['symbol'] == ordinary.IAT_SOURCE_NAME)],
        unit_verified_functions=functions,iat_import_observation=imports,provenance=provenance)


def namespace_plan(obj,contract,closure,providers):
    require(closure['closure_observed'] and not closure['blockers'],'root omission closure blocked')
    roots={r['symbol_index']:r for r in contract['roots']};runtime=set(closure['retained_runtime_section_indices'])
    names={i:pool.canonical(providers[r['original_address']]) for i,r in roots.items()};facts={};obligations=[]
    fields={ (r['physical_section'],r['physical_offset'],r['coff_relocation']['symbol_index'],r['coff_relocation']['kind']):r for r in contract['fields']}
    for reference in closure['references']:
        si=reference['symbol_index'];symbol=obj['symbols'][si];base=reference['original_base'];role=reference['role']
        key=(reference['section'],reference['offset'],si,reference['kind']);row=fields[key]
        if symbol['section'] in runtime:
            if si not in roots:continue # retained exact local offsets stay local
            name=names[si]
        elif role == 'code':
            require(base in providers and row['classification'] == 'SELECTED_CODE_ENTRY','unselected/interior CODE target lacks exact logical provider')
            require(row.get('code_ownership_ambiguous') is False and row.get('code_owners') == [dict(address=base,offset=0)],'ambiguous CODE provider field')
            name=pool.canonical(providers[base])
        else:
            require(role in ('data','iat-cell','crt-contract'),'unknown unresolved address role')
            name=pool.unresolved(base,role)
        fact=(base,role)
        require(si not in facts or facts[si] == fact,'conflicting physical reference role/base')
        require(si not in names or names[si] == name,'conflicting logical namespace')
        facts[si]=fact;names[si]=name
        if symbol['section'] not in runtime:
            obligations.append(dict(symbol_index=si,original_base=base,role=role,logical_name=name,
                original_target=reference['original_target'],addend_bits=reference['addend_bits'],field=key,
                converted_omitted_definition=symbol['section'] > 0,provider_selected=False))
    groups=[];by_name=defaultdict(list)
    for i,name in names.items():by_name[name].append(i)
    conversions={r['symbol_index'] for r in closure['omitted_definition_conversions']}
    for name,members in sorted(by_name.items()):
        if len(members) < 2:continue
        bases={facts[i][0] if i in facts else roots[i]['original_address'] for i in members}
        require(len(bases) == 1,'logical alias group has different bases');base=next(iter(bases))
        require(base in providers and name == pool.canonical(providers[base]),'non-CODE logical aliases unsupported')
        definitions=[i for i in members if i in roots];require(len(definitions) <= 1,'multiple retained strong providers')
        uses=[]
        for i in members:
            symbol=obj['symbols'][i]
            require(symbol['storage'] == 2 and symbol['type'] == 32 and not symbol['aux_count'] and symbol['value'] == 0 and
                    (symbol['section'] == 0 or i in roots or i in conversions),'incompatible logical alias record')
            used=[r for r in contract['fields'] if r['coff_relocation']['symbol_index'] == i]
            require(used or i in roots,'unused alias physical record')
            for row in used:
                require(row['classification'] == 'SELECTED_CODE_ENTRY' and row['derived_source_symbol_base_va'] == row['exact_original_target_va'] == base and
                        row['coff_relocation']['addend'] == 0 and row['proof_consistency'] == 'EXACT_OWN_SOURCE_RESOLUTION' and
                        row.get('code_ownership_ambiguous') is False and row.get('code_owners') == [dict(address=base,offset=0)],'unproved alias field')
                uses.append(dict(physical_index=i,section=row['physical_section'],offset=row['physical_offset'],kind=row['coff_relocation']['kind'],row_sha256=digest(row)))
        groups.append(dict(name=name,members=sorted(members),provider=providers[base],fields=uses,
            retained_strong_definitions=definitions,converted_omitted_definitions=sorted(set(members)&conversions),coalescing_allowed=False))
    require(all(obj['symbols'][i]['storage'] != 2 or i in names for i in closure['retained_primary_indices']),'unnamespaced external record')
    existing={s['name'] for s in obj['symbols'].values()}
    require(not any(name in existing for name in names.values()),'preexisting logical namespace collision')
    return dict(bindings=sorted(names.items()),groups=groups,obligations=obligations,
        expected_exports=sorted(names[i] for i in roots),sections=closure['retained_section_indices'],
        symbols=closure['retained_primary_indices'],undefined=sorted(conversions))


def choose_group(context,unit,bindings,providers,coverage,exports,imports):
    roots=context['roots'];remaining={r['function_va'] for r in bindings if r.get('coff_relocation') is None}
    complete=[r for r in roots if r['original_address'] not in remaining];attempts=[]
    require(len(complete) <= 3,'finite per-recipe root subset bound')
    for count in range(len(complete),0,-1):
        for selected in itertools.combinations(sorted(complete,key=lambda r:r['original_address']),count):
            selected=[{k:r[k] for k in ('original_address','symbol','symbol_index','section','value','size')} for r in selected]
            contract=closure_contract(context,unit,bindings,selected,imports)
            closure=ordinary.assess_object(unit['parsed'],contract)
            record=dict(roots=[r['original_address'] for r in selected],closure_sha256=digest(closure),blockers=closure['blockers'])
            attempts.append(record)
            if not closure['closure_observed']:continue
            try:
                no_competing_exports(selected,providers,coverage,exports)
                namespace=namespace_plan(unit['parsed'],contract,closure,providers)
            except ValueError as error:record['namespace_blocker']=str(error);continue
            return dict(candidate=True,contract=contract,closure=closure,namespace=namespace,attempts=attempts,
                blocked_missing_roots=[r['original_address'] for r in roots if r['original_address'] in remaining])
    return dict(candidate=False,attempts=attempts,blocked_missing_roots=[r['original_address'] for r in roots if r['original_address'] in remaining])


def apply_names(data,bindings,groups):
    obj=coff.parse(data);result=bytearray(data);extra=bytearray();expected={i:dict(s) for i,s in obj['symbols'].items()};targets=defaultdict(list)
    for i,name in bindings:targets[name].append(i)
    require({n:sorted(v) for n,v in targets.items() if len(v)>1} == {g['name']:g['members'] for g in groups},'unproved duplicate namespace')
    existing={s['name'] for s in obj['symbols'].values()};allowed=set(range(obj['string_pointer'],obj['string_pointer']+4));seen=set()
    for i,name in bindings:
        s=obj['symbols'][i];require(i not in seen and s['storage'] in (2,3) and s['section'] >= 0 and not s['aux_count'] and name not in existing,'invalid name-only record')
        require(name and all(33 <= ord(c) <= 126 for c in name),'invalid logical name')
        seen.add(i);struct.pack_into('<II',result,obj['symbol_pointer']+18*i,0,obj['string_length']+len(extra));extra+=name.encode()+b'\0';expected[i]['name']=name
        allowed.update(range(obj['symbol_pointer']+18*i,obj['symbol_pointer']+18*i+8))
    struct.pack_into('<I',result,obj['string_pointer'],obj['string_length']+len(extra));result+=extra
    parsed=coff.parse(bytes(result));require(parsed['symbols'] == expected and parsed['sections'] == obj['sections'] and
        all(a == b or i in allowed for i,(a,b) in enumerate(zip(data,result))),'non-name byte changed')
    return bytes(result)


def project(raw,context,unit,bindings,providers,coverage,exports,imports,approved):
    require(coff.digest(raw) == context['actual_object']['sha256'] and coff.parse(raw) == unit['parsed'],'stale physical overlay object')
    recomputed=choose_group(context,unit,bindings,providers,coverage,exports,imports)
    require(recomputed['candidate'] and digest(recomputed) == digest(approved),'whole-root plan does not recompute')
    plan=recomputed['namespace'];selected,maps=coff.serialize(raw,plan['sections'],plan['symbols'],plan['undefined'])
    renamed=[(maps['symbol_map'][i],name) for i,name in plan['bindings']]
    groups=[dict(g,members=sorted(maps['symbol_map'][i] for i in g['members'])) for g in plan['groups']]
    output=apply_names(selected,renamed,groups)
    require(coff.exports(output) == plan['expected_exports'] and len(coff.exports(output)) == len(set(coff.exports(output))),'extra/duplicate/missing export')
    return output,dict(maps=maps,plan_sha256=digest(recomputed),exports=plan['expected_exports'],
        old_logical_identities=[providers[r['original_address']] for r in recomputed['contract']['roots']],**FALSE)


def validate_inventory(obj,inventory,object_hash):
    require(inventory['object_sha256'] == object_hash,'inventory object lineage differs')
    sections={s['index']:s for s in inventory['sections']};symbols={s['index']:s for s in inventory['symbols']}
    require(set(sections) == set(obj['sections']) and set(symbols) == set(obj['symbols']),'complete physical inventory differs')
    for i,s in obj['sections'].items():
        old=sections[i]
        require(all(old[k] == s[k] for k in ('name','size','flags')) and old['payload_sha256'] == coff.digest(s['payload']) and
                [tuple(r) for r in old['relocs']] == s['relocs'],'native section inventory differs')
    for i,s in obj['symbols'].items():
        old=symbols[i];require(all(old[k] == s[k] for k in ('name','section','value','type','storage','aux_count')) and
            old['auxiliary_record_sha256'] == (coff.digest(s['aux']) if s['aux_count'] else None),'native primary/aux inventory differs')
    actual=Counter((sec,off,si,kind) for sec,s in obj['sections'].items() for off,si,kind in s['relocs'])
    saved=Counter((r['section'],r['offset'],r['symbol_index'],r['kind']) for r in inventory['all_physical_fields'])
    require(actual == saved,'all physical fields inventory differs')


def validate_bindings(raw,path,unit,context):
    require(coff.digest(raw) == context['actual_object']['sha256'],'stale binding object identity')
    rows=[r for _,r in records(path)];obj=coff.parse(raw);scope=unit['scope'];fmap={(f['address'],f['symbol']):f for f in scope};expected=[];observed=[]
    for f in scope:
        n=f['overlay_native'];s=obj['symbols'][n['symbol_index']]
        require((s['name'],s['section'],s['value']) == (f['symbol'],n['section'],n['value']),'fresh native function placement differs')
        for off,si,kind in obj['sections'][n['section']]['relocs']:
            if n['value'] <= off < n['value']+f['size']:expected.append((f['address'],f['symbol'],n['section'],off,si,kind))
    for row in rows:
        require(row['overlay_unit_id'] == context['overlay_unit_id'] and row['actual_object_sha256'] == context['actual_object']['sha256'] and
                row['actual_generated_source_sha256'] == context['actual_source_proof']['generated_source_sha256'],'binding source/object lane differs')
        f=fmap[(row['function_va'],row['function_symbol'])];n=f['overlay_native'];require(row['physical_section'] == n['section'] and
            row['physical_offset']-n['value'] == row['source_field_offset'] and
            row['original_field_va'] == '0x%08x'%(int(f['address'],16)+row['source_field_offset']),'binding parent context differs')
        cr=row.get('coff_relocation')
        if cr:
            si=cr['symbol_index'];symbol=obj['symbols'][si];key=(f['address'],f['symbol'],n['section'],cr['offset'],si,cr['kind']);observed.append(key)
            require((cr['offset'],si,cr['kind']) in obj['sections'][n['section']]['relocs'] and cr['symbol'] == symbol['name'] and
                all(cr['symbol_'+k] == symbol[k] for k in ('section','value','type','storage')),'fresh physical field/symbol differs')
            if cr['width']:
                operand=int.from_bytes(obj['sections'][n['section']]['payload'][cr['offset']:cr['offset']+cr['width']],'little')
                require(operand == cr['addend'],'fresh field operand differs')
                overlaps=sum(o < cr['offset']+cr['width'] and o+WIDTHS[k] > cr['offset'] for o,_,k in obj['sections'][n['section']]['relocs'] if WIDTHS[k])
                require(overlaps == row['physical_field_overlap_count'],'fresh physical overlap census differs')
        else:
            off=row['physical_offset'];require(not any(o < off+4 and o+4 > off for o,_,_ in obj['sections'][n['section']]['relocs']),'remaining missing field acquired unproved relocation')
    require(Counter(expected) == Counter(observed),'complete fresh function field coverage differs')
    for root in context['roots']:
        refs=[dict(ordinal=i+1,sha256=digest(row)) for i,row in enumerate(rows) if row['function_va'] == root['original_address'] and row['function_symbol'] == root['symbol']]
        require(refs == root['binding_refs'],'whole root binding ordinal/hash list differs')
    return rows


def run(args):
    start=time.monotonic();p=batch.frozen.read_bound(POLICY,POLICY_SHA);require(file_hash(__file__) == args.implementation_sha256,'unreviewed projector source')
    require(args.operation in ('observe','project') and (args.operation != 'project' or args.authorize_private_emission),'explicit private emission opt-in required')
    require(Path(ordinary.__file__).resolve() == ROOT/'tools/rebuild/root_code_closure.py' and
            Path(coff.__file__).resolve() == ROOT/'tools/rebuild/coff_code_archive.py','unexpected frozen observer/parser module')
    paths={rel:ROOT/rel for rel in p['inputs']};data={};observations={Path(__file__).resolve():args.implementation_sha256,POLICY:POLICY_SHA}
    for rel,pin in p['inputs'].items():
        observations[paths[rel]]=pin;require(file_hash(paths[rel]) == pin,'stale fixed metadata input')
        if rel.endswith('.json'):data[rel]=json.loads(paths[rel].read_text())
    r=data[REGISTRY];require(r['status'] == 'pass_pending_independent_review' and r['input_stability_verified'] and r['terminal_protected_input_stability_verified'],'registry not accepted/stable')
    observations.update({Path(path):pin for path,pin in r['inputs'].items()})
    for name,pin in [('root_code_closure.py',p['ordinary_observer_sha256']),('coff_code_archive.py',p['parser_sha256'])]:observations[ROOT/'tools/rebuild'/name]=pin
    for name in ('runtime_code_pool.py','overlay_code_projection.py','runtime_overlay_inputs_v2.py'):
        path=ROOT/'tools/rebuild'/name;observations.setdefault(path,file_hash(path))
    selection=batch.frozen.read_bound(batch.frozen.DEFAULTS['selection'],batch.frozen.PINS['selection'])['selections']
    manifest=batch.frozen.read_bound(batch.frozen.DEFAULTS['manifest'],batch.frozen.PINS['manifest'])
    providers=logical_providers((row for _,row in records(paths[INVENTORY])),selection,manifest)
    coverage={row['original_address']:row for _,row in records(paths[COVERAGE])}
    require(len(coverage) == 68657 and set(coverage) == set(providers),'baseline coverage incomplete')
    exports=[name for _,row in records(paths[MEMBERS]) for name in row['exports']]
    require(len(exports) == len(set(exports)) == 12946 and sum(row['status'] == 'EMITTED' for row in coverage.values()) == 12946,'baseline export census differs')
    contexts=[row for _,row in records(paths[CONTEXTS])];require(len(contexts) == 9,'whole registry contract set differs')
    imported=next(i for i in data[IMPORTS]['imports'] if i['import_id'] == 175)
    index=ROOT/'build/function_index.json';require(not index.exists() and all(file_hash(path) == pin for path,pin in observations.items()),'protected input drift')
    out=batch.frozen.new_output(args.out,observations);out.mkdir(parents=True)
    report=dict(kind='fnv-overlay-code-projection',operation=args.operation,status='error',units=[],emission_performed=False,inputs={str(k):v for k,v in observations.items()},**FALSE)
    def note(state,**fields):
        with (out/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(dict(state=state,**fields))+'\n');f.flush();os.fsync(f.fileno())
    note('started',operation=args.operation);members=[]
    try:
        image=None
        if args.operation == 'project':
            require(args.reference is not None and file_hash(args.reference) == batch.frozen.PINS['reference'],'owned reference required for projection comparison')
            observations[Path(args.reference).resolve()]=batch.frozen.PINS['reference'];image=ImagePe(args.reference);require(image_ok(image)[0],'owned image probes failed')
        for context in contexts:
            unit_record=next(u for u in r['units'] if u['overlay_unit_id'] == context['overlay_unit_id']);rid=unit_record['recipe_id'];base=paths[REGISTRY].parent/rid
            require(digest(context) == unit_record['contract_sha256'],'whole root observer contract differs')
            for name,pin in unit_record['artifacts'].items():observations[base/name]=pin;require(file_hash(base/name) == pin,'registry unit artifact differs')
            source=Path(context['actual_source_proof']['generated_source']);objpath=Path(context['actual_object']['path'])
            observations[source]=context['actual_source_proof']['generated_source_sha256'];observations[objpath]=context['actual_object']['sha256']
            require(all(file_hash(path) == pin for path,pin in ((source,observations[source]),(objpath,observations[objpath]))),'fresh source/object differs')
            raw=objpath.read_bytes();require(coff.digest(raw) == observations[objpath],'fresh object drift')
            source_meta=json.loads((base/'source-and-replacements.json').read_text());scope=source_meta['function_scope']
            require(len(scope) == context['actual_source_proof']['complete_original_function_rows'],'complete fresh unit row count differs')
            comparison=json.loads((base/'comparison.json').read_text())['rows']
            require(Counter((x['address'],x['symbol'],x['size']) for x in comparison) == Counter((x['address'],x['symbol'],x['size']) for x in scope) and
                    all(x['verdict'] == 'match' for x in comparison),'complete fresh comparison proof differs')
            by_address={x['address']:x for x in scope}
            for root in context['roots']:
                old=by_address[root['original_address']]['original_native']
                require(providers[root['original_address']] == dict(recipe_id=context['original_ancestry']['recipe_id'],
                    object_sha256=context['original_ancestry']['object_sha256'],symbol_index=old['symbol_index']),'old logical provider differs from explicit registry ancestry')
            unit=dict(scope=scope,parsed=coff.parse(raw),registry_sha256=p['inputs'][REGISTRY],observer_sha256=p['ordinary_observer_sha256'],parser_sha256=p['parser_sha256'])
            validate_inventory(unit['parsed'],json.loads((base/'native-inventory.json').read_text()),context['actual_object']['sha256'])
            bindings=validate_bindings(raw,base/'bindings.jsonl.gz',unit,context)
            chosen=choose_group(context,unit,bindings,providers,coverage,exports,imported)
            record=dict(recipe_id=rid,overlay_unit_id=context['overlay_unit_id'],chosen=chosen,
                remaining_unit_missing=unit_record['migration']['remaining_missing'],original_ancestry=context['original_ancestry'],
                actual_object=context['actual_object'],actual_source_proof=context['actual_source_proof'])
            batch.frozen.save(out/(rid+'.plan.json'),record)
            if chosen['candidate'] and args.operation == 'project':
                output,receipt=project(raw,context,unit,bindings,providers,coverage,exports,imported,chosen);name=rid+'.obj';target=out/name
                with target.open('xb') as f:f.write(output)
                require(file_hash(target) == coff.digest(output),'projected object changed before comparison')
                names=dict(chosen['namespace']['bindings']);symbols={}
                for use in chosen['closure']['references']:
                    if use['symbol_index'] in names:
                        name0=names[use['symbol_index']];base0=use['original_base'];require(name0 not in symbols or symbols[name0] == base0,'projection oracle namespace base conflict');symbols[name0]=base0
                recipe=dict(functions=[dict(address=root['original_address'],symbol=names[root['symbol_index']],size=root['size']) for root in chosen['contract']['roots']],symbols=symbols)
                result=plain_compare(CompareCoff(target),image,recipe)
                require(len(result) == len(recipe['functions']) and all(row['verdict'] == 'match' for row in result),'projected old-logical CODE original comparison failed')
                require(file_hash(target) == coff.digest(output),'projected object changed during comparison')
                batch.frozen.save(out/(rid+'.projection.json'),dict(receipt=receipt,comparison=[{k:v for k,v in row.items() if k != 'byte_differences'} for row in result]))
                members.append((rid+'.obj',output));record['projection']=dict(output_sha256=coff.digest(output),exports=receipt['exports'])
            report['units'].append(record);note('unit_observed',recipe_id=rid,candidate=chosen['candidate'])
            require(time.monotonic()-start <= 600 and (peak_memory_bytes() or 0) <= 1024**3,'projection observation resource checkpoint exceeded')
            require(sum(f.stat().st_size for f in out.rglob('*') if f.is_file()) <= 100*1024**2,'private projection output bound exceeded')
        require(sum(len(u['remaining_unit_missing']) for u in report['units']) == 7,'remaining seven missing fields not preserved')
        if members:
            archive=coff.archive(members);path=out/'overlay-code.lib'
            with path.open('xb') as f:f.write(archive)
            recovered=coff.read_archive(archive);require(recovered['members'] == members,'isolated overlay archive recovery differs')
            report.update(emission_performed=True,archive_sha256=coff.digest(archive))
        require(not index.exists() and all(file_hash(path) == pin for path,pin in observations.items()),'protected input drift after observation/projection')
        report.update(status='pass_pending_independent_review',input_stability_verified=True,
            candidate_roots=sum(len(u['chosen']['contract']['roots']) for u in report['units'] if u['chosen']['candidate']),
            projected_roots=sum(len(u['chosen']['contract']['roots']) for u in report['units'] if u.get('projection')),
            original_entry_missing_census_unchanged=47,original_global_missing_census_unchanged=88,baseline_archive_unchanged=True)
        report['artifacts']={f.relative_to(out).as_posix():file_hash(f) for f in out.rglob('*') if f.is_file() and f.name != 'progress.jsonl'}
        require(all(file_hash(out/name) == pin for name,pin in report['artifacts'].items()),'generated projection artifact drift')
        note('verified_pending_review')
    except Exception as error:report['error']=str(error);note('failed',error_type=type(error).__name__)
    try:report['terminal_protected_input_stability_verified']=not index.exists() and all(file_hash(path) == pin for path,pin in observations.items())
    except OSError:report['terminal_protected_input_stability_verified']=False
    if not report['terminal_protected_input_stability_verified']:report.update(status='error',error='terminal protected input drift')
    report['elapsed_seconds']=time.monotonic()-start;report['observer_peak_memory_bytes']=peak_memory_bytes();report['inputs']={str(k):v for k,v in observations.items()};batch.frozen.save(out/'receipt.json',report);return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--operation',choices=['observe','project'],required=True)
    parser.add_argument('--authorize-private-emission',action='store_true');parser.add_argument('--implementation-sha256',required=True)
    parser.add_argument('--reference',type=Path);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    try:result=run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:parser.exit(2,'overlay projection rejected: '+str(error)+'\n')
    print(result['status']);return 0 if result['status'] == 'pass_pending_independent_review' else 1


if __name__=='__main__':raise SystemExit(main())
