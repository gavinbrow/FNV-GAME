import json,re,sys,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;sys.path.insert(0,str(M));import gen_m3 as G
j=lambda p:json.load(open(p,encoding='utf-8-sig'))
entries=j(M/'out/batch8-promoted-default-verified/evidence/batch8_final_selection.json')['entries'];inv={int(x['addr'],16):x for x in j(M/'inventory/dat_globals.json')['globals']}
types={'H':('int',4),'I':('unsigned int',4),'J':('long',4),'K':('unsigned long',4),'M':('float',4),'N':('double',8),'F':('short',2),'G':('unsigned short',2),'D':('char',1),'E':('unsigned char',1),'_N':('bool',1),'C':('signed char',1)}
out=[]
for e in entries:
 if e['tc']!='W' or not e.get('named') or len(e.get('decl',[]))!=1:continue
 k=e['decl'][0];m=re.fullmatch(r'\?DAT_([0-9a-f]{8})@([A-Za-z0-9_]+)@@3(.+)[AB]',k)
 if not m or m.group(2)!=e['ns'] or m.group(3) not in types:continue
 code=m.group(3); ctype,sz=types[code];a=e['va'];g=inv.get(a)
 if e['size']!=sz or not g or g['defs'] or not g['decls'] or any(a-3<=r<a+sz for r in G.ORIG_SITES):continue
 # only captured declaration texts of the same straightforward scalar spelling
 pat=r'extern\s+(?:const\s+)?'+re.escape(ctype)+r'\s+DAT_%08x\s*;'%a
 if not all(re.fullmatch(pat,x.strip()) for x in g['decls']):continue
 out.append({'va':a,'size':sz,'namespace':e['ns'],'proposed_type':ctype,'unit_symbol':k,'source_locations':[],'w_runs':e['runs'],'kind':e['kind'],'limitation':'Lexical source evidence does not establish all scopes, alias identity or no earlier ownership; requires targeted source and COFF verification.'})
for e in out:
 name='DAT_%08x'%e['va']; q=subprocess.run(['rg','-n','-F','-g','*.cpp','-g','*.h',name,str(M.parent.parent/'fnv_decomp/src'),str(M.parent.parent/'fnv_decomp/include')],capture_output=True,text=True)
 for line in q.stdout.splitlines():
  z=re.match(r'^(.*?):(\d+):(.*)$',line)
  if z and 'extern ' in z.group(3) and name in z.group(3): e['source_locations'].append({'path':str(Path(z.group(1)).relative_to(M.parent.parent)).replace('\\','/'),'line':int(z.group(2))})
 e['source_locations']=e['source_locations'][:8]
 e['scope_checks']=[]
 for loc in e['source_locations']:
  lines=(M.parent.parent/loc['path']).read_text(encoding='utf-8',errors='replace').splitlines(); ln=loc['line']
  starts=[i+1 for i,x in enumerate(lines[:ln]) if re.search(r'\bnamespace\s+'+re.escape(e['namespace'])+r'\s*\{',x)]
  ends=[i+1 for i,x in enumerate(lines[:ln]) if re.search(r'\}\s*//\s*namespace\s+'+re.escape(e['namespace'])+r'\b',x)]
  e['scope_checks'].append(dict(path=loc['path'],line=ln,namespace_marker_before_unclosed_comment=bool(starts and (not ends or starts[-1]>ends[-1])),const_matches_mangled=bool(re.search(r'\bconst\b',lines[ln-1])) == e['unit_symbol'].endswith('B')))
json.dump({'schema':1,'description':'Conservative W heads with exact scalar-size W object, one namespaced unit scalar encoding, consistent lexical source declaration and no original relocation; review candidates, not integration-ready.','candidates':out,'count':len(out),'bytes':sum(x['size'] for x in out)},open(H/'w_candidates.json','w'),indent=2);print('candidates',len(out),'bytes',sum(x['size'] for x in out));print(out[:3])



