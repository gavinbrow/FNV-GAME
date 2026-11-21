"""Read-only source-context NiRef 119 cohort pair classification."""
import hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;sys.path.insert(0,str(R/'fnv_decomp/tools'));from compare import Coff
D=M/'out/phase2-niref-inline-cohort';OUT=D/'independent-pair-provider-review.json';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if OUT.exists():raise FileExistsError(OUT)
 progress=D/'progress.json';raw=progress.read_bytes();p=j(progress);manifest=j(D/'manifest.json');idx={x['unit']:x for x in p['units']}
 if p['status']!='complete-review-required' or len(idx)!=119 or len(p['units'])!=119 or any('comparison_sha256' not in x for x in p['units']):raise ValueError('cohort incomplete')
 if len(manifest['units'])!=119 or set(idx)!={x['unit'] for x in manifest['units']}:raise ValueError('scope differs')
 literal={147,392,509,548,592,703,773};code={111,1200,1433,1598,1630};found=set();out=[]
 for i,x in idx.items():
  d=D/('unit-%04d'%i);cp=d/'comparison.json'
  if h(cp)!=x['comparison_sha256']:raise ValueError('comparison differs')
  r=j(cp);diffs=r['mapped_pair_differences']
  if not diffs:continue
  found.add(i);o=Coff(str(d/'original.obj'));c=Coff(str(d/'candidate.obj'));facts=[]
  for z in diffs:
   if i in literal:
    if not z.get('bytes_equal'):raise ValueError('literal unit code changed')
    a={(q[0],q[1]):(q[2],q[3]) for q in z['original_relocations']};b={(q[0],q[1]):(q[2],q[3]) for q in z['candidate_relocations']};fs=[]
    for k in sorted(a.keys()|b.keys()):
     if a.get(k)==b.get(k):continue
     left,right=a.get(k),b.get(k)
     if not left or not right or not left[0].startswith('$SG') or not right[0].startswith('$SG') or left[1]!=right[1] or k[1]!=6:raise ValueError('nonliteral change')
     ls=o.named(left[0]);rs=c.named(right[0]);lb=o.sections[ls['section']]['data'];rb=c.sections[rs['section']]['data']
     if ls['value']!=rs['value'] or lb!=rb:raise ValueError('pool mismatch')
     fs.append({'offset':k[0],'before':left[0],'after':right[0],'pool_offset':ls['value'],'whole_pool_sha256':hashlib.sha256(lb).hexdigest()})
    facts.append({'address':z['address'],'kind':'same-unit SG renumbering','fields':fs})
   elif i in code:
    facts.append({'address':z['address'],'kind':'actual instruction/extent change','candidate_failure':next(y for y in r['results']['candidate']['failures'] if y['address']==z['address'])})
   elif i==612:facts.append({'address':z['address'],'kind':'source owner symbol transition','bytes_equal':z.get('bytes_equal'),'original_relocations':z.get('original_relocations'),'candidate_relocations':z.get('candidate_relocations')})
   else:raise ValueError('unexpected diff unit '+str(i))
  out.append({'unit':i,'facts':facts,'matches':x['matches'],'comparison_sha256':h(cp)})
 if found!=literal|code|{612}:raise ValueError('unexpected pair-diff scope')
 providers=[]
 for i in (612,1503):
  path=D/('unit-%04d'%i)/'candidate.obj';c=Coff(str(path));start=struct.unpack_from('<I',c.data,8)[0];symbols=[]
  for n in ('??1NiRefObject@@UAE@XZ','??_GNiRefObject@@UAEPAXI@Z','??_ENiRefObject@@UAEPAXI@Z'):
   for z,s in c.symbols.items():
    if s['name']!=n:continue
    item={'name':n,'storage':s['storage'],'section':s['section']}
    if s['section']>0:
     sec=c.sections[s['section']];item.update(size=len(sec['data'])-s['value'],section_flags=sec['flags']);aux=[(k,t) for k,t in c.symbols.items() if t['section']==s['section'] and t['storage']==3 and t['name']==sec['name'] and c.data[start+k*18+17]]
     if len(aux)!=1:raise ValueError('COMDAT section auxiliary ambiguous')
     item['selection']=c.data[start+aux[0][0]*18+18+14]
    elif s['storage']==105:
     target,mode=struct.unpack_from('<II',c.data,start+(z+1)*18);item.update(weak_mode=mode,fallback=c.symbols[target]['name'])
    symbols.append(item)
  providers.append({'unit':i,'object_sha256':h(path),'symbols':symbols})
 totals={t:sum(x.get('matches',{}).get(t,0) or 0 for x in p['units']) for t in ('production','original','candidate')}
 if progress.read_bytes()!=raw:raise ValueError('progress drift')
 result={'scope':'all 119 units; non-additive pair categories','progress_sha256':hashlib.sha256(raw).hexdigest(),'unit_count':119,'function_count':2080,'strict_matches':totals,'literal_units':sorted(literal),'instruction_change_units':sorted(code),'source_owner_transition_unit':612,'units':out,'providers':providers,'ordinary_eh_union':p['ordinary_eh_union'],'limitations':['same-unit pool pairing does not itself authorize recipe aliases','real inline instruction/extent changes remain strict reference regressions','76 listed tails passing does not imply every ordinary EH section passed','same-name COMDAT selection and weak fallback are observed, not final provider/link proof','full class ODR and image/runtime remain separate']}
 OUT.write_text(json.dumps(result,indent=2));print(json.dumps({'sha256':h(OUT),'totals':totals,'unit_count':len(out)}))
if __name__=='__main__':main()
