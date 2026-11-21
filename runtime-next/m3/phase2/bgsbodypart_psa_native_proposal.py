"""Stage uncompiled native PSA constructor and independently check reference EH graph."""
import hashlib
import json
import struct
import sys
from pathlib import Path

H=Path(__file__).resolve().parent
M=H.parent
ROOT=M.parent.parent
FN=ROOT/'fnv_decomp'
PRIOR=M/'out/phase2-bgsbodypart-psa-proposal'
OUT=M/'out/phase2-bgsbodypart-psa-native-proposal'
sys.path[:0]=[str(M),str(FN/'tools')]
import gen_m3 as G
from compare import Coff


def sha(data):return hashlib.sha256(data).hexdigest()
def dword(va):return struct.unpack('<I',G.refbytes(va,4))[0]
def rel(va):
    if va not in G.ORIG_SET:raise ValueError('expected original relocation '+hex(va))
    return dword(va)


def main():
    manifest=json.loads((PRIOR/'manifest.json').read_text())
    src=(PRIOR/'620/bgsbodypart.cpp').read_bytes()
    header=(PRIOR/'620/bgsbodypart_decls.h').read_bytes()
    units=(FN/'build/units.json').read_bytes()
    if sha(src)!=manifest['input_sha256']['620.cpp'] or sha(header)!=manifest['candidate_header_sha256'] or sha(units)!=manifest['input_sha256']['units']:
        raise ValueError('proposal input digest mismatch')
    old=(b'// @fnv 0x005e3be0\r\nTESModel* __fastcall FUN_005e3be0(TESModel* pThis)\r\n{\r\n'
         b'    pThis->TESModel::TESModel();\r\n    *(int**)pThis = &DAT_0104540c;\r\n    return pThis;\r\n}')
    new=b'// @fnv 0x005e3be0\r\nTESModelPSA::TESModelPSA()\r\n{\r\n}'
    if src.count(old)!=1:raise ValueError('original constructor body mismatch')
    candidate=src.replace(old,new,1)
    unit=json.loads(units)['units'][620]
    f=[x for x in unit['functions'] if x['address']=='0x005e3be0']
    if len(f)!=1:raise ValueError('constructor function mapping absent')
    if rel(0x5e3af6)!=0xef9e3d or rel(0xef9e4f)!=0x114b464 or rel(0x114b46c)!=0x114b488:
        raise ValueError('reference EH chain differs')
    rows=[]
    for i in range(7):
        p=0x114b488+i*8; state=struct.unpack('<i',G.refbytes(p,4))[0]; action=rel(p+4)
        rows.append({'state':i,'next_state':state,'action_va':hex(action),'action_pointer_site':hex(p+4)})
    if rows[6]['next_state']!=5 or rows[6]['action_va']!='0xef9e32':raise ValueError('wrong PSA cleanup state')
    # Check exact control-flow encodings, not just a disassembler interpretation.
    action=G.refbytes(0xef9e32,11)
    if action[:7]!=bytes.fromhex('8b4df083c144e9') or 0xef9e3d+struct.unpack('<i',action[7:11])[0]!=0x51b950:
        raise ValueError('reference member cleanup thunk differs')
    archive=(PRIOR/'lane-compile.json').read_bytes()
    records={(x['unit'],x['tag']):x for x in json.loads(archive)['outcomes']}
    expected={'original':'198d78151c8815637c1d5a16cc75c7f23faaebc664dfb32eee2b8dc35dd4841d',
              'mirror':'b43c3ac51857e9e0f7c298f5f10473e9d018fcbbc9045586f5560b4b46219e01'}
    coffs={}
    for tag in ('original','mirror'):
        p=PRIOR/('0620.'+tag+'.obj'); rec=records[620,tag]
        if rec['rc']!=0 or rec['object_sha256']!=expected[tag] or sha(p.read_bytes())!=expected[tag] or rec['source_sha256']!=manifest['input_sha256']['620.cpp']:
            raise ValueError('archived compilation evidence mismatch')
        c=Coff(str(p)); matches=[]
        for sec in c.sections:
            if not sec or sec['name']!='.text$x':continue
            refs=[(off,kind,c.symbols[idx]['name']) for off,idx,kind in sec['relocs']]
            if any(off==0x49 and name in ('??1FUN_005e3be0@@QAE@XZ','??1TESModelPSA@@QAE@XZ') for off,kind,name in refs):
                matches.append({'section_sha256':sha(sec['data']),'size':len(sec['data']),'relocations':refs,
                                'state6_offset':0x42,'state6_relocation_offset':0x49})
        if len(matches)!=1:raise ValueError('cleanup COFF section ambiguous')
        coffs[tag]={'object_sha256':sha(p.read_bytes()),'cleanup':matches[0]}
    if coffs['original']['cleanup']['section_sha256']!=coffs['mirror']['cleanup']['section_sha256']:
        raise ValueError('cleanup thunk bytes differ')
    OUT.mkdir(exist_ok=False)
    (OUT/'bgsbodypart.cpp').write_bytes(candidate)
    (OUT/'bgsbodypart_decls.h').write_bytes(header)
    report={'status':'private uncompiled hypothesis; table identity and canonical class unresolved',
      'input_sha256':{'source':sha(src),'header':sha(header),'units':sha(units)},
      'output_sha256':{'source':sha(candidate),'header':sha(header)},
      'reference_eh':{'constructor_handler_pointer_site':'0x5e3af6','handler':'0xef9e3d',
          'handler_funcinfo_pointer_site':'0xef9e4f','funcinfo':'0x114b464',
          'unwind_pointer_site':'0x114b46c','unwind_map':'0x114b488','states':rows,
          'state6_member_offset':68,'state6_target':'0x51b950'},
      'coff':coffs,'prior_compile_result_sha256':sha(archive),
      'recipe_proposal':{'constructor':{'before':f[0]['symbol'],'after':'??0TESModelPSA@@QAE@XZ','address':'0x005e3be0'},
                         'member_destructor':{'symbol':'??1TESModelPSA@@QAE@XZ','address':'0x0051b950'},
                         'surrogate_comparison_only':{'symbol':'??1FUN_005e3be0@@QAE@XZ','address':'0x0051b950'}},
      'requirements':['exact compiler COFF constructor and observed vtable prefix with original targets; full extent unresolved',
                      '15+10 functions and complete EH and metadata comparison','canonical base virtual signatures remain unresolved',
                      'native constructor compiler must emit real PSA vptr, not manual vptr store']}
    (OUT/'manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'source_sha256':sha(candidate),'manifest':str(OUT/'manifest.json')}))


if __name__=='__main__':main()
