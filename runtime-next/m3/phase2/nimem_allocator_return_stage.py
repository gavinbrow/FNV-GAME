"""Stage the allocator's pointer-return source owner as a private hypothesis."""
import copy,hashlib,json
from pathlib import Path
import baseformcomponent_core_stage as core,tescontainer_install
H=Path(__file__).resolve().parent;M=H.parent;RN=M.parent;F=RN.parent/'fnv_decomp';O=M/'out/phase2-nimem-allocator-return';BASE='6757c8a0b6611e29b38061f489cd0f1e05f862dc65f3700f9dd39b78ccdb8d0c';SOURCE='src/staging/blk_00aa0000_o2.cpp';PRE='de080a4aac262320db78b029a03b09a3854c48e560e71cc184ff0818662ad43c';OLD='?FUN_00aa13e0@@YAXH@Z';NEW='?FUN_00aa13e0@@YAPAXI@Z'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError('preserve prior fixture')
 raw=(F/'build/units.json').read_bytes();doc=json.loads(raw);u=doc['units'][2734];old=(F/SOURCE).read_bytes()
 if sha(raw)!=BASE or sha(old)!=PRE or u['source']!=SOURCE or len(u['functions'])!=43 or u['compiler']!='sp1':raise ValueError('pinned input differs')
 owner=[f for f in u['functions'] if f['address']=='0x00aa13e0']
 if len(owner)!=1 or owner[0]['symbol']!=OLD or owner[0]['size']!=62:raise ValueError('source owner differs')
 refs=[i for i,z in enumerate(doc['units']) if OLD in z.get('symbols',{}) or any(OLD==f['symbol'] or OLD in f.get('fold_aliases',[]) for f in z['functions'])]
 if refs!=[2734]:raise ValueError('old source symbol has outside recipe use')
 pairs=[(b'    virtual void Dispatch(int* value, int* command, int a, int b, int c, int d, int e);',b'    virtual void* Dispatch(unsigned int* value, int* command, int a, int b, int c, int d, int e);'),(b'void __cdecl FUN_00aa13e0(int value)',b'void* __cdecl FUN_00aa13e0(unsigned int value)'),(b'    int adjusted = value;',b'    unsigned int adjusted = value;'),(b'    device->Dispatch(&adjusted, &command, 1, 1, 0, -1, 0);',b'    return device->Dispatch(&adjusted, &command, 1, 1, 0, -1, 0);')]
 new=old
 for a,b in pairs:
  if new.count(a)!=1:raise ValueError('source anchor differs '+repr(a))
  new=new.replace(a,b,1)
 candidate=copy.deepcopy(u);next(x for x in candidate['functions'] if x['address']=='0x00aa13e0')['symbol']=NEW;generated=tescontainer_install.replace_unit(raw,2734,candidate);nd=json.loads(generated)
 if [i for i,(a,b) in enumerate(zip(doc['units'],nd['units'])) if a!=b]!=[2734] or any(doc[k]!=nd[k] for k in doc if k!='units'):raise ValueError('recipe scope differs')
 before=core.walk(F,SOURCE,{});after=core.walk(F,SOURCE,{SOURCE:new})
 if set(before['files'])!=set(after['files']):raise ValueError('include closure differs')
 O.mkdir();(O/'units.original').write_bytes(raw);(O/'units.generated').write_bytes(generated);(O/'source.original').write_bytes(old);(O/'source.generated').write_bytes(new)
 for tag,graph in (('original',before),('candidate',after)):
  for rel,digest in graph['files'].items():
   data=new if tag=='candidate' and rel==SOURCE else (F/rel).read_bytes()
   if sha(data)!=digest:raise ValueError('closure changed')
   q=O/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
 mm={'schema_version':1,'source':SOURCE,'units_sha256':BASE,'unit':2734,'original_inputs':before['files'],'original':before,'candidate':after,'production_include_order':['/I<mirror>/include'],'limits':['private owner contract hypothesis; no live source or recipe changes']};(O/'mirror-manifest.json').write_text(json.dumps(mm,indent=2))
 m={'base_recipe_sha256':BASE,'candidate_recipe_sha256':sha(generated),'before_source_sha256':sha(old),'after_source_sha256':sha(new),'unit':2734,'functions':43,'recipe_eh_tails':len(u.get('eh_tails',[])),'owner_address':'0x00aa13e0','owner_size':62,'old_symbol':OLD,'candidate_symbol':NEW,'old_recipe_consumers':refs,'existing_pointer_return_bindings':sum(NEW in z.get('symbols',{}) for z in doc['units']),'independent_consumers':[{'unit':253,'address':'0x008c4d10','call':'0x008c4d42','size':108},{'unit':98,'address':'0x00a1fd50','calls':['0x00a2002c','0x00a200cb','0x00a201ec','0x00a20299','0x00a20432']}],'limits':['private source ABI contract hypothesis; exact 62-byte and all 43 function/relocation comparisons required','virtual allocator dispatch prototype and failure semantics remain limited to observed calling/return behavior','full ownership and final image/runtime remain separate','allocation API hypothesis and class-key cohort remain distinct']}
 (O/'manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'unit':2734,'functions':43,'existing_pointer_return_bindings':m['existing_pointer_return_bindings'],'candidate_recipe_sha256':sha(generated)}))
if __name__=='__main__':main()
