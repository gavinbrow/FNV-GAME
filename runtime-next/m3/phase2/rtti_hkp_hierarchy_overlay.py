"""Create a single private source overlay testing a reference-guided hierarchy hypothesis."""
import hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;M3=HERE.parent;PROJECT=M3.parent.parent
sys.path.insert(0,str(HERE));import rtti_hkp_viewer_overlay as base

MAP=(('D698B0BaseA','hkReferencedObject',2),('D698B0BaseB','hkProcess',2),
     ('D698B0BaseC','hkpPhysicsContextWorldListener',2),('D698B0Base','hkpWorldViewerBase',4),
     ('D698B0Listener','hkpWorldPostSimulationListener',3))


def transform(data):
    out=base.rename_source(data)
    for old,new,count in MAP:
        if re.search(rb'\b'+new.encode()+rb'\b',out):raise ValueError('new base name already present in unit: '+new)
        out,n=re.subn(rb'\b'+old.encode()+rb'\b',new.encode(),out)
        if n!=count:raise ValueError('unexpected token count for '+old)
    old=b'class hkReferencedObject\r\n{\r\n  public:\r\n    virtual void unk00();'
    new=(b'class hkBaseObject\r\n{\r\n  public:\r\n    virtual void unk00();\r\n};\r\n\r\n'
         b'class hkReferencedObject : public hkBaseObject\r\n{\r\n  public:\r\n    virtual void unk00();')
    if out.count(old)!=1:raise ValueError('base insertion anchor changed')
    out=out.replace(old,new,1)
    old=b'class hkpWorldViewerBase : public hkReferencedObject, public hkProcess, public hkpPhysicsContextWorldListener'
    new=b'class hkpWorldViewerBase : public hkReferencedObject, public hkProcess, protected hkpPhysicsContextWorldListener'
    if out.count(old)!=1:raise ValueError('world viewer inheritance anchor changed')
    out=out.replace(old,new,1)
    old=b'class hkpConstraintViewer : public hkpWorldViewerBase, public hkpWorldPostSimulationListener'
    new=b'class hkpConstraintViewer : public hkpWorldViewerBase, protected hkpWorldPostSimulationListener'
    if out.count(old)!=1:raise ValueError('constraint viewer inheritance anchor changed')
    return out.replace(old,new,1)


def main():
    source=PROJECT/'fnv_decomp'/base.SOURCE_REL;units=PROJECT/'fnv_decomp/build/units.json';data=source.read_bytes()
    if base.sha(data)!=base.SOURCE_SHA or base.sha(units.read_bytes())!=base.UNITS_SHA:raise ValueError('source or unit digest changed')
    if base.scan_name(base.NEW):raise ValueError('candidate class name collision')
    if base.scan_name(base.OLD)!=[source.resolve()]:raise ValueError('synthetic class used by another source')
    if re.findall(rb'^\s*#\s*include\s*([^\r\n]+)',data,re.M)!=[b'<windows.h>']:raise ValueError('include closure changed')
    overlay=transform(data);out=M3/'out/phase2-hkp-hierarchy-v1';out.mkdir(parents=False,exist_ok=False)
    with (out/'hkpconstraintviewer.cpp').open('xb') as f:f.write(overlay)
    collisions={new:len(base.scan_name(new)) for _,new,_ in MAP}
    collisions['hkBaseObject']=len(base.scan_name('hkBaseObject'))
    record={'schema_version':1,'source':base.SOURCE_REL,'source_sha256':base.SOURCE_SHA,'units_sha256':base.UNITS_SHA,'overlay_sha256':hashlib.sha256(overlay).hexdigest(),
      'unit_index':2501,'compiler':'sp1','flags':base.FLAGS,'status':'uncompiled hypothesis; no integration or new coverage',
      'name_map':dict((old,new) for old,new,_ in MAP),'added_base':'hkBaseObject','access_hypotheses':['protected hkpPhysicsContextWorldListener','protected hkpWorldPostSimulationListener'],
      'source_name_collision_file_counts':collisions,'warning':'Other source declarations of native base names exist and may be ODR-incompatible. Isolated experiment only; compare compiler RTTI, slots, all code and relocations before any integration.'}
    with (out/'manifest.json').open('x',encoding='utf8') as f:json.dump(record,f,indent=2)
    print(json.dumps({'overlay_sha256':record['overlay_sha256'],'status':record['status'],'base_name_collision_file_counts':collisions}))

if __name__=='__main__':main()
