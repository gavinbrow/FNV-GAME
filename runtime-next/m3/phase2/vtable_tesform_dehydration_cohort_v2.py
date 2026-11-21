"""Pin affected TESForm getter cohort and both syntactic include closures."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';S=M/'out/phase2-tesform-dehydration-getters-v2';O=M/'out/phase2-tesform-dehydration-cohort-v2';U=F/'build/units.json';AUDIT=M/'out/phase2-tesform-dehydration-impact-v2.json';sys.path.insert(0,str(H));import rtti_mirror_prepare as walk
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('refusing overwrite')
 raw=U.read_bytes();meta=json.loads((S/'manifest.json').read_bytes());audit=json.loads(AUDIT.read_bytes())
 if sha(raw)!=BASE or audit['recipe_sha256']!=BASE or meta['input_sha256']['build/units.json']!=BASE:raise ValueError('recipe mismatch')
 units=json.loads(raw)['units'];overrides={'src/fallout_shared/bgsdehydration.cpp':(S/'bgsdehydration.cpp').read_bytes(),'include/TESForm.h':(S/'include__TESForm.h').read_bytes(),'src/fallout_shared/tesform_TESForm.h':(S/'src__fallout_shared__tesform_TESForm.h').read_bytes(),'src/bgsencounterzone_TESForm.h':(S/'src__bgsencounterzone_TESForm.h').read_bytes(),'src/fallout_shared/TESForm.h':(S/'src__fallout_shared__TESForm.h').read_bytes()}
 mapping={'src/fallout_shared/bgsdehydration.cpp':'bgsdehydration.cpp','include/TESForm.h':'include__TESForm.h','src/fallout_shared/tesform_TESForm.h':'src__fallout_shared__tesform_TESForm.h','src/bgsencounterzone_TESForm.h':'src__bgsencounterzone_TESForm.h','src/fallout_shared/TESForm.h':'src__fallout_shared__TESForm.h'}
 for n,b in overrides.items():
  if sha(b)!=meta['outputs'][mapping[n]] or sha((F/n).read_bytes())!=meta['input_sha256'][n]:raise ValueError('candidate/input mismatch '+n)
 indices=sorted(x['index'] for x in audit['affected_units'])
 if len(indices)!=204 or len(set(indices))!=204 or not {2,633,998}<=set(indices):raise ValueError('affected cohort changed')
 rows=[]
 for i in indices:
  u=units[i];old=walk.walk(F,u['source'],{});new=walk.walk(F,u['source'],overrides);changed=[n for n in overrides if n in new['files']]
  if not changed:raise ValueError('candidate not reached '+str(i))
  rows.append({'unit':i,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'functions':len(u['functions']),'eh_tails':len(u.get('eh_tails',[])),'changed_paths':changed,'original':old,'candidate':new})
 excluded=[]
 for x in audit['walk_errors']:
  source=x['source']
  if not source.startswith('third_party/zlib-1.2.1/'):raise ValueError('unexpected unclassified unit')
  data=(F/source).read_bytes()
  if b'TESForm' in data or b'bgsencounterzone' in data.lower():raise ValueError('third-party lexical exclusion failed')
  excluded.append({'unit':x['index'],'source':source,'sha256':sha(data),'reason':'third-party C source contains no direct TESForm spelling; transitive includes not classified'})
 if len(excluded)!=9 or sha(U.read_bytes())!=BASE:raise ValueError('input changed or exclusions differ')
 O.mkdir();result={'schema_version':1,'scope':'syntactic candidate include cohort only; actual compiler traces and all-function/EH comparison required','recipe_sha256':BASE,'candidate_manifest_sha256':sha((S/'manifest.json').read_bytes()),'impact_sha256':sha(AUDIT.read_bytes()),'overrides':{k:sha(v) for k,v in overrides.items()},'units':rows,'third_party_excluded':excluded,'limits':['quoted include walk is conservative syntactic approximation; conditional/macro include effects and compiler search order require showIncludes','other TESForm views/ODR/callers unresolved','candidate global header may affect more TUs than syntactic cohort','no objects compiled; full function, EH and image gates remain']}
 (O/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'units':len(rows),'functions':sum(x['functions'] for x in rows),'eh_tails':sum(x['eh_tails'] for x in rows),'third_party_excluded':len(excluded)}))
if __name__=='__main__':main()
