"""Prepare a private BGSBodyPart virtual declaration reconciliation experiment."""
import hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;PROJECT=M.parent.parent;FN=PROJECT/'fnv_decomp';OUT=M/'out/phase2-bgsbodypart-slot0'
sys.path.insert(0,str(H));from rtti_bgse_merge import include_closure
SRC=FN/'src/fallout_shared/bgsbodypart.cpp';HDR=FN/'src/fallout_shared/bgsbodypart_decls.h';EVIDENCE=FN/'src/fallout_shared/bgsbodypartdata.h';UNIT=FN/'build/units.json'
HASHES={'source':'ee15edd67d8e772904a296648ffbe7b29b5cd3c5cc5e0dc6517c5a4feb65f476','header':'a3005475923645a909fcf105d914b260e222960f326569d0636f1362910930df','support_header':'13750b1435e7d003a6c6bb786f1d13b134e55c9a29d52b1a7c0e32bf6ee4695b','units':'a7470e7f0f8c59ea4b201a1e1f72bb552d3bbd00596db2fdc4911b94b6c18a56'}
PRIOR_UNITS_SHA='ae4182c8062cf566210935d284b6663a83ab63e077b41d8e147fa66cb7aca70e'
TRANSITION=M/'out/phase2-tescontainer-install-v1'
OLD=b'    virtual void vfn_00();\r\n    void QueueResourceLoad(IO_TASK_PRIORITY, QueuedFile*);'
NEW=b'    virtual void QueueResourceLoad(IO_TASK_PRIORITY, QueuedFile*);'


def sha(b):return hashlib.sha256(b).hexdigest()

def class_body(data):
 matches=list(re.finditer(rb'\bclass\s+BGSBodyPart\s*\{',data))
 if len(matches)!=1:raise ValueError('expected one BGSBodyPart definition')
 start=matches[0].end();end=data.find(b'\n};',start)
 if end<0:raise ValueError('BGSBodyPart definition not terminated')
 return data[start:end]

def transform(header):
 if header.count(OLD)!=1 or class_body(header).count(OLD)!=1:raise ValueError('expected one adjacent BGSBodyPart declaration pair')
 return header.replace(OLD,NEW,1)


def validate_units_transition(prior,generated,current):
 if sha(prior)!=PRIOR_UNITS_SHA or sha(generated)!=HASHES['units'] or generated!=current:
  raise ValueError('unit transaction hashes or generated payload mismatch')
 before=json.loads(prior);after=json.loads(generated)
 if before.keys()!=after.keys() or any(before[k]!=after[k] for k in before if k!='units'):
  raise ValueError('unit transaction changed non-unit metadata')
 a,b=before['units'],after['units']
 if len(a)!=len(b) or [i for i,(x,y) in enumerate(zip(a,b)) if x!=y]!=[980]:
  raise ValueError('unit transaction changed outside unit 980')
 import copy
 expected=copy.deepcopy(a[980]);found=[x for x in expected['functions'] if x['address']=='0x00481d10']
 if len(found)!=1 or found[0]['symbol']!='?FUN_00481d10@FUN_00481d10_shell@@QAE_NPAVBaseFormComponent@@@Z':raise ValueError('unexpected prior TES function')
 found[0]['symbol']='?CompareWithBase@TESContainer@@UAE_NPAVBaseFormComponent@@@Z'
 removed={'$SG4920':'0x0101c140','$SG4912':'0x0101c178','$SG4922':'0x0101c140','$SG4914':'0x01012058'}
 added={'$SG4925':'0x0101c140','$SG4927':'0x0101c140','$SG4919':'0x01012058','$SG4917':'0x0101c178'}
 for k,v in removed.items():
  if expected['symbols'].pop(k,None)!=v:raise ValueError('unexpected prior literal mapping')
 for k,v in added.items():
  if k in expected['symbols']:raise ValueError('new literal mapping collision')
  expected['symbols'][k]=v
 if expected!=b[980]:raise ValueError('unit 980 transition differs from reviewed payload')
 return {'changed_unit_indexes':[980],'unit_620_unchanged':a[620]==b[620],'unit_2_unchanged':a[2]==b[2],'unit_2501_unchanged':a[2501]==b[2501]}


def main():
 data={'source':SRC.read_bytes(),'header':HDR.read_bytes(),'support_header':EVIDENCE.read_bytes(),'units':UNIT.read_bytes()}
 for k,b in data.items():
  if sha(b)!=HASHES[k]:raise ValueError('input digest mismatch: '+k)
 transition=validate_units_transition((TRANSITION/'2.original').read_bytes(),(TRANSITION/'2.generated').read_bytes(),data['units'])
 support=data['support_header']
 if not re.search(rb'virtual\s+void\s+QueueResourceLoad\s*\(\s*IO_TASK_PRIORITY\s+priority\s*,\s*QueuedFile\s*\*\s*file\s*\)',class_body(support)):raise ValueError('independent BGSBodyPart virtual signature absent')
 unit=json.loads(data['units'])['units'][620];old='?QueueResourceLoad@BGSBodyPart@@QAEXW4IO_TASK_PRIORITY@@PAVQueuedFile@@@Z';new='?QueueResourceLoad@BGSBodyPart@@UAEXW4IO_TASK_PRIORITY@@PAVQueuedFile@@@Z'
 f=[x for x in unit['functions'] if x['address']=='0x005e45e0']
 if unit['source']!='src/fallout_shared/bgsbodypart.cpp' or len(unit['functions'])!=15 or len(f)!=1 or f[0]['symbol']!=old:raise ValueError('unit recipe changed')
 if unit['symbols'].get('??_7BGSBodyPart@@6B@')!='0x01045404':raise ValueError('unit vtable map changed')
 h=transform(data['header']);closure,external=include_closure(SRC);OUT.mkdir(parents=False,exist_ok=False)
 for p,b in [(OUT/'bgsbodypart.cpp',data['source']),(OUT/'bgsbodypart_decls.h',h)]:
  with p.open('xb') as q:q.write(b)
 meta={'schema_version':1,'scope':'private reconciliation of one native virtual declaration; no class identity or complete vtable extent claim',
  'input_sha256':HASHES,'reviewed_prior_units_sha256':PRIOR_UNITS_SHA,'units_transition':transition,'unit_index':620,'source':unit['source'],'compiler':unit['compiler'],'flags':unit['flags'],
  'proposed_function_symbol_changes':[{'address':'0x005e45e0','before':old,'after':new,'size':f[0]['size']}],
  'source_overlay_sha256':sha(data['source']),'header_overlay_sha256':sha(h),'original_include_closure':closure,'system_includes':external,
  'observed_reference_vtable_va':'0x01045404','observed_prefix_slots':1,'independent_source_signature':'src/fallout_shared/bgsbodypartdata.h',
  'risks':['virtual dispatch may alter callers or generated code','additional class definitions and full ODR compatibility remain unproved','reference code-pointer prefix does not establish complete vtable extent','object placement/overlap and relocations unverified'],
  'status':'uncompiled; require all 15 function and relocation checks plus complete emitted metadata and observed prefix checks'}
 with (OUT/'manifest.json').open('x',encoding='utf8') as q:json.dump(meta,q,indent=2)
 print(json.dumps({'source_sha256':meta['source_overlay_sha256'],'header_sha256':meta['header_overlay_sha256'],'closure_files':len(closure)}))

if __name__=='__main__':main()
