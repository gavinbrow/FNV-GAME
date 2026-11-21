"""Merge two independently checked disjoint source transactions privately."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;P=RN.parent;F=P/'fnv_decomp';O=M/'out';A=O/'phase2-flagpairs-transaction';B=O/'phase2-tescontainer-script-transaction-v2';T=O/'phase2-combined-source-transaction';sys.path.insert(0,str(H));import tescontainer_install as recipe
BASE='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';AP='58540236d8d682fbd2838599e6ee9d071156b903e3cb48931ae363cbe24a0fe9';BP='36d86875ca04c92df9531336ef0896804a65d74dae3f28c98a8defd9aca83a7a'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if T.exists():raise FileExistsError('no overwrite')
 am=(A/'manifest.json').read_bytes();bm=(B/'manifest.json').read_bytes()
 if sha(am)!=AP or sha(bm)!=BP:raise ValueError('reviewed manifest changed')
 a=json.loads(am);b=json.loads(bm);ar=(A/'3.original').read_bytes();br=(B/'1.original').read_bytes();current=(F/'build/units.json').read_bytes()
 if sha(current)!=BASE or ar!=current or br!=current:raise ValueError('recipe preimage mismatch')
 for tx,m in ((A,a),(B,b)):
  for x in m['files']:
   if sha((tx/x['original']).read_bytes())!=x['old_sha256'] or sha((tx/x['generated']).read_bytes())!=x['new_sha256'] or (F/x['path']).read_bytes()!=(tx/x['original']).read_bytes():raise ValueError('payload mismatch '+x['path'])
 da=json.loads((A/'3.generated').read_bytes());db=json.loads((B/'1.generated').read_bytes());base=json.loads(current)
 if [i for i,(x,y) in enumerate(zip(base['units'],da['units'])) if x!=y]!=[998] or [i for i,(x,y) in enumerate(zip(base['units'],db['units'])) if x!=y]!=[1111,1112]:raise ValueError('recipe unit scope changed')
 flagfiles=[x for x in a['files'] if x['path']!='build/units.json'];scriptfiles=[x for x in b['files'] if x['path']!='build/units.json'];fa={x['path'] for x in flagfiles};fb={x['path'] for x in scriptfiles}
 if len(fa)!=3 or len(fb)!=1 or fa&fb:raise ValueError('source paths overlap')
 fc=set()
 for name in ('phase2-tesform-two-flagpairs-mirror','phase2-bgs-two-flagpairs-mirror'):
  fc.update(json.loads((O/name/'mirror-manifest.json').read_bytes())['original_inputs'])
 sc=set();sm=json.loads((O/'phase2-tescontainer-script-removal/manifest.json').read_bytes())
 for i in ('1111','1112'):sc.update(sm['original_closures'][i]['original_project_files'])
 if fa&sc or fb&fc:raise ValueError('changed file appears in other proposal closure')
 new=current
 for i,unit in [(998,da['units'][998]),(1111,db['units'][1111]),(1112,db['units'][1112])]:new=recipe.replace_unit(new,i,unit)
 expected=json.loads(current)
 for i,unit in [(998,da['units'][998]),(1111,db['units'][1111]),(1112,db['units'][1112])]:expected['units'][i]=unit
 if json.loads(new)!=expected:raise ValueError('merged recipe changed other fields')
 payload=[]
 for tx,items in ((A,flagfiles),(B,scriptfiles)):
  for x in items:payload.append((x['path'],(tx/x['original']).read_bytes(),(tx/x['generated']).read_bytes()))
 payload.append(('build/units.json',current,new));T.mkdir();entries=[]
 for i,(rel,old,new) in enumerate(payload):
  (T/(str(i)+'.original')).write_bytes(old);(T/(str(i)+'.generated')).write_bytes(new);entries.append({'path':rel,'old_sha256':sha(old),'new_sha256':sha(new),'original':str(i)+'.original','generated':str(i)+'.generated'})
 m={'scope':'two independent source proposals merged; no full native class claim','base_recipe_sha256':BASE,'files':entries,'parent_manifests':{'flagpairs':AP,'script':BP},'parent_recipe_units':[998,1111,1112],'closure_interaction':{'changed_paths_overlap':False,'flag_changes_in_script_closure':False,'script_changes_in_flag_closure':False,'flag_closure_count':len(fc),'script_closure_count':len(sc)},'status':'private prepared; production literal reproof required for units998,1111,1112 before full build','limitations':['cross-TU TESForm signatures and global ODR unresolved','fold owner and final image/ICF checks remain','mirror labels are provisional']}
 (T/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({'files':len(entries),'recipe_sha256':sha(new),'unit_changes':[998,1111,1112]}))
if __name__=='__main__':main()
