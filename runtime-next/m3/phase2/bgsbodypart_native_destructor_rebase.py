"""Rebase a frozen private fixture only across the verified combined transaction."""
import hashlib,json,shutil
from pathlib import Path
M=Path(__file__).resolve().parent.parent;F=M.parent.parent/'fnv_decomp';P=M/'out/phase2-bgsbodypart-native-destructor-proposal';T=M/'out/phase2-combined-source-transaction';O=M/'out/phase2-bgsbodypart-native-destructor-rebase6757'
OLD='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';NEW='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';TM='b0d4204b54df8d37fc96e15bd5ef174a10ef0d7c5b022e81d1b076a6f4808130'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if sha((P/'lane.py').read_bytes())!='d76ae0dad216b4819ecde8a3a1e48e4a1cfa68713a6f9bf9f81ba068f7474d16' or sha((P/'lane-freeze.json').read_bytes())!='4a87e86dba77068bd75eb3d6f357a1964274f8994d07486545b71ac37e57a8f9':raise ValueError('original fixture changed')
 if sha((T/'manifest.json').read_bytes())!=TM:raise ValueError('transaction manifest changed')
 tx=json.loads((T/'manifest.json').read_bytes());old=(T/'4.original').read_bytes();new=(T/'4.generated').read_bytes();current=(F/'build/units.json').read_bytes()
 if sha(old)!=OLD or sha(new)!=NEW or current!=new or tx['base_recipe_sha256']!=OLD:raise ValueError('recipe transition mismatch')
 a=json.loads(old);b=json.loads(new)
 if a.keys()!=b.keys() or any(a[k]!=b[k] for k in a if k!='units') or len(a['units'])!=len(b['units']):raise ValueError('recipe nonunit structure changed')
 changed=[i for i,(x,y) in enumerate(zip(a['units'],b['units'])) if x!=y]
 if changed!=[998,1111,1112] or any(a['units'][i]!=b['units'][i] for i in (620,621)):raise ValueError('unexpected affected recipes')
 for x in tx['files']:
  if sha((T/x['original']).read_bytes())!=x['old_sha256'] or sha((T/x['generated']).read_bytes())!=x['new_sha256'] or sha((F/x['path']).read_bytes())!=x['new_sha256']:raise ValueError('transaction file mismatch '+x['path'])
 frozen=json.loads((P/'lane-freeze.json').read_bytes());manifest=json.loads((P/'manifest.json').read_bytes());meta=json.loads((P/'lane-manifest.json').read_bytes())
 if frozen['files']['units']!=OLD or meta['input_sha256']['units']!=OLD:raise ValueError('prior recipe not pinned')
 for row in frozen['include_closure'].values():
  for x in row['quoted']:
   if sha((F/x['path']).read_bytes())!=x['sha256']:raise ValueError('captured source closure changed '+x['path'])
 for n,v in manifest['outputs'].items():
  if sha((P/n).read_bytes())!=v:raise ValueError('prior candidate changed '+n)
 O.mkdir(exist_ok=False)
 for unit in ('620','621'):
  (O/unit).mkdir()
  for x in (P/unit).iterdir():shutil.copyfile(x,O/unit/x.name)
 shutil.copyfile(P/'previous-compile-provenance.json',O/'previous-compile-provenance.json')
 meta['input_sha256']['units']=NEW;(O/'lane-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
 manifest['semantic_rebase']={'transaction_manifest_sha256':TM,'old_units_sha256':OLD,'new_units_sha256':NEW,'changed_unit_indexes':changed,'units_620_621_unchanged':True,'prior_freeze_sha256':sha((P/'lane-freeze.json').read_bytes()),'captured_source_closure_unchanged':True}
 (O/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');digest=sha((O/'manifest.json').read_bytes())
 driver=(P/'lane.py').read_text();changes=[('out/phase2-bgsbodypart-native-destructor-proposal','out/phase2-bgsbodypart-native-destructor-rebase6757'),(sha((P/'manifest.json').read_bytes()),digest),
  ('byte-identical source mirrors and unit621 header; unit620 header is sole override','semantic rebase of two-unit native-destructor fixture with pinned split headers')]
 for x,y in changes:
  if driver.count(x)!=1:raise ValueError('driver anchor mismatch')
  driver=driver.replace(x,y,1)
 (O/'lane.py').write_text(driver,encoding='utf8');print(json.dumps({'driver_sha256':sha((O/'lane.py').read_bytes()),'manifest_sha256':digest,'transaction_sha256':TM,'changed_units':changed}))
if __name__=='__main__':main()
