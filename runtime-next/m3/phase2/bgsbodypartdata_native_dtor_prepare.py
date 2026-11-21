"""Private BGSBodyPartData native destructor recovery hypothesis."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out/phase2-bgsbodypartdata-native-dtor-v1';sys.path.insert(0,str(H));import rtti_mirror_prepare as prep
BASE='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68';h=lambda b:hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError(O)
 units=(F/'build/units.json').read_bytes()
 if h(units)!=BASE:raise ValueError('recipe mismatch')
 u=json.loads(units)['units'];owner=[f for f in u[2656]['functions'] if f['address']=='0x005e4bc0'];wrapper=[f for f in u[2656]['functions'] if f['address']=='0x005e4b90']
 if len(owner)!=1 or owner[0]['size']!=127 or len(wrapper)!=1 or wrapper[0]['size']!=44 or len(u[621]['functions'])!=10:raise ValueError('owner scope mismatch')
 src='src/fallout_shared/bgsbodypartdata.cpp';hdr='src/fallout_shared/bgsbodypartdata.h';oldsrc=(F/src).read_bytes();oldhdr=(F/hdr).read_bytes();x=oldhdr.replace(b'    BGSBodyPartData();',b'    BGSBodyPartData();\n    virtual ~BGSBodyPartData();',1)
 if x==oldhdr or oldhdr.count(b'    BGSBodyPartData();')!=1:raise ValueError('header anchor')
 anchor=b'// @fnv 0x005e4c40';y=oldsrc.replace(anchor,b'// Candidate: source-owned destructor body from 0x005e4bc0.\nBGSBodyPartData::~BGSBodyPartData()\n{\n    BGSBodyPartData::ClearData();\n}\n\n'+anchor,1)
 if y==oldsrc or oldsrc.count(anchor)!=1:raise ValueError('source anchor')
 prep.transition=lambda old,new,current: json.loads(current) if h(current)==BASE else (_ for _ in ()).throw(ValueError('recipe changed'))
 m=prep.prepare(src,{src:y,hdr:x},O);m.update(unit=621,units_sha256=BASE,reviewed_units_sha256=BASE,scope='private native destructor hypothesis, source and layout unproven',proposed_owner={'donor_unit':2656,'old':owner[0],'native_symbol':'??1BGSBodyPartData@@UAE@XZ','wrapper_owner':wrapper[0]},limits=['strict all10 ordinary functions and native 127-byte destructor with full resolved relocations','all affected include closures and global ODR','full EH graph and vtable slots/thunks; weak E remains unresolved','no recipe edit or native owner transfer yet']);(O/'mirror-manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'source_sha256':h(y),'header_sha256':h(x),'files':len(m['candidate']['files'])}))
if __name__=='__main__':main()
