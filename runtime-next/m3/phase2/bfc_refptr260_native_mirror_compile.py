"""Exclusive-lane compiler wrapper for private unit260 split hypothesis."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;S=M/'out/phase2-bfc-refptr260-native-v1';sys.path.insert(0,str(H));import baseformcomponent_core_compile_v2 as compiler
BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def transition(old,new,current):
 meta=json.loads((S/'manifest.json').read_bytes())
 if meta['base_recipe_sha256']!=BASE or hashlib.sha256(current).hexdigest()!=BASE:raise ValueError('recipe mismatch')
 return json.loads(current)
compiler.prep.transition=transition
if __name__=='__main__':compiler.main()
