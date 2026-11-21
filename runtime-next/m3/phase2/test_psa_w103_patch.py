"""Private focused regression tests for W103 targeted control patch."""
import contextlib,hashlib,importlib.util,io,json,os,tempfile,unittest
from pathlib import Path
M=Path(__file__).resolve().parent.parent;P=M/'out/phase2-psa-w103-control-patch/payload/runtime-next/m3';D=M/'out/phase2-psa-metadata-ownership-proposal/compiled-selector-replay-v3/dv1_pieces.json'
spec=importlib.util.spec_from_file_location('psa_staged_splice',P/'splice.py');splice=importlib.util.module_from_spec(spec);spec.loader.exec_module(splice)
class Controls(unittest.TestCase):
 def setUp(self):self.old=os.environ.pop('FNV_M3_NEGCTL',None);self.sha=hashlib.sha256(D.read_bytes()).hexdigest()
 def tearDown(self):
  if self.old is None:os.environ.pop('FNV_M3_NEGCTL',None)
  else:os.environ['FNV_M3_NEGCTL']=self.old
  self.assertEqual(self.sha,hashlib.sha256(D.read_bytes()).hexdigest())
 def test_exact_control_effects(self):
  base=splice.load_dv1(str(D))
  for mode,va in [('p2rv',0x1196e20),('p2rp',0x110fbe8)]:
   os.environ['FNV_M3_NEGCTL']=mode
   with contextlib.redirect_stdout(io.StringIO()) as text:after=splice.load_dv1(str(D))
   changed=[(a,b) for a,b in zip(base,after) if a!=b];self.assertEqual(len(changed),1);self.assertEqual(changed[0][0]['va'],va);self.assertIn('NEGATIVE CONTROL',text.getvalue())
   if mode=='p2rv':self.assertEqual(changed[0][0]['data'][8]^changed[0][1]['data'][8],1);self.assertEqual(changed[0][0]['relocs'],changed[0][1]['relocs'])
   else:self.assertEqual(changed[0][0]['data'],changed[0][1]['data']);self.assertEqual(changed[0][1]['reloc_va'][0],0x11831e8)
 def test_saved_checker_labels_and_rejects_wrong_id(self):
  checker=P/'tools/verify_saved_runs.py';spec=importlib.util.spec_from_file_location('psa_candidate_checker',checker);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'gen').write_text('');summary={'steps':[{'name':'m3-gen','log':'gen'},{'name':'data-v3','log':'verify'}],'provenance':{'m3_config':{}}}
   for mode,kind,diag in [('p2rv','value',' DIFFERENT relocs '),('p2rp','pointer','M3 RELOC VALUE MISMATCH')]:
    line=('NEGATIVE CONTROL (p2 PSA value): VA 01196e20 offset 8 changed from 2e to 2f' if kind=='value' else 'NEGATIVE CONTROL (p2 PSA pointer): VA 0110fbe8 offset 12 changed from 01196e20 to 011831e8');suffix='\nROUND TRIP FAILED\nnegative control: failure is expected\n'+diag;(root/'verify').write_text(line+suffix);summary['provenance']['m3_config']['negative_control']=mode;self.assertEqual(mod.check_control_logs(root/'s.json',summary),kind)
    for altered in (line.replace('VA 01','VA 02'),line.replace(' to ',' to 0'),line.replace(' from ',' from 0')):
     (root/'verify').write_text(altered+suffix)
     with self.assertRaises(ValueError):mod.check_control_logs(root/'s.json',summary)
    (root/'verify').write_text(line+suffix);summary['provenance']['m3_config'].pop('negative_control')
    with self.assertRaises(ValueError):mod.check_control_logs(root/'s.json',summary)
    summary['provenance']['m3_config']['negative_control']='wrong'
    with self.assertRaises(ValueError):mod.check_control_logs(root/'s.json',summary)
 def test_wrong_producer_size_content_and_duplicate_fail(self):
  doc=json.loads(D.read_bytes())
  cases=[('p2rv',0x1196e20,'unit',621),('p2rv',0x1196e20,'size',25),('p2rv',0x1196e20,'data','00'*26),('p2rp',0x11831e8,'unit',251),('p2rp',0x11831e8,'data','00'*23)]
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'pieces.json'
   for mode,va,key,value in cases:
    changed=json.loads(json.dumps(doc));next(x for x in changed['pieces'] if x['va']==va)[key]=value;p.write_text(json.dumps(changed));os.environ['FNV_M3_NEGCTL']=mode
    with self.assertRaises(ValueError):splice.load_dv1(str(p))
   changed=json.loads(json.dumps(doc));changed['pieces'].append(next(x for x in changed['pieces'] if x['va']==0x110fbe8));p.write_text(json.dumps(changed));os.environ['FNV_M3_NEGCTL']='p2rp'
   with self.assertRaises(ValueError):splice.load_dv1(str(p))
 def test_missing_piece_fails(self):
  for mode in ('p2rv','p2rp'):
   os.environ['FNV_M3_NEGCTL']=mode
   with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'empty.json';p.write_text('{"pieces":[]}')
    with self.assertRaises(ValueError):splice.load_dv1(str(p))
if __name__=='__main__':unittest.main()
