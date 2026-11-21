"""Snapshot completed NiMem-kind baseline failures with source-backed external candidates."""
import argparse,collections,hashlib,json,struct,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';RUN=M/'out/phase2-nimem-kind-cohort-run';ARCH=M/'out/phase2-nimem-kind-production-archive';sys.path[:0]=[str(F/'tools'),str(RN)]
from compare import Coff,Pe,compare
import paths
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve()
 if not out.is_relative_to((M/'out').resolve()) or out.exists():raise ValueError('fresh private output required')
 progress=RUN/'progress.json';raw=progress.read_bytes();p=json.loads(raw);recipe=RUN/'units.snapshot.json';doc=json.loads(recipe.read_text());units=doc['units'];archive=json.loads((ARCH/'manifest.json').read_text());seen={x['unit']:x for x in archive['objects']};source=collections.defaultdict(lambda:collections.defaultdict(list))
 for i,u in enumerate(units):
  for k,v in u.get('symbols',{}).items():
   if not k.startswith('$'):source[k][int(v,0)].append(i)
  for f in u['functions']:
   for k in [f['symbol']]+f.get('fold_aliases',[]):
    if not k.startswith('$'):source[k][int(f['address'],0)].append(i)
 pe=Pe(paths.REF_IMAGE);fields=[];units_out=[];counts=collections.Counter()
 for x in p['units']:
  if x['status']!='review-required':continue
  i=x['unit'];report=RUN/('unit-%04d/comparison.json'%i)
  if not report.exists() or sha(report)!=x['comparison_sha256']:raise ValueError('comparison changed')
  cpath=ARCH/('%04d.obj'%i)
  if sha(cpath)!=seen[i]['sha256']:raise ValueError('archive object changed')
  c=Coff(str(cpath));rows=compare(c,pe,units[i]);units_out.append({'unit':i,'functions':len(rows),'strict_matches':sum(r['verdict']=='match' for r in rows),'pair_differences':x['pair_differences'],'classkey_warnings':x['classkey_warning_count'],'eh_errors':x['eh_errors'],'failed_eh_sections':x['failed_eh_sections'],'report_sha256':sha(report)})
  specs={f['address']:f for f in units[i]['functions']}
  for f in rows:
   for z in f['relocations']:
    if z.get('match'):continue
    name=z['symbol'];status='unproved';target=None;sourceunits=[];sym=c.by_name.get(name,[])
    if name.startswith('$'):status='local-label-deferred'
    elif len([x for x in sym if x['section']==0 and x['storage']==2])!=1 or any(x['section']>0 for x in sym):status='not-unique-undefined-external'
    elif len(source.get(name,{}))!=1:status='source-binding-not-unique'
    else:
     target,sourceunits=next(iter(source[name].items()));spec=specs[f['address']];s=c.named(spec['symbol']);sec=c.sections[s['section']];add=struct.unpack_from('<i',sec['data'],s['value']+z['offset'])[0];field=int(f['address'],16)+z['offset'];data=pe.read(field,4);obs=(field+4+struct.unpack('<i',data)[0])&0xffffffff if z['kind']==20 else struct.unpack('<I',data)[0] if z['kind']==6 else None
     status='source-unique-reference-agree' if obs==(target+add)&0xffffffff else 'source-reference-disagree'
    counts[status]+=1;fields.append({'unit':i,'function':f['address'],'field_offset':z['offset'],'symbol':name,'status':status,'source_target':'0x%08x'%target if target is not None else None,'source_units':sorted(set(sourceunits))})
 result={'scope':'point-in-time completed units; diagnostic only, no new bindings installed','progress_sha256':hashlib.sha256(raw).hexdigest(),'recipe_sha256':sha(recipe),'archive_manifest_sha256':sha(ARCH/'manifest.json'),'completed_units':len(p['units']),'review_required_units':len(units_out),'field_counts':dict(counts),'units':units_out,'fields':fields,'limits':['runner is still active; counts are partial','unique global source names apply only to actually undefined strong externals','local SG/LN labels remain same-unit source-pair proof only','EH inferred targets and failure sections require independent source/ownership proof']}
 out.write_text(json.dumps(result,indent=2));print(json.dumps({'completed_units':len(p['units']),'review_required_units':len(units_out),'field_counts':counts}))
if __name__=='__main__':main()
