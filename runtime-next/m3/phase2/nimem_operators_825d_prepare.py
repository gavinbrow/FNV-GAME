"""Build one minimal 825d native-operator consumer mirror on demand."""
import argparse,hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-nimem-operators-825d';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PIN='7689a05cc64e094a726f8d8261378e4cdcbad790f7b05a73295a4439d01da4bf'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--unit',type=int,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.resolve();raw=(F/'build/units.json').read_bytes();mr=(P/'manifest.json').read_bytes()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private path required')
 if sha(raw)!=BASE or sha(mr)!=PIN:raise ValueError('recipe/manifest changed')
 m=json.loads(mr);u=json.loads(raw)['units'];row=next((x for x in m['units'] if x['unit']==a.unit),None)
 if row is None or row['source']!=u[a.unit]['source'] or row['functions']!=u[a.unit]['functions'] or row['flags']!=u[a.unit]['flags']:raise ValueError('unit scope differs')
 ov={}
 for rel,h in m['source_payload_sha256'].items():
  b=(P/'payload'/rel).read_bytes()
  if sha(b)!=h:raise ValueError('payload differs '+rel)
  ov[rel]=b
 original=core.walk(F,row['source'],{});candidate=core.walk(F,row['source'],ov)
 if original!=row['original'] or candidate!=row['candidate']:raise ValueError('closure changed')
 out.mkdir(parents=True)
 for tag,g in (('original',original),('candidate',candidate)):
  for rel,digest in g['files'].items():
   b=ov[rel] if tag=='candidate' and rel in ov else (F/rel).read_bytes()
   if sha(b)!=digest:raise ValueError('input changed')
   q=out/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 mm={'schema_version':1,'source':row['source'],'unit':a.unit,'units_sha256':BASE,'proposal_manifest_sha256':PIN,'original_inputs':original['files'],'original':original,'candidate':candidate,'production_include_order':['/I<mirror>/include'],'limits':['private operator API hypothesis; all consumer code and weak sections require review']};(out/'mirror-manifest.json').write_text(json.dumps(mm,indent=2));print(json.dumps({'unit':a.unit,'original_files':len(original['files']),'candidate_files':len(candidate['files'])}))
if __name__=='__main__':main()
