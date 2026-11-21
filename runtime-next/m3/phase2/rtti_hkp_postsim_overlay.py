"""Add a source-backed post-simulation override to a private hkp destructor prototype."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;PROJECT=M.parent.parent;BASE=M/'out/phase2-hkp-destructor-v2';OUT=M/'out/phase2-hkp-postsim-v3'
BASE_SHA='7e5201f77e8d2aae22f4f83f780b95959958d5eb87019d0eb97d88acd5abfcd2'


def once(data,old,new,label):
 if data.count(old)!=1:raise ValueError('unexpected '+label+' anchor')
 return data.replace(old,new,1)


def transform(data):
 if re.search(rb'\bhkpConstraintViewer::FUN_00d69730\s*\(',data):raise ValueError('candidate method already defined')
 data=once(data,b'class hkpWorldPostSimulationListener\r\n{',b'struct World;\r\nstruct Entity;\r\n\r\nclass hkpWorldPostSimulationListener\r\n{','forward declarations')
 data=once(data,b'    virtual ~hkpWorldPostSimulationListener() {}\r\n',b'    virtual ~hkpWorldPostSimulationListener() {}\r\n    virtual void FUN_00d69730(World* world);\r\n    virtual void unk08();\r\n','listener slots')
 anchor=b'class hkProcess\r\n{\r\n  public:\r\n    virtual ~hkProcess();\r\n\r\n    int unk04;\r\n    int unk08;\r\n    int unk0C;\r\n    int unk10;'
 replacement=anchor.replace(b'int unk10;',b'int m_ucOperationType;')
 data=once(data,anchor,replacement,'operation type field')
 anchor=b'    hkpConstraintViewer(void* info);\r\n    virtual ~hkpConstraintViewer() throw();\r\n'
 replacement=anchor+b'    void FUN_00d69260(int constraint, Entity* entity, int tag);\r\n    virtual void FUN_00d69730(World* world);\r\n'
 data=once(data,anchor,replacement,'viewer methods')
 return once(data,b'void ConstraintViewer::FUN_00d69730(World* world)',b'void hkpConstraintViewer::FUN_00d69730(World* world)','method definition')


def main():
 m=json.loads((BASE/'manifest.json').read_text());p=BASE/'hkpconstraintviewer.cpp';data=p.read_bytes()
 if hashlib.sha256(data).hexdigest()!=BASE_SHA or m['new_overlay_sha256']!=BASE_SHA:raise ValueError('prior overlay changed')
 up=PROJECT/'fnv_decomp/build/units.json';ub=up.read_bytes()
 if hashlib.sha256(ub).hexdigest()!=m['units_sha256']:raise ValueError('unit recipe changed')
 u=json.loads(ub)['units'][2501];old='?FUN_00d69730@ConstraintViewer@@UAEXPAUWorld@@@Z';new='?FUN_00d69730@hkpConstraintViewer@@UAEXPAUWorld@@@Z';f=[x for x in u['functions'] if x['address']=='0x00d69730']
 if len(f)!=1 or f[0]['symbol']!=old or u['symbols'].get('?FUN_00d69260@ConstraintViewer@@QAEXHPAUEntity@@H@Z')!='0x00d69260':raise ValueError('source method mapping changed')
 patched=transform(data);OUT.mkdir(parents=False,exist_ok=False)
 with (OUT/'hkpconstraintviewer.cpp').open('xb') as q:q.write(patched)
 meta={'schema_version':1,'scope':'private post-simulation slot prototype; native method semantics and ABI are not established',
  'prior_overlay_sha256':BASE_SHA,'new_overlay_sha256':hashlib.sha256(patched).hexdigest(),'units_sha256':m['units_sha256'],'original_source_sha256':m['original_source_sha256'],
  'unit_index':2501,'compiler':'sp1','flags':m['flags'],'proposed_method':{'address':'0x00d69730','before':old,'after':new,'size':f[0]['size']},
  'proposed_helper_alias':{'before':'?FUN_00d69260@ConstraintViewer@@QAEXHPAUEntity@@H@Z','after':'?FUN_00d69260@hkpConstraintViewer@@QAEXHPAUEntity@@H@Z','address':'0x00d69260','basis':'same-unit existing source symbol map; candidate must independently pass code/relocation comparison'},
  'evidence':'reference post-simulation vtable subobject offset 40 slot 1 points to mapped 0x00d69730; source method body and World signature exist',
  'risks':['prior destructor hierarchy hypothesis unverified','slot 2 remains unknown','method movement may alter code, this adjustment or other source uses','cross-TU ODR unresolved','no source or unit recipe modified'],
  'status':'uncompiled; preserve all 16 original function/reference gates and inspect all slots'}
 with (OUT/'manifest.json').open('x',encoding='utf8') as q:json.dump(meta,q,indent=2)
 print(json.dumps({'overlay_sha256':meta['new_overlay_sha256'],'status':meta['status']}))

if __name__=='__main__':main()
