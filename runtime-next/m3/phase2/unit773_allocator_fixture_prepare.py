"""Prepare 773 pair from the pinned composed-source mirror; no compilation."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';B=M/'out/phase2-nimem-next-source-composed-u0773';P=M/'out/phase2-unit773-allocator-generated';O=M/'out/phase2-unit773-allocator-fixture';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError(O)
 if sha(P/'manifest.json')!='2cdb1e6d703f812c729931181ea730b7be3bdd157232fe0b5b4e38dfceab52e2' or sha(B/'mirror-manifest.json')!='a1bc491c5ea5eb5b60a350b48502c564b452d43b0289fe752980c503ea3115dd':raise ValueError('input drift')
 p=json.loads((P/'manifest.json').read_text());b=json.loads((B/'mirror-manifest.json').read_text());source=b['candidate'];rel=p['changed_source'];assert source==p['parent_closure'] and b['unit']==773 and len(p['functions'])==39
 for name,digest in b['original_inputs'].items():
  if sha(F/name)!=digest:raise ValueError('live input drift '+name)
 for name,digest in source['files'].items():
  if sha(B/'candidate'/name)!=digest:raise ValueError('saved mirror drift '+name)
 if sha(P/'payload'/rel)!=p['after_sha256']:raise ValueError('candidate drift')
 O.mkdir()
 for tag in ('original','candidate'):
  for name,digest in source['files'].items():
   data=(P/'payload'/rel).read_bytes() if tag=='candidate' and name==rel else (B/'candidate'/name).read_bytes();q=O/tag/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 candidate=json.loads(json.dumps(source));candidate['files'][rel]=p['after_sha256'];assert candidate==p['candidate_closure']
 mm={'unit':773,'source':p['source'],'units_sha256':b['units_sha256'],'proposal_sha256':sha(P/'manifest.json'),'prior_mirror_sha256':sha(B/'mirror-manifest.json'),'original_inputs':b['original_inputs'],'original':source,'candidate':candidate,'production_include_order':['/I<mirror>/include']};(O/'mirror-manifest.json').write_text(json.dumps(mm,indent=2)+'\n');print(sha(O/'mirror-manifest.json'))
if __name__=='__main__':main()
