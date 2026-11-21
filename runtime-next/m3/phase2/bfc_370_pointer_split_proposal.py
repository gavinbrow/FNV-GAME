"""Stage distinct existing pointer-view identities for unit 370's constructor."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;F=ROOT/'fnv_decomp';O=M/'out/phase2-bfc-370-pointer-split';sys.path.insert(0,str(H));from rtti_bgse_merge import include_closure
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 units=(F/'build/units.json').read_bytes();source=F/'src/fallout/ai/middlehighprocess.cpp';raw=source.read_bytes()
 if sha(units)!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c' or sha(raw)!='201694a10e24141b4e8a38bfc7d7fa7b7dac0a51a7e4f4a399f58756de56a0cc':raise ValueError('input mismatch')
 u=json.loads(units)['units'][370]
 if len(u['functions'])!=178 or u['symbols'].get('??0FUN_00528cb0@@QAE@H@Z')!='0x00528cb0' or u['symbols'].get('??1PtrA96@@QAE@XZ')!='0x0044cbf0' or u['symbols'].get('??1PtrB96@@QAE@XZ')!='0x0092c890':raise ValueError('recipe evidence mismatch')
 a=b'struct PtrA96\r\n{\r\n    void* p;\r\n    ~PtrA96();\r\n    void FUN_006f74f0(void*);\r\n};'
 b=b'struct PtrB96\r\n{\r\n    void* p;\r\n    ~PtrB96();\r\n    void FUN_0092c8b0(void*);\r\n};'
 anchor=b'struct FUN_00528cb0\r\n{';field=b'    FUN_00528cb0 m_11c;\r\n    FUN_00528cb0 m_120;'
 if any(raw.count(x)!=1 for x in (a,b,anchor,field)):raise ValueError('source anchor mismatch')
 aa=a.replace(b'    ~PtrA96();',b'    PtrA96(int);\r\n    ~PtrA96();');bb=b.replace(b'    ~PtrB96();',b'    PtrB96(int);\r\n    ~PtrB96();')
 candidate=raw.replace(a,b'',1).replace(b,b'',1).replace(anchor,aa+b'\r\n'+bb+b'\r\n'+anchor,1).replace(field,b'    PtrA96 m_11c;\r\n    PtrB96 m_120;',1)
 mapped=copy.deepcopy(u);adds={'??0PtrA96@@QAE@H@Z':'0x00528cb0','??0PtrB96@@QAE@H@Z':'0x00528cb0'}
 for k,v in adds.items():
  if k in mapped['symbols']:raise ValueError('constructor alias collision')
  mapped['symbols'][k]=v
 closure,system=include_closure(source);O.mkdir(exist_ok=False);(O/'middlehighprocess.cpp').write_bytes(candidate);(O/'unit-overlay.json').write_text(json.dumps(mapped,indent=2),encoding='utf8')
 meta={'status':'private uncompiled source-backed view split, constructor bindings provisional','units_sha256':sha(units),'source_sha256':sha(raw),'candidate_sha256':sha(candidate),
       'unit_overlay_sha256':sha((O/'unit-overlay.json').read_bytes()),'unit':370,'mapped_functions':178,'closure':closure,'system_includes':system,
       'members':{'0x11c':{'view':'PtrA96','destructor':'0x0044cbf0','method':'0x006f74f0'},'0x120':{'view':'PtrB96','destructor':'0x0092c890','method':'0x0092c8b0'}},
       'proposed_constructor_bindings':adds,'limitations':['constructor identities have equal direct targets but source type semantics remain views','compiler, all 178 functions and unmodified EH oracle required','literal label and production-object grounding required']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print(json.dumps({'candidate_sha256':sha(candidate),'closure_files':len(closure),'functions':178}))
if __name__=='__main__':main()
