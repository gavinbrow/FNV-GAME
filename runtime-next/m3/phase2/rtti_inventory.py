"""Read-only RTTI alias evidence; no source, selection or build artifacts changed."""
import collections,hashlib,json,re,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; M3=HERE.parent; sys.path.insert(0,str(M3))
import gen_m3 as g


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pointer(a):
    raw=g.refbytes(a,4)
    if len(raw)!=4: raise ValueError('unreadable pointer')
    return struct.unpack('<I',raw)[0]


def collect():
    units_path=Path(g.PROJ)/'fnv_decomp/build/units.json'; units=json.loads(units_path.read_text())['units']
    groups=collections.defaultdict(lambda:collections.defaultdict(set)); stats=collections.Counter()
    for u in units:
        for symbol,v in u.get('symbols',{}).items():
            if not symbol.startswith('??_7'): continue
            try:
                a=int(v,0); col=pointer(a-4); td=pointer(col+12)
                if (a-4 not in g.ORIG_SET or col+12 not in g.ORIG_SET or g.sec_of(a)!='.rdata' or
                    g.sec_of(col)!='.rdata' or g.sec_of(td)!='.data'): raise ValueError('missing chain proof')
                raw=g.refbytes(td+8,256); nul=raw.find(b'\x00')
                if nul<0: raise ValueError('unterminated')
                name=raw[:nul].decode('ascii')
                if not name.startswith(('.?AV','.?AU')) or not name.endswith('@@'): raise ValueError('bad name')
            except (TypeError,ValueError,UnicodeDecodeError,struct.error,KeyError):
                stats['rejected_unit_symbol_references']+=1; continue
            groups[(a,col,td,name)][symbol].add(u.get('source',''))
            stats['validated_unit_symbol_references']+=1
    rows=[]
    for (a,col,td,name),symbols in sorted(groups.items()):
        simple=re.fullmatch(r'\.\?A([VU])([A-Za-z_][A-Za-z_0-9]*)@@',name)
        native='??_7'+simple.group(2)+'@@6B@' if simple else None
        synthetics=sorted(k for k in symbols if re.match(r'^\?\?_7FUN_[0-9a-f]{8}@@6B@$',k))
        aliases=[{'symbol':k,'sources':sorted(v)} for k,v in sorted(symbols.items())]
        rows.append({'vtable_va':a,'col_va':col,'type_descriptor_va':td,'reference_type_name':name,
                     'reference_name_prefix_bytes':8+len(name)+1,'reference_kind':('class' if simple and simple.group(1)=='V' else 'struct' if simple else 'complex'),
                     'unit_symbol_aliases':aliases,'matching_named_vtable_symbol':native if native in symbols else None,
                     'synthetic_simple_vtable_symbols':synthetics,
                     'status':'coaddressed_named_and_synthetic' if native in symbols and synthetics else 'unresolved',
                     'limitations':'COL chain and co-addressed symbol labels do not prove source type identity, class layout, inheritance or virtual slot implementation.'})
    stats['distinct_vtable_col_type_groups']=len(rows)
    stats['coaddressed_named_and_synthetic']=sum(r['status']=='coaddressed_named_and_synthetic' for r in rows)
    return {'schema_version':1,'scope':'Reference-assisted address evidence; not original source type or recoverable byte proof.',
            'inputs':{'units_sha256':digest(units_path),'selection_sha256':digest(M3/'batch8_final_selection.json')},'stats':dict(stats),'groups':rows}


def main():
    result=collect();target=HERE/'rtti_alias_inventory.json'
    with target.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result['stats']))

if __name__=='__main__':main()
