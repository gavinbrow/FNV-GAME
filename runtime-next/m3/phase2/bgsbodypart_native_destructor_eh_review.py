"""Source- and reference-grounded native BGSBodyPart EH graph review."""
import copy,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';D=M/'out/phase2-bgsbodypart-native-destructor-rebase6757';OUT=D/'independent-eh-owner-review.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve existing review')
 recipe=F/'build/units.json';raw=recipe.read_bytes();u=json.loads(raw)['units'];run=json.loads((D/'lane-compile.json').read_text());outcomes={(x['unit'],x['tag']):x for x in run['outcomes']};pe=Pe(paths.REF_IMAGE);names=recipe_names(u);graph=json.loads((D/'graph-unit.json').read_text());unit620=u[620];done={};details={}
 expected={'??1?$BSStringT@D@@QAE@XZ':0x4037d0,'??1TESModel@@UAE@XZ':0x489070,'??1TESModelPSA@@UAE@XZ':0x51b950,'@__security_check_cookie@4':0xec408c,'___CxxFrameHandler3':0xec3d33}
 for k,v in expected.items():
  if k in graph['symbols'] and int(graph['symbols'][k],16)!=v:raise ValueError('candidate mapping differs')
 if unit620['symbols']['??1FUN_005e3c60_psa@@QAE@XZ']!='0x0051b950' or unit620['symbols']['??1?$BSStringT@D@@QAE@XZ']!='0x004037d0':raise ValueError('source bindings differ')
 for tag in ('original','mirror'):
  done[tag]=[];details[tag]={}
  for i in (620,621):
   path=D/('%04d.%s.obj'%(i,tag));record=outcomes[i,tag]
   if record['rc'] or sha(path)!=record['object_sha256']:raise ValueError('object differs')
   spec=graph if i==620 and tag=='mirror' else u[i];c=Coff(str(path));rows=compare(c,pe,spec)
   if len(rows)!=(15 if i==620 else 10) or any(r['verdict']!='match' for r in rows):raise ValueError('function mismatch '+str((i,tag)))
   sections,inferred,errors=eh_sections(c,pe,spec,rows,names)
   if errors or any(not x[2] for x in sections):raise ValueError('ordinary EH mismatch')
   done[tag].append({'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()}});details[tag][str(i)]={'object_sha256':sha(path),'functions':len(rows),'eh_sections':len(sections),'inferred_names':{k:'0x%08x'%v for k,v in inferred.items()}}
  tails,bad,inf,_,conf=eh_tails([u[620],u[621]],done[tag],pe)
  if len(tails)!=2 or bad or conf:raise ValueError('ordinary listed tails failed')
  details[tag]['listed_tails']={'count':len(tails),'inferred':list(inf),'conflicts':conf}
 c=Coff(str(D/'0620.mirror.obj'));oldc=Coff(str(D/'0620.original.obj'));spec=copy.deepcopy(graph);spec['functions']=[{'address':'0x0051b950','symbol':'??1TESModelPSA@@UAE@XZ','size':19}];check=compare(c,pe,spec)
 if len(check)!=1 or check[0]['verdict']!='match':raise ValueError('native PSA destructor differs from sole source owner')
 graphs=[]
 for label,obj,name in [('original',oldc,'??1FUN_005e3c60_cls@@UAE@XZ'),('mirror',c,'??1BGSBodyPart@@QAE@XZ')]:
  h=obj.named('__ehhandler$'+name);fi=obj.named('__ehfuncinfo$'+name);table=obj.named('__unwindtable$'+name);hs=obj.sections[h['section']];xs=obj.sections[fi['section']]
  if h['value']!=77 or len(hs['data'])!=104 or fi['value']!=0 or table['value']!=36 or fi['section']!=table['section']:raise ValueError('EH section shape differs')
  rel=[]
  for off,j,kind in hs['relocs']:
   target=obj.symbols[j];add=int.from_bytes(hs['data'][off:off+4],'little',signed=kind==20);ref=int.from_bytes(pe.read(0xef9df0+off,4),'little',signed=kind==20);resolved=(ref+0xef9df0+off+4 if kind==20 else ref)&0xffffffff
   rel.append({'offset':off,'kind':kind,'symbol':target['name'],'addend':add,'reference_target':'0x%08x'%resolved})
  if [(x['offset'],x['reference_target']) for x in rel]!=[(7,'0x004037d0'),(18,'0x004037d0'),(29,'0x004037d0'),(40,'0x004037d0'),(51,'0x004037d0'),(62,'0x00489070'),(73,'0x0051b950'),(90,'0x00ec408c'),(95,'0x0114b464'),(100,'0x00ec3d33')]:raise ValueError('reference EH relocation target differs')
  xr=[(off,kind,obj.symbols[j]['name'],obj.symbols[j]['section'],obj.symbols[j]['value']) for off,j,kind in xs['relocs']]
  if len(xr)!=8 or xr[0][0]!=8 or xr[0][3:]!=(fi['section'],36) or [x[0] for x in xr[1:]]!=[40,48,56,64,72,80,88] or [x[4] for x in xr[1:]]!=[0,11,22,33,44,55,66] or any(x[3]!=h['section'] for x in xr[1:]):raise ValueError('FuncInfo/unwind graph differs')
  graphs.append({'tag':label,'handler_symbol':'__ehhandler$'+name,'handler_section_offset':h['value'],'funcinfo_symbol':'__ehfuncinfo$'+name,'unwind_symbol':'__unwindtable$'+name,'handler_relocations':rel,'xdata_relocations':xr})
 vals=struct.unpack('<9I',pe.read(0x114b464,36));actions=[struct.unpack('<II',pe.read(vals[2]+8*i,8)) for i in range(vals[1])]
 if vals[0]!=0x19930522 or vals[1]!=7 or vals[2]!=0x114b488 or [x[1] for x in actions]!=[0xef9df0+11*i for i in range(7)]:raise ValueError('reference FuncInfo differs')
 owner_targets=[{'target':'0x004037d0','owner_unit':1051,'source':u[1051]['source'],'evidence':'source-recipe BSString destructor; original unit 620 binding'}, {'target':'0x00489070','owner_unit':1037,'source':u[1037]['source'],'evidence':'source-recipe TESModel destructor and repeated source bindings'}, {'target':'0x0051b950','owner_unit':2909,'source':u[2909]['source'],'evidence':'source TESModel-derived destructor wrapper; original unit 620 PSA member binding; candidate emitted native destructor strict 19-byte reference match'}, {'target':'0x00ec408c','owner_unit':2993,'source':u[2993]['source'],'evidence':'security cookie helper source recipe'}, {'target':'0x00ec3d33','owner_unit':None,'source':None,'evidence':'runtime CxxFrameHandler3; four consistent recipe bindings, reference target; linker ownership remains open'}]
 for x in owner_targets:
  if x['source']:x['source_sha256']=sha(F/x['source'])
 OUT.write_text(json.dumps({'scope':'ordinary EH and named handler/FuncInfo/unwind references for private candidate; not final linker ownership','recipe_sha256':hashlib.sha256(raw).hexdigest(),'compile_sha256':sha(D/'lane-compile.json'),'candidate_mapping_sha256':sha(D/'graph-unit.json'),'reference_sha256':sha(Path(paths.REF_IMAGE)),'ordinary':details,'reference_funcinfo':'0x0114b464','reference_unwind_map':'0x0114b488','reference_actions':[{'state':s,'target':'0x%08x'%t} for s,t in actions],'graphs':graphs,'targets':owner_targets,'limits':['candidate emitted PSA destructor matches source owner bytes/relocations; global COMDAT ownership and final placement not proven','runtime CxxFrameHandler3 symbol identity supported by recipe bindings; runtime library ownership not proven','historical candidate object is private; actual installed production and full image/runtime remain separate']},indent=2));print('PASS 15+10 functions, ordinary 2 tails, 7 unwind entries; PSA 19-byte source owner match')
if __name__=='__main__':main()
