"""Prepare d569-pinned script-shell mirrors without compiling."""
import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';sys.path.insert(0,str(H));import rtti_mirror_prepare as r,tesform_ten_stage as helpers,rtti_tesform_bindings_transaction as prior
T=M/'out/phase2-tesform-load-typed-v4-transaction';S=M/'out/phase2-tescontainer-script-shell';FA='fa36603e3e9a2ea495644f383db983a9269d2e7cf558282a80746439386dbfc8';D='d5694cc09e31ff441e38fb546459b11f8c4b0e0f570f252aad1853da563a8160';PIN='d9965041daea337cd7ece0afe81df50721f49cc9dd26c12c77d50f26c1f62701'
def sha(b):return hashlib.sha256(b).hexdigest()
def transition(old,new,current):
 raw=(T/'manifest.json').read_bytes();m=json.loads(raw);a=(T/'5.original').read_bytes();b=(T/'5.generated').read_bytes()
 baseline=M/'out/phase2-tesform-binding-repair-v3';ba=(baseline/'units.original').read_bytes();bb=(baseline/'units.generated').read_bytes();ev=json.loads((baseline/'manifest.json').read_bytes());prior.validate_payloads(ba,bb,ev)
 if sha(raw)!=PIN or sha(a)!=FA or sha(b)!=D or ba!=new or bb!=a or b!=current or not (T/'applied.json').exists():raise ValueError('unreviewed exact d569 transition')
 x=json.loads(a);y=json.loads(b)
 if x.keys()!=y.keys() or any(x[k]!=y[k] for k in x if k!='units') or len(x['units'])!=len(y['units']) or [i for i,(z,w) in enumerate(zip(x['units'],y['units'])) if z!=w]!=[2,998]:raise ValueError('unexpected changed units')
 for i,key in ((2,'unit2_function_remaps'),(998,'unit998_function_remaps')):
  expected=helpers.remap(x['units'][i],m[key])
  if i==2:
   for v in m['source_backed_typed_base_bindings']:
    if x['units'][2]['symbols'].get(v['before'])!=v['address']:raise ValueError('typed base source binding changed')
    expected['symbols'][v['after']]=v['address']
  else:
   fold=m['noop_fold'];f=[v for v in expected['functions'] if v['address']==fold['source_address']]
   if len(f)!=1 or f[0].get('fold_aliases'):raise ValueError('noop owner changed')
   f[0]['fold_aliases']=fold['new_symbols'];expected['symbols'].update(m['mirror_only_literal_bindings'])
  if expected!=y['units'][i]:raise ValueError('unexpected semantic recipe edit unit '+str(i))
 return y
r.transition=transition
def main():
 m=json.loads((S/'manifest.json').read_text());header=(S/'tesscript_decls.h').read_bytes()
 if sha(header)!=m['candidate_header_sha256']:raise ValueError('candidate header changed')
 for source,name in [('src/fallout_shared/tesscript.cpp','phase2-tescontainer-script-1111-mirror'),('src/fallout_shared/tesscript_ctx_variant.cpp','phase2-tescontainer-script-1112-mirror')]:
  out=M/'out'/name;v=r.prepare(source,{'src/fallout_shared/tesscript_decls.h':header},out);v['units_sha256']=D;v['reviewed_units_sha256']=FA;v['typed_transaction_manifest_sha256']=PIN;(out/'mirror-manifest.json').write_text(json.dumps(v,indent=2));print(json.dumps({'mirror':name,'original_files':len(v['original']['files']),'candidate_files':len(v['candidate']['files']),'unresolved':len(v['candidate']['unresolved'])}))
if __name__=='__main__':main()
