"""Conservative whole-token source screen over saved reference-assisted RTTI leads."""
import collections,hashlib,json,re,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;M3=HERE.parent;PROJECT=M3.parent.parent;FN=PROJECT/'fnv_decomp'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def screen_reasons(kind,new,old,src,occurrences,recipe_count,data,includes,source_exists):
    reasons=[]
    if occurrences.get(new):reasons.append('native_name_mentioned_in_source_or_include')
    if occurrences.get(old,set())!={src}:reasons.append('synthetic_name_not_confined_to_unit_source')
    if recipe_count!=1:reasons.append('source_recipe_count_not_one')
    if not source_exists:reasons.append('source_missing')
    decl=re.findall(rb'\b(class|struct)\s+'+old.encode()+rb'\s*:',data)
    if len(decl)!=1:reasons.append('one_simple_derived_declaration_not_found')
    elif (decl[0]==b'class')!=(kind=='V'):reasons.append('class_struct_discriminator_differs')
    if any(x.startswith('"') for x in includes):reasons.append('local_include_closure_requires_review')
    return reasons


def main():
    inv=json.loads((HERE/'rtti_alias_inventory.json').read_text());units_path=FN/'build/units.json'
    if sha(units_path)!=inv['inputs']['units_sha256']:raise ValueError('unit recipe changed since inventory')
    groups=collections.defaultdict(list)
    for row in inv['groups']:
        name=re.fullmatch(r'\.\?A([VU])([A-Za-z_][A-Za-z_0-9]*)@@',row['reference_type_name'])
        if not name or len(row['synthetic_simple_vtable_symbols'])!=1:continue
        old=row['synthetic_simple_vtable_symbols'][0][4:].split('@@')[0]
        aliases=next(x for x in row['unit_symbol_aliases'] if x['symbol']==row['synthetic_simple_vtable_symbols'][0])
        for src in aliases['sources']:
            groups[(name.group(1),name.group(2),old,src)].append(row)
    identifiers=sorted({x for key in groups for x in (key[1],key[2])},key=lambda x:(-len(x),x))
    with tempfile.TemporaryDirectory(prefix='rtti_screen_') as tmp:
        pattern=Path(tmp)/'tokens.regex';pattern.write_text(r'\b(?:'+'|'.join(map(re.escape,identifiers))+r')\b',encoding='utf8')
        cmd=['rg','--json','--no-ignore','-f',str(pattern),'src','include','-g','*.cpp','-g','*.h','-g','*.hpp','-g','*.inl']
        proc=subprocess.Popen(cmd,cwd=FN,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf8',errors='replace')
        occurrences=collections.defaultdict(set)
        for line in proc.stdout:
            e=json.loads(line)
            if e.get('type')!='match':continue
            data=e['data'];path=data['path']['text'].replace('\\','/')
            for match in data['submatches']:occurrences[match['match']['text']].add(path)
        err=proc.stderr.read();rc=proc.wait()
        if rc not in (0,1):raise RuntimeError('source scan failed: '+err)
    manifest=json.loads((M3/'out/batch8-promoted-default-verified/evidence/m3_manifest.json').read_text())['entries']
    pieces=json.loads((M3/'out/batch8-promoted-default-verified/evidence/dv1_pieces.json').read_text())['pieces']
    unit_rows=json.loads(units_path.read_text())['units'];unit_sources=collections.Counter(u.get('source') for u in unit_rows)
    rows=[]
    for (kind,new,old,src),entries in sorted(groups.items()):
        path=FN/src; data=path.read_bytes() if path.is_file() else b''
        includes=[x.decode('latin1') for x in re.findall(rb'^\s*#\s*include\s*([^\r\n]+)',data,re.M)]
        reasons=screen_reasons(kind,new,old,src,occurrences,unit_sources[src],data,includes,path.is_file())
        descriptors={r['type_descriptor_va'] for r in entries}; owners=[]
        for address in sorted(descriptors):
            m=[{'name':x['name'],'kind':x['tc'],'va':x['va'],'size':x['size']} for x in manifest if x['va']<=address<x['va']+x['size']]
            d=[{'kind':x['kind'],'va':x['va'],'size':x['size']} for x in pieces if x['va']<=address<x['va']+x['size']]
            owners.append({'descriptor_va':address,'m3':m,'dv1':d})
        rows.append({'reference_name':new,'reference_discriminator':'class' if kind=='V' else 'struct','synthetic_name':old,'unit_source':src,
          'unit_source_sha256':sha(path) if path.is_file() else None,'unit_recipe_count':unit_sources[src],
          'source_files_mentioning_native_name':sorted(occurrences[new]),'source_files_mentioning_synthetic_name':sorted(occurrences[old]),
          'unit_include_directives':includes,'vtable_vas':sorted({r['vtable_va'] for r in entries}),'descriptor_owners':owners,
          'screen_status':'review_candidate' if not reasons else 'deferred','reasons':reasons,
          'caveat':'Lexical screen and reference-assisted vtable addresses do not prove class identity, inheritance, virtual slots or safe integration; system-header collisions are not excluded.'})
    counts=collections.Counter(r['screen_status'] for r in rows);reasons=collections.Counter(x for r in rows for x in r['reasons'])
    result={'schema_version':1,'scope':'Conservative lexical candidate screen; no byte-recovery or ABI claims.',
       'input_sha256':{'units':inv['inputs']['units_sha256'],'alias_inventory':sha(HERE/'rtti_alias_inventory.json'),'m3_manifest':sha(M3/'out/batch8-promoted-default-verified/evidence/m3_manifest.json'),'dv1_pieces':sha(M3/'out/batch8-promoted-default-verified/evidence/dv1_pieces.json')},
       'stats':{'candidate_groups':len(rows),'status':dict(counts),'reason_counts_nonexclusive':dict(reasons)},'groups':rows}
    output=HERE/'rtti_scalable_candidates.json'
    with output.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result['stats']));print('candidates',[(r['reference_name'],r['synthetic_name'],r['unit_source']) for r in rows if r['screen_status']=='review_candidate'])

if __name__=='__main__':main()
