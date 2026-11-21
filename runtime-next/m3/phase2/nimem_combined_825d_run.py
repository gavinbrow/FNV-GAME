"""Run the 128-unit native operator cohort on a serialized verifier lane."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';P=M/'out/phase2-nimem-combined-825d';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PIN='6b9dc1950f489c696364820186a4beba3e1618d127c4a656ecb677b53e32e1a3';sys.path[:0]=[str(H),str(F/'tools'),str(RN)];import rtti_tesform_bindings_transaction as locks
from compare import Pe
from build_and_match import eh_tails
import paths
import baseformcomponent_core_stage as core
ARCHIVE_PIN='25e303cfcef7555e59437901586e1085cec1df91b6487d9acb1bee6e12a30bdc'
EXTRA_PIN='6279b74d19087a65dda4ec37c22e3c96a1dd1c5bb3b26455f94a72bee96f1e08'
SECTION_PIN='29db1fc1dc763665d70c7f2bb2af81672dfc4b7877d4d271a39cace3463df428'
CLOSURE_PIN='e38e07bd411a44d165e81e80034b9f0fb231311973b8a6b977571470ab63051c'
class ToolDrift(RuntimeError):pass
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_tool_closure(root,manifest,expected,self_path,self_pin):
 if sha(manifest)!=expected or sha(self_path)!=self_pin:raise ToolDrift('runner or closure manifest changed')
 for name,digest in json.loads(manifest.read_text())['files'].items():
  if sha(root/name)!=digest:raise ToolDrift('tool changed: '+name)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--archive',type=Path,required=True);p.add_argument('--archive-manifest-sha256',required=True);p.add_argument('--extra-archive',type=Path,required=True);p.add_argument('--extra-archive-manifest-sha256',required=True);p.add_argument('--runner-sha256',required=True);p.add_argument('--ack-serialized-lane',action='store_true');a=p.parse_args();out=a.out.resolve();archive=a.archive.resolve();am=archive/'manifest.json';closure=P/'tool-closure.json'
 def check_tools():verify_tool_closure(F.parent,closure,CLOSURE_PIN,Path(__file__),a.runner_sha256.lower())
 check_tools()
 if not a.ack_serialized_lane or out.exists() or not out.is_relative_to((M/'out').resolve()) or not out.name.startswith('phase2-') or not archive.is_relative_to((M/'out').resolve()):raise ValueError('fresh private paths and serialized lane required')
 if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN or sha(am)!=ARCHIVE_PIN or a.archive_manifest_sha256.lower()!=ARCHIVE_PIN or a.extra_archive_manifest_sha256.lower()!=EXTRA_PIN:raise ValueError('pinned input differs')
 proposal=json.loads((P/'manifest.json').read_text());items=proposal['combined_api_units']+proposal['fresh_kind_only_units'];old=json.loads((P/'units.original').read_text())['units'];new=json.loads((P/'units.generated').read_text())['units']
 if len(items)!=133:raise ValueError('cohort scope differs')
 inventory=json.loads(am.read_text());entries={x['unit']:x for x in inventory['objects']}
 extra=a.extra_archive.resolve(); em=extra/'capture-manifest.json'; extra_inventory=json.loads(em.read_text()); extra_entries={x['unit']:x for x in extra_inventory['objects']}; extra_ids={253,370,621,2909,2910}
 if not extra.is_relative_to((M/'out').resolve()) or sha(em)!=EXTRA_PIN or inventory['recipe_sha256']!=BASE or extra_inventory.get('ten_snapshot_inputs_verified') is not True or len(entries)!=len(inventory['objects']) or len(extra_entries)!=len(extra_inventory['objects']) or not extra_ids<=set(extra_entries) or not ({x['unit'] for x in items}-extra_ids)<=set(entries):raise ValueError('archive provenance differs')
 if any(any(extra_entries[i][k]!=old[i][k] for k in ('source','flags','compiler')) for i in extra_ids):raise ValueError('extra archive source/flags differ')
 def archive_item(i):return (extra,extra_entries[i]) if i in extra_ids else (archive,entries[i])
 tools=[H/x for x in ('nimem_combined_825d_prepare.py','nimem_combined_825d_compile.py','nimem_combined_825d_compare.py')];toolhash={x.name:sha(x) for x in tools};guards=locks.acquire_guard()
 try:
  check_tools()
  if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN or sha(am)!=ARCHIVE_PIN or sha(em)!=EXTRA_PIN:raise ValueError('input changed after lock')
  scope_path=M/'out/phase2-nimemobject-coherent-kind-consumers.json';scope=json.loads(scope_path.read_text());scope_rows={x['unit']:x for x in scope['units']};oldpath=M/'out/phase2-source-integration6757-transaction-v2/0.original'
  if sha(oldpath)!='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c':raise ValueError('old recipe changed')
  previous=json.loads(oldpath.read_text())['units']
  section_path=M/'out/phase2-nimem-kind-root-section-review.json'
  if sha(scope_path)!='c45dad435c9c172c149afa1fb4054ae5844f59299e1a1dcb6ffaa1e3ca2bc67f' or sha(section_path)!=SECTION_PIN or len(proposal['unchanged_kind_only_units'])!=618:raise ValueError('reuse evidence changed')
  bindings=M/'out/phase2-nimem-kind-source-bindings-final.json'
  if sha(bindings)!='1b08d57f69d9fb473ed511de4b9dfc172072f3836244cdce596774cf413200de':raise ValueError('source-backed diagnostics changed')
  section={r['unit']:r for r in json.loads(section_path.read_text())['units']}
  for reuse in proposal['unchanged_kind_only_units']:
   i=reuse['unit'];r=section[i];scope_row=scope_rows[i]
   report=M/('out/phase2-nimem-kind-cohort-run/unit-%04d/comparison.json'%i)
   if old[i]!=previous[i] or core.walk(F,old[i]['source'],{})['files']!=scope_row['quoted_project_closure'] or not r['normalized_nondebug_sections_equal'] or not r['comdat_selection_and_weak_lookup_equal'] or r['comparison_sha256']!=reuse['archived_comparison_sha256'] or sha(report)!=reuse['archived_comparison_sha256']:raise ValueError('reuse evidence mismatch '+str(i))
  for x in items:
   i=x['unit'];objdir,entry=archive_item(i);obj=objdir/('%04d.obj'%i)
   if not obj.exists() or ('size' in entry and obj.stat().st_size!=entry['size']) or sha(obj)!=entry['sha256']:raise ValueError('archived object differs '+str(i))
  out.mkdir();logs=out/'logs';logs.mkdir();result={'status':'running','recipe_sha256':BASE,'proposal_sha256':PIN,'archive_manifest_sha256':sha(am),'tool_sha256':toolhash,'unit_count':len(items),'function_count':sum(len(x['functions']) for x in items),'requested_recipe_eh_tails':sum(len(x['eh_tails']) for x in items),'extra_archive_manifest_sha256':sha(em),'reused_kind_only_count':618,'source_binding_diagnostics_sha256':sha(bindings),'units':[],'limits':['private API effects, generated/deleting code and source baseline failures require independent review','source binding proof is an index for field-scoped diagnosis, not an applied map; 44 historical immediate proofs remain field-scoped','no automatic normalization or unsupported function aliases','listed EH coverage does not clear other located section failures','first declaration/packing, weak/COMDAT/linker and full image/runtime remain separate']}
  def save():
   q=out/'progress.tmp';q.write_text(json.dumps(result,indent=2));os.replace(q,out/'progress.json')
  def command(i,label,args):
   check_tools()
   log=logs/('%04d-%s.log'%(i,label))
   with log.open('xb') as f:r=subprocess.run([sys.executable]+[str(x) for x in args],cwd=F.parent,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,timeout=1800)
   check_tools()
   return {'rc':r.returncode,'log':str(log.relative_to(out))}
  save()
  for x in items:
   i=x['unit'];d=out/('unit-%04d'%i);entry={'unit':i,'functions':len(x['functions']),'eh_tails':len(x['eh_tails'])}
   try:
    if sha(F/'build/units.json')!=BASE or sha(P/'manifest.json')!=PIN or sha(am)!=ARCHIVE_PIN or sha(em)!=EXTRA_PIN or any(sha(t)!=toolhash[t.name] for t in tools):raise ValueError('inputs changed')
    entry['prepare']=command(i,'prepare',[tools[0],'--unit',i,'--out',d])
    if entry['prepare']['rc']:raise ValueError('mirror preparation failed')
    entry['compile']=command(i,'compile',[tools[1],'--unit',i,'--out',d])
    if entry['compile']['rc']:raise ValueError('compiler or trace failed')
    objdir,objentry=archive_item(i);entry['compare']=command(i,'compare',[tools[2],'--unit',i,'--out',d,'--production-object',objdir/('%04d.obj'%i),'--production-object-sha256',objentry['sha256']])
    if entry['compare']['rc']:raise ValueError('comparison execution failed')
    r=json.loads((d/'comparison.json').read_text());entry['comparison_sha256']=sha(d/'comparison.json');entry['coff_section_report_sha256']=sha(d/'coff-sections-raw.json');entry['kind_normalized_pair']=json.loads((d/'coff-sections-raw.json').read_text())['kind_normalized_pair'];entry['strict_matches']={k:v.get('matches') for k,v in r['reference'].items()};entry['pair_differences']=len(r['mapped_function_pair_differences']);entry['warning_count']=sum(len(v) for v in r['compiler_warnings'].values());entry['eh_errors']={k:len(v['errors']) for k,v in r['ordinary_eh'].items()};entry['failed_eh_sections']={k:sum(not y[2] for y in v['eh_sections']) for k,v in r['ordinary_eh'].items()};entry['status']='pass' if all(v==entry['functions'] for v in entry['strict_matches'].values()) and not entry['pair_differences'] and not entry['warning_count'] and not any(entry['eh_errors'].values()) and not any(entry['failed_eh_sections'].values()) and (i not in extra_ids or (entry['kind_normalized_pair']['nondebug_sections_equal'] and entry['kind_normalized_pair']['comdat_and_weak_equal'])) else 'review-required'
   except ToolDrift:raise
   except Exception as e:entry['status']='failed';entry['error']=str(e)
   result['units'].append(entry);save();print(json.dumps({'unit':i,'status':entry['status']}),flush=True)
  done={'production':[],'original':[],'candidate':[]}
  for x in result['units']:
   q=out/('unit-%04d/comparison.json'%x['unit'])
   if q.exists():
    r=json.loads(q.read_text())
    for tag in done:done[tag].append(r['ordinary_eh'][tag])
  pe=Pe(paths.REF_IMAGE);result['ordinary_eh_union']={}
  for tag in done:
   units=new if tag=='candidate' else old;tails,bad,inferred,_,conflicts=eh_tails([units[x['unit']] for x in items],done[tag],pe);result['ordinary_eh_union'][tag]={'requested_unique_tails':len(tails),'bad':bad,'inferred_tails':len(inferred),'conflicts':conflicts,'reports':len(done[tag]),'complete_scope':len(done[tag])==len(items)}
  result['status']='function-and-eh-pass-metadata-review-required' if all(x['status']=='pass' for x in result['units']) and all(not x['bad'] and not x['conflicts'] and x['complete_scope'] for x in result['ordinary_eh_union'].values()) else 'complete-review-required';save()
 finally:
  for q in reversed(guards):q.unlink()
 if result['status']=='complete-review-required':raise SystemExit(1)
if __name__=='__main__':main()
