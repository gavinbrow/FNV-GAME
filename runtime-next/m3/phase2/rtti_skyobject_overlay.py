"""Generate an isolated SkyObject destructor reconciliation experiment."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out/phase2-skyobject-destructor-v1'
sys.path.insert(0,str(H));from rtti_bgse_merge import include_closure
S=F/'src/fallout_shared/sky/skyobject.cpp';D=F/'src/fallout_shared/sky/skyobject.h';U=F/'build/units.json'
HASH={'source':'9540187f8315edc5de7ed90845300b722db93c512e89999c0fce66ed9f829900','header':'298a7d361a8882b31cb3f4cdd074607df749ef70297ba9e507f2f8b8d0be3e98','units':'a7470e7f0f8c59ea4b201a1e1f72bb552d3bbd00596db2fdc4911b94b6c18a56'}
def sha(b):return hashlib.sha256(b).hexdigest()
def transform(source):
 old=b'''struct Mem_63f8d0\r\n{\r\n    void Reset(int);\r\n    ~Mem_63f8d0();\r\n};\r\nstruct FUN_0063f8d0\r\n{\r\n    virtual void v0();\r\n    Mem_63f8d0 m_mem;\r\n    ~FUN_0063f8d0();\r\n};'''
 new=b'// Destructor is emitted by the named SkyObject declaration.'
 body=b'FUN_0063f8d0::~FUN_0063f8d0()\r\n{\r\n    m_mem.Reset(0);\r\n}'
 if source.count(old)!=1 or source.count(body)!=1:raise ValueError('surrogate pattern changed')
 return source.replace(old,new).replace(body,b'SkyObject::~SkyObject()\r\n{\r\n    m_pRootNode = 0;\r\n}')
def main():
 data={k:p.read_bytes() for k,p in [('source',S),('header',D),('units',U)]}
 for k,v in data.items():
  if sha(v)!=HASH[k]:raise ValueError('input digest mismatch '+k)
 units=json.loads(data['units'])['units'];u=units[925]
 if len(u['functions'])!=4 or u['symbols'].get('??_7SkyObject@@6B@')!='0x0104f0f8' or u['symbols'].get('??_7FUN_0063f8d0@@6B@')!='0x0104f0f8':raise ValueError('unit mismatch')
 aliases=[('?Reset@Mem_63f8d0@@QAEXH@Z','??4?$NiPointer@VNiNode@@@@QAEAAV0@PAVNiNode@@@Z','0x0066b0d0'),('??1Mem_63f8d0@@QAE@XZ','??1?$NiPointer@VNiNode@@@@QAE@XZ','0x0045cec0')]
 evidence=[]
 for old,new,va in aliases:
  hits=[i for i,x in enumerate(units) if x.get('symbols',{}).get(new)==va]
  if u['symbols'].get(old)!=va or len(hits)<2:raise ValueError('alias evidence absent')
  evidence.append({'old':old,'new':new,'address':va,'independent_units':hits})
 overlay=transform(data['source']);closure,external=include_closure(S);O.mkdir(exist_ok=False)
 (O/'skyobject.cpp').write_bytes(overlay);(O/'skyobject.h').write_bytes(data['header'])
 m={'scope':'isolated source hypothesis; deleting destructor and full ABI unresolved','unit_index':925,'source':u['source'],'flags':u['flags'],'input_sha256':HASH,'source_overlay_sha256':sha(overlay),'header_overlay_sha256':sha(data['header']),'original_include_closure':closure,'system_includes':external,'proposed_function_symbol_changes':[{'address':'0x0063f8d0','before':'??1FUN_0063f8d0@@QAE@XZ','after':'??1SkyObject@@UAE@XZ'}],'proposed_external_aliases':evidence,'reference_vtable':'0x0104f0f8','all_function_count':4,'status':'uncompiled; compare all functions, EH, relocations, deleting destructor, graph and all observed slots'}
 (O/'manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'sha256':sha(overlay),'closure_files':len(closure)}))
if __name__=='__main__':main()
