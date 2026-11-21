"""Package the reviewed next data batch against the exact accepted preimages."""
import hashlib,json,shutil
from pathlib import Path
M=Path(__file__).resolve().parent.parent;RN=M.parent;ROOT=RN.parent;A=M/'out/phase2-flags-script-positive/evidence';O=M/'out/phase2-next-data-transaction6757'
CORE=[('runtime-next/m3/gen_m3.py','out/phase2-point3-proposal/baseline-gen_m3.py','out/phase2-cost245-proposal/candidate-gen_m3.py'),
 ('runtime-next/m3/phase2/cost245_records.py','out/phase2-cost245-proposal/baseline-cost245_records.py','out/phase2-cost245-proposal/candidate-cost245_records.py'),
 ('runtime-next/m3/splice.py','out/phase2-align16/baseline-splice.py','out/phase2-align16/candidate-splice.py'),
 ('runtime-next/m3/m3secs.py','out/phase2-align16/baseline-m3secs.py','out/phase2-align16/candidate-m3secs.py'),
 ('runtime-next/layout-v2/make_image.py','out/phase2-align16/baseline-make_image.py','out/phase2-align16/candidate-make_image.py'),
 ('runtime-next/m3/phase2/library_overlay.py','out/phase2-library-splits/baseline-library_overlay.py','out/phase2-library-splits/candidate-library_overlay.py')]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 prior=load(M/'phase2/next_batch_manifest.json')
 for key in ('next_m3_selection','next_generator','cost245_hardened_helper','simd_splice','simd_m3secs','simd_image_builder','next_library_selection','next_library_overlay'):
  x=prior['inputs'][key]
  if sha((M/x['path']).read_bytes())!=x['sha256']:raise ValueError('staged input changed '+key)
 for n,h in {'selection.json':'2dc3eb28083648d0d701268d8aa858a4d90fddd45e6ffb2613073cbb83672045','library_candidates.json':'da19c0a782f6ba4ac986e992daf4af7ed67c282d0b70f35e8804a22227bce645','units.json':'6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'}.items():
  if sha((A/n).read_bytes())!=h:raise ValueError('accepted archive mismatch '+n)
 if sha((ROOT/'fnv_decomp/build/units.json').read_bytes())!=sha((A/'units.json').read_bytes()):raise ValueError('live recipe differs from accepted epoch')
 for x in prior['source_evidence']:
  if sha((ROOT/x['path']).read_bytes())!=x['sha256']:raise ValueError('source evidence changed '+x['path'])
 selected=load(M/'out/phase2-cost245-proposal/selection.json')['entries'];current=load(A/'selection.json')['entries'];lib=load(M/'out/phase2-library-splits/selection-with-atan.json')['candidates'];dv=load(A/'dv1_pieces.json')['pieces']
 sizes={'H':4,'I':4,'M':4,'N':8,'J':4,'K':4,'F':2,'G':2,'D':1,'E':1,'_N':1,'C':1,'P':4}
 def span(x):return x['va'],x['va']+(sizes[x['tc']] if x['tc'] in sizes else x['size'])
 def merge(rows):
  out=[]
  for a,b in sorted(rows):
   if out and a<out[-1][1]:raise ValueError('overlapping selection')
   if out and a==out[-1][1]:out[-1]=(out[-1][0],b)
   else:out.append((a,b))
  return out
 if len(current)!=8265 or len(selected)!=8268 or merge(map(span,current))!=merge(map(span,selected)):raise ValueError('M3 union changed')
 merge((x['va'],x['va']+x['size']) for x in lib)
 for x in selected:
  a,b=span(x)
  if any(a<y['va']+y['size'] and y['va']<b for y in dv):raise ValueError('M3 and DV1 overlap')
 same=[];extra=[]
 for x in lib:
  matches=[y for y in dv if x['va']<y['va']+y['size'] and y['va']<x['va']+x['size']]
  if matches:
   if len(matches)!=1:raise ValueError('ambiguous library overlap')
   y=matches[0]
   if (x['va'],x['size'],x['unit'])!=(y['va'],y['size'],y['unit']) or not y.get('library_opt_in') or sha(bytes.fromhex(y['data']))!=x['compiler_bytes_sha256']:raise ValueError('library ownership differs')
   same.append(x)
  else:extra.append(x)
 if (len(same),sum(x['size'] for x in same),len(extra),sum(x['size'] for x in extra))!=(370,6374,35,10356):raise ValueError('library accounting differs')
 point=load(M/'out/phase2-point3/isolated-fixture/result.json');simd=load(M/'out/phase2-align16/isolated-fixture/result.json');cost=load(M/'out/phase2-cost245-proposal/isolated-fixture/result.json')
 if point['head']['size']!=12 or point['tail_size']!=252 or point['tail_relocations']!=2 or simd['head_count']!=2 or simd['head_bytes']!=32 or cost['entries']!=2 or cost['bytes']!=384 or cost['relocations']!=59:raise ValueError('fixture results differ')
 if cost['generator_sha256']!=prior['inputs']['next_generator']['sha256'] or cost['helper_sha256']!=prior['inputs']['cost245_hardened_helper']['sha256']:raise ValueError('cost fixture provenance differs')
 for dest,base,generated in CORE:
  if (ROOT/dest).read_bytes()!=(M/base).read_bytes():raise ValueError('core preimage differs '+dest)
 O.mkdir(exist_ok=False);entries=[]
 for i,(dest,base,generated) in enumerate(CORE):
  old=(ROOT/dest).read_bytes();new=(M/generated).read_bytes();(O/(str(i)+'.original')).write_bytes(old);(O/(str(i)+'.generated')).write_bytes(new)
  entries.append({'path':dest,'old_sha256':sha(old),'new_sha256':sha(new),'original':str(i)+'.original','generated':str(i)+'.generated'})
 for name,p in (('selection.json',M/'out/phase2-cost245-proposal/selection.json'),('library_candidates.json',M/'out/phase2-library-splits/selection-with-atan.json')):shutil.copyfile(p,O/name)
 results={'schema':1,'scope':'private guarded code payload and opt-in selections; not installed','accepted_epoch_recipe_sha256':sha((A/'units.json').read_bytes()),
  'accepted_selection_sha256':sha((A/'selection.json').read_bytes()),'accepted_library_sha256':sha((A/'library_candidates.json').read_bytes()),
  'accepted_m3_manifest_sha256':sha((A/'m3_manifest.json').read_bytes()),'accepted_dv1_pieces_sha256':sha((A/'dv1_pieces.json').read_bytes()),
  'files':entries,'selection_sha256':sha((O/'selection.json').read_bytes()),'library_selection_sha256':sha((O/'library_candidates.json').read_bytes()),
  'range_proof':{'accepted_entries':8265,'candidate_entries':8268,'m3_union_equal':True,'m3_dv1_disjoint':True,'library_existing_pieces':370,'library_existing_bytes':6374,'library_incremental_pieces':35,'library_incremental_bytes':10356},
  'fixture_sha256':{n:sha((M/p).read_bytes()) for n,p in {'point3':'out/phase2-point3/isolated-fixture/result.json','simd':'out/phase2-align16/isolated-fixture/result.json','cost':'out/phase2-cost245-proposal/isolated-fixture/result.json'}.items()},
  'limitations':['all six code changes must be reviewed/integrated together','captured fixture success is not an integrated build','Cost245 int fields transport address-valued data and are not proven native pointers','atan smaller overlapping annotations remain unresolved provenance','fresh library placement, controls, repeat and full gameplay required','accepted defaults remain unchanged']}
 (O/'manifest.json').write_text(json.dumps(results,indent=2),encoding='utf8');print(json.dumps({'manifest_sha256':sha((O/'manifest.json').read_bytes()),'files':len(entries),'selection_sha256':results['selection_sha256'],'library_sha256':results['library_selection_sha256']}))
if __name__=='__main__':main()
