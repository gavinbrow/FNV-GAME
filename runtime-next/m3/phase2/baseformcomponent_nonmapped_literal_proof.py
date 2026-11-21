"""Resolve four BFC nonmapped-section literal-renumbering cases by full-pool evidence."""
import collections,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';O=M/'out';sys.path[:0]=[str(F/'tools'),str(H)];from compare import Coff
import baseformcomponent_nonmapped_sections_audit as base
IDX=O/'phase2-bfc-core-proof-index.json';PRIOR=O/'phase2-bfc-nonmapped-sections-audit.json';OUT=O/'phase2-bfc-nonmapped-literal-proof.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('no overwrite')
 index=json.loads(IDX.read_bytes());prior=json.loads(PRIOR.read_bytes());units=json.loads((O/'phase2-flags-script-production-before/units.json').read_bytes())['units'];rows=[]
 for i in (367,590,597,1040):
  item=next(x for x in index['units'] if x['unit']==i);d=(M/item['report']).parent;report=M/item['report'];pr=json.loads(report.read_bytes())
  if sha(report.read_bytes())!=item['report_sha256']:raise ValueError('report changed')
  for k in ('original','candidate'):
   if sha((d/(k+'.obj')).read_bytes())!=item['objects'][k]:raise ValueError('object changed')
  a=Coff(str(d/'original.obj'));b=Coff(str(d/'candidate.obj'));skip_a,miss_a=base.mapped(a,units[i]);skip_b,miss_b=base.mapped(b,units[i])
  if miss_a or miss_b:raise ValueError('recipe symbols absent')
  norm={};evidence=[]
  for x in pr['mirror_to_candidate_literals']:
   if x['after'] in norm and norm[x['after']]!=x['before']:raise ValueError('existing mapping ambiguous')
   norm[x['after']]=x['before']
  unmatched=next(x for x in prior['mismatch_units'] if x['unit']==i);poolrows=[x for x in unmatched['original_only'] if x['section']=='.rdata']
  if len(poolrows)!=1:raise ValueError('expected one unmatched literal pool')
  target=poolrows[0];poola=[(k,s) for k,s in enumerate(a.sections) if s and k not in skip_a and s['name']=='.rdata' and len(s['data'])==target['size'] and sha(s['data'])==target['data_sha256']]
  poolb=[(k,s) for k,s in enumerate(b.sections) if s and k not in skip_b and s['name']=='.rdata' and len(s['data'])==target['size'] and sha(s['data'])==target['data_sha256']]
  if len(poola)!=1 or len(poolb)!=1:raise ValueError('pool section identity ambiguous')
  ia,sa=poola[0];ib,sb=poolb[0]
  if sa['flags']!=sb['flags'] or sa['data']!=sb['data'] or sa['relocs'] or sb['relocs']:raise ValueError('whole pool changed')
  def labels(c,k):
   v=collections.defaultdict(list)
   for s in c.symbols.values():
    if s['section']==k and s['name'].startswith('$SG'):v[s['value']].append(s)
   return v
  x,y=labels(a,ia),labels(b,ib)
  if set(x)!=set(y) or any(len(v)!=1 for v in x.values()) or any(len(v)!=1 for v in y.values()):raise ValueError('pool label offset ambiguity')
  for off in sorted(x):
   old,new=x[off][0],y[off][0]
   if (old['value'],old['type'],old['storage'])!=(new['value'],new['type'],new['storage']):raise ValueError('symbol metadata mismatch')
   if new['name'] in norm and norm[new['name']]!=old['name']:raise ValueError('normalization conflict')
   norm[new['name']]=old['name'];evidence.append({'offset':off,'original':old['name'],'candidate':new['name']})
  aa=base.signatures(a,skip_a,{});bb=base.signatures(b,skip_b,norm);ca=collections.Counter(x[1] for x in aa if x[1][1]!='.debug$S');cb=collections.Counter(x[1] for x in bb if x[1][1]!='.debug$S');left=ca-cb;right=cb-ca
  if left or right:raise ValueError('nondebug structural mismatch remains in unit '+str(i))
  # Require all relocation target records, names and addends in every full matched section; uniqueness below is not placement proof.
  duplicates=sum(n for n in ca.values() if n>1)
  rows.append({'unit':i,'source':units[i]['source'],'original_obj_sha256':sha((d/'original.obj').read_bytes()),'candidate_obj_sha256':sha((d/'candidate.obj').read_bytes()),'pool_size':len(sa['data']),'pool_sha256':sha(sa['data']),'pool_labels':evidence,'nondebug_sections_checked':sum(ca.values()),'duplicate_equal_sections':duplicates,'all_section_data_definitions_and_relocations_equal':True})
 output={'scope':'same-unit non-recipe-containing section equivalence only; literal names re-associated through equal whole nonrelocated pool and exact unique offsets','prior_audit_sha256':sha(PRIOR.read_bytes()),'cohort_index_sha256':sha(IDX.read_bytes()),'units':rows,'limitations':['proof does not establish canonical reference address or ownership for any literal','equal section multisets do not prove final placement, COMDAT selection or ICF','mapped-function sections and BSS virtual extents remain separate','global source identity and cross-unit ODR remain open']}
 OUT.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'units':len(rows),'labels':sum(len(x['pool_labels']) for x in rows),'sections':sum(x['nondebug_sections_checked'] for x in rows)}))
if __name__=='__main__':main()
