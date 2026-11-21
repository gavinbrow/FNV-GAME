"""Serialized, pinned private NiRef inline 119-unit compiler and ordinary audit."""
import argparse,hashlib,json,os,re,struct,subprocess,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;R=RN.parent;F=R/'fnv_decomp';D=M/'out/phase2-niref-inline-cohort';sys.path[:0]=[str(H),str(RN/'pinned-build'),str(RN),str(F/'tools')]
import paths,compile_units_v3 as CU,rtti_tesform_bindings_transaction as locks
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
from rtti_hkp_viewer_compare import relocated
MAN='5c0fcd389d315d7af4b2d01d94214b03143b7c5672f231b0c7b134e623407830';LIVE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PARENT='92b5d4058d196208672a6479f1d5e33414c2e022172fa3f3674d1d8e12ede9b8';CAND='28a9c36294a23f10b0cb2df60590c6aa892762f853b047396516df2c5bff3148';FREEZE='583a18ca008d1a9849c5cca6c449c8b818c632a729468deb75e7dd5c558a3a12'
class ToolDrift(RuntimeError):pass
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def clean(e):return {k:v for k,v in e.items() if k.upper() not in ('CL','_CL_') and not k.upper().startswith(('FNV_','CODEX_NEGATIVE'))}
def validate(selfpin):
 if sha(Path(__file__))!=selfpin or sha(D/'tool-freeze.json')!=FREEZE:raise ValueError('runner/tool freeze changed')
 frozen=j(D/'tool-freeze.json')
 for rel,v in frozen['files'].items():
  if sha(R/rel)!=v:raise ValueError('tool/input drift '+rel)
 if sha(Path(paths.REF_IMAGE))!=frozen['reference_sha256'] or sha(D/'manifest.json')!=MAN or sha(F/'build/units.json')!=LIVE or sha(D/'units.original')!=PARENT or sha(D/'units.generated')!=CAND:raise ValueError('recipe/reference drift')
 m=j(D/'manifest.json');rows=m['units'];ids={x['unit'] for x in rows}
 for rel,digest in m['input_sha256'].items():
  if sha(R/rel)!=digest:raise ValueError('evidence drift '+rel)
 parent=M/'out/phase2-nimem-next-source-composed';parentm=j(parent/'manifest.json');overlays=parentm['source_payload_sha256']
 for rel,digest in overlays.items():
  if sha(parent/'payload'/rel)!=digest:raise ValueError('parent overlay drift '+rel)
 original_units=j(D/'units.original')['units']
 if len(rows)!=119 or len(ids)!=119 or sum(j(D/('unit-%04d'%x['unit'])/'mirror-manifest.json')['functions'] for x in rows)!=2080:raise ValueError('scope differs')
 for x in rows:
  d=D/('unit-%04d'%x['unit']);p=d/'mirror-manifest.json'
  if sha(p)!=x['mirror_manifest_sha256'] or sha(d/'production.obj')!=x['production_object_sha256']:raise ValueError('archive/mirror manifest drift')
  z=j(p)
  if any(z[k]!=original_units[x['unit']][k] for k in ('source','flags','compiler')):raise ValueError('unit source/flags drift')
  for rel,digest in z['original']['files'].items():
   source=parent/'payload'/rel if rel in overlays else F/rel
   if sha(source)!=digest:raise ValueError('parent source drift '+rel)
  for tag in ('original','candidate'):
   for rel,digest in z[tag]['files'].items():
    if sha(d/tag/rel)!=digest:raise ValueError('mirror file drift '+rel)
 return m,j(D/'units.original')['units'],j(D/'units.generated')['units'],j(F/'build/units.json')['units']
def compile_pair(d,u,checktools):
 mm=j(d/'mirror-manifest.json');tmp=d/'compiler-tmp';result=d/'compile-result.json'
 if tmp.exists() or result.exists() or any((d/(t+'.'+e)).exists() for t in ('original','candidate') for e in ('obj','log')):raise FileExistsError('preserve output')
 tc=CU.find_toolchains()[u['compiler']]
 if not tc.get('ok'):raise ValueError('toolchain unavailable')
 vc=Path(tc['vc']);sdk=Path(tc['sdk']) if tc['sdk']!='None' else None;env=clean(CU.make_env(vc,sdk));tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);out=[]
 for tag in ('original','candidate'):
  root=d/tag;obj=d/(tag+'.obj');log=d/(tag+'.log');cmd=[str(vc/'bin/cl.exe'),'/c','/nologo','/showIncludes']+u['flags']+['/I'+str(root/'include'),str(root/u['source']),'/Fo'+str(obj)]
  checktools();r=subprocess.run(cmd,cwd=root,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,errors='replace',timeout=900);checktools();log.write_text(r.stdout+'\n'+r.stderr,encoding='utf8');shown=re.findall(r'(?im)^Note: including file:\s*(.+?)\s*$',r.stdout+'\n'+r.stderr);bad=[]
  for line in shown:
   p=Path(line.strip()).resolve()
   if p.is_relative_to(root.resolve()):
    if p.relative_to(root.resolve()).as_posix() not in mm[tag]['files']:bad.append(line)
   elif not p.is_relative_to(vc.resolve()) and not (sdk and p.is_relative_to(sdk.resolve())):bad.append(line)
  out.append({'tag':tag,'rc':r.returncode,'object_sha256':sha(obj) if obj.exists() else None,'log_sha256':sha(log),'trace_valid':bool(shown) and not bad,'unrecognized_includes':bad,'warnings':[line for line in (r.stdout+'\n'+r.stderr).splitlines() if re.search(r'(?i)\bwarning\s+C\d+',line)]})
 result.write_text(json.dumps({'unit':mm['unit'],'flags':u['flags'],'compiler_version':tc['version'],'mirror_manifest_sha256':sha(d/'mirror-manifest.json'),'outcomes':out},indent=2));return out
def raw_sections(c):
 result=[]
 for i,s in enumerate(c.sections[1:],1):
  if s['name'].startswith('.debug'):continue
  result.append({'index':i,'name':s['name'],'flags':s['flags'],'size':len(s['data']),'sha256':hashlib.sha256(s['data']).hexdigest(),'relocations':[(o,t,c.symbols[k]['name'],c.symbols[k]['section'],c.symbols[k]['value']) for o,k,t in s['relocs']]})
 weak=[];comdat=[];start=struct.unpack_from('<I',c.data,8)[0]
 for i,z in c.symbols.items():
  at=start+i*18
  if z['storage']==105 and c.data[at+17]:
   k,mode=struct.unpack_from('<II',c.data,at+18);weak.append({'symbol':z['name'],'fallback':c.symbols[k]['name'],'mode':mode})
  if z['storage']==3 and z['section']>0 and z['value']==0 and c.data[at+17] and z['name']==c.sections[z['section']]['name']:
   length,reloc,lines,checksum,assoc,selection=struct.unpack_from('<IHHIhB',c.data,at+18);comdat.append({'section':z['section'],'selection':selection,'associated_section':assoc,'length':length})
 return {'sections':result,'weak':weak,'comdat':comdat}
def compare_unit(d,i,orig,cand,live,pe):
 run=j(d/'compile-result.json');objects={'production':Coff(str(d/'production.obj'))};result={};raw={}
 for z in run['outcomes']:
  p=d/(z['tag']+'.obj')
  if z['rc'] or not z['trace_valid'] or not p.exists() or sha(p)!=z['object_sha256']:result[z['tag']]={'status':'compile or trace failure','rc':z['rc']}
  else:objects[z['tag']]=Coff(str(p))
 for tag,c in objects.items():
  units=live if tag=='production' else orig if tag=='original' else cand
  try:
   rr=compare(c,pe,units[i]);sections,inf,errors=eh_sections(c,pe,units[i],rr,recipe_names(units));result[tag]={'functions':len(rr),'matches':sum(x['verdict']=='match' for x in rr),'failures':[{'address':x['address'],'errors':x['errors']} for x in rr if x['verdict']!='match'],'eh_sections':sections,'eh_inferred':{k:hex(v) for k,v in inf.items()},'eh_errors':errors}
  except Exception as exc:result[tag]={'status':'comparison exception','error':type(exc).__name__+': '+str(exc),'eh_sections':[],'eh_inferred':{},'eh_errors':['comparison failed']}
  raw[tag]=raw_sections(c)
 diffs=[]
 if 'original' in objects and 'candidate' in objects:
  old={x['address']:x for x in orig[i]['functions']}
  for f in cand[i]['functions']:
   try:
    z=old[f['address']];a,ar=relocated(objects['original'],z['symbol'],z['size'],{});b,br=relocated(objects['candidate'],f['symbol'],f['size'],{})
    if a!=b or ar!=br:diffs.append({'address':f['address'],'bytes_equal':a==b,'original_relocations':ar,'candidate_relocations':br})
   except Exception as exc:diffs.append({'address':f['address'],'error':type(exc).__name__+': '+str(exc)})
 (d/'raw-sections.json').write_text(json.dumps(raw,indent=2));out={'unit':i,'results':result,'mapped_pair_differences':diffs,'raw_sections_sha256':sha(d/'raw-sections.json'),'limitations':['no function, class-key or relocation target normalization','raw EH inference remains reported separately','same-name weak/COMDAT provider selection is not decided here']};(d/'comparison.json').write_text(json.dumps(out,indent=2));return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--runner-sha256',required=True);ap.add_argument('--ack-serialized-lane',action='store_true');args=ap.parse_args();pin=args.runner_sha256.lower()
 if not args.ack_serialized_lane:raise ValueError('serialized lane acknowledgement required')
 m,old,new,live=validate(pin);progress=D/'progress.json'
 if progress.exists():raise FileExistsError('no resume or overwrite')
 guards=locks.acquire_guard()
 try:
  m,old,new,live=validate(pin);env=clean(os.environ);os.environ.clear();os.environ.update(env);os.environ.update(FNV_MSVC9_ROOT=paths.MSVC9_SP1,FNV_MSVC9_RTM_ROOT=paths.MSVC9_RTM,FNV_MSVC8_ROOT=paths.MSVC8)
  result={'status':'running','manifest_sha256':MAN,'parent_recipe_sha256':PARENT,'candidate_recipe_sha256':CAND,'units':[],'limits':['production archive is 825d or unchanged 6757 unit612; original is fresh private parent','raw function/section/weak comparisons retain all changes','G46/G44 effective provider remains unproved','no automatic alias or COMDAT selection']}
  def save():
   q=D/'progress.tmp';q.write_text(json.dumps(result,indent=2));os.replace(q,progress)
  def checktools():
   if sha(Path(__file__))!=pin or sha(D/'tool-freeze.json')!=FREEZE:raise ToolDrift('runner/tool manifest drift')
   for rel,v in j(D/'tool-freeze.json')['files'].items():
    if sha(R/rel)!=v:raise ToolDrift('tool drift '+rel)
  pe=Pe(paths.REF_IMAGE);save()
  for x in m['units']:
   i=x['unit'];d=D/('unit-%04d'%i);row={'unit':i}
   try:
    checktools();out=compile_pair(d,old[i],checktools);checktools();row['compile_outcomes']=out
    if any(z['rc'] or not z['trace_valid'] or not z['object_sha256'] for z in out):row['status']='compile-or-trace-failed'
    else:
     report=compare_unit(d,i,old,new,live,pe);checktools();row.update({'status':'review-required','comparison_sha256':sha(d/'comparison.json'),'raw_sections_sha256':sha(d/'raw-sections.json'),'matches':{k:v.get('matches') for k,v in report['results'].items()},'pair_differences':len(report['mapped_pair_differences'])})
   except ToolDrift:raise
   except Exception as exc:
    checktools()
    row.update(status='failed',error=type(exc).__name__+': '+str(exc))
   result['units'].append(row);save();print(json.dumps({'unit':i,'status':row['status']}),flush=True)
  done={k:[] for k in ('production','original','candidate')}
  for row in result['units']:
   p=D/('unit-%04d'%row['unit'])/'comparison.json'
   if p.exists():
    report=j(p)
    for tag in done:
     q=report['results'].get(tag,{})
     if 'eh_sections' in q:done[tag].append(q)
  result['ordinary_eh_union']={}
  for tag in done:
   specs=live if tag=='production' else old if tag=='original' else new;tails,bad,inferred,_,conflicts=eh_tails([specs[x['unit']] for x in m['units']],done[tag],pe);result['ordinary_eh_union'][tag]={'reports':len(done[tag]),'complete_scope':len(done[tag])==119,'requested_tails':len(tails),'bad':bad,'inferred_tails':len(inferred),'conflicts':conflicts}
  validate(pin);result['status']='complete-review-required';save()
 finally:
  for p in reversed(guards):p.unlink()
if __name__=='__main__':main()
