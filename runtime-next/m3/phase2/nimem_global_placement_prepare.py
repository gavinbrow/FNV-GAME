"""Create one combined-kind/API mirror with the scoped placement hypothesis."""
import argparse,hashlib,json,sys
from pathlib import Path
import baseformcomponent_core_stage as core
import nimem_combined_825d_prepare as base
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';P=M/'out/phase2-nimem-combined-825d';Q=M/'out/phase2-nimem-global-placement-v2'
QP='085f79dfe40efd9276219ed27320f8761d77dc17fff7e979fd088882b9403678';UNITS={200,1203,1271,1598}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--unit',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.unit not in UNITS or sha((Q/'manifest.json').read_bytes())!=QP:raise ValueError('unreviewed unit or placement payload')
 cm=json.loads((P/'manifest.json').read_bytes());qm=json.loads((Q/'manifest.json').read_bytes());row=next(x for x in cm['combined_api_units'] if x['unit']==a.unit);file=next(x for x in qm['files'] if x['path']==row['source'])
 if sha((F/row['source']).read_bytes())!=file['before_sha256']:raise ValueError('placement preimage changed')
 b=(Q/'payload'/row['source']).read_bytes()
 if sha(b)!=file['after_sha256']:raise ValueError('placement payload changed')
 ov={}
 for rel,h in cm['source_payload_sha256'].items():
  data=(P/'payload'/rel).read_bytes()
  if sha(data)!=h:raise ValueError('combined payload changed')
  ov[rel]=data
 ov[row['source']]=b;candidate=core.walk(F,row['source'],ov)
 saved=sys.argv;sys.argv=[saved[0],'--unit',str(a.unit),'--out',str(a.out)]
 try:base.main()
 finally:sys.argv=saved
 q=a.out/'candidate'/row['source'];q.write_bytes(b);mp=a.out/'mirror-manifest.json';m=json.loads(mp.read_text());m['candidate']=candidate;m['placement_manifest_sha256']=QP;m['limits'].append('scoped global-placement hypothesis; reference, EH and actual emission still require proof');mp.write_text(json.dumps(m,indent=2))
if __name__=='__main__':main()
