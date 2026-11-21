import json,re,sys,collections
from pathlib import Path
P=Path(r'C:\path\to\Decompilation'); M=P/'runtime-next/m3'; sys.path.insert(0,str(P/'fnv_decomp/tools'));from compare import Coff
sel=json.load(open(M/'out/phase2-w-scalar/selection.json'))['entries']; es=[e for e in sel if 'scalar_symbol' in e]; candidates={x['va']:x for x in json.load(open(M/'phase2/w_candidates.json'))['candidates']}; inv={int(g['addr'],16):g for g in json.load(open(M/'inventory/dat_globals.json'))['globals']}; units=json.load(open(P/'fnv_decomp/build/units.json'))['units']
def strip(s):
 # Preserve offsets and newlines; ignore comments, string and character literals.
 pat=re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
 return pat.sub(lambda m: ''.join('\n' if c=='\n' else ' ' for c in m.group()),s)
def at_scope(clean,pos):
 stack=[]; last=0
 for m in re.finditer(r'[{};]',clean[:pos]):
  c=m.group(); i=m.start()
  if c=='{':
   prefix=clean[last:i]; n=re.search(r'\bnamespace\s+([A-Za-z_]\w*)\s*$',prefix)
   stack.append(('namespace',n.group(1)) if n else ('block',None));last=i+1
  elif c=='}':
   if stack:stack.pop()
   else:return None
   last=i+1
  else:last=i+1
 return stack
cache={};out=[]
for e in es:
 va=e['va']; x=candidates[va]; expected=e['scalar_symbol']; g=inv.get(va,{}); unitmatches=[]
 for i,u in enumerate(units):
  hit={k:v for k,v in u.get('symbols',{}).items() if re.search(r'(?:DAT|PTR|OFF|UNK|BYTE|WORD|DWORD)_%08x\b'%va,k)}
  if hit:
   obj=P/'runtime-next/pinned-build/obj_v3'/('%04d.obj'%i);actual=[];err=None
   try:
    c=Coff(str(obj)); actual=[{'name':z['name'],'section':z['section'],'storage':z['storage']} for z in c.symbols.values() if z['name']==expected]
   except Exception as ex:err=str(ex)
   unitmatches.append({'unit':i,'source':u['source'],'maps':hit,'coff_symbol':actual,'coff_error':err})
 scopes=[]
 for loc in x['source_locations']:
  path=P/loc['path']; raw=path.read_text(encoding='utf8',errors='replace'); lines=raw.splitlines(keepends=True);pos=sum(len(l) for l in lines[:loc['line']-1]);line=lines[loc['line']-1].strip(); clean=cache.setdefault(str(path),strip(raw));stack=at_scope(clean,pos);scopes.append({'path':loc['path'],'line':loc['line'],'line_text':line,'lexical_scope':stack})
 types=g.get('declared_types',[]); decls=g.get('decls',[])
 out.append({'va':va,'expected':expected,'proposed_type':x['proposed_type'],'const':e['scalar_const'],'scopes':scopes,'inventory_types':types,'inventory_declarations':decls,'unitmatches':unitmatches})
print('count',len(out))
for r in out:
 print(hex(r['va']),'scope',r['scopes'][0]['lexical_scope'],'decl',r['scopes'][0]['line_text'],'types',r['inventory_types'],'units',[(z['unit'],z['coff_symbol']) for z in r['unitmatches']])
json.dump({'note':'Lexical brace stack, source and COFF facts; preprocessor not evaluated. No compiler or runtime test.','candidates':out},open(M/'phase2/w_scalar_scope_audit.json','w'),indent=2)
