"""Read-only coverage, queue/payload and source-preimage audit of prepared jobs."""
import collections,hashlib,json,sqlite3
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent.parent.parent;O=H.parent/'out/phase2-web-backlog-20261119'
PRIVATE=P/'FNV/local/runtime-jobs/phase2-20261119'

def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(data):return hashlib.sha256(data).hexdigest()
def facts(spec):return [f for n,t in spec['files'].items() if n.startswith('docs/facts-') for f in json.loads(t)]
def strip(value):
    if isinstance(value,dict):return {k:strip(v) for k,v in value.items() if k not in ('source_offset','evidence_fragment')}
    if isinstance(value,list):return [strip(v) for v in value]
    return value
def reconstruct(rows):
    result=[];i=0
    while i<len(rows):
        row=rows[i];fragment=row.get('evidence_fragment')
        if not fragment:result.append(strip(row));i+=1;continue
        assert fragment['index']==0;field=fragment['field'];count=fragment['count'];base=strip(row);base[field]=[]
        for k in range(count):
            part=rows[i+k];f=part['evidence_fragment'];assert f['field']==field and f['index']==k and f['count']==count
            others=strip(part);values=others.pop(field);compare={a:b for a,b in base.items() if a!=field};assert others==compare
            base[field].extend(values)
        result.append(base);i+=count
    return result

def main():
    ledger=j(O/'job-ledger.json');summary=j(O/'summary.json');census=j(O/'census.json')
    db=sqlite3.connect((P/'FNV/local/runtime-jobs/queue.sqlite3').resolve().as_uri()+'?mode=ro',uri=True)
    before=sqlite3.connect((PRIVATE/'queue-before-navigation.sqlite3').resolve().as_uri()+'?mode=ro',uri=True)
    classes=set();tables=set();table_prefixes=set();hierarchies=set();ws={};bs={};gs={};surveys=set();totals=collections.Counter();context=0;metadata=0
    for row in ledger:
        path=O/'packets'/(row['id']+'.json');raw=path.read_bytes();assert digest(raw)==row['manifest_sha256'];spec=json.loads(raw)
        assert json.loads(db.execute('SELECT spec FROM planner_tickets WHERE id=?',(row['id'],)).fetchone()[0])==spec
        live=db.execute('SELECT spec,state FROM jobs WHERE id=?',(row['id'],)).fetchone()
        if row['status']=='ready':assert live and json.loads(live[0])==spec;totals[live[1]]+=1
        else:assert live is None;totals['held_evidence']+=1
        old=before.execute('SELECT spec FROM planner_tickets WHERE id=?',(row['id'],)).fetchone();current=facts(spec)
        if old:
            original=facts(json.loads(old[0]));assert reconstruct(current)==original
        else:
            assert row['kind']=='vtable_identity_investigation'
            record=current[0]['unclassified_table'];assert record in census['rejected_named_symbol_addresses']
        assert len(spec['files'])<=30 and sum(len(t.encode()) for t in spec['files'].values())<=400000
        assert all(len(t.encode())<=120000 for t in spec['files'].values())
        context=max(context,sum(len(t.encode()) for t in spec['files'].values()));metadata+=len(raw)
        logical=reconstruct(current)
        if row['kind'].startswith('class_'):
            td=next(f['target']['type_descriptor_va'] for f in logical if 'target' in f);assert td not in classes;classes.add(td)
            for fact in logical:
                if 'table' in fact:table_prefixes.add(fact['table'])
                if 'hierarchy' in fact:hierarchies.add(fact['hierarchy']['va'])
            if 'docs/additional-hierarchy-evidence.json' in spec['files']:
                for graph in json.loads(spec['files']['docs/additional-hierarchy-evidence.json']):
                    assert graph in census['hierarchies'] and graph['bases'][0]['type_descriptor_va']==td
                    hierarchies.add(graph['va'])
        elif row['kind']=='placeholder_type_recovery':
            for f in logical:assert f['va'] not in ws;ws[f['va']]=f['size']
        elif row['kind']=='bss_definition_recovery':
            for f in logical:assert f['inventory']['va'] not in bs;bs[f['inventory']['va']]=f
        elif row['kind']=='uncovered_global_recovery':
            for f in logical:assert f['va'] not in gs;gs[f['va']]=f
        elif row['kind']=='source_identity_reconciliation':
            for f in logical:assert f['name'] not in surveys;surveys.add(f['name'])
        elif row['kind']=='vtable_identity_investigation':
            address=logical[0]['unclassified_table']['vtable_va'];assert address not in tables;tables.add(address)
    assert classes=={x['type_descriptor_va'] for x in census['classes']}
    assert tables=={x['vtable_va'] for x in census['rejected_named_symbol_addresses']}
    assert table_prefixes=={x['vtable_va'] for x in census['vtables']}
    assert hierarchies=={x['va'] for x in census['hierarchies']}
    assert len(ws)==6218 and sum(ws.values())==878262 and len(bs)==7171 and len(surveys)==86938
    assert sum(f['zero_bytes'] for f in gs.values())==100045 and sum(f['nonzero_bytes'] for f in gs.values())==67551
    for mapping in (ws,{a:r['size'] for a,r in gs.items()}):
        end=0
        for a,n in sorted(mapping.items()):assert a>=end;end=a+n
    profile=j(P/'FNV/local/runtime-jobs/source-snapshots/fnv-phase2-accepted-825d-20261119-v1/manifest.json')
    for name,meta in profile['files'].items():assert digest((P/'fnv_decomp'/name).read_bytes())==meta['original_sha256']
    assert digest((P/'fnv_decomp/build/units.json').read_bytes())==summary['recipe_sha256']
    placements=j(O/'local-placement-jobs.json');assert len(placements)==67 and sum(x['bytes'] for x in placements)==190878
    assert sum(len(x['ranges']) for x in placements)==4238
    report={'pass':True,'packets':len(ledger),'queue_states':dict(totals),'class_records_once':len(classes),
        'observed_vtable_prefixes_covered':len(table_prefixes),'hierarchy_records_covered':len(hierarchies),
        'unclassified_named_tables_once':len(tables),'W_objects_once':len(ws),'W_bytes':sum(ws.values()),'BSS_names_once':len(bs),
        'uncovered_ranges_once':len(gs),'uncovered_bytes':sum(f['size'] for f in gs.values()),
        'source_only_lexical_names_once':len(surveys),'metadata_disk_bytes':metadata,'largest_context_bytes':context,
        'all_navigation_facts_lossless':True,'all_queue_specs_equal_disk_manifests':True,
        'all_5497_live_source_preimages_unchanged':True,'local_placement_jobs':67,'local_placement_bytes':190878,
        'ledger_sha256':digest((O/'job-ledger.json').read_bytes())}
    (O/'final-coverage-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
