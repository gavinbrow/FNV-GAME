"""Read-only comparison of one reference RTTI hierarchy and private overlay COFF."""
import hashlib,json,struct,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; M3=HERE.parent;PROJ=M3.parent.parent;OUT=M3/'out/phase2-hkp-constraint-viewer'
sys.path[:0]=[str(PROJ/'fnv_decomp/tools'),str(M3)]
from compare import Coff
import gen_m3 as g


def u32(a):return struct.unpack('<I',g.refbytes(a,4))[0]

def original():
    locators=[]; hierarchy=None
    for vt in (0x010d21c4,0x010d21a4,0x010d2194,0x010d2184):
        if vt-4 not in g.ORIG_SET: raise ValueError('unrelocated locator pointer')
        col=u32(vt-4); sig,offset,cd,td,chd=struct.unpack('<IIIII',g.refbytes(col,20))
        if col+12 not in g.ORIG_SET or col+16 not in g.ORIG_SET:raise ValueError('unrelocated COL fields')
        if hierarchy is None:hierarchy=chd
        elif hierarchy!=chd:raise ValueError('locators disagree on hierarchy')
        locators.append({'vtable_va':hex(vt),'col_va':hex(col),'signature':sig,'offset':offset,'constructor_displacement':cd,'type_descriptor_va':hex(td),'hierarchy_va':hex(chd)})
    sig,attrs,count,array=struct.unpack('<IIII',g.refbytes(hierarchy,16))
    if hierarchy+12 not in g.ORIG_SET or count!=7:raise ValueError('unexpected reference hierarchy')
    bases=[]
    for i in range(count):
        slot=array+4*i
        if slot not in g.ORIG_SET:raise ValueError('unrelocated base array element')
        b=u32(slot);td,n,m,p,v,attr,ch=struct.unpack('<IIiiiII',g.refbytes(b,28))
        if b not in g.ORIG_SET or b+24 not in g.ORIG_SET:raise ValueError('unrelocated base descriptor fields')
        name=g.refbytes(td+8,256).split(b'\x00',1)[0].decode('ascii')
        bases.append({'preorder_index':i,'descriptor_va':hex(b),'type_descriptor_va':hex(td),'type_name':name,'contained_bases':n,'pmd':{'mdisp':m,'pdisp':p,'vdisp':v},'attributes':hex(attr),'class_hierarchy_va':hex(ch)})
    return {'locators':locators,'hierarchy':{'va':hex(hierarchy),'signature':sig,'attributes':hex(attrs),'base_count':count,'base_array_va':hex(array),'bases':bases}}


def obj_symbol(c,name):
    sy=c.named(name);sec=c.sections[sy['section']]
    return sy,sec


def overlay(path=None):
    path=Path(path) if path is not None else OUT/'2501.overlay.obj';c=Coff(str(path));s,sec=obj_symbol(c,'??_R3hkpConstraintViewer@@8');sig,attr,count,_=struct.unpack_from('<IIII',sec['data'],s['value'])
    rel3=[c.symbols[i]['name'] for off,i,k in sec['relocs'] if off==s['value']+12 and k==6]
    if rel3!=['??_R2hkpConstraintViewer@@8'] or not 1 <= count <= 32:raise ValueError('unexpected overlay hierarchy')
    a,arr=obj_symbol(c,rel3[0]); rels=sorted((off-a['value'],i,k) for off,i,k in arr['relocs'] if a['value']<=off<a['value']+4*count)
    if [x[0] for x in rels]!=list(range(0,4*count,4)) or any(x[2]!=6 for x in rels):raise ValueError('unexpected overlay base array')
    bases=[]
    for index,(off,idx,kind) in enumerate(rels):
        b=c.symbols[idx];sec=c.sections[b['section']];v=struct.unpack_from('<IIiiiII',sec['data'],b['value']);targets=[c.symbols[i]['name'] for q,i,k in sec['relocs'] if q==b['value'] and k==6]
        if len(targets)!=1:raise ValueError('unexpected overlay type pointer')
        bases.append({'preorder_index':index,'descriptor_symbol':b['name'],'type_symbol':targets[0],'contained_bases':v[1],'pmd':{'mdisp':v[2],'pdisp':v[3],'vdisp':v[4]},'attributes':hex(v[5])})
    locators=[]
    for sym in c.symbols.values():
        if sym['section']>0 and sym['name'].startswith('??_R4hkpConstraintViewer@@'):
            sec=c.sections[sym['section']];v=struct.unpack_from('<IIIII',sec['data'],sym['value']);rel=[{'offset':o-sym['value'],'target_symbol':c.symbols[i]['name'],'kind':k} for o,i,k in sec['relocs'] if sym['value']<=o<sym['value']+20]
            locators.append({'symbol':sym['name'],'signature':v[0],'offset':v[1],'constructor_displacement':v[2],'relocations':rel})
    return {'object_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'locators':sorted(locators,key=lambda x:x['offset']),'hierarchy':{'signature':sig,'attributes':hex(attr),'base_count':count,'bases':bases}}


def main():
    out=OUT/'hierarchy-analysis.json'
    if out.exists():raise FileExistsError('refusing to overwrite analysis')
    orig=original();obj=overlay();data={'schema_version':1,'scope':'Observed reference record fields and private overlay COFF fields only; no semantic base-equivalence proof.','reference':orig,'overlay':obj,
      'comparison':{'locator_offsets_equal':sorted(x['offset'] for x in orig['locators'])==sorted(x['offset'] for x in obj['locators']),'hierarchy_signature_equal':orig['hierarchy']['signature']==obj['hierarchy']['signature'],'hierarchy_attributes_equal':orig['hierarchy']['attributes']==obj['hierarchy']['attributes'],'hierarchy_base_count_equal':orig['hierarchy']['base_count']==obj['hierarchy']['base_count'],
      'reference_base_count':orig['hierarchy']['base_count'],'overlay_base_count':obj['hierarchy']['base_count'],'limitation':'Similar offsets do not establish type identity, inheritance semantics, vtable slots, placement, or runtime compatibility.'}}
    with out.open('x',encoding='utf8') as f:json.dump(data,f,indent=2)
    print(json.dumps(data['comparison']))

if __name__=='__main__':main()
