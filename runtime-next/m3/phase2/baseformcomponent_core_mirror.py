"""Materialize one pinned BFC cohort mirror for later exclusive-lane compilation."""
import argparse,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';S=M/'out/phase2-baseformcomponent-core';PIN='93f5e6c6392d35a3524cbf78ebcfbf9fba27ad83607f7617f82c7697449e32ec';D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',required=True,type=int);a=ap.parse_args();raw=(S/'manifest.json').read_bytes()
 if sha(raw)!=PIN:raise ValueError('cohort manifest changed')
 m=json.loads(raw);units=(F/'build/units.json').read_bytes()
 if sha(units)!=D:raise ValueError('recipe changed')
 rows=[x for x in m['units'] if x['unit']==a.unit]
 if len(rows)!=1:raise ValueError('unit is not in reviewed cohort')
 row=rows[0];overrides={}
 for x in m['files']:
  data=(S/x['generated']).read_bytes()
  if sha(data)!=x['new_sha256']:raise ValueError('staged payload changed')
  overrides[x['path']]=data
 out=M/('out/phase2-bfc-core-u%04d'%a.unit)
 if out.exists():raise FileExistsError('refusing overwrite')
 for name,digest in row['original']['files'].items():
  if sha((F/name).read_bytes())!=digest:raise ValueError('original include changed '+name)
 out.mkdir()
 for tag in ('original','candidate'):
  for name,digest in row[tag]['files'].items():
   data=overrides[name] if tag=='candidate' and name in overrides else (F/name).read_bytes()
   if sha(data)!=digest:raise ValueError('mirror content changed '+name)
   path=out/tag/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 manifest={'schema_version':1,'source':row['source'],'units_sha256':D,'reviewed_units_sha256':m['base_units_sha256'],'bfc_cohort_manifest_sha256':PIN,'original_inputs':row['original']['files'],'overrides':{k:sha(v) for k,v in overrides.items() if k in row['candidate']['files']},'original':row['original'],'candidate':row['candidate'],'production_include_order':['/I<mirror>/include'],'limits':m['limits']}
 (out/'mirror-manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps({'unit':a.unit,'source':row['source'],'functions':len(row['functions']),'original_files':len(row['original']['files']),'candidate_files':len(row['candidate']['files'])}))
if __name__=='__main__':main()
