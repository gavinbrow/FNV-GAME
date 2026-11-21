"""Build an evidence-only lexical class/recipe/include registry from local sources."""
import collections,hashlib,json,os,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;M3=HERE.parent;PROJECT=M3.parent.parent;FN=PROJECT/'fnv_decomp';OUT=M3/'out/phase2-rtti-class-registry'
SCRUB=re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
DECL=re.compile(r'\b(class|struct)\s+([A-Za-z_]\w*)\s*(?:\:\s*[^;{}]*?)?\{')
INCLUDE=re.compile(r'^\s*#\s*include\s*"([^"\r\n]+)"',re.M)


def clean(s):
    return SCRUB.sub(lambda m:''.join('\n' if c=='\n' else ' ' for c in m.group()),s)


def without_comments(s):
    return SCRUB.sub(lambda m: ''.join('\n' if c=='\n' else ' ' for c in m.group())
                     if m.group().startswith(('//','/*')) else m.group(),s)


def definitions(text,wanted):
    """Lexical balanced class bodies only; namespace/conditional state remains unknown."""
    cleaned=clean(text)
    for m in DECL.finditer(cleaned):
        name=m.group(2)
        if name not in wanted:continue
        depth=1;i=m.end()
        while depth and i<len(cleaned):
            if cleaned[i]=='{':depth+=1
            elif cleaned[i]=='}':depth-=1
            i+=1
        if depth:continue
        tokens=re.findall(r'[A-Za-z_]\w*|\d+|\S',cleaned[m.start():i])
        yield {'name':name,'keyword':m.group(1),'line':cleaned.count('\n',0,m.start())+1,
               'lexical_token_sha256':hashlib.sha256('\x1f'.join(tokens).encode()).hexdigest()}


def main():
    census_path=M3/'out/phase2-class-census/census-v2.json';census=json.loads(census_path.read_text());units_path=FN/'build/units.json';raw=units_path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=census['inputs']['units_sha256']:raise ValueError('unit recipe hash differs from census')
    units=json.loads(raw)['units'];wanted={c['simple_identifier'] for c in census['classes'] if c['simple_identifier']}
    files=[]
    for root in (FN/'src',FN/'include'):
        for directory,dirs,names in os.walk(root,followlinks=False):
            files.extend(Path(directory)/n for n in names if Path(n).suffix.lower() in ('.cpp','.h','.hpp','.inl'))
    files=sorted(files);data={};occ=collections.defaultdict(list)
    for p in files:
        text=p.read_text(encoding='utf-8-sig',errors='replace');rel=p.relative_to(FN).as_posix();data[rel]=text
        for d in definitions(text,wanted):d['path']=rel;occ[d.pop('name')].append(d)
    available={str((FN/k).resolve()).casefold():k for k in data};edges={};missing=collections.Counter()
    for rel,text in data.items():
        parents=[]
        for include in INCLUDE.findall(without_comments(text)):
            choices=[(FN/rel).parent/include,FN/'include'/include]
            target=next((available[str(x.resolve()).casefold()] for x in choices if str(x.resolve()).casefold() in available),None)
            if target:parents.append(target)
            else:missing[include]+=1
        edges[rel]=parents
    users=collections.defaultdict(set)
    for i,u in enumerate(units):
        root=u.get('source');stack=[root];visited=set()
        while stack:
            n=stack.pop()
            if n in visited or n not in edges:continue
            visited.add(n);users[n].add(i);stack.extend(edges[n])
    grouped=collections.defaultdict(list)
    for c in census['classes']:
        if c['simple_identifier']:grouped[c['simple_identifier']].append(c)
    rows=[]
    for name,types in sorted(grouped.items()):
        defs=occ[name]
        for d in defs:
            u=sorted(users[d['path']]);d['reachable_unit_count']=len(u);d['reachable_unit_indexes']=u
        fingerprints={d['lexical_token_sha256'] for d in defs};keywords={d['keyword'] for d in defs}
        rows.append({'name':name,'reference_types':[{'type_descriptor_va':t['type_descriptor_va'],'type_name':t['type_name'],'vtable_vas':t['observed_vtables']} for t in types],
                     'definitions':defs,'lexical_definition_count':len(defs),'distinct_token_fingerprints':len(fingerprints),'definition_keywords':sorted(keywords),
                     'status':'no_lexical_definition' if not defs else 'multiple_lexical_definitions' if len(defs)>1 else 'single_lexical_definition',
                     'caveat':'Lexical only: comments and literals are masked; namespaces, preprocessor branches, macro expansion, packing, ABI, access and full include flags are not evaluated. Matching fingerprints are not ABI or ODR proof.'})
    stats=collections.Counter(x['status'] for x in rows)
    report={'schema_version':1,'scope':'Private source/recipe/include lexical evidence registry; not class identity, ODR safety, virtual-slot completeness or coverage proof.',
      'inputs':{'census_sha256':hashlib.sha256(census_path.read_bytes()).hexdigest(),'units_sha256':hashlib.sha256(raw).hexdigest()},
      'stats':{'source_files_scanned':len(files),'simple_identifier_groups':len(rows),'status':dict(stats),'unresolved_quoted_include_names':len(missing)},
      'unresolved_quoted_includes':dict(missing),'classes':rows}
    OUT.mkdir(parents=False,exist_ok=False)
    with (OUT/'class-registry.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report['stats']))

if __name__=='__main__':main()
