"""Private unit260 visible-release cleanup-type split hypothesis; no live edits or compile."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-bfc-refptr260-split-v3';U=F/'build/units.json';SRC=F/'src/fallout/ai/actor_o2_variant.cpp';OWNER=F/'src/fallout/ai/movement/actormover.cpp';OBJ=M/'out/phase2-bfc-cohort-production-archive/0260.obj';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';SOURCE='3859d64a2611c71a4882d3dabff0908903f5058441fd0c59d66a50ebffcb6915'
def sha(b):return hashlib.sha256(b).hexdigest()
def rep(s,a,b):
 if s.count(a)!=1:raise ValueError('anchor mismatch '+a[:80])
 return s.replace(a,b,1)
def main():
 if O.exists():raise FileExistsError('no overwrite')
 raw=SRC.read_bytes();units=U.read_bytes();owner=OWNER.read_bytes();obj=OBJ.read_bytes()
 if sha(raw)!=SOURCE or sha(units)!=BASE:raise ValueError('source or recipe changed')
 doc=json.loads(units)['units'];u=doc[260];f=[x for x in u['functions'] if x['address']=='0x00c7d900'];q=[x for x in doc[386]['functions'] if x['address']=='0x0045cec0'];r=[x for x in doc[1515]['functions'] if x['address']=='0x00b66f20']
 if len(f)!=1 or len(q)!=1 or q[0]['size']!=29 or len(r)!=1 or r[0]['size']!=33:raise ValueError('source owner mismatch')
 baseline=owner.decode().replace('\r\n','\n');anchor='''void __thiscall FUN_0045cec0_Class::FUN_0045cec0()
{
    if (*(void**)this != 0)
    {
        ((SeqObj*)*(void**)this)->FUN_00401970();
    }
}'''
 if baseline.count(anchor)!=1 or doc[386]['symbols'].get('?FUN_00401970@SeqObj@@QAEXXZ')!='0x00401970':raise ValueError('indirect cleanup source evidence changed')
 s=raw.decode().replace('\r\n','\n');anchor2='''extern int DAT_0109b220;
struct FixedStr9'''
 proposal='''// Provisional source-local adapter: identical storage and Reset behavior;
// its cleanup delegates to the independently source-mapped pointee operation.
struct RefRelease260
{
    virtual void vf0();
    virtual void vf1();
    long references;
    __forceinline void FUN_00401970()
    {
        if (InterlockedDecrement(&references) == 0) vf1();
    }
};
struct IndirectRefPtr260
{
    RefObj* m_p;
    void Reset()
    {
        RefObj* p = m_p;
        if (p)
        {
            if (InterlockedDecrement(&p->m_iObjectReferenceCount) == 0)
                p->vf1();
            m_p = 0;
        }
    }
    ~IndirectRefPtr260()
    {
        if (m_p)
            reinterpret_cast<RefRelease260*>(m_p)->FUN_00401970();
    }
};
extern int DAT_0109b220;
struct FixedStr9'''
 s=rep(s,anchor2,proposal);s=rep(s,'    RefPtr m_84;','    IndirectRefPtr260 m_84;');s=rep(s,'    RefPtr m_250;','    IndirectRefPtr260 m_250;')
 if s.count('    RefPtr m_2a4;')!=1:raise ValueError('third member changed')
 O.mkdir();candidate=s.encode();(O/'actor_o2_variant.cpp').write_bytes(candidate)
 result={'scope':'private source type-splitting hypothesis; no runtime binding or per-site alias','base_recipe_sha256':BASE,'source_sha256':sha(raw),'candidate_sha256':sha(candidate),'source_owner386_sha256':sha(owner),'archived_unit260_object_sha256':sha(obj),'unit':260,'function_count':len(u['functions']),'target_parent':f[0], 'fields':[{'offset':'0x84','proposed_type':'IndirectRefPtr260','expected_source_owner':'0x0045cec0'},{'offset':'0x250','proposed_type':'IndirectRefPtr260','expected_source_owner':'0x0045cec0'},{'offset':'0x2a4','proposed_type':'RefPtr','expected_source_owner':'0x00b66f20'}], 'indirect_owner':{'unit':386,'function':q[0],'callee_source_symbol':'?FUN_00401970@SeqObj@@QAEXXZ','callee_address':'0x00401970'},'direct_owner':{'unit':1515,'function':r[0]},'status':'uncompiled; symbol names must be read from emitted COFF; no provisional recipe aliases installed','required_gates':['exact unit260 43 function bodies and relocations vs archived/reference','independently compare entire emitted indirect/direct destructor bodies and normal callee relocations against source-backed owners','all ordinary EH states, xdata and reference targets, plus unchanged fields/this offsets','distinct unique decorated names and no global collisions; initializers/RTTI/ODR audit','final placement, image and runtime gates'],'limitations':['adapter names and pointee semantic type are provisional','existing Reset inline behavior is copied but must be checked in compiler output','inline callee uses independently sourced decrement/virtual-release semantics; exact generated code and canonical ownership remain unproven']}
 (O/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'source_sha256':sha(candidate),'unit_functions':len(u['functions'])}))
if __name__=='__main__':main()
