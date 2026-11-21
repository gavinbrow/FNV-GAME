"""Conservative lexical scope evidence for a reference-global simple class name."""
import argparse,collections,hashlib,json,os,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;P=M.parent.parent;F=P/'fnv_decomp';OUT=M/'out/phase2-scoped-registry';sys.path.insert(0,str(H));import rtti_class_registry as R
NS=re.compile(r'\bnamespace\s*([A-Za-z_]\w*(?:::[A-Za-z_]\w*)*)?\s*$')
CLASS=re.compile(r'\b(class|struct|union)\s+([A-Za-z_]\w*)\b[^{};]*$')
EXTERN=re.compile(r'\bextern\s+\s*$')
TOKEN=re.compile(r'[A-Za-z_]\w*|\d+|\S')
def scopes(text,name):
 c=R.clean(text);c=re.sub(r'(?m)^[ \t]*#[^\r\n]*',lambda m:' '*len(m.group()),c);stack=[];start=0;matches={m.end()-1:m for m in R.DECL.finditer(c) if m.group(2)==name};results=[];conditional=[]
 directives={};depth=[]
 for i,line in enumerate(text.splitlines(),1):
  q=re.match(r'^\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b(.*)',line)
  if q:
   op=q.group(1)
   if op in ('if','ifdef','ifndef'):depth.append(f'{op} {q.group(2).strip()}')
   elif op in ('elif','else') and depth:depth[-1]=op+' '+q.group(2).strip()
   elif op=='endif' and depth:depth.pop()
  directives[i]=list(depth)
 for i,ch in enumerate(c):
  if ch=='{':
   prefix=c[start:i];n=NS.search(prefix);cl=CLASS.search(prefix);external=EXTERN.search(prefix)
   if n:entry=('namespace',n.group(1) or '<anonymous>')
   elif cl:entry=('class',cl.group(2))
   elif external:entry=('extern','C-or-other')
   else:entry=('other','<local-or-unknown>')
   if i in matches:
    m=matches[i];line=c.count('\n',0,m.start())+1;parts=[v for k,v in stack if k in ('namespace','class')];unknown=any(k=='other' for k,v in stack);anonymous=any(v=='<anonymous>' for k,v in stack)
    category='local_or_unknown' if unknown else 'anonymous_namespace' if anonymous else 'nested_class' if any(k=='class' for k,v in stack) else 'namespace' if parts else 'global'
    j=i+1;level=1
    while j<len(c) and level:
     if c[j]=='{':level+=1
     elif c[j]=='}':level-=1
     j+=1
    if level:category='unknown_unbalanced'
    toks=TOKEN.findall(c[m.start():j]);results.append({'line':line,'keyword':m.group(1),'qualified_name':'::'.join(parts+[name]),'category':category,'enclosing_scopes':[{'kind':k,'name':v} for k,v in stack],'conditional_directives':directives[line],'lexical_token_sha256':hashlib.sha256('\x1f'.join(toks).encode()).hexdigest()})
   stack.append(entry);start=i+1
  elif ch=='}':
   if stack:stack.pop()
   else:stack.append(('other','<unmatched-close>'))
   start=i+1
  elif ch==';':start=i+1
 return results
def main():
 p=argparse.ArgumentParser();p.add_argument('--name',default='TESContainer');p.add_argument('--suffix',default='');a=p.parse_args();results=[];files=0
 for root in (F/'src',F/'include'):
  for directory,dirs,names in os.walk(root,followlinks=False):
   for n in names:
    path=Path(directory)/n
    if path.suffix.lower() not in ('.cpp','.h','.hpp','.inl'):continue
    files+=1;text=path.read_text(encoding='utf-8-sig',errors='replace')
    if a.name not in text:continue
    for r in scopes(text,a.name):r['path']=path.relative_to(F).as_posix();results.append(r)
 rows=sorted(results,key=lambda x:(x['path'],x['line']));counts=collections.Counter(x['category'] for x in rows)
 output={'name':a.name,'reference_join':'global only; conditional, macro and ABI status unresolved','source_files_scanned':files,'definition_count':len(rows),'category_counts':dict(counts),'definitions':rows,'limitations':['lexical only; no macro expansion or preprocessor evaluation','conditional branches may yield false scopes or unbalanced braces','function/block scopes and unknown braces are classified conservatively','extern linkage is treated as transparent without asserting linkage spelling','token fingerprints do not prove ABI or ODR equivalence']}
 if a.suffix and not re.fullmatch(r'[A-Za-z0-9_-]+',a.suffix):raise ValueError('invalid suffix')
 OUT.mkdir(exist_ok=True);target=OUT/(a.name+'-scopes'+('-'+a.suffix if a.suffix else '')+'.json')
 if target.exists():raise FileExistsError('refusing overwrite')
 target.write_text(json.dumps(output,indent=2));print(json.dumps({'definitions':len(rows),'counts':counts,'output':str(target)}))
if __name__=='__main__':main()
