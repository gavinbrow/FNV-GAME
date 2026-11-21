"""Record original sized cleanup calls and independently source-owned target."""
import hashlib,json,struct,sys
from pathlib import Path
M=Path(__file__).resolve().parent.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';O=R/'phase2-nimem-149-194-sized-eh-reference.json';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Pe
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior proof')
 owner=R/'phase2-nimem-unit200-normal-new-v3/source-owner-replay.json'
 if sha(owner)!='6acfb2049b12049418545c7dc8b813735b1341c134baaf5c9d4580a06db59af3':raise ValueError('owner proof changed')
 proof=json.loads(owner.read_text())['owner_1664']
 if proof['address']!='0x00aa1460' or proof['source_native_symbol']!='??3NiMemObject@@SAXPAXI@Z' or proof['functions_matched']!=proof['functions_total']:raise ValueError('owner proof not strict')
 pe=Pe(paths.REF_IMAGE);rows=[]
 for unit,va,size,calloff,expected in [(149,0xf2c310,0xc0,10,b'\x68\xc0\x00\x00\x00'),(194,0xf26d90,0x64,7,b'\x6a\x64')]:
  data=pe.read(va,calloff+4)
  if not data.startswith(expected) or data[calloff-1]!=0xe8:raise ValueError('unexpected original instruction shape')
  target=(va+calloff+4+struct.unpack_from('<i',data,calloff)[0])&0xffffffff
  if target!=int(proof['address'],16):raise ValueError('cleanup target differs')
  rows.append({'unit':unit,'reference_funclet':'0x%08x'%va,'explicit_size':size,'direct_call_field_offset':calloff,'source_owner_unit':1664,'target':'0x%08x'%target})
 O.write_text(json.dumps({'reference_sha256':sha(Path(paths.REF_IMAGE)),'owner_proof_sha256':sha(owner),'cases':rows,'source_size_assertions':['BloodSplatterBeamShader == 192','BSFogProperty == 100'],'limits':['call and size establish target behavior; complete source/class ABI and generated placement require separate proof']},indent=2));print(sha(O))
if __name__=='__main__':main()
