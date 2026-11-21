"""Stage a private unit425 menu-node adapter without modifying production source."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;ROOT=M.parent.parent;F=ROOT/'fnv_decomp';O=M/'out/phase2-forenderedmenu-node-view'
sys.path.insert(0,str(H));from rtti_bgse_merge import include_closure
UNITS_SHA='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
SOURCE_SHA='889c087856c25fe7d4632b9d1bbb72a11aeb9549269eec147adfce0fdb1942d8'
OLD='?GetPartName@BGSBodyPart@@QAEPAUNiAVObjectS@@XZ'
NEW='?GetMenuNode@FORenderedMenuNodeView@@QAEPAUNiAVObjectS@@XZ'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 up=F/'build/units.json';raw=up.read_bytes()
 if sha(raw)!=UNITS_SHA:raise ValueError('unit recipe digest changed')
 u=json.loads(raw)['units'][425]
 if u['source']!='src/fallout/interface/forenderedmenu.cpp' or u['compiler']!='sp1' or len(u['functions'])!=44 or u['symbols'].get(OLD)!='0x006838b0':raise ValueError('unit recipe mismatch')
 target=[x for x in u['functions'] if x['address']=='0x007ff740']
 if len(target)!=1 or target[0]['size']!=125:raise ValueError('caller mapping mismatch')
 src=F/u['source'];data=src.read_bytes()
 if sha(data)!=SOURCE_SHA:raise ValueError('source digest changed')
 old=b'struct BGSBodyPart\r\n{\r\n    NiAVObjectS* GetPartName();\r\n};'
 new=b'struct FORenderedMenuNodeView\r\n{\r\n    NiAVObjectS* GetMenuNode();\r\n};'
 oldcall=b'((BGSBodyPart*)this)->GetPartName()';newcall=b'((FORenderedMenuNodeView*)this)->GetMenuNode()'
 if data.count(old)!=1 or data.count(oldcall)!=3 or data.count(b'BGSBodyPart')!=4:raise ValueError('source view use mismatch')
 result=data.replace(old,new,1).replace(oldcall,newcall)
 mapped=copy.deepcopy(u)
 if NEW in mapped['symbols']:raise ValueError('new symbol already mapped')
 value=mapped['symbols'].pop(OLD);mapped['symbols'][NEW]=value
 closure,external=include_closure(src)
 O.mkdir(exist_ok=False);(O/'forenderedmenu.cpp').write_bytes(result)
 (O/'unit-overlay.json').write_text(json.dumps(mapped,indent=2),encoding='utf8')
 output={'status':'private uncompiled source-view correction; not canonical class integration',
  'units_sha256':UNITS_SHA,'original_source_sha256':SOURCE_SHA,'candidate_source_sha256':sha(result),
  'unit_index':425,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'mapped_function_count':44,
  'caller':{'address':'0x007ff740','size':125,'use_count':3},
  'symbol_change':{'before':OLD,'after':NEW,'reference_target':'0x006838b0'},
  'unit_overlay_sha256':sha((O/'unit-overlay.json').read_bytes()),'original_quoted_include_closure':closure,'external_headers':external,
  'source_evidence':'src/fallout/interface/forenderedmenu.cpp:3024-3035',
  'reference_evidence':'0x007ff74c,0x007ff75a,0x007ff77f call 0x006838b0; result used as NiAVObject this',
  'limitations':['the adapter is a source view, not proof of native menu member name or layout','all 44 functions, relocations, literals and EH metadata require private compilation and reference comparison','include resolution and full source trace must be preserved','no source, recipe or build integration performed']}
 (O/'manifest.json').write_text(json.dumps(output,indent=2),encoding='utf8')
 print(json.dumps({'source_sha256':sha(result),'closure_files':len(closure),'unit_overlay_sha256':output['unit_overlay_sha256']}))
if __name__=='__main__':main()
