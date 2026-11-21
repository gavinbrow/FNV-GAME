"""Stage private native BGSBodyPart destructor hypothesis atop split headers."""
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-bgsbodypart-split-headers-proposal';O=M/'out/phase2-bgsbodypart-native-destructor-proposal'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 manifest=json.loads((P/'manifest.json').read_text())
 for n,v in manifest['outputs'].items():
  if sha((P/n).read_bytes())!=v:raise ValueError('input changed '+n)
 source=(P/'620/bgsbodypart.cpp').read_bytes().decode('ascii').replace('\r\n','\n')
 start=source.index('struct FUN_005e3c60_psa\n{');end=source.index('\nclass PartList;',start)
 block=source[start:end]
 if block.count('FUN_005e3c60_cls::~FUN_005e3c60_cls()')!=1 or block.count('FUN_005e3d50();')!=2:raise ValueError('destructor source anchor changed')
 source=source[:start]+'// @fnv 0x005e3c60\nBGSBodyPart::~BGSBodyPart()\n{\n    FUN_005e3d50();\n}\n'+source[end:]
 header=(P/'620/BGSBodyPart_native.h').read_bytes().decode('ascii').replace('\r\n','\n');old='    void FUN_005e3d20();'
 if header.count(old)!=1:raise ValueError('class helper anchor changed')
 header=header.replace(old,old+'\n    void FUN_005e3d50();',1)
 O.mkdir(exist_ok=False)
 for unit in ('620','621'):
  d=O/unit;d.mkdir()
  for item in (P/unit).iterdir():
   data=item.read_bytes()
   if item.name=='BGSBodyPart_native.h':data=header.encode()
   if unit=='620' and item.name=='bgsbodypart.cpp':data=source.encode()
   (d/item.name).write_bytes(data)
 files={str(p.relative_to(O)).replace('\\','/'):sha(p.read_bytes()) for n in ('620','621') for p in (O/n).iterdir()}
 out={'status':'private uncompiled native nonvirtual destructor hypothesis','input_manifest_sha256':sha((P/'manifest.json').read_bytes()),'outputs':files,
  'proposed_function_change':{'address':'0x005e3c60','before':'??1FUN_005e3c60_cls@@UAE@XZ','after':'??1BGSBodyPart@@QAE@XZ'},
  'proposed_helper_binding':{'symbol':'?FUN_005e3d50@BGSBodyPart@@QAEXXZ','address':'0x005e3d50'},
  'limits':['method and EH/body equality must be established with actual COFF and original reference','separate deleting/free wrappers are untouched',
            'all 15+10 functions, native PSA/BGS vtables, RTTI and EH/weak graph need revalidation','private canonical headers are not installed']}
 (O/'manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({'source_sha256':files['620/bgsbodypart.cpp'],'class_header_sha256':files['620/BGSBodyPart_native.h']}))
if __name__=='__main__':main()
