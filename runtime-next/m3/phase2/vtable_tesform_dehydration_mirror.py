"""Materialize one affected-unit mirror from pinned dehydration getter cohort."""
import argparse,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';S=M/'out/phase2-tesform-dehydration-getters-v2';C=M/'out/phase2-tesform-dehydration-cohort-v2';PIN='b9802ebc7d45c8082fc41e86e57497a983cf5c060c8f0b0c17bab485c3086ed6';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--unit',required=True,type=int);a=p.parse_args();raw=(C/'manifest.json').read_bytes()
 if sha(raw)!=PIN or sha((F/'build/units.json').read_bytes())!=BASE:raise ValueError('cohort or recipe changed')
 m=json.loads(raw);rows=[x for x in m['units'] if x['unit']==a.unit]
 if len(rows)!=1:raise ValueError('unit absent from cohort')
 r=rows[0];names={'src/fallout_shared/bgsdehydration.cpp':'bgsdehydration.cpp','include/TESForm.h':'include__TESForm.h','src/fallout_shared/tesform_TESForm.h':'src__fallout_shared__tesform_TESForm.h','src/bgsencounterzone_TESForm.h':'src__bgsencounterzone_TESForm.h','src/fallout_shared/TESForm.h':'src__fallout_shared__TESForm.h'}
 overrides={n:(S/p).read_bytes() for n,p in names.items()}
 for n,b in overrides.items():
  if sha(b)!=m['overrides'][n]:raise ValueError('candidate changed '+n)
 out=M/('out/phase2-tesform-dehydration-u%04d'%a.unit)
 if out.exists():raise FileExistsError('no overwrite')
 for n,d in r['original']['files'].items():
  if sha((F/n).read_bytes())!=d:raise ValueError('source closure changed '+n)
 out.mkdir()
 for tag in ('original','candidate'):
  for n,d in r[tag]['files'].items():
   data=overrides[n] if tag=='candidate' and n in overrides else (F/n).read_bytes()
   if sha(data)!=d:raise ValueError('mirror data changed '+n)
   path=out/tag/n;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 manifest={'schema_version':1,'source':r['source'],'units_sha256':BASE,'cohort_manifest_sha256':PIN,'unit_index':a.unit,'compiler':r['compiler'],'flags':r['flags'],'original_inputs':r['original']['files'],'overrides':{n:sha(v) for n,v in overrides.items() if n in r['candidate']['files']},'original':r['original'],'candidate':r['candidate'],'production_include_order':['/I<mirror>/include'],'limits':m['limits']}
 (out/'mirror-manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'unit':a.unit,'source':r['source'],'compiler':r['compiler'],'functions':r['functions'],'files':len(r['candidate']['files'])}))
if __name__=='__main__':main()
