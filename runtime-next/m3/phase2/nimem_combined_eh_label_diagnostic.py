import sys,json,copy,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';sys.path[:0]=[str(F/'tools'),str(M.parent),str(H)]
from compare import Coff,Pe,compare
from rtti_hkp_viewer_compare import relocated
from build_and_match import eh_sections,recipe_names
import paths
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 u=json.loads((F/'build/units.json').read_bytes())['units'];pe=Pe(paths.REF_IMAGE);base=M/'out/phase2-nimem-combined-825d-run';output=M/'out/phase2-nimem-combined-eh-label-diagnostic.json'
 if output.exists():raise FileExistsError(output)
 result={}
 for i in [548,721,722,726]:
  d=base/('unit-%04d'%i);c=Coff(str(d/'candidate.obj'));o=Coff(str(d/'original.obj'));spec=copy.deepcopy(u[i]);rows=compare(c,pe,spec);binding={};facts=[];issues=[]
  for r in rows:
   if r['verdict']=='match':continue
   f=next(z for z in spec['functions'] if z['address']==r['address'])
   try:
    old,orls=relocated(o,f['symbol'],f['size'],{});new,nrls=relocated(c,f['symbol'],f['size'],{})
    if old!=new or [(x[0],x[1],x[3]) for x in orls]!=[(x[0],x[1],x[3]) for x in nrls]:raise ValueError('function or relocation shapes differ')
    for nr in nrls:
     if not nr[2].startswith('$SG') or nr[2] in spec['symbols']:continue
     paired=[x for x in orls if x[0]==nr[0] and x[1]==nr[1] and x[3]==nr[3]]
     if len(paired)!=1:raise ValueError('no paired field')
     oldname=paired[0][2];bound=spec['symbols'].get(oldname)
     if not bound:raise ValueError('old name unbound '+oldname)
     def pool(co,name):
      z=co.named(name);sec=co.sections[z['section']];raw=sec['data'];start=z['value'];end=raw.find(b'\0',start)
      if sec['name']!='.rdata' or sec['relocs'] or end<0:raise ValueError('pool unsupported')
      return raw[start:end+1]
     data=pool(o,oldname)
     if data!=pool(c,nr[2]) or data!=pe.read(int(bound,16),len(data)):raise ValueError('pool differs')
     if nr[2] in binding and binding[nr[2]]!=bound:raise ValueError('conflict')
     binding[nr[2]]=bound;facts.append({'function':f['address'],'field_offset':nr[0],'new':nr[2],'old':oldname,'target':bound,'literal_sha256':hashlib.sha256(data).hexdigest()})
   except (ValueError,KeyError,IndexError) as e:issues.append({'function':r['address'],'reason':str(e)})
  spec['symbols'].update(binding);rows=compare(c,pe,spec);sec,inf,err=eh_sections(c,pe,spec,rows,recipe_names(u));result[str(i)]={'original_sha256':sha(d/'original.obj'),'candidate_sha256':sha(d/'candidate.obj'),'bindings':binding,'facts':facts,'issues':issues,'unmatched':[{'address':r['address'],'errors':r['errors']} for r in rows if r['verdict']!='match'],'eh_sections':len(sec),'eh_failed':[x for x in sec if not x[2]],'eh_errors':err}
 output.write_text(json.dumps({'scope':'private same-unit SG field/pool pairing, no handler or recipe changes','units':result,'limitations':['historical source ownership and final production objects require independent verification','ordinary EH result uses unchanged reference oracle','no global aliases or function body rewrites']},indent=2)+'\n');print(json.dumps({k:{'bindings':len(v['bindings']),'unmatched':v['unmatched'],'eh_failed':len(v['eh_failed']),'eh_errors':v['eh_errors']} for k,v in result.items()}))
if __name__=='__main__':main()
