"""Prepare a pinned private unit149/194 source-closure mirror."""
import argparse,hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';P=M/'out/phase2-nimem-149-194-sized-eh-v1';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PIN='dca9aece504241d985be62def30a1e2eb67ad08cf2bab3dc9eac8ee167fa0948'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();raw=(F/'build/units.json').read_bytes();data=(P/'manifest.json').read_bytes()
 if out.exists() or not out.is_relative_to((M/'out').resolve()) or sha(raw)!=BASE or sha(data)!=PIN:raise ValueError('input or output differs')
 m=json.loads(data);r=next(x for x in m['units'] if x['unit']==a.unit);u=json.loads(raw)['units'][a.unit]
 if any(r[k]!=u[k] for k in ('source','compiler','flags','functions')) or r['eh_tails']!=u.get('eh_tails',[]):raise ValueError('unit recipe differs')
 ov={}
 for rel,h in m['source_payload_sha256'].items():
  b=(P/'payload'/rel).read_bytes()
  if sha(b)!=h:raise ValueError('payload changed')
  ov[rel]=b
 original=core.walk(F,r['source'],{});candidate=core.walk(F,r['source'],ov)
 if original!=r['original'] or candidate!=r['candidate']:raise ValueError('closure changed')
 out.mkdir(parents=True)
 for tag,g in (('original',original),('candidate',candidate)):
  for rel,h in g['files'].items():
   b=ov[rel] if tag=='candidate' and rel in ov else (F/rel).read_bytes()
   if sha(b)!=h:raise ValueError('input changed')
   q=out/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 mm={'schema_version':1,'source':r['source'],'unit':a.unit,'units_sha256':BASE,'proposal_manifest_sha256':m['composed_manifest_sha256'],'sized_eh_manifest_sha256':PIN,'original_inputs':original['files'],'original':original,'candidate':candidate,'production_include_order':['/I<mirror>/include'],'limits':m['limits']};(out/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
if __name__=='__main__':main()
