"""Index source-recipe address leads for one private vtable comparison report."""
import argparse,collections,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;PROJECT=M.parent.parent;PRIVATE=(M/'out').resolve()


def bounded(path):
    p=path.resolve()
    if not p.is_relative_to(PRIVATE):raise ValueError('input/output must stay below private m3/out')
    return p


def index_units(units):
    functions=collections.defaultdict(set);symbols=collections.defaultdict(set)
    for i,u in enumerate(units):
        source=u.get('source','')
        for f in u.get('functions',[]):
            address=int(f['address'],0)
            for name in [f['symbol']]+f.get('fold_aliases',[]):functions[address].add((name,source,i))
        for name,value in u.get('symbols',{}).items():
            try:address=int(value,0) if isinstance(value,str) else int(value)
            except (ValueError,TypeError):continue
            symbols[address].add((name,source,i))
    return functions,symbols


def rows_for_table(table,reference_targets,functions,symbols):
    rows=[]
    emitted={x['index']:x for x in table.get('slots',[])}
    for index in range(max(len(reference_targets),len(emitted))):
        slot=emitted.get(index,{});va=reference_targets[index] if index<len(reference_targets) else None
        if slot and slot.get('reference_target')!=va:raise ValueError('slot metadata differs from census')
        fs=sorted(functions.get(va,()));ss=sorted(symbols.get(va,()))
        rows.append({'slot_index':index,'reference_target':va,'emitted_symbol':slot.get('symbol'),'current_resolved_target':slot.get('resolved_target'),'current_match':slot.get('match',False),
          'function_recipe_candidates':[{'symbol':n,'source':s,'unit':i} for n,s,i in fs],
          'source_symbol_candidates':[{'symbol':n,'source':s,'unit':i} for n,s,i in ss],
          'unique_function_spellings':len({x[0] for x in fs}),'unique_symbol_spellings':len({x[0] for x in ss}),
          'status':'not_emitted_source_recipe_leads' if not slot and (fs or ss) else 'not_emitted_no_lead' if not slot else 'already_matching' if slot['match'] else 'source_recipe_leads' if fs or ss else 'no_source_recipe_lead',
          'caveat':'Address association is a lead, not proof of virtual signature, class ownership, thunk adjustment or native ABI.'})
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--metadata',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    source=bounded(a.metadata);out=bounded(a.out)
    if out.exists():raise FileExistsError('refusing overwrite')
    data=json.loads(source.read_text());up=PROJECT/'fnv_decomp/build/units.json';raw=up.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    recorded=data.get('inputs',{}).get('units_sha256')
    if recorded and recorded!=digest:raise ValueError('unit recipe differs from metadata comparison')
    census_path=M/'out/phase2-class-census/census-v2.json';census=json.loads(census_path.read_text())
    if census['inputs']['units_sha256']!=digest:raise ValueError('census unit recipe differs')
    expected_census=data.get('inputs',{}).get('census_sha256')
    if expected_census and hashlib.sha256(census_path.read_bytes()).hexdigest()!=expected_census:raise ValueError('census digest differs')
    ref_tables={t['vtable_va']:t for t in census['vtables']}
    units=json.loads(raw)['units'];funcs,syms=index_units(units);tables=[]
    for table in data['tables']:
        ref=ref_tables.get(table.get('reference_vtable_va'))
        if not ref or ref['locator']['type_name']!=data['type_name']:raise ValueError('reference vtable missing or mismatched')
        rows=rows_for_table(table,ref['contiguous_code_pointer_prefix_targets'],funcs,syms)
        tables.append({'symbol':table['symbol'],'subobject_offset':table['subobject_offset'],'emitted_slot_count':table['emitted_slot_count'],
          'observed_reference_prefix_count':table.get('original_code_pointer_prefix_count'),'reference_vtable_va':table.get('reference_vtable_va'),'slots':rows})
    status=collections.Counter(r['status'] for t in tables for r in t['slots'])
    result={'schema_version':1,'scope':'Reverse address-to-source leads only; no generated source or native method identity claim.',
      'inputs':{'metadata_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'units_sha256':digest,'census_sha256':hashlib.sha256(census_path.read_bytes()).hexdigest()},
      'type_name':data['type_name'],'summary':{'tables':len(tables),'observed_prefix_slots':sum(len(t['slots']) for t in tables),'status':dict(status)},'tables':tables}
    with out.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result['summary']))

if __name__=='__main__':main()
