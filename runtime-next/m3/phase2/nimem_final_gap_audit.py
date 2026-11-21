"""Bound pre-existing normal gaps and compare EH failures field by field."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';P=R/'phase2-nimem-next-source-composed';OUT=R/'phase2-nimem-final-gap-audit.json';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,recipe_names
from rtti_hkp_viewer_compare import relocated
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve evidence')
 idx=R/'phase2-nimem-next-source-proof-index-v4.json'
 if sha(idx)!='f02c075f5dff6da865990f0fb85c06eb49192955389f42f5610195cfe5e9b826':raise ValueError('proof index changed')
 index=json.loads(idx.read_text());old=json.loads((R/'phase2-nimem-combined-825d/units.generated').read_text())['units'];new=json.loads((P/'units.generated').read_text())['units'];pe=Pe(paths.REF_IMAGE)
 if sha(P/'units.generated')!=index['recipe_sha256']:raise ValueError('recipe changed')
 owner=R/'phase2-nimem-kind-production-archive/0574.obj'
 if sha(owner)!='0422135a4db5a064496dacd029a2890057a9a117729f5c4ff786afbf30dd5074':raise ValueError('owner object changed')
 owner_recipe=json.loads((R/'phase2-source-integration6757-transaction-v2/0.original').read_text())['units'][574];owner_result=compare(Coff(str(owner)),pe,owner_recipe);method=[x for x in owner_result if x['address']=='0x00867d60']
 if len(method)!=1 or method[0]['verdict']!='match':raise ValueError('Calendar source owner fails strict reference')
 result={'calendar_owner':{'unit':574,'source':'src/fallout/misc/calendar.cpp','symbol':'?GetDayOfMonth@Calendar@@QAEHXZ','address':'0x00867d60','size':55,'object_sha256':sha(owner),'strict_matches':sum(x['verdict']=='match' for x in owner_result),'strict_functions':len(owner_result),'method_result':method[0]},'normal_gaps':[],'eh_units':[]}
 for i in (368,1592):
  d=R/('phase2-nimem-combined-825d-run/unit-%04d'%i);obj=d/'candidate.obj';c=Coff(str(obj));before=compare(c,pe,old[i]);after=compare(c,pe,new[i]);b={x['address']:x for x in before};a={x['address']:x for x in after};addresses=['0x0090a1a0','0x0090ad40','0x0090c3e0'] if i==368 else ['0x00c2d240']
  for address in addresses:
   f=next(x for x in new[i]['functions'] if x['address']==address);raw,rel=relocated(c,f['symbol'],f['size'],{})
   result['normal_gaps'].append({'unit':i,'address':address,'symbol':f['symbol'],'object_sha256':sha(obj),'function_bytes_sha256':hashlib.sha256(raw).hexdigest(),'relocations':rel,'before':b[address],'after':a[address],'identical_failure':b[address]==a[address]})
  if i==368:
   fixed=copy.deepcopy(new[i]);fixed['symbols']['?GetDayOfMonth@Calendar@@QAEHXZ']='0x00867d60';r=compare(c,pe,fixed);result['calendar_owner_binding_diagnostic']={'matches':sum(x['verdict']=='match' for x in r),'functions':len(r),'failures':[{'address':x['address'],'errors':x['errors']} for x in r if x['verdict']!='match'],'binding':'source-owned unit574 Calendar::GetDayOfMonth','not_installed':True}
 for row in index['source_identical_replay']:
  if not row['failed_eh_sections'] and not row['eh_errors']:continue
  i=row['unit'];d=R/('phase2-nimem-combined-825d-run/unit-%04d'%i);obj=d/'candidate.obj';prior=json.loads((d/'comparison.json').read_text())['ordinary_eh']['candidate'];c=Coff(str(obj));r=compare(c,pe,new[i]);sections,inferred,errors=eh_sections(c,pe,new[i],r,recipe_names(new));after=json.loads(json.dumps({'eh_sections':sections,'eh_inferred':{k:'0x%08x'%v for k,v in inferred.items()},'errors':errors}));bf=[x for x in prior['eh_sections'] if not x[2]];af=[x for x in after['eh_sections'] if not x[2]]
  result['eh_units'].append({'unit':i,'object_sha256':sha(obj),'prior_comparison_sha256':sha(d/'comparison.json'),'before_failed_sections':bf,'after_failed_sections':af,'before_errors':prior['errors'],'after_errors':after['errors'],'same_failed_sections':bf==af,'same_errors':prior['errors']==after['errors'],'same_inferred_bindings':prior['eh_inferred']==after['eh_inferred']})
 result['limits']=['unit1592 PTR is only a source extern and vptr-like assignment; symbol spelling is not evidence of its address or complete object','unchanged diagnostic failures do not imply source or EH correctness','Calendar binding is source-owner-backed diagnostic only; no recipe was modified']
 OUT.write_text(json.dumps(result,indent=2));print(json.dumps({'calendar':result['calendar_owner_binding_diagnostic'],'gap_same':[x['identical_failure'] for x in result['normal_gaps']],'eh_units':[(x['unit'],x['same_failed_sections'],x['same_errors'],x['same_inferred_bindings']) for x in result['eh_units']],'sha256':sha(OUT)}))
if __name__=='__main__':main()
