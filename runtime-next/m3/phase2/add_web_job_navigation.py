"""Losslessly add direct source positions to unclaimed prepared MCP packets."""
import hashlib,json,os,re,sqlite3,sys
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent.parent.parent;O=H.parent/'out/phase2-web-backlog-20261119'
S=P/'FNV/local/runtime-jobs/source-snapshots/fnv-phase2-accepted-825d-20261119-v1'
PRIVATE=P/'FNV/local/runtime-jobs/phase2-20261119';PILOT='P2N19-000-TESContainer775'
sys.path.insert(0,str(P/'FNV/scripts'));import runtime_jobs as r

def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))

def fragments(record):
    if len(compact(record).encode())<=60000:return [record]
    fields=[(len(compact(value).encode()),key) for key,value in record.items() if isinstance(value,list)]
    if not fields:raise ValueError('large atomic evidence record needs coordinator split')
    key=max(fields)[1];base={k:v for k,v in record.items() if k!=key};parts=[];part=[]
    for value in record[key]:
        if part and len(compact({**base,key:part+[value]}).encode())>60000:parts.append(part);part=[]
        part.append(value)
    if part:parts.append(part)
    output=[]
    for i,part in enumerate(parts):
        item={**base,key:part,'evidence_fragment':{'field':key,'index':i,'count':len(parts),'same_logical_record':True}}
        if len(compact(item).encode())>65000:raise ValueError('fragment still exceeds evidence limit')
        output.append(item)
    return output

def main():
    ledger=json.loads((O/'job-ledger.json').read_text());summary=json.loads((O/'summary.json').read_text())
    meta=json.loads((S/'manifest.json').read_text())['files'];cache={};stats={'source_location_offsets':0,'mapped_method_offsets':0}
    def source_info(name):
        if name not in cache:
            text=(S/name).read_text(encoding='utf-8');lines=[0]+[m.end() for m in re.finditer('\n',text)];addresses={}
            for match in re.finditer(r'(?im)^[ \t]*//[^\r\n]*@fnv\s+(?:0x)?([0-9a-f]{8})',text):addresses.setdefault(int(match.group(1),16),match.start())
            cache[name]=(lines,addresses)
        return cache[name]
    def walk(value,target=None):
        if isinstance(value,dict):
            if isinstance(value.get('target'),int):target=value['target']
            name=value.get('path')
            if isinstance(name,str) and name in meta:
                lines,addresses=source_info(name)
                if isinstance(value.get('line'),int) and 1<=value['line']<=len(lines):
                    value['source_offset']=lines[value['line']-1];stats['source_location_offsets']+=1
                elif 'symbol' in value and target in addresses:
                    value['source_offset']=addresses[target];stats['mapped_method_offsets']+=1
            for item in list(value.values()):walk(item,target)
        elif isinstance(value,list):
            for item in value:walk(item,target)
    updates=[]
    for row in ledger:
        if row['id']==PILOT:continue
        path=O/'packets'/(row['id']+'.json');spec=json.loads(path.read_text());facts=[]
        for name,text in list(spec['files'].items()):
            if name.startswith('docs/facts-'):
                records=json.loads(text);walk(records)
                for record in records:facts.extend(fragments(record))
                del spec['files'][name]
        pages=[];page=[]
        for fact in facts:
            if page and len(compact(page+[fact]).encode())>80000:pages.append(page);page=[]
            page.append(fact)
        if page:pages.append(page)
        for i,page in enumerate(pages):spec['files'][f'docs/facts-{i+1:03}.json']=compact(page)+'\n'
        spec['files']['docs/navigation.md']='source_offset is a character offset into the frozen UTF-8/LF text. For a path/offset record read runtime_context(name="repo:"+path, offset=max(0,source_offset-500)); follow next_offset until the relevant declaration/method is complete. Method positions come from source @fnv comments as navigation hints, not identity or ownership proof. Evidence fragments with the same name remain ONE logical record. Interior spaces in exact source paths are allowed. Do not scan every file or read local project sources.\n'
        r.validate_spec(spec)
        raw=(json.dumps(spec,ensure_ascii=False,indent=2)+'\n').encode();updates.append((row,path,spec,raw))
    print(json.dumps({'stage':'navigation packets validated','count':len(updates),**stats}),flush=True)
    with r.connect() as db:
        other=db.execute("SELECT id FROM jobs WHERE id LIKE 'P2N19-%' AND state IN ('leased','submitted') AND id!=?",(PILOT,)).fetchall()
        if other:raise ValueError('another packet is owned; no context updates allowed')
        backup=PRIVATE/'queue-before-navigation.sqlite3'
        if backup.exists():raise FileExistsError('prior navigation transaction exists; reconcile')
        with sqlite3.connect(backup) as connection:db.backup(connection)
        db.execute('BEGIN IMMEDIATE')
        try:
            for row,path,spec,raw in updates:
                text=json.dumps(spec,ensure_ascii=False);item=db.execute('SELECT state FROM jobs WHERE id=?',(row['id'],)).fetchone()
                if item and item['state']!='ready':raise ValueError('packet acquired during preparation')
                db.execute('UPDATE planner_tickets SET spec=? WHERE id=?',(text,row['id']))
                if item:db.execute('UPDATE jobs SET spec=?,version=version+1 WHERE id=?',(text,row['id']))
            db.commit()
        except BaseException:db.rollback();raise
    for row,path,spec,raw in updates:
        temp=path.with_suffix('.navigation');temp.write_bytes(raw);os.replace(temp,path)
        row['manifest_sha256']=hashlib.sha256(raw).hexdigest();row['context_bytes']=sum(len(s.encode()) for s in spec['files'].values())
    (O/'job-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
    summary['navigation']={**stats,'facts_losslessly_compacted':True,'pilot_spec_untouched':True}
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    report={'jobs_updated':len(updates),**summary['navigation'],'ledger_sha256':hashlib.sha256((O/'job-ledger.json').read_bytes()).hexdigest()}
    (O/'navigation-receipt.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
