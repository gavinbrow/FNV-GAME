"""Private unit258 distinct 48/208-byte element array cleanup hypothesis."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-bfc-arrays258-split-v3';U=F/'build/units.json';SRC=F/'src/fallout/ai/actor_o2_nood_variant.cpp';RELATED=F/'src/fallout/ai/actor_o2_variant.cpp';OWN=F/'src/staging/blk_00c60000_o2.cpp';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';PIN='8aabdf1041faf3599c580e29ba329e06598bf91cd5e527afefa1d5c9a66e5498'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch')
 return s.replace(a,b,1)
def main():
 if O.exists():raise FileExistsError('no overwrite')
 raw=SRC.read_bytes();unitsraw=U.read_bytes();related=RELATED.read_bytes();own=OWN.read_bytes()
 if sha(raw)!=PIN or sha(unitsraw)!=BASE:raise ValueError('source or recipe changed')
 units=json.loads(unitsraw)['units'];u=units[258];expected=[('0x00c7bf90',62),('0x00c7b0b0',62)];owners=[]
 for va,size in expected:
  matches=[(i,f) for i,x in enumerate(units) for f in x['functions'] if f['address']==va]
  if len(matches)!=1 or matches[0][1]['size']!=size:raise ValueError('independent array owner changed')
  owners.append({'unit':matches[0][0],'function':matches[0][1]})
 text=related.decode().replace('\r\n','\n')
 for anchor in ('HkArrX<T48> m_94;','HkArrX<T208> m_22c;'):
  if text.count(anchor)!=1:raise ValueError('related field evidence changed')
 source=raw.decode().replace('\r\n','\n');anchor='''struct SmallArray {
    void* vtable; unsigned int data,size,capacity;'''
 addition='''// Provisional distinct element-width array cleanup types.
struct RefSlotArray48_258 {
    unsigned int data, size, capacity;
    RefSlotArray48_258():data(0),size(0),capacity(0x80000000){}
    ~RefSlotArray48_258() {
        Allocator& a = GetRouter()->AllocatorInstance();
        unsigned int flags=capacity; size=0;
        if ((flags & 0x80000000u)==0) a.Resize((void*)data,(flags & 0x3fffffffu)*48);
        data=0; capacity=0x80000000u;
    }
};
struct RefSlotArray208_258 {
    volatile unsigned int data, size, capacity;
    RefSlotArray208_258():data(0),size(0),capacity(0x80000000){}
    ~RefSlotArray208_258() {
        Allocator& a = GetRouter()->AllocatorInstance();
        unsigned int flags=capacity; size=0;
        if ((flags & 0x80000000u)==0) a.Resize((void*)data,(flags & 0x3fffffffu)*208);
        capacity=0x80000000u; data=0;
    }
};
struct SmallArray {
    void* vtable; unsigned int data,size,capacity;'''
 source=rep(source,anchor,addition);source=rep(source,'    RefSlotArray array94;','    RefSlotArray48_258 array94;');source=rep(source,'    RefSlotArray array22c;','    RefSlotArray208_258 array22c;')
 O.mkdir();out=source.encode();(O/'actor_o2_nood_variant.cpp').write_bytes(out)
 m={'scope':'private element-width cleanup split; no installed source/aliases','base_recipe_sha256':BASE,'source_sha256':sha(raw),'candidate_sha256':sha(out),'related_unit260_source_sha256':sha(related),'independent_owner_source_sha256':sha(own),'unit':258,'function_count':len(u['functions']),'fields':[{'offset':'0x94','element_size':48,'source_owner':'0x00c7bf90'},{'offset':'0x22c','element_size':208,'source_owner':'0x00c7b0b0'}],'independent_owners':owners,'status':'uncompiled; full helper/reference/ordinary EH comparison required','limitations':['source type identities are provisional despite independent related field layouts','ArrayStorage/ScratchArray and RefSlot collisions remain unresolved','constructor code, field layouts, all11 functions and EH/xdata must be verified','callee and final linker ownership are not established']}
 (O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'unit':258,'functions':len(u['functions']),'source_sha256':sha(out)}))
if __name__=='__main__':main()
