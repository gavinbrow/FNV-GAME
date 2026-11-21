"""Run existing private mirror compiler only after exact reviewed recipe transition."""
import hashlib,json,runpy,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(H));import rtti_mirror_prepare as r,rtti_tesform_bindings_transaction as tx
B=M/'out/phase2-tesform-binding-repair-v3';EXPECTED='7242e851405ec30aed816f65d1c134405f229b4458ee6ec3f4a5bca4cb327c59'
def transition(old,new,current):
 a=(B/'units.original').read_bytes();b=(B/'units.generated').read_bytes();e=(B/'manifest.json').read_bytes()
 if hashlib.sha256(e).hexdigest()!=EXPECTED:raise ValueError('binding proof changed')
 tx.validate_payloads(a,b,json.loads(e))
 if a!=new or b!=current:raise ValueError('current recipe differs from reviewed seven-binding transition')
 return json.loads(b)
r.transition=transition
if __name__=='__main__':runpy.run_path(str(H/'rtti_mirror_compile.py'),run_name='__main__')
