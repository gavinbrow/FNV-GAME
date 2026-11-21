"""Stage forward declarations needed by isolated TESContainer consumers."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';OUT=M/'out/phase2-tescontainer-forward-decls';EXPECTED='fa04e82ae34b60fbb75e97fc100bd791b7b490a213496b9478c1b07daeeef0f0'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 data=(F/'include/TESContainer.h').read_bytes()
 if sha(data)!=EXPECTED:raise ValueError('header changed')
 old=b'class InventoryStackRecord;\n';new=b'class TESForm;\nclass TESObject;\nclass InventoryStackRecord;\n'
 if data.count(old)!=1:raise ValueError('header anchor mismatch')
 result=data.replace(old,new,1);OUT.mkdir(exist_ok=False);(OUT/'TESContainer.h').write_bytes(result)
 (OUT/'manifest.json').write_text(json.dumps({'original_sha256':EXPECTED,'staged_sha256':sha(result),'change':'forward declarations for TESForm and TESObject','status':'uncompiled; unit980 production-context byte/relocation and literal-map verification plus full gate required before installation','limitations':['BSSimpleList requires its complete definition from BaseFormComponent/layout_support guard history','both source-local and include-root BaseFormComponent contexts require compile proof']},indent=2));print(sha(result))
if __name__=='__main__':main()
