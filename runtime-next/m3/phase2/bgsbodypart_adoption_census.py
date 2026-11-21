"""Bounded source/include census for five BGSBodyPart-related native names."""
import collections,hashlib,json,re,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;F=ROOT/'fnv_decomp';OUT=M/'out/phase2-bgsbodypart-adoption-census'
NAMES=('FileEntryList','TESModel','TESModelPSA','BodyPartInfo','BGSBodyPart')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 unitsraw=(F/'build/units.json').read_bytes();units=json.loads(unitsraw)['units'];files=[]
 for base in (F/'src',F/'include'):
  rows=subprocess.run(['rg','--files',str(base),'-g','*.cpp','-g','*.h'],capture_output=True,text=True,check=True).stdout.splitlines()
  files.extend(Path(x).resolve() for x in rows)
 file_set=set(files);defs={};edges={};unresolved={};pattern=re.compile(rb'\b(?:class|struct)\s+(' + b'|'.join(n.encode() for n in NAMES)+rb')\s*(?:\:[^;{}]+)?\s*\{')
 for p in files:
  b=p.read_bytes();hits=[]
  for m in pattern.finditer(b):hits.append({'name':m.group(1).decode(),'line':b.count(b'\n',0,m.start())+1})
  if hits:defs[p]=hits
  links=[];miss=[]
  for name in re.findall(rb'^\s*#\s*include\s*"([^"\r\n]+)"',b,re.M):
   try:n=name.decode('ascii')
   except UnicodeDecodeError:continue
   choices=[(p.parent/n).resolve(),(F/'src'/n).resolve(),(F/'src/fallout_shared'/n).resolve(),(F/'include'/n).resolve()]
   found=[q for q in choices if q in file_set]
   if found:links.extend(found)
   else:miss.append(n)
  edges[p]=set(links)
  if miss:unresolved[p]=sorted(set(miss))
 def rel(p):return p.relative_to(F.resolve()).as_posix()
 byunit=[]
 for i,u in enumerate(units):
  start=(F/u['source']).resolve()
  if start not in file_set:continue
  todo=[start];seen=set()
  while todo:
   p=todo.pop()
   if p in seen:continue
   seen.add(p);todo.extend(edges.get(p,()))
  relevant=[{'path':rel(p),'definitions':defs[p]} for p in sorted(seen,key=str) if p in defs]
  if relevant:
   names=collections.Counter(x['name'] for row in relevant for x in row['definitions'])
   byunit.append({'unit':i,'source':u['source'],'files':relevant,'name_counts':dict(names),'ambiguous_possible':any(n>1 for n in names.values()),'unresolved_quoted_include_count':sum(len(unresolved.get(p,())) for p in seen)})
 results={'scope':'lexical overapproximation: all existing quoted-include search candidates, not preprocessed compiler trace; comments/macros may produce false definition hits',
          'units_sha256':sha(unitsraw),'name_definition_files':{n:sum(any(x['name']==n for x in v) for v in defs.values()) for n in NAMES},
          'affected_recipe_units':len(byunit),'units_with_possible_duplicate_names':sum(x['ambiguous_possible'] for x in byunit),
          'definition_files':[{'path':rel(p),'sha256':sha(p.read_bytes()),'definitions':v} for p,v in sorted(defs.items(),key=lambda x:str(x[0]))],
          'units':byunit}
 OUT.mkdir(exist_ok=False);(OUT/'census.json').write_text(json.dumps(results,indent=2),encoding='utf8')
 print(json.dumps({k:results[k] for k in ('name_definition_files','affected_recipe_units','units_with_possible_duplicate_names')}))
if __name__=='__main__':main()
