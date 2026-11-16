import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import types
import struct
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('prepare_fixture',ROOT/'tools/rebuild/application_successor_prepare_v4.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def enc(obj):return json.dumps(obj,separators=(',',':')).encode()

def archive_bytes(symbol):
    names=[symbol,'__imp_'+symbol];strings=b''.join(x.encode()+b'\0' for x in names)
    a,b=12+len(strings),16+len(strings)
    offset=8+60+a+(a&1)+60+b+(b&1)
    first=struct.pack('>III',2,offset,offset)+strings
    second=struct.pack('<IIIHH',1,offset,2,1,1)+strings
    payload=symbol.encode()+b'\0fixture.dll\0'
    short=struct.pack('<HHHHIIHH',0,0xffff,0,0x14c,0,len(payload),7,8)+payload
    def member(name,data):
        return ('%-16s%-12d%-6d%-6d%-8d%-10d`\n' % (name,0,0,0,0,len(data))).encode()+data+(b'\n' if len(data)&1 else b'')
    return b'!<arch>\n'+member('/',first)+member('/',second)+member('fixture.dll/',short)

class Tests(unittest.TestCase):
    def setUp(self):
        self.old=(m.ROLE_PINS,m.SOURCE_GRAPH,m.PEER_SCHEMAS,m.ROOT);self.addCleanup(self.restore)
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);m.ROOT=Path(self.tmp.name)
        data={r:b'evidence' for r in m.CORE_ROLES};data['member:a.obj']=b'member';data['archive']=b'archive'
        data['semantic']=enc({'wrappers':[],'members':[{'name':'a.obj'}],'handoff':{},'member_count':1,'field_count':0,
          'namespace_by_member':{},'expected_providers':[],'expected_fields':[],'component':'fixture','selected_providers':{}})
        data['factory']=enc({'selections':[],'outcomes':[],'emitted':[]})
        data['iat']=enc({'full_proofs':{},'kernel_role':'iat_library:lib0',
            'replay':{'native':{},'request':{},'request_sha256':'a'*64,'originals':{},
                      'expected_sources':{},'catalog':{},'prior_iat':[]}});data['crt']=enc({'bindings':[],'source_evidence':{},'prior_crt':[]})
        data['response']=enc({'old_out':'old','new_out':'new','inherited_aliases':[],
                              'fresh_uuid_identity':{},'qualified_uuid':{}})
        for i in range(4):data['iat_library:lib'+str(i)]=b'library'+bytes([i])
        self.data=data
        m.ROLE_PINS={k:{'path':k.replace(':','_'),'sha256':m.sha(v)} for k,v in data.items()}
        self.ids={}
        for i,(k,pin) in enumerate(m.ROLE_PINS.items()):
            path=m.ROOT/pin['path'];path.write_bytes(data[k]);absolute=str(path.absolute())
            self.ids[k]={'requested_path':absolute,'path':absolute,'sha256':pin['sha256'],
                         'size':len(data[k]),'device':1,'inode':i+1}
        names=['application_import34_diagnostic','import_kernel32_fifteen','iat_code21_annotations','application_link_diagnostic','normal_import_archive_bytes_v1']
        finder=types.SimpleNamespace(snapshots={n:('module '+n).encode() for n in names})
        self.finder=finder;sys.meta_path.insert(0,finder);self.addCleanup(sys.meta_path.remove,finder)
        m.SOURCE_GRAPH={n:{'path':'tools/'+n+'.py','sha256':m.sha(finder.snapshots[n])} for n in names}
        for name in names:
            previous=sys.modules.get(name);mod=types.ModuleType(name);mod.__loader__=finder
            sys.modules[name]=mod;self.addCleanup(self._restore_module,name,previous)
        sys.modules[names[4]].parse_archive=lambda data:{'archive_sha256':m.sha(data)}
        sys.modules[names[3]].partial=types.SimpleNamespace(native_archive=lambda data:{'fixture':data})
    @staticmethod
    def _restore_module(name,old):
        if old is None:sys.modules.pop(name,None)
        else:sys.modules[name]=old
    def restore(self):m.ROLE_PINS,m.SOURCE_GRAPH,m.PEER_SCHEMAS,m.ROOT=self.old
    def test_exact_role_wiring_and_archive_phase_identity(self):
        args=m._arguments(self.data,self.ids)
        self.assertEqual(args['archive_bytes'],b'archive');self.assertEqual(args['archive_identity'],self.ids['archive'])
        self.assertEqual(args['response_inputs']['new_archive'],self.ids['archive']['path'])
        self.assertEqual(args['semantic_inputs']['member_bytes'],{'a.obj':b'member'})
        self.assertEqual(args['factory_inputs']['member_bytes'],args['semantic_inputs']['member_bytes'])
        called=[];fake=types.ModuleType('application_successor_compose_v12')
        fake.compose=lambda **kw:called.append(kw) or {'link_approved':False}
        previous=sys.modules.get(fake.__name__);sys.modules[fake.__name__]=fake
        try:self.assertEqual(m._compose_v12_untrusted_fixture(self.data,self.ids),{'link_approved':False})
        finally:
            if previous is None:sys.modules.pop(fake.__name__,None)
            else:sys.modules[fake.__name__]=previous
        self.assertEqual(called[0]['archive_identity'],self.ids['archive'])
    def test_missing_extra_or_substituted_archive_and_member_rejected(self):
        missing=copy.deepcopy(self.data);missing.pop('archive')
        extra=copy.deepcopy(self.data);extra['surprise']=b'x'
        changed=copy.deepcopy(self.data);changed['archive']=b'other'
        for data in (missing,extra,changed):
            with self.assertRaises(ValueError):m._arguments(data,self.ids)
        ids=copy.deepcopy(self.ids);ids['archive']['path']=str(m.ROOT/'other.lib')
        with self.assertRaises(ValueError):m._arguments(self.data,ids)
        ids=copy.deepcopy(self.ids);ids['archive']['inode']=True
        with self.assertRaises(ValueError):m._arguments(self.data,ids)
        data=copy.deepcopy(self.data);data['member:a.obj']=b'other'
        with self.assertRaises(ValueError):m._arguments(data,self.ids)
    def test_replay_uses_snapshot_modules_and_rejects_preload(self):
        args=m._arguments(self.data,self.ids)
        replay=args['iat_inputs']['replay']
        self.assertIs(replay['old'],sys.modules['application_import34_diagnostic'])
        self.assertIs(replay['producer'],sys.modules['import_kernel32_fifteen'])
        self.assertEqual(len(replay['libraries']),4)
        loaded=sys.modules['iat_code21_annotations'];loaded.__loader__=object()
        with self.assertRaises(ValueError):m._arguments(self.data,self.ids)
        loaded.__loader__=self.finder

    def test_every_role_required_in_ordered_phase_ledger(self):
        ledger=list(self.ids.values());op={'input_bindings':ledger,'phases':[{'name':'compose-v12'}]}
        self.assertEqual(m._phase_role_binding(op,self.ids),self.ids['archive'])
        for role in ('factory_peer','semantic','iat_library:lib2','member:a.obj'):
            bad={'input_bindings':[x for x in ledger if x is not self.ids[role]],'phases':op['phases']}
            with self.subTest(role=role),self.assertRaises(ValueError):m._phase_role_binding(bad,self.ids)
        bad={'input_bindings':list(reversed(ledger)),'phases':op['phases']}
        with self.assertRaises(ValueError):m._phase_role_binding(bad,self.ids)

    def test_archive_a_is_parsed_and_hashed_from_same_buffer_when_path_changes_to_b(self):
        a=archive_bytes('_EntryA');b=archive_bytes('_EntryB');role='iat_library:lib0'
        pin=m.ROLE_PINS[role];pin['sha256']=m.sha(a);self.data[role]=a
        self.ids[role]['sha256']=m.sha(a);self.ids[role]['size']=len(a)
        (m.ROOT/pin['path']).write_bytes(b)
        parser_path=ROOT/'tools/rebuild/normal_import_archive_bytes_v1.py'
        parser_spec=importlib.util.spec_from_file_location('normal_import_archive_bytes_v1',parser_path)
        parser=importlib.util.module_from_spec(parser_spec);parser_spec.loader.exec_module(parser)
        parser.__loader__=self.finder;sys.modules['normal_import_archive_bytes_v1']=parser
        self.finder.snapshots['normal_import_archive_bytes_v1']=parser_path.read_bytes()
        m.SOURCE_GRAPH['normal_import_archive_bytes_v1']['sha256']=m.sha(self.finder.snapshots['normal_import_archive_bytes_v1'])
        parsed=m._arguments(self.data,self.ids)['iat_inputs']['replay']['parsed']
        self.assertEqual(parsed['archive_sha256'],m.sha(a))
        self.assertEqual(parsed['imports'][0]['symbol'],'_EntryA')
        self.assertNotEqual(parsed['archive_sha256'],m.sha(b))
        with self.assertRaises(ValueError):parser.parse_archive(bytearray(a))
        with self.assertRaises(ValueError):parser.parse_archive(a[:-1])

    def test_actual_transitive_factory_and_parser_are_required(self):
        graph={name:{'path':path,'sha256':'a'*64} for name,path in m.SOURCE_PATHS.items()}
        self.assertIn('application_actual_factory_join_v5',graph)
        self.assertNotIn('application_actual_factory_join_v2',graph)
        for name in ('application_actual_factory_join_v5','normal_import_archive_bytes_v1'):
            bad=copy.deepcopy(graph);bad.pop(name);m.SOURCE_GRAPH=bad
            with self.subTest(missing=name),self.assertRaises(ValueError):m.check_graph(bad)
            bad=copy.deepcopy(graph);bad[name]['path']='tools/rebuild/substitute.py';m.SOURCE_GRAPH=bad
            with self.subTest(substitute=name),self.assertRaises(ValueError):m.check_graph(bad)
        m.SOURCE_GRAPH=graph
        bad=copy.deepcopy(graph);bad['application_actual_factory_join_v5']['sha256']='b'*64
        with self.assertRaises(ValueError):m.check_graph(bad)

    def test_static_import_closure_matches_pinned_paths(self):
        queue=['application_successor_compose_v12','normal_import_archive_bytes_v1',
               'application_import34_diagnostic','import_kernel32_fifteen','iat_code21_annotations']
        observed={}
        while queue:
            name=queue.pop()
            if name in observed:continue
            candidates=[ROOT/'tools/rebuild'/f'{name}.py',ROOT/'tools'/f'{name}.py']
            path=next((p for p in candidates if p.is_file()),None)
            if path is None:continue
            observed[name]=path.relative_to(ROOT).as_posix()
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
                if isinstance(node,ast.Import):queue.extend(alias.name.split('.')[0] for alias in node.names)
                elif isinstance(node,ast.ImportFrom) and node.module:queue.append(node.module.split('.')[0])
                elif isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='import_module' and node.args and isinstance(node.args[0],ast.Constant) and type(node.args[0].value) is str:queue.append(node.args[0].value.split('.')[0])
        self.assertEqual(observed,m.SOURCE_PATHS)

    def test_wrong_role_schema_and_duplicate_json_rejected(self):
        data=copy.deepcopy(self.data);data['semantic']=b'{"members":[],"members":[]}'
        m.ROLE_PINS['semantic']['sha256']=m.sha(data['semantic']);ids=copy.deepcopy(self.ids)
        ids['semantic']['sha256']=m.sha(data['semantic']);ids['semantic']['size']=len(data['semantic'])
        with self.assertRaises(ValueError):m._arguments(data,ids)
    def test_graph_and_peer_gates_fail_closed(self):
        with self.assertRaises(ValueError):m.check_graph({})
        graph={name:{'path':path,'sha256':'a'*64} for name,path in m.SOURCE_PATHS.items()}
        for name,pin in m.SOURCE_GRAPH.items():graph[name]['sha256']=pin['sha256']
        m.SOURCE_GRAPH=graph;m.check_graph(graph)
        with self.assertRaises(ValueError):m.check_graph({k:v for k,v in graph.items() if k!='application_successor_compose_v12'})
        op={'input_bindings':list(self.ids.values()),'phases':[{'name':'compose-v12'}]}
        bad=copy.deepcopy(op);bad['input_bindings'].remove(self.ids['archive'])
        with self.assertRaises(ValueError):m._phase_role_binding(bad,self.ids)
        with self.assertRaises(ValueError):m._prepare_inside_authenticated_session(self.data,self.ids,graph,op)
        m.PEER_SCHEMAS={'caller_says_approved':True}
        with self.assertRaises(RuntimeError):m._prepare_inside_authenticated_session(self.data,self.ids,graph,op)
        with self.assertRaises(RuntimeError):m.run()

if __name__=='__main__':unittest.main()
