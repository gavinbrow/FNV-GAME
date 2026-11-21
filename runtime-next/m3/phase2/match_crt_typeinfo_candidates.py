"""Match existing compiled CRT code with independent recipe anchors; no function decompilation."""
from pathlib import Path
import argparse,collections,hashlib,json,struct,sys
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'fnv_decomp/tools'));from compare import Pe

def run(out):
 assert not out.exists();out.mkdir(parents=True);source=R/'runtime-next/m3/out/non-ai-integration-20261119/crt-proof/library-symbol-scan.json';scan=json.loads(source.read_bytes());u=json.loads((R/'fnv_decomp/build/units.json').read_bytes())['units'];maps=collections.defaultdict(set)
 for unit in u:
  for name,va in unit['symbols'].items():
   try:maps[name].add(int(va,16))
   except (ValueError,TypeError):pass
 required={'??3@YAXPAX@Z':0x401030,'??_7type_info@@6B@':0x10f1ee0,'_free':0xecd291}
 for name,va in required.items():assert maps[name]=={va}
 anchors=dict(required);pe=Pe(str(R/'FNV/work/worker1/FalloutNV.runtime-text.exe'));sec=next(x for x,n in zip(pe.sections,pe.names) if n=='.text');base=pe.base+sec[0];blob=pe.read(base,sec[2]);order=['?_Type_info_dtor@type_info@@CAXPAV1@@Z','??1type_info@@UAE@XZ','??_Gtype_info@@UAEPAXI@Z'];results=[]
 for name in order:
  ds=[x for x in scan['definitions'] if x['symbol']==name];assert len(ds)==1;d=ds[0];data=bytes.fromhex(d['bytes']);masked={i for r in d['relocations'] for i in range(r['offset'],r['offset']+4)};runs=[];i=0
  while i<len(data):
   if i in masked:i+=1;continue
   start=i
   while i<len(data) and i not in masked:i+=1
   runs.append((start,data[start:i]))
  offset,key=max(runs,key=lambda x:len(x[1]));positions=[];start=0
  while True:
   at=blob.find(key,start)
   if at<0:break
   start=at+1;p=at-offset
   if p<0 or p+len(data)>len(blob):continue
   actual=blob[p:p+len(data)]
   if not all(actual[n]==b for n,b in enumerate(data) if n not in masked):continue
   va=base+p;resolved=[];good=True
   for rel in d['relocations']:
    if rel['target'] not in anchors:continue
    off=rel['offset'];addend=struct.unpack_from('<i' if rel['kind']==20 else '<I',data,off)[0];expected=(anchors[rel['target']]+addend-(va+off+4) if rel['kind']==20 else anchors[rel['target']]+addend)&0xffffffff
    if struct.unpack_from('<I',actual,off)[0]!=expected:good=False;break
    resolved.append(rel['target'])
   if good:positions.append({'va':va,'independent_known_relocation_targets':resolved})
  assert len(positions)==1,(name,positions);va=positions[0]['va'];anchors[name]=va;relocations=[]
  for rel in d['relocations']:
   off=rel['offset'];raw=pe.read(va+off,4);addend=struct.unpack_from('<i' if rel['kind']==20 else '<I',data,off)[0];observed=(va+off+4+struct.unpack('<i',raw)[0] if rel['kind']==20 else struct.unpack('<I',raw)[0])&0xffffffff;relocations.append(dict(rel,observed_target=observed,object_addend=addend,independently_bound=rel['target'] in required,graph_bound=rel['target'] in anchors))
  results.append({'symbol':name,'unique_candidate':va,'code_bytes':len(data),'matching_method':'All nonrelocation bytes plus independently known call/vtable anchors, followed by graph constraints','source_object_sha256':d['object_sha256'],'relocations':relocations})
 assert anchors['??_Gtype_info@@UAEPAXI@Z']==0xec40ab and anchors['??1type_info@@UAE@XZ']==0xec409b and anchors['?_Type_info_dtor@type_info@@CAXPAV1@@Z']==0xed16a2
 result={'scope':'Compiled CRT source-object matching candidates. No installed symbol aliases; helper EH/lock/BSS dependencies and native code provenance still require review.','records':results,'seed_anchors':required,'derived_candidates':{k:v for k,v in anchors.items() if k not in required},'source_scan_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'unresolved_helper_target_names':sorted({r['target'] for x in results for r in x['relocations'] if not r['graph_bound']}),'accepted_provider':False};(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps({'unique_candidates':result['derived_candidates'],'unresolved_helper_dependencies':result['unresolved_helper_target_names']}))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);v=a.parse_args();run(v.out)
