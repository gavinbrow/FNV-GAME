import ast
import copy
from pathlib import Path
import sys
import struct
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools/rebuild'),str(ROOT/'tests/rebuild')]
import uuid_directive_projection as projection
import uuid_directive_root_composer as composer
import uuid_directive_occurrence_witness as witness
import coff_code_archive as coff
import root_code_closure as ordinary
from test_ordinary_relocation_projection import authored
from test_coff_code_archive import object_bytes, symbol, aux

def function(path,name):
    mod=ast.parse(path.read_text(encoding='utf8'))
    return next(x for x in mod.body if isinstance(x,ast.FunctionDef) and x.name==name)

class SourceProofTests(unittest.TestCase):
    def test_field_plan_diff_is_exactly_the_reviewed_uuid_delta(self):
        old=function(ROOT/'tools/rebuild/composed_relocation_projection.py','_plan')
        new=function(ROOT/'tools/rebuild/uuid_directive_projection.py','_plan_core')
        # Remove only the explicit UUID list initialization, the exact condition/continue,
        # and the exact count assertion + reporting addition. Compare all other AST nodes.
        new.name='_plan'
        self.assertEqual([x.arg for x in new.args.kwonlyargs],['identity_fn'])
        new.args.kwonlyargs=[];new.args.kw_defaults=[]
        for node in ast.walk(new):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='identity_fn':
                node.func.id='_identity'
        b=new.body
        init=next(x for x in b if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='uuid_legacy' for t in x.targets))
        self.assertEqual(ast.dump(init.value),ast.dump(ast.List(elts=[],ctx=ast.Load())))
        b.remove(init)
        loop=next(x for x in b if isinstance(x,ast.For) and isinstance(x.target,ast.Name) and x.target.id=='blocker')
        branch=loop.body[1]
        expected=ast.parse("if code == 'UNKNOWN_DIRECTIVE_CONTRACT' and e == uuid_witness.TOKENS:\n    uuid_legacy.append(blocker); continue").body[0]
        self.assertEqual(ast.dump(branch),ast.dump(expected));loop.body.remove(branch)
        expected_require=ast.parse("require(len(uuid_legacy)==1, 'exact single UUID legacy directive observation required')").body[0]
        expected_extend=ast.parse('typed_legacy.extend(uuid_legacy)').body[0]
        for expected in (expected_require,expected_extend):
            found=next(x for x in b if ast.dump(x)==ast.dump(expected));b.remove(found)
        self.assertEqual(ast.dump(new,include_attributes=False),ast.dump(old,include_attributes=False))
    def test_exact_legacy_occurrence_and_other_blockers(self):
        fn=function(ROOT/'tools/rebuild/uuid_directive_projection.py','_plan_core')
        init=next(x for x in fn.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='uuid_legacy' for t in x.targets))
        loop=next(x for x in fn.body if isinstance(x,ast.For) and isinstance(x.target,ast.Name) and x.target.id=='blocker')
        req=next(x for x in fn.body if ast.dump(x)==ast.dump(ast.parse("require(len(uuid_legacy)==1, 'exact single UUID legacy directive observation required')").body[0]))
        extend=next(x for x in fn.body if ast.dump(x)==ast.dump(ast.parse('typed_legacy.extend(uuid_legacy)').body[0]))
        unit=ast.Module(body=[copy.deepcopy(init),copy.deepcopy(loop),copy.deepcopy(req),copy.deepcopy(extend)],type_ignores=[])
        code=compile(ast.fix_missing_locations(unit),'<synthetic legacy conjunct>','exec')
        def run(blockers):
            env=dict(assessment={'blockers':blockers},remaining=[],typed_legacy=[],label_indices=set(),primary=set(),
                     obj={'symbols':{}},fields=projection.fields,uuid_witness=projection.uuid_witness,require=projection.require)
            exec(code,env);return env
        exact={'code':'UNKNOWN_DIRECTIVE_CONTRACT','evidence':list(projection.uuid_witness.TOKENS)}
        self.assertEqual(run([exact])['typed_legacy'],[exact])
        for rows in ([],[exact,exact],[{'code':'UNKNOWN_DIRECTIVE_CONTRACT','evidence':list(reversed(exact['evidence']))}]):
            with self.assertRaises(ValueError):run(rows)
        other={'code':'UNSUPPORTED_CODE_SECTION','evidence':'fixture'}
        self.assertEqual(run([exact,other])['remaining'],[other])

    def test_directive_mapping_checks_header_payload_and_bounds(self):
        payload=b'x'*93
        header=struct.pack('<8sIIIIIIHHI',b'.drectve',0,0,93,60,0,0,0,0,0x100a00)
        raw=struct.pack('<HHIIIHH',0x14c,1,0,153,1,0,0)+header+payload
        projection._verify_directive_mapping(raw,{7:1},{'index':7},payload.hex())
        for offset,value in [(20,b'X'),(36,b'\x00'),(40,b'\x01'),(57,b'\x00'),(60,b'y')]:
            damaged=bytearray(raw);damaged[offset:offset+len(value)]=value
            with self.assertRaises(ValueError):projection._verify_directive_mapping(bytes(damaged),{7:1},{'index':7},payload.hex())
        with self.assertRaises(ValueError):projection._verify_directive_mapping(raw,{7:1,8:1},{'index':7},payload.hex())
        with self.assertRaises(ValueError):projection._verify_directive_mapping(raw[:100],{7:1},{'index':7},payload.hex())

    def test_authored_integration_private_core_and_fixed_public_rejection(self):
        raw,contract,_,roots,providers=copy.deepcopy(authored())
        obj=coff.parse(raw);sections=list(obj['sections'].values())
        symbols=[symbol(x['name'],x['section'],x['value'],x['type'],x['storage'],x['aux'])
                 for x in obj['symbols'].values()]
        payload=b' '.join(x.encode() for x in witness.TOKENS);payload+=b' '*(93-len(payload))
        sections[2]['payload']=payload;sections[2]['size']=93
        idx=next(i for i,x in enumerate(symbols) if x[0]=='.drectve')
        symbols[idx]=symbol('.drectve',3,storage=3,auxiliary=aux(93,selection=0))
        raw=object_bytes(sections,symbols);digest=coff.digest(raw)
        contract['provenance']['object_sha256']=digest;roots[0]['object_sha256']=digest
        providers[roots[0]['original_address']]['object_sha256']=digest
        base=ordinary.assess_object(coff.parse(raw),contract);self.assertEqual(len(base['blockers']),3)
        _,vs,va,size,ptr,rp,lp,nr,nl,flags=struct.unpack_from('<8sIIIIIIHHI',raw,100)
        header=dict(index=3,name='.drectve',size=size,flags=flags,virtual_size=vs,virtual_address=va,
            object_size=len(raw),raw_data_offset=ptr,section_count=3,optional_header_size=0,
            relocation_count=nr,relocation_pointer=rp,line_number_count=nl,line_number_pointer=lp)
        path=r'C:\SDK\Lib\uuid.lib';binding=dict(path=path,sha256='1'*64)
        declaration=dict(kind='explicit-normal-sdk-library-dependency-v1',library_name='uuid.lib',
                         absolute_path=path,sha256='1'*64,required_response_token=path)
        review=dict(kind='independent-normal-dependency-declaration-review-v1',status='accepted',
                    declaration_sha256=composer.digest(declaration),reviewer='independent')
        authority=dict(declaration_sha256=composer.digest(declaration),review_sha256=composer.digest(review))
        def authored_proposal(root,contract_,base_,payload_,header_,binding_,authority_):
            self.assertEqual(base_['blockers'],base['blockers']);self.assertEqual(payload_,payload)
            return dict(raw_section_hex=payload_.hex(),proposed_blocker_occurrences=[
                dict(ordinal=i,blocker_id=b['blocker_id'],blocker=b) for i,b in enumerate(base_['blockers'],1)])
        def fake_compose(raw_,contract_,base_,root_,header_,binding_,wa,dec,rev,da,*,policy_id):
            return composer._compose_core(raw_,contract_,base_,root_,header_,binding_,wa,dec,rev,da,
                                          policy_id=policy_id,proposal_fn=authored_proposal)
        w=dict(header=header,binding=binding,witness_authority={},declaration=declaration,
               review=review,declaration_authority=authority)
        composed=fake_compose(raw,contract,base,roots[0],header,binding,{},declaration,review,authority,
                              policy_id=composer.POLICY)
        def identity(*args):
            return projection._identity_core(*args,roots={roots[0]['original_address']:{}},compose_fn=fake_compose)
        def plan(*args):return projection._plan_core(*args,identity_fn=identity)
        args=(raw,contract,base,[w],composed,roots,providers)
        assessment=projection._assess_core(*args,existing_exports=(),policy_id=projection.POLICY,plan_fn=plan)
        self.assertTrue(assessment['eligible']);self.assertEqual(len(assessment['fields']),1)
        self.assertFalse(assessment['runtime_eligible'])
        out,receipt=projection._project_core(*args,existing_exports=(),policy_id=projection.POLICY,plan_fn=plan)
        self.assertEqual(len(coff.exports(out)),1);self.assertEqual(len(receipt['fields']),1)
        self.assertFalse(base['closure_observed']);self.assertFalse(receipt['runtime_eligible'])
        self.assertNotEqual(header['raw_data_offset'],struct.unpack_from('<I',out,20+40*(receipt['maps']['section_map'][3]-1)+20)[0])
        with self.assertRaises(ValueError):
            projection.project_member(*args,existing_exports=(),policy_id=projection.POLICY)

    def test_public_wrappers_bind_only_fixed_private_dependencies(self):
        for name,expected in [('assess_member','_plan'),('project_member','_plan')]:
            fn=function(ROOT/'tools/rebuild/uuid_directive_projection.py',name)
            self.assertNotIn('plan_fn',[x.arg for x in fn.args.kwonlyargs])
            call=next(x for x in ast.walk(fn) if isinstance(x,ast.Call))
            self.assertEqual(ast.dump(next(k.value for k in call.keywords if k.arg=='plan_fn')),ast.dump(ast.Name(id=expected,ctx=ast.Load())))
        for name,kw,expected in [('_identity','roots',"uuid_witness.ROOTS"),('_identity','compose_fn','composer.compose'),('_plan','identity_fn','_identity')]:
            fn=function(ROOT/'tools/rebuild/uuid_directive_projection.py',name)
            self.assertNotIn(kw,[x.arg for x in fn.args.kwonlyargs])
            call=next(x for x in ast.walk(fn) if isinstance(x,ast.Call))
            self.assertEqual(ast.dump(next(k.value for k in call.keywords if k.arg==kw)),
                             ast.dump(ast.parse(expected,mode='eval').body))
        fn=function(ROOT/'tools/rebuild/uuid_directive_root_composer.py','compose')
        self.assertNotIn('proposal_fn',[x.arg for x in fn.args.kwonlyargs])
        call=next(x for x in ast.walk(fn) if isinstance(x,ast.Call))
        self.assertEqual(ast.dump(next(k.value for k in call.keywords if k.arg=='proposal_fn')),
                         ast.dump(ast.Attribute(value=ast.Name(id='witness',ctx=ast.Load()),attr='assess',ctx=ast.Load())))

    def test_projection_rejects_wrong_policy_before_object_read(self):
        with self.assertRaises(ValueError):
            projection._identity(b'x',{}, {}, [], {}, [], {}, [], 'not-authorized')
    def test_full_old_conjuncts_are_not_mutated(self):
        source=(ROOT/'tools/rebuild/uuid_directive_projection.py').read_text(encoding='utf8')
        self.assertNotIn('assessment[\'candidate_eligible\'] =',source)
        self.assertNotIn('assessment[\'blockers\'] =',source)
        self.assertIn("coff.exports(output)==[export]",source)
        self.assertIn("base['retained_physical_slots']",source)

if __name__=='__main__':unittest.main()

