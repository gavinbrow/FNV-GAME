import copy
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('prepare_fixture',ROOT/'tools/rebuild/application_successor_prepare_v1.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def enc(obj):return json.dumps(obj,separators=(',',':')).encode()

class Tests(unittest.TestCase):
    def setUp(self):
        self.old=(m.ROLE_PINS,m.SOURCE_GRAPH,m.PEER_SCHEMAS);self.addCleanup(self.restore)
        data={r:b'evidence' for r in m.CORE_ROLES};data['member:a.obj']=b'member';data['archive']=b'archive'
        data['semantic']=enc({'wrappers':[],'members':[{'name':'a.obj'}],'handoff':{},'member_count':1,'field_count':0,
          'namespace_by_member':{},'expected_providers':[],'expected_fields':[],'component':'fixture','selected_providers':{}})
        data['factory']=enc({'selections':[],'outcomes':[],'emitted':[]})
        data['iat']=enc({'full_proofs':{},'replay':{}});data['crt']=enc({'bindings':[],'source_evidence':{},'prior_crt':[]})
        data['response']=enc({'old_out':'old','new_out':'new','inherited_aliases':[],
                              'fresh_uuid_identity':{},'qualified_uuid':{}})
        self.data=data
        m.ROLE_PINS={k:{'path':'C:/fixture/'+k.replace(':','_'),'sha256':m.sha(v)} for k,v in data.items()}
        self.ids={k:{'requested_path':pin['path'],'path':pin['path'],'sha256':pin['sha256'],
                     'size':len(data[k]),'device':1,'inode':i+1} for i,(k,pin) in enumerate(m.ROLE_PINS.items())}
    def restore(self):m.ROLE_PINS,m.SOURCE_GRAPH,m.PEER_SCHEMAS=self.old
    def test_exact_role_wiring_and_archive_phase_identity(self):
        args=m._arguments(self.data,self.ids)
        self.assertEqual(args['archive_bytes'],b'archive');self.assertEqual(args['archive_identity'],self.ids['archive'])
        self.assertEqual(args['response_inputs']['new_archive'],self.ids['archive']['path'])
        self.assertEqual(args['semantic_inputs']['member_bytes'],{'a.obj':b'member'})
        self.assertEqual(args['factory_inputs']['member_bytes'],args['semantic_inputs']['member_bytes'])
        called=[];fake=types.ModuleType('application_successor_compose_v11')
        fake.compose=lambda **kw:called.append(kw) or {'link_approved':False}
        previous=sys.modules.get(fake.__name__);sys.modules[fake.__name__]=fake
        try:self.assertEqual(m._compose_v11_untrusted_fixture(self.data,self.ids),{'link_approved':False})
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
        ids=copy.deepcopy(self.ids);ids['archive']['path']='C:/other.lib'
        with self.assertRaises(ValueError):m._arguments(self.data,ids)
        ids=copy.deepcopy(self.ids);ids['archive']['inode']=True
        with self.assertRaises(ValueError):m._arguments(self.data,ids)
        data=copy.deepcopy(self.data);data['member:a.obj']=b'other'
        with self.assertRaises(ValueError):m._arguments(data,self.ids)
    def test_wrong_role_schema_and_duplicate_json_rejected(self):
        data=copy.deepcopy(self.data);data['semantic']=b'{"members":[],"members":[]}'
        m.ROLE_PINS['semantic']['sha256']=m.sha(data['semantic']);ids=copy.deepcopy(self.ids)
        ids['semantic']['sha256']=m.sha(data['semantic']);ids['semantic']['size']=len(data['semantic'])
        with self.assertRaises(ValueError):m._arguments(data,ids)
    def test_graph_and_peer_gates_fail_closed(self):
        with self.assertRaises(ValueError):m.check_graph({})
        graph={name:{'path':'tools/'+name+'.py','sha256':'a'*64} for name in m.REQUIRED_SOURCES}
        m.SOURCE_GRAPH=graph;m.check_graph(graph)
        with self.assertRaises(ValueError):m.check_graph({k:v for k,v in graph.items() if k!='application_successor_compose_v11'})
        op={'input_bindings':list(self.ids.values()),'phases':[{'name':'compose-v11'}]}
        bad=copy.deepcopy(op);bad['input_bindings'].remove(self.ids['archive'])
        with self.assertRaises(ValueError):m._phase_archive_binding(bad,self.ids)
        with self.assertRaises(ValueError):m._prepare_inside_authenticated_session(self.data,self.ids,graph,op)
        m.PEER_SCHEMAS={'caller_says_approved':True}
        with self.assertRaises(RuntimeError):m._prepare_inside_authenticated_session(self.data,self.ids,graph,op)
        with self.assertRaises(RuntimeError):m.run()

if __name__=='__main__':unittest.main()
