"""Materialize private unit260 split mirror on exact current recipe."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';S=M/'out/phase2-bfc-refptr260-native-v1';O=M/'out/phase2-bfc-refptr260-native-mirror';sys.path.insert(0,str(H));import rtti_mirror_prepare as r
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def sha(b):return hashlib.sha256(b).hexdigest()
def transition(old,new,current):
 if sha(current)!=BASE:raise ValueError('recipe changed')
 return json.loads(current)
r.transition=transition
def main():
 m=json.loads((S/'manifest.json').read_bytes());candidate=(S/'actor_o2_variant.cpp').read_bytes();source='src/fallout/ai/actor_o2_variant.cpp'
 if m['base_recipe_sha256']!=BASE or sha(candidate)!=m['candidate_sha256'] or sha((F/source).read_bytes())!=m['source_sha256']:raise ValueError('candidate inputs changed')
 mirror=r.prepare(source,{source:candidate},O);mirror['units_sha256']=BASE;mirror['reviewed_units_sha256']=BASE;mirror['candidate_manifest_sha256']=sha((S/'manifest.json').read_bytes());(O/'mirror-manifest.json').write_text(json.dumps(mirror,indent=2));print(json.dumps({'unit':260,'original_files':len(mirror['original']['files']),'candidate_files':len(mirror['candidate']['files']),'candidate_sha256':m['candidate_sha256']}))
if __name__=='__main__':main()
