"""Produce a private destructor-aware hkp class hypothesis, never install it."""
import hashlib,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;BASE=M/'out/phase2-hkp-hierarchy-v1';OUT=M/'out/phase2-hkp-destructor-v2'
BASE_SHA='c931da2cd84e8abd629938e8a42ce5bd8f8448225a4fa04511edcc1ab51cba75'


def once(data,old,new,label):
 if data.count(old)!=1:raise ValueError('unexpected '+label+' anchor')
 return data.replace(old,new,1)


def transform(data):
 # Related Havok source shows hkBaseObject non-polymorphic and hkReferencedObject
 # as the first virtual destructor; exact game semantics still require verification.
 replacements=[
 (b'class hkBaseObject\r\n{\r\n  public:\r\n    virtual void unk00();\r\n};',b'class hkBaseObject\r\n{\r\n};','hkBaseObject'),
 (b'class hkReferencedObject : public hkBaseObject\r\n{\r\n  public:\r\n    virtual void unk00();',b'class hkReferencedObject : public hkBaseObject\r\n{\r\n  public:\r\n    virtual ~hkReferencedObject();','hkReferencedObject'),
 (b'class hkProcess\r\n{\r\n  public:\r\n    virtual void unk00();',b'class hkProcess\r\n{\r\n  public:\r\n    virtual ~hkProcess();','hkProcess'),
 (b'class hkpPhysicsContextWorldListener\r\n{\r\n  public:\r\n    virtual void unk00();',b'class hkpPhysicsContextWorldListener\r\n{\r\n  public:\r\n    virtual ~hkpPhysicsContextWorldListener();','world listener'),
 (b'class hkpWorldPostSimulationListener\r\n{\r\n  public:\r\n    virtual void unk00();',b'class hkpWorldPostSimulationListener\r\n{\r\n  public:\r\n    virtual ~hkpWorldPostSimulationListener() {}','post listener'),
 (b'    hkpWorldViewerBase(void* info);\r\n',b'    hkpWorldViewerBase(void* info);\r\n    virtual ~hkpWorldViewerBase();\r\n','world base'),
 (b'    hkpConstraintViewer(void* info);\r\n',b'    hkpConstraintViewer(void* info);\r\n    virtual ~hkpConstraintViewer() throw();\r\n    static void operator delete(void* p, unsigned int nbytes);\r\n','viewer declaration')]
 for old,new,label in replacements:data=once(data,old,new,label)
 anchor=b'}  // namespace fnv_00d69af0\r\n'
 addition=b'''\r\n// Experimental reconstruction from the existing mapped destructor surrogates.\r\n__forceinline void hkpConstraintViewer::operator delete(void* p, unsigned int nbytes)\r\n{\r\n    fnv_00d69af0::FUN_00d69af0::operator delete(p, nbytes);\r\n}\r\n\r\nhkpConstraintViewer::~hkpConstraintViewer() throw()\r\n{\r\n    fnv_00d69920::OwnerNode* owner = reinterpret_cast<fnv_00d69920::OwnerNode*>(m_pOwningWorld);\r\n    if (owner != 0)\r\n    {\r\n        for (int i = 0; i < owner->m_iArrayLength; ++i)\r\n        {\r\n            owner->m_ppItems[i]->ClearValue(static_cast<hkpWorldPostSimulationListener*>(this));\r\n        }\r\n    }\r\n    fnv_00d69920::AudioHolder* pHolder = fnv_00d69920::FUN_00c85750();\r\n    fnv_00d69920::AudioAllocator* pAllocator = pHolder->m_pAllocator;\r\n    m_entries.m_iElementCount = 0;\r\n    unsigned int uiDataFlags = m_entries.m_iCapacityState;\r\n    if ((uiDataFlags & 0x80000000u) == 0)\r\n    {\r\n        pAllocator->FreeData(m_entries.m_data, (uiDataFlags & 0x3fffffffu) * 4);\r\n    }\r\n    m_entries.m_data = 0;\r\n    m_entries.m_iCapacityState = 0x80000000u;\r\n}\r\n'''
 return once(data,anchor,anchor+addition,'destructor insertion')


def main():
 source=BASE/'hkpconstraintviewer.cpp';m=json.loads((BASE/'manifest.json').read_text());raw=source.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=BASE_SHA or m['overlay_sha256']!=BASE_SHA:raise ValueError('input overlay hash changed')
 patched=transform(raw);OUT.mkdir(parents=False,exist_ok=False)
 with (OUT/'hkpconstraintviewer.cpp').open('xb') as f:f.write(patched)
 meta={'schema_version':1,'scope':'private hypothesis for compiler-generated deleting destructor and secondary thunks; not native ABI proof',
  'source_overlay_sha256':BASE_SHA,'new_overlay_sha256':hashlib.sha256(patched).hexdigest(),'original_source_sha256':m['source_sha256'],'units_sha256':m['units_sha256'],
  'unit_index':2501,'flags':m['flags'],'hypotheses':['hkBaseObject is non-polymorphic','hkReferencedObject first virtual is destructor','secondary bases have virtual destructors','source destructor surrogate is semantically same class','sized delete matches reference'],
  'preserve_original_functions':16,'candidate_destructor_reference_va':'0x00d69920','candidate_scalar_deleting_dtor_reference_va':'0x00d69af0',
  'candidate_adjustor_thunks':[{'this_offset':8,'va':'0x00d69ad0'},{'this_offset':32,'va':'0x00d69ac0'},{'this_offset':40,'va':'0x00d69ae0'}],
  'status':'uncompiled; no integration, no W/selection changes; exact code and relocation checks plus all slot checks required'}
 with (OUT/'manifest.json').open('x',encoding='utf8') as f:json.dump(meta,f,indent=2)
 print(json.dumps({'overlay_sha256':meta['new_overlay_sha256'],'status':meta['status']}))

if __name__=='__main__':main()
