"""Prepare private four-file typed flag getter/setter transaction; no apply."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';T=M/'out/phase2-flagpairs-transaction';A=M/'out/phase2-tesform-two-flagpairs-mirror';B=M/'out/phase2-bgs-two-flagpairs-mirror';sys.path[:0]=[str(F/'tools'),str(RN),str(H)]
from compare import Coff,Pe,compare
import paths,tescontainer_install as recipe
BASE='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';PROOF='1e83828f55cc404194b33a489dc87557bbd649abdcf4f9fbb96395fc2e450c34';META='f2b0425f64eb938644981af0998b2a81d8b2d182fc0d16a9a54c5a082e9b5d05';TM='dbae87db044f6c2af7d5e40703a550e693b7704251038a90bcfde61cc72782e0';BM='e257a49546c4cdfa70ad5d1a741fdd6f812d6b5926a472a3b2a5851c1ae09027'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if T.exists():raise FileExistsError('refusing overwrite')
 paths_=[(M/'out/phase2-two-flagpairs-report.json',PROOF),(M/'out/phase2-tesform-two-flagpairs-setters/manifest.json',META),(A/'mirror-manifest.json',TM),(B/'mirror-manifest.json',BM)]
 for p,h in paths_:
  if sha(p.read_bytes())!=h:raise ValueError('evidence changed '+p.name)
 proof=json.loads(paths_[0][0].read_bytes());meta=json.loads(paths_[1][0].read_bytes());raw=(F/'build/units.json').read_bytes()
 if sha(raw)!=BASE or proof['recipe_sha256']!=BASE or proof['functions']!={'tes':128,'bgs':24} or proof['eh_named_section_tails']!={'tes':34,'bgs':4}:raise ValueError('scope or proof mismatch')
 if sha((A/'candidate.obj').read_bytes())!=proof['tes_obj_sha256'] or sha((B/'candidate.obj').read_bytes())!=proof['bgs_obj_sha256']:raise ValueError('candidate object mismatch')
 slots=proof['graph']['tables'][0]['slots']
 if len(slots)!=78 or not proof['graph']['tables'][0]['graph_fields_equal'] or any(not next(x for x in slots if x['index']==i)['match'] for i in (39,40,41,42,52,53,54)):raise ValueError('slot proof missing')
 doc=json.loads(raw);u=copy.deepcopy(doc['units'][998]);pairs=[meta['getter'],meta['getter2']]
 for x in pairs:
  f=[f for f in u['functions'] if f['address']==x['address']]
  if len(f)!=1 or f[0]['symbol']!=x['source_symbol'] or f[0]['size']!=x['size'] or f[0].get('fold_aliases'):raise ValueError('source owner changed')
  overlaps=[(i,f) for i,z in enumerate(doc['units']) for f in z['functions'] if int(f['address'],16)<int(x['address'],16)+x['size'] and int(x['address'],16)<int(f['address'],16)+f['size']]
  if len(overlaps)!=1 or overlaps[0][0]!=998:raise ValueError('owner overlap')
  f[0]['symbol']=x['canonical'];f[0]['fold_aliases']=[x['fold_alias']]
 literals={}
 for x in proof['literal_facts']:
  if x['after'] in literals and literals[x['after']]!=x['binding']:raise ValueError('literal ambiguity')
  literals[x['after']]=x['binding']
 if len(literals)!=8:raise ValueError('unexpected mirror label count')
 u['symbols'].update(literals)
 rows=compare(Coff(str(A/'candidate.obj')),Pe(paths.REF_IMAGE),u)
 if len(rows)!=128 or any(x['verdict']!='match' for x in rows):raise ValueError('strict mirror candidate mismatch')
 generated=recipe.replace_unit(raw,998,u);n=json.loads(generated)
 if [i for i,(x,y) in enumerate(zip(doc['units'],n['units'])) if x!=y]!=[998] or any(doc[k]!=n[k] for k in doc if k!='units'):raise ValueError('recipe scope changed')
 files=[]
 for root,rel in [(A,'src/fallout_shared/tesform.cpp'),(A,'src/fallout_shared/tesform_TESForm.h'),(B,'src/bgsencounterzone_TESForm.h')]:
  mm=json.loads((root/'mirror-manifest.json').read_bytes());old=(F/rel).read_bytes();new=(root/'candidate'/rel).read_bytes()
  if sha(old)!=mm['original_inputs'][rel] or sha(new)!=mm['candidate']['files'][rel]:raise ValueError('source payload mismatch '+rel)
  files.append((rel,old,new))
 files.append(('build/units.json',raw,generated));T.mkdir();entries=[]
 for i,(rel,old,new) in enumerate(files):
  (T/(str(i)+'.original')).write_bytes(old);(T/(str(i)+'.generated')).write_bytes(new);entries.append({'path':rel,'old_sha256':sha(old),'new_sha256':sha(new),'original':str(i)+'.original','generated':str(i)+'.generated'})
 result={'scope':'private seven-slot source proposal; no full-class claim','base_units_sha256':BASE,'files':entries,'evidence_sha256':{str(p.relative_to(M/'out')).replace('\\','/'):h for p,h in paths_},'getter_folds':pairs,'setter_alignments':meta['setters'],'mirror_only_literal_bindings':literals,'strict_functions':{'tes':128,'bgs':24},'eh_named_section_tails':proof['eh_named_section_tails'],'matched_slots':33,'status':'prepared; production literal reproof required before any full build','limitations':['other TESForm declarations retain incompatible guessed bool arguments','fold alias placement and global ODR not yet established','mirror literal labels may differ in actual production compilation']}
 (T/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'files':len(files),'recipe_sha256':sha(generated),'literal_labels':len(literals)}))
if __name__=='__main__':main()
