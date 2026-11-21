"""Guarded NiRef two-unit private mirror lane; no source or default writes."""
import argparse,hashlib,json,os,re,struct,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;R=RN.parent;F=R/'fnv_decomp';D=M/'out/phase2-niref-primary-owner-fixture';P=M/'out/phase2-nimem-next-source-composed';sys.path[:0]=[str(H),str(RN/'pinned-build'),str(RN),str(F/'tools')]
import paths,compile_units_v3 as CU
import rtti_tesform_bindings_transaction as locks
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
FP='81cc3c7b15fd142f1284d91b16c72dc435e67ba273a340dbc88ca3dfbdc83d53';PP='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';OLD='13350f07cdc4c63683867d034fbb0a6ba89e83f170ef7f97c486ec39d7377876';NEW='7918744302394852a0afe800e01c83fd27a1ab0e8884d3c621afc2544370f41d';CAP='f1fd552073c5e32219ce5896adfe40307a8fa124580edcc5571c7ee7d7dc86b9';FREEZE='7e4e55cd53098166afd99874e4472d7c66ff14498bca6eb8cf2a5c5e2c4e51d7'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def clean(e):return {k:v for k,v in e.items() if k.upper() not in ('CL','_CL_') and not k.upper().startswith(('FNV_','CODEX_NEGATIVE'))}
def validate():
 if any(sha(p)!=v for p,v in ((D/'manifest.json',FP),(P/'manifest.json',PP),(F/'build/units.json',BASE),(D/'units.original',OLD),(D/'units.generated',NEW),(D/'production-capture.json',CAP))):raise ValueError('fixture/baseline changed')
 if sha(D/'tool-freeze.json')!=FREEZE:raise ValueError('tool freeze changed')
 if sha(Path(paths.REF_IMAGE))!=load(D/'tool-freeze.json')['reference_sha256']:raise ValueError('reference changed')
 for rel,v in load(D/'tool-freeze.json')['files'].items():
  if sha(R/rel)!=v:raise ValueError('tool drift '+rel)
 parent=load(P/'manifest.json');ov={}
 for rel,h in parent['source_payload_sha256'].items():
  p=P/'payload'/rel
  if sha(p)!=h:raise ValueError('parent overlay drift '+rel)
  ov[rel]=p
 fixture=load(D/'manifest.json');capture=load(D/'production-capture.json')['objects']
 archives=[(M/'out/phase2-nimem-kind-production-archive/manifest.json','62a67ba7b952e0b04f52c019652e035214dee8ffb425daedfbbf099ebf0967e5',(612,2725)),(M/'out/phase2-nimem-operators-825d-production-archive/manifest.json','25e303cfcef7555e59437901586e1085cec1df91b6487d9acb1bee6e12a30bdc',(1503,))]
 for path,pin,ids in archives:
  if sha(path)!=pin:raise ValueError('archive manifest changed')
  rows={x['unit']:x for x in load(path)['objects']}
  for i in ids:
   if rows[i]['sha256']!=capture[str(i)]['sha256']:raise ValueError('captured object not archive pinned')
 for i in (612,1503,2725):
  q=D/('production-%04d.obj'%i)
  if sha(q)!=capture[str(i)]['sha256']:raise ValueError('production archive drift')
 for i in (612,1503):
  x=load(D/str(i)/'mirror-manifest.json')
  for tag in ('original','candidate'):
   if x[tag]!=fixture['mirrors'][str(i)][tag]:raise ValueError('mirror manifest differs from fixture')
   for rel,v in x[tag]['files'].items():
    q=D/str(i)/tag/rel
    if sha(q)!=v:raise ValueError('mirror drift '+rel)
  for rel,v in x['original_inputs'].items():
   q=ov.get(rel,F/rel)
   if sha(q)!=v:raise ValueError('parent source drift '+rel)
 return load(D/'units.original')['units'],load(D/'units.generated')['units']
def compile_lane():
 before,_=validate();env0=clean(os.environ);env0.update(FNV_MSVC9_ROOT=paths.MSVC9_SP1,FNV_MSVC9_RTM_ROOT=paths.MSVC9_RTM,FNV_MSVC8_ROOT=paths.MSVC8);os.environ.clear();os.environ.update(env0);results=[]
 for i in (612,1503):
  d=D/str(i);m=load(d/'mirror-manifest.json');u=before[i];tmp=d/'compiler-tmp';result=d/'compile-result.json'
  if tmp.exists() or result.exists() or any((d/(tag+'.'+ext)).exists() for tag in ('original','candidate') for ext in ('obj','log')):raise FileExistsError('preserve existing output')
  tc=CU.find_toolchains()[u['compiler']]
  if not tc.get('ok'):raise ValueError('toolchain unavailable')
  vc=Path(tc['vc']);sdk=Path(tc['sdk']) if tc['sdk']!='None' else None;env=clean(CU.make_env(vc,sdk));tmp.mkdir();env['TMP']=env['TEMP']=str(tmp);out=[]
  for tag in ('original','candidate'):
   root=d/tag;obj=d/(tag+'.obj');log=d/(tag+'.log');cmd=[str(vc/'bin/cl.exe'),'/c','/nologo','/showIncludes']+u['flags']+['/I'+str(root/'include'),str(root/u['source']),'/Fo'+str(obj)]
   r=subprocess.run(cmd,cwd=root,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,errors='replace',timeout=900);log.write_text(r.stdout+'\n'+r.stderr,encoding='utf8');shown=re.findall(r'(?im)^Note: including file:\s*(.+?)\s*$',r.stdout+'\n'+r.stderr);bad=[];seen=[]
   for value in shown:
    p=Path(value.strip()).resolve()
    if p.is_relative_to(root.resolve()):
     rel=p.relative_to(root.resolve()).as_posix();seen.append(rel)
     if rel not in m[tag]['files']:bad.append(value)
    elif not p.is_relative_to(vc.resolve()) and not (sdk and p.is_relative_to(sdk.resolve())):bad.append(value)
   out.append({'tag':tag,'rc':r.returncode,'object_sha256':sha(obj) if obj.exists() else None,'log_sha256':sha(log),'trace_valid':bool(shown) and not bad,'unrecognized_includes':bad,'project_includes':seen,'warnings':[line for line in (r.stdout+'\n'+r.stderr).splitlines() if re.search(r'(?i)\bwarning\s+C\d+',line)]})
  result.write_text(json.dumps({'unit':i,'flags':u['flags'],'mirror_manifest_sha256':sha(d/'mirror-manifest.json'),'compiler_version':tc['version'],'outcomes':out},indent=2));results.append({'unit':i,'outcomes':out})
 validate();print(json.dumps(results))
def compare_lane():
 before,after=validate();pe=Pe(paths.REF_IMAGE);results={};metadata={}
 for i in (612,1503):
  d=D/str(i);run=load(d/'compile-result.json');result={}
  if len(run['outcomes'])!=2 or {x['tag'] for x in run['outcomes']}!={'original','candidate'}:raise ValueError('outcome scope')
  for x in run['outcomes']:
   p=d/(x['tag']+'.obj')
   if x['rc'] or not x['trace_valid'] or not p.exists() or sha(p)!=x['object_sha256']:result[x['tag']]={'status':'compile or trace failed','rc':x['rc']};continue
   spec=before[i] if x['tag']=='original' else after[i];c=Coff(str(p))
   try:
    rows=compare(c,pe,spec);sec,inf,errors=eh_sections(c,pe,spec,rows,recipe_names(before if x['tag']=='original' else after));result[x['tag']]={'object_sha256':sha(p),'functions':len(rows),'matches':sum(z['verdict']=='match' for z in rows),'failures':[{'address':z['address'],'errors':z['errors']} for z in rows if z['verdict']!='match'],'eh_sections':len(sec),'eh_failed':[z for z in sec if not z[2]],'eh_errors':errors,'eh_inferred':{k:hex(v) for k,v in inf.items()}}
   except Exception as e:result[x['tag']]={'status':'comparison failed','error':type(e).__name__+': '+str(e)}
   if x['tag']=='candidate':
    facts=[];comdat=[];symstart=struct.unpack_from('<I',c.data,8)[0]
    for idx,z in c.symbols.items():
     at=symstart+18*idx
     if z['storage']==3 and z['section']>0 and z['value']==0 and c.data[at+17] and z['name']==c.sections[z['section']]['name']:
      length,reloc,lines,checksum,assoc,selection=struct.unpack_from('<IHHIhB',c.data,at+18);comdat.append({'section_index':z['section'],'selection':selection,'associative_section':assoc,'length':length})
    for n,group in c.by_name.items():
     if 'NiRefObject' not in n:continue
     for z in group:
      if z['section']<=0:continue
      s=c.sections[z['section']];facts.append({'symbol':n,'section':s['name'],'section_index':z['section'],'symbol_offset':z['value'],'section_size':len(s['data']),'section_flags':s['flags'],'section_sha256':hashlib.sha256(s['data']).hexdigest(),'relocations':[(off,kind,c.symbols[idx]['name']) for off,idx,kind in s['relocs']]})
    weak=[]
    for idx,z in c.symbols.items():
     if 'NiRefObject' in z['name'] and z['storage']==105:
      start=struct.unpack_from('<I',c.data,8)[0];target,mode=struct.unpack_from('<II',c.data,start+18*(idx+1));weak.append({'symbol':z['name'],'fallback':c.symbols[target]['name'],'mode':mode})
    metadata[str(i)]={'sections':facts,'weak_aux':weak,'section_comdat_aux':comdat}
  prod=D/('production-%04d.obj'%i);pc=Coff(str(prod));live=load(F/'build/units.json')['units'];pr=compare(pc,pe,live[i]);ps,pi,perr=eh_sections(pc,pe,live[i],pr,recipe_names(live));result['production']={'object_sha256':sha(prod),'recipe_sha256':BASE,'functions':len(pr),'matches':sum(z['verdict']=='match' for z in pr),'failures':[{'address':z['address'],'errors':z['errors']} for z in pr if z['verdict']!='match'],'eh_sections':len(ps),'eh_failed':[z for z in ps if not z[2]],'eh_errors':perr,'eh_inferred':{k:hex(v) for k,v in pi.items()},'scope':'prior archived production source, not 38-source parent'}
  results[str(i)]=result
 # The optimized clone is a distinct physical reference owner; do not reassign it.
 old=load(D/'units.original')['units'];c=Coff(str(D/'production-2725.obj'));spec=copy_spec=old[2725];entry=next(z for z in spec['functions'] if z['address']=='0x00a5d3d0');one=dict(spec,functions=[entry]);rr=compare(c,pe,one);clone={'unit':2725,'object_sha256':sha(D/'production-2725.obj'),'function':entry,'verdict':rr[0]['verdict'],'errors':rr[0]['errors']}
 out={'status':'PRIVATE DIAGNOSTIC, no automatic acceptance','fixture_manifest_sha256':FP,'results':results,'candidate_niref_sections':metadata,'optimized_clone':clone,'limits':['candidate metadata and emitted missing sections are recorded; independent full RTTI/weak/COMDAT and actual final provider review remain required','raw compare never manufactures alias or binds from reference fields','ordinary EH inferred symbols reported separately','fresh production/image/runtime gates required']};q=D/'lane-comparison.json'
 if q.exists():raise FileExistsError(q)
 q.write_text(json.dumps(out,indent=2));print(json.dumps({'out':str(q),'sha256':sha(q),'clone':clone}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=('compile','compare'));p.add_argument('--ack-serialized-lane',action='store_true');a=p.parse_args()
 if a.action=='compile':
  if not a.ack_serialized_lane:raise ValueError('serialized lane acknowledgement required')
  guards=locks.acquire_guard()
  try:compile_lane()
  finally:
   for q in reversed(guards):q.unlink()
 else:compare_lane()
