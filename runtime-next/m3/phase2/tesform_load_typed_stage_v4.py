"""Stage guarded ten-remap TESForm/BGSE source and mirror-recipe candidate."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-tesform-load-typed-v4-transaction';T=M/'out/phase2-tesform-load-typed-v4-mirror';B=M/'out/phase2-bgs-load-typed-v4-mirror';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,tescontainer_install as replace,rtti_bgse_six_compare as bg,rtti_mirror_compare as mirror
FA='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';REF='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'
PINS={'phase2-load-typed-v4-paired-report.json':'cd73fec0f934d3f5746b400ae8b72d6585d255ed869f94d2bead514627846972','phase2-tesform-load-typed-v4-mirror/noop-proof.json':'149a0dda6b718f334959a8b7d48538f2d3e4b579adba1038163db653e14a836d','phase2-class-typed-v4/tesform-manifest.json':'6b002a3ebb57b08f604bb94610af42707ed02be50dc04d4554303556c4bbf38e','phase2-class-typed-v4/bgs-manifest.json':'51ba4eda3a1073fa497d74d6b10ad965d6b303a891352703e4be84878ff23eb9','phase2-tesform-load-typed-v4-mirror/mirror-manifest.json':'e1cbe91590f6da29021e92abaa41d2a0f922d37e0bfa080b6b5bf149192df87b','phase2-bgs-load-typed-v4-mirror/mirror-manifest.json':'f6da1ff3a2e3e5c2f0b412928f97c3b0da575e27452edd7b989be2b7fd3c77ac'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(path):return json.loads(path.read_bytes())
def remap(unit,changes):
 if len({x['before'] for x in changes})!=len(changes):raise ValueError('duplicate source function')
 out=copy.deepcopy(unit);names={x['before']:x['after'] for x in changes};hits=0
 for f in out['functions']:
  if f['symbol'] in names:
   x=next(q for q in changes if q['before']==f['symbol'])
   if f['address']!=x['address'] or f['size']!=x['size']:raise ValueError('function identity changed')
   f['symbol']=x['after'];hits+=1
  if 'fold_aliases' in f:f['fold_aliases']=[names.get(x,x) for x in f['fold_aliases']]
 if hits!=len(changes):raise ValueError('missing remapped functions')
 symbols={}
 for k,v in unit['symbols'].items():
  n=names.get(k,k)
  if n in symbols and symbols[n]!=v:raise ValueError('symbol collision')
  symbols[n]=v
 out['symbols']=symbols;return out

def main():
 for rel,d in PINS.items():
  if sha((M/'out'/rel).read_bytes())!=d:raise ValueError('proof changed '+rel)
 raw=(F/'build/units.json').read_bytes()
 if sha(raw)!=FA or sha(Path(paths.REF_IMAGE).read_bytes())!=REF:raise ValueError('recipe/reference changed')
 u=json.loads(raw)['units'];tm=load(M/'out/phase2-class-typed-v4/tesform-manifest.json');bm=load(M/'out/phase2-class-typed-v4/bgs-manifest.json');proof=load(M/'out/phase2-load-typed-v4-paired-report.json');noop=load(T/'noop-proof.json')
 if len(tm['proposed_function_symbol_changes'])!=11 or len(bm['proposed_function_symbol_changes'])!=9 or proof['units_sha256']!=FA or proof['tes_functions_equal_and_strict']!=128 or proof['bgs_functions_equal_and_strict']!=24:raise ValueError('scope/proof mismatch')
 if sha((T/'candidate.obj').read_bytes())!=proof['tes_obj_sha256'] or sha((B/'candidate.obj').read_bytes())!=proof['bgs_obj_sha256'] or proof['noop_proof_sha256']!=sha((T/'noop-proof.json').read_bytes()) or noop['identical_bodies'] is not True:raise ValueError('object/noop proof mismatch')
 fold=tm['proposed_noop_fold'];owners=[f for q in u for f in q['functions'] if f['address']==fold['source_address']]
 if len(owners)!=1 or owners[0]['symbol']!=fold['source_body_symbol'] or owners[0]['size']!=11:raise ValueError('fold owner changed')
 # Object-derived names, not guessed class-key decoration.
 discovered=proof['discovered_typed_symbols']
 for x in tm['proposed_function_symbol_changes']:
  if x['address']=='0x00484da0':x['after']=discovered['tes_load']
 for x in bm['proposed_function_symbol_changes']:
  if x['address']=='0x005264a0':x['after']=discovered['bgs_load']
  if x['address']=='0x00526570':x['after']=discovered['bgs_revert']
 tu=remap(u[998],tm['proposed_function_symbol_changes']);bu=remap(u[2],bm['proposed_function_symbol_changes']);owner=next(f for f in tu['functions'] if f['address']==fold['source_address'])
 source_aliases=load(M/'out/phase2-class-typed-v4/manifest.json')['base_external_symbol_aliases']
 if len(source_aliases)!=2:raise ValueError('typed external aliases missing')
 for x in source_aliases:
  x['after']=discovered['base_load'] if 'LoadGame@TESForm' in x['before'] else discovered['base_revert']
  if u[2]['symbols'].get(x['before'])!=x['address']:raise ValueError('typed base-call source evidence changed')
  if x['after'] in bu['symbols'] and bu['symbols'][x['after']]!=x['address']:raise ValueError('typed base-call collision')
  bu['symbols'][x['after']]=x['address']
 if owner.get('fold_aliases'):raise ValueError('owner aliases already set')
 owner['fold_aliases']=fold['new_symbols'];literal={}
 for fact in proof['candidate_literal_fields']:
  k=fact['after'];v=fact['binding']
  if k in literal and literal[k]!=v:raise ValueError('ambiguous literal')
  literal[k]=v
 if len(literal)!=9:raise ValueError('unexpected mirror literal count')
 for k,v in literal.items():tu['symbols'][k]=v
 pe=Pe(paths.REF_IMAGE);r=compare(Coff(str(T/'candidate.obj')),pe,tu)
 if len(r)!=128 or any(x['verdict']!='match' for x in r):raise ValueError('TES candidate not 128/128')
 # Strict comparator has no global recipe resolver; this one scoped diagnostic
 # alias is NOT installed. Existing units 658 and 973 agree at this address.
 alias='??1TESForm@@UAE@XZ';va='0x00483630'
 if any(u[i]['symbols'].get(alias)!=va for i in (658,973)):raise ValueError('global destructor evidence changed')
 diag=copy.deepcopy(bu);diag['symbols'][alias]=va
 for x in tm['proposed_function_symbol_changes']:diag['symbols'][x['after']]=x['address']
 for name in fold['new_symbols']:diag['symbols'][name]=fold['source_address']
 r=compare(Coff(str(B/'candidate.obj')),pe,diag)
 if len(r)!=24 or any(x['verdict']!='match' for x in r):raise ValueError('BGSE candidate not 24/24')
 graph=proof['graph']['tables'];slots=[x for table in graph for x in table['slots']]
 if len(slots)!=78 or sum(x['match'] for x in slots)!=26 or any(not next(x for x in slots if x['index']==i)['match'] for i in (21,22)):raise ValueError('slot evidence changed')
 rows=[]
 for root,rel in [(T,'src/fallout_shared/tesform.cpp'),(T,'src/fallout_shared/tesform_TESForm.h'),(B,'src/bgsencounterzone.cpp'),(B,'src/bgsencounterzone_decls.h'),(B,'src/bgsencounterzone_TESForm.h')]:
  m=load(root/'mirror-manifest.json');old=(F/rel).read_bytes();new=(root/'candidate'/rel).read_bytes()
  if sha(old)!=m['original_inputs'][rel] or sha(new)!=m['candidate']['files'][rel]:raise ValueError('source payload changed '+rel)
  rows.append((rel,old,new))
 recipe=replace.replace_unit(raw,2,bu);recipe=replace.replace_unit(recipe,998,tu);new=json.loads(recipe);prior=json.loads(raw)
 if [i for i,(a,b) in enumerate(zip(prior['units'],new['units'])) if a!=b]!=[2,998] or any(prior[k]!=new[k] for k in prior if k!='units'):raise ValueError('recipe scope changed')
 eh={}
 for label,root in [('tes',T),('bgs',B)]:
  a=mirror.exception_sections(Coff(str(root/'original.obj')));b=mirror.exception_sections(Coff(str(root/'candidate.obj')))
  if a.keys()!=b.keys() or any(a[k]!=b[k] for k in a):raise ValueError('EH section mismatch '+label)
  eh[label]={'matching_named_section_tails':len(a),'scope':'exact section-tail bytes and relocations; not all object thunks or final placement'}
 if O.exists():raise FileExistsError('refusing overwrite')
 O.mkdir();files=[]
 for i,(rel,old,new) in enumerate(rows):
  (O/(str(i)+'.original')).write_bytes(old);(O/(str(i)+'.generated')).write_bytes(new);files.append({'path':rel,'old_sha256':sha(old),'new_sha256':sha(new),'original':str(i)+'.original','generated':str(i)+'.generated'})
 (O/'5.original').write_bytes(raw);(O/'5.generated').write_bytes(recipe);files.append({'path':'build/units.json','old_sha256':FA,'new_sha256':sha(recipe),'original':'5.original','generated':'5.generated'})
 meta={'schema_version':1,'base_units_sha256':FA,'files':files,'evidence_sha256':PINS,'unit2_function_remaps':bm['proposed_function_symbol_changes'],'unit998_function_remaps':tm['proposed_function_symbol_changes'],'noop_fold':fold,'mirror_only_literal_bindings':literal,'source_backed_typed_base_bindings':source_aliases,'diagnostic_global_destructor_binding':{'symbol':alias,'address':va,'independent_units':[658,973],'installed_in_recipe':False},'private_strict_matches':{'unit998':128,'unit2':24},'eh_section_evidence':eh,'slot_matches':26,'slot_total':78,'slot21':next(x for x in slots if x['index']==21),'slot22':next(x for x in slots if x['index']==22),'status':'private staged transaction; mirror labels must be rederived from actual installed production object before any full build','limitations':['52 observed BGSE slots still unmatched or unresolved','native class/ODR identity and full vtable extent unresolved','provisional no-op folding needs final ownership/ICF verification','original and candidate EH section tails match but removed surrogate deleting destructor requires ownership review','production object can renumber literal labels; mirror bindings must never be assumed valid']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'files':len(files),'recipe_sha256':sha(recipe),'unit998':128,'unit2':24,'eh':eh}))
if __name__=='__main__':main()

