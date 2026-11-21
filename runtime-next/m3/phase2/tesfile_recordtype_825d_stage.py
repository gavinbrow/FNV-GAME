"""Stage 825d-rebased TESFile global correction with proved candidate labels."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-tesfile-recordtype-825d';D=M/'out/phase2-tesfile-recordtype-global';T=M/'out/phase2-source-integration6757-transaction-v2';A=M/'out/phase2-nimem-kind-production-archive';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
from build_and_match import eh_sections,eh_tails,recipe_names
import paths,tescontainer_install
OLD='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';PINS={'manifest.json':'70942035e99ac5326cc2f9017941e040e0b766e586552060526f94f90a368d03','comparison.json':'82f1f333f1cc96c9a715e53f057990b802b9f36c5f2987094e9847486d9f2c5e','eh-outside-owner-proof.json':'e8ba160f8294421374c1fe29941f1eeb07a20011334b5a383b0e6bdbdc976fa2'};TPIN='9422dd1642f66ddca78a1b161b040cdb55847afd3ad447fbf66e86a6ed47e9da';SRC='src/fallout_shared/tesfile.cpp'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve proposal')
 for n,h in PINS.items():
  if sha((D/n).read_bytes())!=h:raise ValueError('source evidence changed '+n)
 if sha((T/'manifest.json').read_bytes())!=TPIN:raise ValueError('transaction provenance changed')
 live=(F/'build/units.json').read_bytes();previous=(T/'0.original').read_bytes();reviewed=(T/'0.candidate').read_bytes()
 if sha(previous)!=OLD or sha(reviewed)!=BASE or live!=reviewed:raise ValueError('reviewed recipe transition differs')
 a=json.loads(previous);b=json.loads(reviewed);current=json.loads(live);changed=[i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y]
 if changed!=[253,370,425,620,2909] or any(a[k]!=b[k] for k in a if k!='units') or a['units'][995]!=b['units'][995] or a['units'][2634]!=b['units'][2634]:raise ValueError('unreviewed semantic transition')
 m=json.loads((D/'manifest.json').read_text());proof=json.loads((D/'comparison.json').read_text());eh=json.loads((D/'eh-outside-owner-proof.json').read_text());source=(F/SRC).read_bytes();before=(D/'source.original').read_bytes();after=(D/'source.generated').read_bytes()
 if source!=before or sha(before)!=m['source_before_sha256'] or sha(after)!=m['source_after_sha256'] or proof['candidate_strict_functions']!=87 or eh['requested_tails']!=4 or eh['bad_tails'] or eh['conflicts']:raise ValueError('source/past proof differs')
 if eh['candidate_comparison_sha256']!=PINS['comparison.json'] or len(proof['candidate_derived_bindings'])!=24:raise ValueError('binding proof differs')
 mm=json.loads((D/'mirror-manifest.json').read_text())
 for rel,digest in mm['original_inputs'].items():
  if sha((F/rel).read_bytes())!=digest:raise ValueError('995 closure changed '+rel)
 u=copy.deepcopy(current['units'][995]);oldsymbols=copy.deepcopy(u['symbols']);sym='?DAT_011873c8@@3IA'
 if current['units'][587]['symbols'].get(sym)!='0x011873c8':raise ValueError('independent source binding changed')
 for name in m['removed_stale_aliases']:
  if u['symbols'].pop(name,None)!='0x011873c8':raise ValueError('stale alias differs '+name)
 u['symbols'][sym]='0x011873c8'
 for name,value in proof['candidate_derived_bindings'].items():u['symbols'][name]=value
 generated=tescontainer_install.replace_unit(live,995,u);afterdoc=json.loads(generated)
 if [i for i,(x,y) in enumerate(zip(current['units'],afterdoc['units'])) if x!=y]!=[995] or any(current[k]!=afterdoc[k] for k in current if k!='units') or any(u[k]!=current['units'][995][k] for k in u if k!='symbols'):raise ValueError('out-of-scope recipe change')
 pe=Pe(paths.REF_IMAGE);candidate=D/'candidate.obj';co=json.loads((D/'compile-result.json').read_text());record=next(x for x in co['outcomes'] if x['tag']=='candidate')
 if record['rc'] or not record['trace_valid'] or sha(candidate.read_bytes())!=record['object_sha256']:raise ValueError('candidate object mismatch')
 rows=compare(Coff(str(candidate)),pe,u)
 if len(rows)!=87 or any(z['verdict']!='match' for z in rows):raise ValueError('candidate strict comparison failed')
 owner=A/'2634.obj';archive=json.loads((A/'manifest.json').read_text());rec=next(x for x in archive['objects'] if x['unit']==2634)
 if sha(owner.read_bytes())!=rec['sha256']:raise ValueError('outside owner archive changed')
 done=[]
 for c,s in ((Coff(str(candidate)),u),(Coff(str(owner)),current['units'][2634])):
  r=compare(c,pe,s);sec,inf,errors=eh_sections(c,pe,s,r,recipe_names(current['units']))
  if any(x['verdict']!='match' for x in r) or errors or any(not x[2] for x in sec):raise ValueError('ordinary EH prerequisite failed')
  done.append({'eh_sections':sec,'eh_inferred':{k:'0x%08x'%v for k,v in inf.items()}})
 tails,bad,inf,_,conf=eh_tails([u],done,pe)
 if len(tails)!=4 or bad or conf:raise ValueError('requested ordinary EH tails failed')
 O.mkdir();(O/'0.original').write_bytes(live);(O/'0.generated').write_bytes(generated);(O/'1.original').write_bytes(before);(O/'1.generated').write_bytes(after)
 changes={k:{'before':oldsymbols.get(k),'after':u['symbols'].get(k)} for k in sorted(oldsymbols.keys()|u['symbols'].keys()) if oldsymbols.get(k)!=u['symbols'].get(k)}
 meta={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(generated),'transition_manifest_sha256':TPIN,'source_evidence_sha256':PINS,'source_closure_sha256':mm['original_inputs'],'files':[{'path':'build/units.json','original':'0.original','generated':'0.generated','old_sha256':sha(live),'new_sha256':sha(generated)},{'path':SRC,'original':'1.original','generated':'1.generated','old_sha256':sha(before),'new_sha256':sha(after)}],'recipe_units_changed':[995],'function_count':87,'candidate_strict':87,'listed_tails_passed':4,'outside_owner_unit':2634,'outside_owner_object_sha256':sha(owner.read_bytes()),'candidate_object_sha256':sha(candidate.read_bytes()),'candidate_literal_count':24,'recipe_symbol_changes':changes,'scope':'source-backed writable record-type global, not string pool alias','limits':['candidate SG labels must be rederived from actual installed production object','global startup initialization and runtime value remain independently unproved','positive image, relocation, ownership and runtime gates required','no active build may run during apply/restore/recover']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'candidate_recipe_sha256':sha(generated),'symbol_changes':len(changes),'functions':87,'ordinary_tails':4}))
if __name__=='__main__':main()
