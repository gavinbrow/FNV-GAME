"""Strictly replay captured owner functions without compiling or rebinding."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';D=R/'phase2-watershader-211-owner-v2-capture';Q=R/'phase2-nimem-psys-pointer-binding-v1';O=D/'strict-owner-replay.json';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve proof')
 if sha(D/'manifest.json')!='0c1a42787fa3bfd556904d4a47d14ec6ebadfd503e42da0f7a1b9724017fb7c4' or sha(Q/'units.generated')!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad' or sha(Path(paths.REF_IMAGE))!='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7':raise ValueError('pinned input changed')
 m=json.loads((D/'manifest.json').read_text());u=json.loads((Q/'units.generated').read_text())['units'];pe=Pe(paths.REF_IMAGE);out={}
 for i,addr in ((47,'0x00404ee0'),(781,'0x00404f70')):
  row=next(x for x in m['objects'] if x['unit']==i);obj=D/('%04d.obj'%i)
  if sha(obj)!=row['object_sha256_start'] or row['object_sha256_start']!=row['object_sha256_end']:raise ValueError('capture differs')
  rows=compare(Coff(str(obj)),pe,u[i]);target=next(x for x in rows if x['address']==addr)
  out[str(i)]={'object_sha256':sha(obj),'source':row['source'],'target':target,'strict_matches':sum(x['verdict']=='match' for x in rows),'functions':len(rows),'failures':[{'address':x['address'],'errors':x['errors']} for x in rows if x['verdict']!='match']}
 if u[47]['symbols'].get('?Leave@AutoMemContext@@QAEXXZ')!='0x00404f70':raise ValueError('source owner Leave mapping changed')
 O.write_text(json.dumps({'capture_manifest_sha256':sha(D/'manifest.json'),'reference_sha256':sha(Path(paths.REF_IMAGE)),'owners':out,'limits':['actual object/source capture does not establish linked final ownership','unit781 is a differently named surrogate for source-defined Leave behavior; class identity and ODR remain separate']},indent=2));print(json.dumps({'targets':{k:v['target']['verdict'] for k,v in out.items()},'totals':{k:[v['strict_matches'],v['functions']] for k,v in out.items()},'sha256':sha(O)}))
if __name__=='__main__':main()
