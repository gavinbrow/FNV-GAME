"""Stage a source-supported TESModelTextureSwap return-type hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-psa-slot7-proposal';O=M/'out/phase2-bgsbodypart-psa-slot7-typed-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 m=json.loads((P/'manifest.json').read_text());h=(P/'bgsbodypart_decls.h').read_bytes();s=(P/'bgsbodypart.cpp').read_bytes()
 if sha(h)!=m['header_sha256'] or sha(s)!=m['source_sha256']:raise ValueError('prior source changed')
 old=b'    virtual void* vfn_1c();';new=b'    virtual TESModelTextureSwap* GetAsModelTextureSwap();'
 if h.count(old)!=1 or h.count(b'class TESModel : public BaseFormComponent')!=1:raise ValueError('model declaration changed')
 h=h.replace(b'class TESModel : public BaseFormComponent',b'class TESModelTextureSwap;\nclass TESModel : public BaseFormComponent',1).replace(old,new,1)
 O.mkdir(exist_ok=False);(O/'bgsbodypart.cpp').write_bytes(s);(O/'bgsbodypart_decls.h').write_bytes(h)
 report={'status':'private uncompiled source-supported return type, qualifier remains unresolved','source_sha256':sha(s),'header_sha256':sha(h),
  'source_evidence':['src/fallout_shared/bipedanim_decls.h:368-384','src/fallout_shared/bipedanim.cpp:2101-2103','src/fallout_shared/bipedanim.cpp:2421-2423'],
  'reference_caller':'0x004aeff5 loads vtable +0x1c; 0x004af00a calls ApplyTextureSwaps at 0x0048afe0 on nonnull returned object',
  'qualification':'bipedanim source is nonconst; tescasinochips source declares const; original machine instructions cannot settle cv qualification',
  'requirements':['unit 620/621 canonical header and consistent source signatures','compiler, complete RTTI, EH and vtable validation','source name and const qualifier independent verification','full link placement and controls']}
 (O/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps({'header_sha256':sha(h)}))
if __name__=='__main__':main()
