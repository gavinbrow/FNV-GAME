"""Serial, archive-backed ten-unit composed-context experiment."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-nimem-next-source-composed';sys.path[:0]=[str(H),str(F/'tools'),str(RN)]
import rtti_tesform_bindings_transaction as locks
from nimem_combined_825d_run import verify_tool_closure
from compare import Pe
from build_and_match import eh_tails
import paths
import baseformcomponent_core_stage as core
BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PIN='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53';CLOSURE='b8eaee662a15d9bbe86c4caf6ed132d4ed2988b6f553fd4752a4358959e46672';ARCHIVE='25e303cfcef7555e59437901586e1085cec1df91b6487d9acb1bee6e12a30bdc';SPECIAL='1373054fe4d6ae9f750b90e35bc684fb18367155a41b829e504f70bcd559987f';POSITIVE='6279b74d19087a65dda4ec37c22e3c96a1dd1c5bb3b26455f94a72bee96f1e08';UNITS=(128,129,191,200,620,773,995,1203,1271,1598)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive-995',type=Path,required=True);ap.add_argument('--archive-995-manifest-sha256',required=True);ap.add_argument('--runner-sha256',required=True);ap.add_argument('--ack-serialized-lane',action='store_true');a=ap.parse_args()
 def check():verify_tool_closure(F.parent,P/'tool-closure.json',CLOSURE,Path(__file__),a.runner_sha256.lower())
 check()
 if not a.ack_serialized_lane or sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN:raise ValueError('lane or frozen input mismatch')
 archive=M/'out/phase2-nimem-operators-825d-production-archive';am=archive/'manifest.json';special=a.archive_995.resolve();sm=special/'manifest.json'
 if not special.is_relative_to((M/'out').resolve()) or sha(am)!=ARCHIVE or sha(sm)!=SPECIAL or a.archive_995_manifest_sha256.lower()!=SPECIAL:raise ValueError('archive manifest mismatch')
 inventory=json.loads(am.read_text());entries={x['unit']:x for x in inventory['objects']};extra=json.loads(sm.read_text());old=json.loads((P/'units.original').read_text())['units'];new=json.loads((P/'units.generated').read_text())['units'];proposal=json.loads((P/'manifest.json').read_text())
 prevpath=M/'out/phase2-nimem-combined-825d/manifest.json';scopepath=M/'out/phase2-nimemobject-coherent-kind-consumers.json';reviewpath=M/'out/phase2-nimem-kind-root-section-review.json';oldpath=M/'out/phase2-source-integration6757-transaction-v2/0.original'
 if sha(prevpath)!='6b9dc1950f489c696364820186a4beba3e1618d127c4a656ecb677b53e32e1a3' or sha(scopepath)!='c45dad435c9c172c149afa1fb4054ae5844f59299e1a1dcb6ffaa1e3ca2bc67f' or sha(reviewpath)!='29db1fc1dc763665d70c7f2bb2af81672dfc4b7877d4d271a39cace3463df428' or sha(oldpath)!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c':raise ValueError('reuse evidence differs')
 prev=json.loads(prevpath.read_text());prior={x['unit']:x for x in prev['combined_api_units']+prev['fresh_kind_only_units']};reuse={x['unit']:x for x in prev['unchanged_kind_only_units'] if x['unit']!=995};affected={x['unit']:x for x in proposal['affected_units']}
 if len(prior)!=133 or len(reuse)!=617 or len(affected)!=752 or set(affected)!=set(prior)|set(reuse)|{620,995} or set(prior)&set(reuse):raise ValueError('scope partition differs')
 for i,r in prior.items():
  if i not in UNITS and affected[i]['candidate']!=r['candidate']:raise ValueError('prior composed candidate differs '+str(i))
 scopes={x['unit']:x for x in json.loads(scopepath.read_text())['units']};reviews={x['unit']:x for x in json.loads(reviewpath.read_text())['units']};historical=json.loads(oldpath.read_text())['units'];extra_sources={'src/bsshader/bsshaderlightingproperty_types_BSShaderLightingProperty.h','src/bsshader/shadowscenelight.cpp','src/fallout_shared/imagespacemodifierinstance.cpp','src/fallout_shared/imagespacemodifierinstance_effects.h','src/bsshader/speedtreeleafshader.cpp','src/gamebryo2.2/corelibs/nianimation/nicolorinterpolator.cpp','src/gamebryo2.2/corelibs/nianimation/nitexturetransformcontroller.cpp','src/gamebryo2.2/corelibs/niparticle/nipsysemitterctlr.cpp','src/fallout_shared/tesfile.cpp'}
 for i,item in reuse.items():
  rv=reviews[i];report=M/('out/phase2-nimem-kind-cohort-run/unit-%04d/comparison.json'%i)
  if old[i]!=historical[i] or core.walk(F,old[i]['source'],{})['files']!=scopes[i]['quoted_project_closure'] or set(affected[i]['source_changes'])&extra_sources or not rv['normalized_nondebug_sections_equal'] or not rv['comdat_selection_and_weak_lookup_equal'] or sha(report)!=item['archived_comparison_sha256']:raise ValueError('reuse provenance differs '+str(i))
 if inventory['recipe_sha256']!=BASE or extra['recipe_sha256']!=BASE or any(extra[k]!=old[995][k] for k in ('source','flags','compiler')):raise ValueError('archive source or recipe mismatch')
 pos=M/'out/phase2-native-source-positive/evidence';pm=pos/'capture-manifest.json'
 if sha(pm)!=POSITIVE:raise ValueError('positive archive manifest mismatch')
 positive=json.loads(pm.read_text());pos620=next(x for x in positive['objects'] if x['unit']==620)
 if positive.get('ten_snapshot_inputs_verified') is not True or any(pos620[k]!=old[620][k] for k in ('source','flags','compiler')):raise ValueError('unit620 archive provenance differs')
 def object_for(i):return (special/'0995.obj',extra['object_sha256']) if i==995 else ((pos/'0620.obj',pos620['sha256']) if i==620 else (archive/('%04d.obj'%i),entries[i]['sha256']))
 for i in UNITS:
  obj,h=object_for(i)
  if sha(obj)!=h:raise ValueError('archived object changed '+str(i))
  d=M/('out/phase2-nimem-next-source-composed-u%04d'%i);m=json.loads((d/'mirror-manifest.json').read_text());row=next(x for x in proposal['affected_units'] if x['unit']==i)
  if m['proposal_manifest_sha256']!=PIN or m['original']!=row['original'] or m['candidate']!=row['candidate']:raise ValueError('mirror evidence changed '+str(i))
 out=M/'out/phase2-nimem-next-source-joint-ten';
 if out.exists():raise FileExistsError('preserve prior run')
 tools=[H/'nimem_combined_825d_compile.py',H/'nimem_next_source_compare.py'];guards=locks.acquire_guard()
 try:
  check()
  if sha(F/'build/units.json')!=BASE or sha(am)!=ARCHIVE or sha(sm)!=a.archive_995_manifest_sha256.lower() or sha(pm)!=POSITIVE:raise ValueError('changed after lock')
  out.mkdir();result={'status':'running','proposal_sha256':PIN,'archive_sha256':ARCHIVE,'archive_995_sha256':sha(sm),'archive_995_provenance':extra.get('provenance'),'units':[],'limits':['raw and NiMem-TD-only normalized sections retain API/deleting-wrapper differences','strict unmodified reference and EH errors remain visible','production label rederivation, cross-unit ownership, full class ODR and final image/runtime remain separate']}
  def save():
   q=out/'progress.tmp';q.write_text(json.dumps(result,indent=2));os.replace(q,out/'progress.json')
  def command(i,label,args):
   check();log=out/('%04d-%s.log'%(i,label))
   with log.open('xb') as f:r=subprocess.run([sys.executable]+[str(x) for x in args],cwd=F.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,timeout=1800)
   check();return r.returncode
  save()
  for i in UNITS:
   d=M/('out/phase2-nimem-next-source-composed-u%04d'%i);obj,h=object_for(i);entry={'unit':i}
   if sha(obj)!=h or sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN:raise ValueError('frozen input changed')
   entry['compile_rc']=command(i,'compile',[tools[0],'--unit',i,'--out',d])
   if entry['compile_rc']==0:
    entry['compare_rc']=command(i,'compare',[tools[1],'--unit',i,'--out',d,'--production-object',obj,'--production-object-sha256',h])
    if entry['compare_rc']==0:
     r=json.loads((d/'comparison.json').read_text());entry['comparison_sha256']=sha(d/'comparison.json');entry['coff_sections_sha256']=sha(d/'coff-sections-raw.json');entry['matches']={k:v.get('matches') for k,v in r['reference'].items()};entry['pair_differences']=len(r['mapped_function_pair_differences']);entry['eh_errors']={k:len(v['errors']) for k,v in r['ordinary_eh'].items()};entry['eh_failed']={k:sum(not x[2] for x in v['eh_sections']) for k,v in r['ordinary_eh'].items()}
   result['units'].append(entry);save()
  pe=Pe(paths.REF_IMAGE);result['ordinary_eh_union']={}
  for tag in ('production','original','candidate'):
   done=[];included=[]
   for i in UNITS:
    q=M/('out/phase2-nimem-next-source-composed-u%04d/comparison.json'%i)
    if q.exists():done.append(json.loads(q.read_text())['ordinary_eh'][tag]);included.append(i)
   specs=new if tag=='candidate' else old;tails,bad,inferred,_,conflicts=eh_tails([specs[i] for i in included],done,pe)
   result['ordinary_eh_union'][tag]={'reports':len(done),'complete_ten':len(done)==len(UNITS),'requested_unique_tails':len(tails),'bad':bad,'inferred_tails':len(inferred),'conflicts':conflicts,'limitation':'outside owner contributions, including 995 owner 2634, are not silently assumed'}
  result['status']='complete-review-required';save()
 finally:
  for q in reversed(guards):q.unlink()
if __name__=='__main__':main()
