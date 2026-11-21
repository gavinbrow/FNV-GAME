"""Private unit258 ref84 cleanup-type split; retain all other fields."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-bfc-refslot258-split';U=F/'build/units.json';SRC=F/'src/fallout/ai/actor_o2_nood_variant.cpp';OWNER=F/'src/fallout/ai/movement/actormover.cpp';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';PIN='8aabdf1041faf3599c580e29ba329e06598bf91cd5e527afefa1d5c9a66e5498'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch')
 return s.replace(a,b,1)
def main():
 if O.exists():raise FileExistsError('no overwrite')
 raw=SRC.read_bytes();unitraw=U.read_bytes();owner=OWNER.read_bytes()
 if sha(raw)!=PIN or sha(unitraw)!=BASE:raise ValueError('input changed')
 units=json.loads(unitraw)['units'];u=units[258];f=[x for x in u['functions'] if x['address']=='0x00c7f060'];q=[x for x in units[386]['functions'] if x['address']=='0x0045cec0'];r=[x for x in units[1515]['functions'] if x['address']=='0x00b66f20']
 if len(f)!=1 or len(q)!=1 or q[0]['size']!=29 or len(r)!=1 or r[0]['size']!=33 or units[386]['symbols'].get('?FUN_00401970@SeqObj@@QAEXXZ')!='0x00401970':raise ValueError('independent source mappings changed')
 source=raw.decode().replace('\r\n','\n');anchor='''struct RefSlotArray {
    unsigned int data, size, capacity;''';addition='''// Provisional source-local cleanup adapter for the ref84 field only.
struct RefRelease258 { void FUN_00401970(); };
struct RefSlotIndirect258 {
    RefTarget* object;
    RefSlotIndirect258():object(0){}
    ~RefSlotIndirect258() { if (object) reinterpret_cast<RefRelease258*>(object)->FUN_00401970(); }
    void clear() { RefTarget* old=object; if(old) { if(!InterlockedDecrement(&old->refs)) old->destroy(); object=0; } }
};
struct RefSlotArray {
    unsigned int data, size, capacity;'''
 source=rep(source,anchor,addition);source=rep(source,'    RefSlot ref84;','    RefSlotIndirect258 ref84;')
 if source.count('    RefSlot ref2a4;')!=1 or source.count('    ref84.clear();')!=1 or source.count('    ref2a4.clear();')!=1:raise ValueError('original field uses changed')
 O.mkdir();out=source.encode();(O/'actor_o2_nood_variant.cpp').write_bytes(out)
 meta={'scope':'unit258 ref84-only provisional type split; no per-call address mappings','base_recipe_sha256':BASE,'source_sha256':sha(raw),'source_owner386_sha256':sha(owner),'candidate_sha256':sha(out),'unit':258,'function_count':len(u['functions']),'constructor':f[0],'fields':[{'offset':'0x84','proposed_type':'RefSlotIndirect258','independent_cleanup_source_owner':'0x0045cec0'},{'offset':'0x2a4','proposed_type':'RefSlot','independent_cleanup_source_owner':'0x00b66f20'}],'status':'uncompiled; actual source/COFF body, all11 functions and exception state graph remain required','limitations':['RefSlot destructor remains undefined in original source; do not infer its native type from target address','ref84 and ref2a4 clear/constructor behavior and layout must be rechecked','ScratchArray/ArrayStorage and RefSlotArray collisions are NOT resolved','pointee and FUN_00401970 semantic identities remain unproven']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({'unit':258,'functions':len(u['functions']),'source_sha256':sha(out)}))
if __name__=='__main__':main()
