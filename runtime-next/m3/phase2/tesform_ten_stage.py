"""Stage guarded ten-remap TESForm/BGSE source and mirror-recipe candidate."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out/phase2-tesform-ten-transaction';T=M/'out/phase2-tesform-savegame-mirror';B=M/'out/phase2-bgs-savegame-paired-mirror';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,tescontainer_install as replace,rtti_bgse_six_compare as bg,rtti_mirror_compare as mirror
FA='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';REF='df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7'
PINS={'phase2-tesform-savegame-paired-report.json':'14c71c41d043a73c068d5680e234233a7c0fcbde793deac11fb1c1f81fdab9e1','phase2-tesform-savegame-mirror/noop-proof.json':'612a0a864017d9cf7399aea2b62cc224bddea7bed769ca68a95a86d2de7b248f','phase2-tesform-savegame-slot/manifest.json':'4c5764c6565c237db5cf6467f68502552aa589ee23e6b1bd7189414e354662ea','phase2-bgsencounterzone-slot21-corrected/manifest.json':'72031f365147db7e1e71b99050285b52ec6b7229e9250cfbcea6485044386cc4','phase2-tesform-savegame-mirror/mirror-manifest.json':'bc103580c74eb1a0e9b4e143a37f9117036502c77504a5852f3bccc1aff90600','phase2-bgs-savegame-paired-mirror/mirror-manifest.json':'703e6a0a80ecd966f0ab8792e6f6d2ef6fed202db0a4e31182be32feac64f7a4'}
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
 u=json.loads(raw)['units'];tm=load(M/'out/phase2-tesform-savegame-slot/manifest.json');bm=load(M/'out/phase2-bgsencounterzone-slot21-corrected/manifest.json');proof=load(M/'out/phase2-tesform-savegame-paired-report.json');noop=load(T/'noop-proof.json')
 if len(tm['proposed_function_symbol_changes'])!=10 or len(bm['proposed_function_symbol_changes'])!=9 or proof['units_sha256']!=FA or proof['tes_functions_equal_and_strict']!=128 or proof['bgs_functions_equal_and_strict']!=24:raise ValueError('scope/proof mismatch')
 if sha((T/'candidate.obj').read_bytes())!=proof['tes_obj_sha256'] or sha((B/'candidate.obj').read_bytes())!=proof['bgs_obj_sha256'] or proof['noop_proof_sha256']!=sha((T/'noop-proof.json').read_bytes()) or noop['identical_bodies'] is not True:raise ValueError('object/noop proof mismatch')
 fold=tm['proposed_noop_fold'];owners=[f for q in u for f in q['functions'] if f['address']==fold['source_address']]
 if len(owners)!=1 or owners[0]['symbol']!=fold['source_body_symbol'] or owners[0]['size']!=11:raise ValueError('fold owner changed')
 tu=remap(u[998],tm['proposed_function_symbol_changes']);bu=remap(u[2],bm['proposed_function_symbol_changes']);owner=next(f for f in tu['functions'] if f['address']==fold['source_address'])
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
 meta={'schema_version':1,'base_units_sha256':FA,'files':files,'evidence_sha256':PINS,'unit2_function_remaps':bm['proposed_function_symbol_changes'],'unit998_function_remaps':tm['proposed_function_symbol_changes'],'noop_fold':fold,'mirror_only_literal_bindings':literal,'diagnostic_global_destructor_binding':{'symbol':alias,'address':va,'independent_units':[658,973],'installed_in_recipe':False},'private_strict_matches':{'unit998':128,'unit2':24},'eh_section_evidence':eh,'slot_matches':26,'slot_total':78,'slot21':next(x for x in slots if x['index']==21),'slot22':next(x for x in slots if x['index']==22),'status':'private staged transaction; mirror labels must be rederived from actual installed production object before any full build','limitations':['52 observed BGSE slots still unmatched or unresolved','native class/ODR identity and full vtable extent unresolved','provisional no-op folding needs final ownership/ICF verification','original and candidate EH section tails match but removed surrogate deleting destructor requires ownership review','production object can renumber literal labels; mirror bindings must never be assumed valid']}
 (O/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'files':len(files),'recipe_sha256':sha(recipe),'unit998':128,'unit2':24,'eh':eh}))
if __name__=='__main__':main()

