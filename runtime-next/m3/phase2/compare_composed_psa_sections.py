"""Compare archived positive and private candidate PSA metadata, no compilation."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path.insert(0,str(R/'fnv_decomp/tools'));from compare import Coff
A=M/'out/phase2-native-source-positive/evidence';B=M/'out/phase2-nimem-next-source-composed-u0620';OUT=B/'independent-psa-section-review.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError(OUT)
 old=A/'0620.obj';new=B/'candidate.obj';capture=json.loads((A/'capture-manifest.json').read_text());p=next(x for x in capture['objects'] if x['unit']==620);run=json.loads((B/'compile-result.json').read_text());q=next(x for x in run['outcomes'] if x['tag']=='candidate')
 if sha(old)!=p['sha256'] or q['rc'] or not q['trace_valid'] or sha(new)!=q['object_sha256']:raise ValueError('object provenance differs')
 a,b=map(lambda p:Coff(str(p)),(old,new));wanted=[]
 for n in a.by_name:
  if (n=='??_7TESModelPSA@@6B@' or n.startswith('??_R') and any(x in n for x in ('TESModelPSA','TESModel@@','BaseFormComponent')) or n in ('??_GTESModelPSA@@UAEPAXI@Z','??1TESModelPSA@@UAE@XZ')) and any(x['section']>0 for x in a.by_name[n]):wanted.append(n)
 def detail(c,n):
  s=c.named(n);z=c.sections[s['section']];rels=[(o,t,c.symbols[i]['name'],c.symbols[i]['section'],c.symbols[i]['value'],c.symbols[i]['type'],c.symbols[i]['storage']) for o,i,t in z['relocs']];return {'section_index':s['section'],'section':z['name'],'flags':z['flags'],'symbol_offset':s['value'],'data_sha256':hashlib.sha256(z['data']).hexdigest(),'size':len(z['data']),'relocations':rels}
 rows=[]
 for n in sorted(wanted):
  x=detail(a,n);y=detail(b,n);rows.append({'symbol':n,'equal':x==y,'old':x,'candidate':y})
 if len(rows)!=16 or not all(x['equal'] for x in rows):raise ValueError('PSA metadata/owner sections differ')
 result={'scope':'actual saved 620 COFF exact section and relocation comparison; no resolver/placement claim','positive_object_sha256':sha(old),'candidate_object_sha256':sha(new),'positive_capture_sha256':sha(A/'capture-manifest.json'),'candidate_compile_sha256':sha(B/'compile-result.json'),'section_count':len(rows),'sections':rows,'limits':['exact section equality does not establish final weak fallback or placement ownership','W103 remains separately gated','whole class ABI and runtime remain separate']}
 OUT.write_text(json.dumps(result,indent=2));print(json.dumps({'sha256':sha(OUT),'sections':len(rows),'old':sha(old),'candidate':sha(new)}))
if __name__=='__main__':main()
