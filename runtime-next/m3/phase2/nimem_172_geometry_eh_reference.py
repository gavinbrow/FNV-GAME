"""Check original unit172 geometry allocation and source-owned cleanup facts."""
import hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';O=R/'phase2-nimem-172-geometry-eh-reference.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve proof')
 owner=R/'phase2-nimem-unit200-normal-new-v3/source-owner-replay.json';recipe=R/'phase2-nimem-psys-pointer-binding-v1/units.generated';obj=R/'phase2-nimem-combined-825d-run/unit-0172/candidate.obj'
 if sha(owner)!='6acfb2049b12049418545c7dc8b813735b1341c134baaf5c9d4580a06db59af3' or sha(recipe)!='5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad':raise ValueError('input changed')
 u=json.loads(recipe.read_text())['units'][172];c=Coff(str(obj));pe=Pe(paths.REF_IMAGE);r=compare(c,pe,u);parent=next(x for x in r if x['address']=='0x00b8c3b0');f=next(x for x in u['functions'] if x['address']==parent['address']);data,rel=relocated(c,f['symbol'],f['size'],{})
 if parent['verdict']!='match' or data[164:169]!=b'\x68\xc4\x00\x00\x00' or not any(x[0]==175 and x[2]=='?FUN_00aa13e0@@YAPAXI@Z' for x in rel):raise ValueError('normal allocation proof differs')
 va=0xf2954f;d=pe.read(va,14)
 if d[:5]!=b'\x68\xc4\x00\x00\x00' or d[9]!=0xe8 or ((va+14+struct.unpack_from('<i',d,10)[0])&0xffffffff)!=0xaa1460:raise ValueError('cleanup proof differs')
 j={'candidate_object_sha256':sha(obj),'reference_sha256':sha(Path(paths.REF_IMAGE)),'source_owner_proof_sha256':sha(owner),'strict_parent':'0x00b8c3b0','allocation_size':196,'allocation_source':'?FUN_00aa13e0@@YAPAXI@Z','reference_cleanup':'0x00f2954f','cleanup_size':196,'cleanup_target':'0x00aa1460','limits':['source declaration and matching allocator/deallocator pair support only a private experiment; actual class ODR, metadata and final image remain unproved']};O.write_text(json.dumps(j,indent=2));print(sha(O))
if __name__=='__main__':main()
