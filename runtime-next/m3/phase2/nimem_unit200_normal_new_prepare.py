"""Private unit200 normal-new hypothesis using existing combined NiMem view."""
import argparse,hashlib,json,sys
from pathlib import Path
import baseformcomponent_core_stage as core
import nimem_combined_825d_prepare as base
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';P=M/'out/phase2-nimem-combined-825d';Q=M/'out/phase2-nimem-global-placement-v2';REL='src/bsshader/speedtreeleafshader.cpp';PIN='085f79dfe40efd9276219ed27320f8761d77dc17fff7e979fd088882b9403678';sha=lambda x:hashlib.sha256(x).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if not a.out.resolve().is_relative_to((M/'out').resolve()) or a.out.exists() or sha((Q/'manifest.json').read_bytes())!=PIN:raise ValueError('output or baseline')
 cm=json.loads((P/'manifest.json').read_bytes());qm=json.loads((Q/'manifest.json').read_bytes());entry=next(x for x in qm['files'] if x['path']==REL);b=(Q/'payload'/REL).read_bytes()
 if sha(b)!=entry['after_sha256'] or sha((F/REL).read_bytes())!=entry['before_sha256']:raise ValueError('source identity')
 old=b'::new ((FadeTag*)0) SpeedTreeLeafShader';new=b'new SpeedTreeLeafShader'
 if b.count(old)!=1:raise ValueError('site anchor')
 b=b.replace(old,new);ov={}
 for rel,h in cm['source_payload_sha256'].items():
  data=(P/'payload'/rel).read_bytes()
  if sha(data)!=h:raise ValueError('combined payload changed')
  ov[rel]=data
 ov[REL]=b;candidate=core.walk(F,REL,ov);saved=sys.argv;sys.argv=[saved[0],'--unit','200','--out',str(a.out)]
 try:base.main()
 finally:sys.argv=saved
 q=a.out/'candidate'/REL;q.write_bytes(b);mp=a.out/'mirror-manifest.json';m=json.loads(mp.read_text());m['candidate']=candidate;m['placement_manifest_sha256']=PIN;m['limits'].append('private normal-new hypothesis; sized-delete EH and whole unit must be proven');mp.write_text(json.dumps(m,indent=2));print(json.dumps({'candidate_sha256':sha(b),'files':len(candidate['files'])}))
if __name__=='__main__':main()
