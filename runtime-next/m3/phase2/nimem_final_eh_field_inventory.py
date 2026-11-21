"""Inventory exact COFF tail relocation fields associated with unchanged EH failures."""
import hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';R=M/'out';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff
from build_and_match import recipe_names
OUT=R/'phase2-nimem-final-eh-field-inventory.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if OUT.exists():raise FileExistsError('preserve evidence')
 audit=R/'phase2-nimem-final-gap-audit.json'
 if sha(audit)!='a5e490dd8ea490f92c4789bc952e97e626e33d72aa4b7568be7ba660abac01af':raise ValueError('audit changed')
 j=json.loads(audit.read_text());old=json.loads((R/'phase2-nimem-combined-825d/units.generated').read_text())['units'];new=json.loads((R/'phase2-nimem-next-source-composed/units.generated').read_text())['units'];oldnames=recipe_names(old);newnames=recipe_names(new);rows=[]
 for unit in j['eh_units']:
  i=unit['unit'];c=Coff(str(R/('phase2-nimem-combined-825d-run/unit-%04d/candidate.obj'%i)));spec=new[i];parents={x[3] for x in unit['after_failed_sections']};fields=[]
  for parent in sorted(parents):
   fn=next(x for x in spec['functions'] if x['address']==parent);symbol=c.named(fn['symbol']);sec=c.sections[symbol['section']];indices=set()
   for off,ti,kind in sec['relocs']:
    t=c.symbols[ti]
    if symbol['value']<=off<symbol['value']+fn['size']-3 and t['section']>0 and c.sections[t['section']]['name'].startswith('.text$x'):indices.add(t['section'])
   for si in sorted(indices):
    tail=c.sections[si]
    for off,ti,kind in tail['relocs']:
     target=c.symbols[ti];name=target['name'];raw=tail['data'][off:off+4];a=old[i].get('symbols',{}).get(name,oldnames.get(name));b=new[i].get('symbols',{}).get(name,newnames.get(name))
     fields.append({'parent':parent,'section_index':si,'section_sha256':hashlib.sha256(tail['data']).hexdigest(),'field_offset':off,'kind':kind,'field_value_hex':raw.hex(),'target_symbol':name,'target_section':target['section'],'target_value':target['value'],'before_recipe_binding':a,'after_recipe_binding':b,'binding_unchanged':a==b})
  rows.append({'unit':i,'object_sha256':unit['object_sha256'],'failed_sections':unit['after_failed_sections'],'exact_error_strings':unit['after_errors'],'parent_tail_fields':fields,'changed_binding_fields':sum(not x['binding_unchanged'] for x in fields)})
 OUT.write_text(json.dumps({'source_audit_sha256':sha(audit),'units':rows,'limits':['inventories all anchored tail fields associated with each failing parent; not every listed field is itself causal','same object and exact failed-section/error/inference identities are proved in parent audit','field identity does not establish a missing target or source ownership']},indent=2));print(json.dumps({'units':len(rows),'failed_sections':sum(len(x['failed_sections']) for x in rows),'fields':sum(len(x['parent_tail_fields']) for x in rows),'changed_binding_fields':sum(x['changed_binding_fields'] for x in rows),'sha256':sha(OUT)}))
if __name__=='__main__':main()
