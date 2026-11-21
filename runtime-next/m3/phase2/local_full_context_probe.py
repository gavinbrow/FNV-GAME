"""Bounded in-process libclang translation-unit probe; not a compiler/build."""
import hashlib,json,time
from pathlib import Path
from clang import cindex
R=Path('C:/path/to/Decompilation');F=R/'fnv_decomp';M=R/'runtime-next/m3';O=M/'out/phase2-local-economy-20261119/full-context-probe';sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 if O.exists():raise FileExistsError(O)
 recipe=(F/'build/units.json').read_bytes();units=json.loads(recipe)['units'];expected='825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68'
 if sha(recipe)!=expected:raise ValueError('recipe changed')
 vc=R/'FNV/tools/vc2008/VC'; incs=[F/'include',vc/'include',vc/'PlatformSDK/Include'];args=['-x','c++','--target=i686-pc-windows-msvc','-fms-extensions','-fms-compatibility','-fms-compatibility-version=15.00','-D_MT','-D_CPPUNWIND','-D_M_IX86=600','-nostdinc']+sum((['-isystem',str(p)] if p!=F/'include' else ['-I',str(p)] for p in incs),[])
 index=cindex.Index.create();rows=[];watched={};t0=time.monotonic()
 for i in (775,620,621):
  u=units[i];source=F/u['source'];source_hash=sha(source.read_bytes());start=time.monotonic();tu=index.parse(str(source),args=args,options=cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES|cindex.TranslationUnit.PARSE_INCOMPLETE);diagnostics=[{'severity':d.severity,'text':d.spelling,'file':str(d.location.file) if d.location.file else None,'line':d.location.line,'column':d.location.column} for d in tu.diagnostics];includes=[]
  for inc in tu.get_includes():
   path=Path(inc.include.name).resolve()
   if path.is_file():
    digest=sha(path.read_bytes());watched[str(path)]=digest;includes.append({'path':str(path),'sha256':digest,'depth':inc.depth})
  valid=not any(x['severity']>=3 for x in diagnostics);nodes=[]
  for node in tu.cursor.walk_preorder():
   if node.spelling not in ('TESContainer','TESModel','TESModelPSA','BGSBodyPartData','BGSBodyPart'):continue
   if node.kind not in (cindex.CursorKind.CLASS_DECL,cindex.CursorKind.STRUCT_DECL):continue
   file=str(node.location.file) if node.location.file else None
   z={'kind':node.kind.name,'spelling':node.spelling,'usr':node.get_usr(),'definition':node.is_definition(),'file':file,'line':node.location.line}
   if valid and node.is_definition():
    z['members']=[{'kind':v.kind.name,'spelling':v.spelling,'type':v.type.spelling,'virtual':v.is_virtual_method() if v.kind==cindex.CursorKind.CXX_METHOD else None} for v in node.get_children() if v.kind in (cindex.CursorKind.CXX_BASE_SPECIFIER,cindex.CursorKind.FIELD_DECL,cindex.CursorKind.CXX_METHOD,cindex.CursorKind.DESTRUCTOR)]
   nodes.append(z)
  rows.append({'unit':i,'source':u['source'],'source_sha256':source_hash,'compiler':u['compiler'],'recipe_flags':u['flags'],'parse_args':args,'translation_notes':'i686/MSVC15 compatibility and MT/unwind macros approximated; /Od,/Oy-,/GS,/EHsc,/Gy,/GF not exactly modeled; actual predefines/system resolution may differ','valid_no_error_diagnostics':valid,'diagnostics':diagnostics,'includes':includes,'declarations':nodes,'elapsed_seconds':round(time.monotonic()-start,3)})
  if sha(source.read_bytes())!=source_hash:raise ValueError('source changed while parsing')
 for path,digest in watched.items():
  if sha(Path(path).read_bytes())!=digest:raise ValueError('include changed while parsing '+path)
 if sha((F/'build/units.json').read_bytes())!=expected:raise ValueError('recipe changed while parsing')
 O.mkdir(parents=True);dll=Path(cindex.Config.library_path)/'libclang.dll';out={'scope':'three in-process libclang real translation units, one bounded pass; no compiler/object emission','recipe_sha256':expected,'libclang_dll_sha256':sha(dll.read_bytes()),'units':rows,'total_seconds':round(time.monotonic()-t0,3),'limits':['libclang/MSVC flags and predefined macros approximated; parser is not VC9','includes hash verified after parse, not snapshotted before open','parse success is not original ABI, virtual-slot or ODR proof','member details omitted from invalid translation units']};(O/'full-context-probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8');print(json.dumps([{'unit':z['unit'],'diagnostics':len(z['diagnostics']),'errors':sum(x['severity']>=3 for x in z['diagnostics']),'includes':len(z['includes']),'declarations':len(z['declarations'])} for z in rows]))
if __name__=='__main__':main()
