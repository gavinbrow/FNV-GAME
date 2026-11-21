"""Exclusive-lane compiler for one pinned dehydration getter cohort mirror."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;C=M/'out/phase2-tesform-dehydration-cohort-v2';sys.path.insert(0,str(H))
import baseformcomponent_core_compile_v2 as compiler
PIN='b9802ebc7d45c8082fc41e86e57497a983cf5c060c8f0b0c17bab485c3086ed6';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c'
def transition(old,new,current):
 if hashlib.sha256((C/'manifest.json').read_bytes()).hexdigest()!=PIN or hashlib.sha256(current).hexdigest()!=BASE:raise ValueError('cohort/recipe changed')
 return json.loads(current)
compiler.prep.transition=transition
if __name__=='__main__':compiler.main()
