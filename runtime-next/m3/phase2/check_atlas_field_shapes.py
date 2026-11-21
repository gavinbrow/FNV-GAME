"""Check the decoder against fresh original-compiler CodeView and malformed inputs."""
from pathlib import Path
import argparse,hashlib,json,sqlite3,struct,subprocess,sys
R=Path(__file__).resolve().parents[3];sys.path[:0]=[str(R/'runtime-next/m3/phase2'),str(R/'fnv_decomp/tools')]
from decode_atlas_field_shapes import Decoder,numeric
from compare import Coff
import rtti_tesform_bindings_transaction as locks

def run(out):
 assert not out.exists();out.mkdir(parents=True);src=out/'fixture.cpp';src.write_text('char fileName[260]; float matrix[16]; unsigned int integers[8]; char* pointers[15]; struct Flags { unsigned int low:3; unsigned int high:5; }; Flags flags;\n')
 obj=out/'fixture.obj';cmd=[str(R/'FNV/tools/vc2008/VC/bin/cl.exe'),'/nologo','/c','/Od','/Z7','/Fo'+str(obj),str(src)];guards=locks.acquire_guard()
 try:
  assert not (R/'runtime-next/direct-v1/harness.lock').exists();cp=subprocess.run(cmd,cwd=out,capture_output=True,text=True);assert cp.returncode==0,cp.stdout+cp.stderr
 finally:
  for p in reversed(guards):p.unlink()
 (out/'compile.log').write_text(cp.stdout+cp.stderr);coff=Coff(str(obj));types=next(s['data'] for s in coff.sections[1:] if s['name']=='.debug$T');assert struct.unpack_from('<I',types)[0]==4
 c=sqlite3.connect(':memory:');c.execute('create table codeview_type_records(type_record_id text,program_id text,type_index integer,leaf_kind integer,raw_body blob,raw_body_sha256 text)');c.execute('create table codeview_tag_layouts(type_record_id text,tag_kind text,size_value text,display_name text,unique_name text,is_forward_reference integer,underlying_type_index integer,program_id text)');i=4;ti=0x1000;records=[]
 while i<len(types):
  length=struct.unpack_from('<H',types,i)[0];assert length>=2 and i+2+length<=len(types);leaf=struct.unpack_from('<H',types,i+2)[0];body=types[i+4:i+2+length];c.execute('insert into codeview_type_records values(?,?,?,?,?,?)',(str(ti),'fixture',ti,leaf,body,hashlib.sha256(body).hexdigest()));records.append((ti,leaf));ti+=1;i+=2+length
 d=Decoder(c);shapes=[d.decode('fixture',ti) for ti,leaf in records if leaf in (0x1503,0x1205)];arrays=[s for s in shapes if s['kind']=='array'];bits=[s for s in shapes if s['kind']=='bitfield'];assert {(s['byte_size'],s['element_count']) for s in arrays}=={(260,260),(64,16),(32,8),(60,15)};assert {(s['bit_width'],s['bit_offset'],s['byte_size']) for s in bits}=={(3,0,4),(5,3,4)}
 assert numeric(struct.pack('<HI',0x8004,70000),0)==(70000,6)
 negative=[]
 for label,body,leaf in [('array_nondivisible',struct.pack('<IIH',0x40,0x22,3)+b'\0',0x1503),('truncated_array',b'\0',0x1503),('invalid_bitfield',struct.pack('<IBB',0x75,31,8),0x1205)]:
  ti+=1;c.execute('insert into codeview_type_records values(?,?,?,?,?,?)',(str(ti),'fixture',ti,leaf,body,hashlib.sha256(body).hexdigest()));rejected=False
  try:d.decode('fixture',ti)
  except (ValueError,struct.error):rejected=True
  assert rejected,label;negative.append(label)
 result={'scope':'Fresh MSVC2008 /Z7 own-data fixture, no game function bodies','command':cmd,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'object_sha256':hashlib.sha256(obj.read_bytes()).hexdigest(),'decoded_shapes':shapes,'checked_array_shapes':4,'checked_bitfield_shapes':2,'encoded_large_integer_case':True,'malformed_cases_rejected':negative,'pass':True};(out/'result.json').write_text(json.dumps(result,indent=2));print('PASS4 compiler arrays,2 compiler bitfields,large numeric,3 malformed records')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.out.resolve())
