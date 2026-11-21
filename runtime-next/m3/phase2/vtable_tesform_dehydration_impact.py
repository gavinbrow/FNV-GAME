"""Inventory static include/call impact of TESForm getter signature candidate."""
import hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';sys.path.insert(0,str(H));import rtti_mirror_prepare as w
OUT=M/'out/phase2-tesform-dehydration-impact.json';U=F/'build/units.json';TARGETS={'include/TESForm.h','src/fallout_shared/tesform_TESForm.h','src/bgsencounterzone_TESForm.h'}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('no overwrite')
 raw=U.read_bytes();units=json.loads(raw)['units'];hits=[];errors=[];source_cache={}
 for i,u in enumerate(units):
  src=u['source']
  try:
   if src not in source_cache:
    graph=w.walk(F,src,{});source_cache[src]=graph
   g=source_cache[src];found=sorted(TARGETS & set(g['files']))
   if found:hits.append({'index':i,'source':src,'headers':found,'unresolved_include_count':len(g['unresolved'])})
  except (OSError,ValueError) as e:errors.append({'index':i,'source':src,'reason':type(e).__name__+': '+str(e)})
 if sha(U.read_bytes())!=sha(raw):raise ValueError('recipe changed during audit')
 # Search exact syntax over recipe sources and captured project headers; no unbounded directory recursion.
 paths={x['source'] for x in units}
 for g in source_cache.values():paths.update(g['files'])
 declarations=[];calls=[];pat=re.compile(r'\bUnk_2D\s*\(');decl=re.compile(r'\b(?:virtual\s+)?bool\s+Unk_2D\s*\(')
 for n in sorted(paths):
  p=F/n
  if not p.is_file():continue
  try:lines=p.read_text(encoding='utf8',errors='replace').splitlines()
  except OSError:continue
  for i,line in enumerate(lines,1):
   if pat.search(line):
    row={'path':n,'line':i,'class':'declaration' if decl.search(line) else 'other-use'}
    (declarations if row['class']=='declaration' else calls).append(row)
 out={'scope':'syntactic quoted-include graph over recipe source files, not a preprocessor trace or full C++ type-resolution proof','recipe_sha256':sha(raw),'units_total':len(units),'unique_source_files':len(source_cache),'affected_units':hits,'walk_errors':errors,'declarations':declarations,'other_textual_uses':calls,'limitations':['conditional/macro includes and actual compiler header search can differ','textual call classification does not establish receiver type','non-recipe source variants and external consumers are not covered','all affected object behavior and global ODR require independent validation']}
 OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'affected_units':len(hits),'walk_errors':len(errors),'declarations':len(declarations),'other_uses':len(calls)}))
if __name__=='__main__':main()
