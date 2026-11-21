"""Stage/apply the previously verified optional library index reader and provenance.

No selection or generated game source is changed. Apply only after reviewing the
private payload/tests; every target preimage is pinned and the shared lock held.
"""
import argparse,ast,difflib,hashlib,json,os,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[3];RN=R/'runtime-next';P=RN/'m3/out/non-ai-resume-20261120/root-tooling-v2'
sys.path.insert(0,str(RN));import buildlock
H=lambda b:hashlib.sha256(b).hexdigest()
FILES=['runtime-next/data-v2/libsecs.py','runtime-next/m3/config.py','runtime-next/build_all.py','runtime-next/m3/phase2/run_frozen.py','runtime-next/m3/tools/verify_saved_runs.py']
def change(text,old,new):
 if text.count(old)!=1:raise ValueError('unexpected source anchor '+old[:70])
 return text.replace(old,new,1)
def stage():
 if P.exists():raise FileExistsError(P)
 verified=RN/'m3/out/non-ai-integration-20261119'
 suite=json.loads((verified/'suite-acceptance.json').read_bytes())
 if not suite['status'].startswith('PASS complete') or suite['default_promoted']:raise ValueError('missing experimental suite')
 candidate=(verified/'libsecs.candidate').read_bytes()
 if H(candidate)!='d64f17457a8274aead033035deac32fa361a2f6711939703084d4755953ea869':raise ValueError('candidate differs')
 if H((R/FILES[0]).read_bytes())!='09ddeaf9fd8b9809d20f1abf25ac2c78ee6e18b7a6fd04b62a1e03de65988f11':raise ValueError('reader preimage differs')
 originals={p:(R/p).read_bytes() for p in FILES};payload=dict(originals);payload[FILES[0]]=candidate
 t=originals[FILES[1]].decode();t=t.replace('\r\n','\n')
 anchor="    weak = env.get('FNV_COFF_WEAK', '0')\n"
 added="""    index_mode = raw.get('FNV_DV1_LIB_COFF_INDEX_V2') or '0'
    if index_mode not in ('0', '1'):
        raise ValueError('FNV_DV1_LIB_COFF_INDEX_V2 must be 0 or 1')
    if index_mode == '1':
        if env.get('FNV_M3') != '1' or env.get('FNV_M3_DV1') != '1' or skip_data_v1:
            raise ValueError('one-based library mode requires active M3/DV1 and fresh data-v1')
        if not selection or not digest or toggle == '0':
            raise ValueError('one-based library mode requires an explicit compatible library selection and SHA-256')
        if _selection_path(selection) == _selection_path(DEFAULT_LIBRARY_SELECTION):
            raise ValueError('default library selection uses legacy section indices')
"""
 payload[FILES[1]]=change(t,anchor,added+anchor).encode()
 t=originals[FILES[2]].decode().replace('\r\n','\n')
 old="selection_sha256=None, archive_sha256=None, selected=None, bytes=None)\n"
 new="selection_sha256=None, archive_sha256=None, selected=None, bytes=None, section_index_base=1 if env.get('FNV_DV1_LIB_COFF_INDEX_V2') == '1' else 0, reader_sha256=None)\n"
 t=change(t,old,new)
 anchor="if env.get('FNV_COFF_WEAK', '0') == '1':\n"
 added="""try:
    with open(J(RN, 'data-v2', 'libsecs.py'), 'rb') as f:
        summary['provenance']['library_overlay']['reader_sha256'] = hashlib.sha256(f.read()).hexdigest()
except OSError as exc:
    finish('failed', 'cannot hash library section reader: ' + str(exc))
"""
 payload[FILES[2]]=change(t,anchor,added+anchor).encode()
 t=originals[FILES[3]].decode().replace('\r\n','\n')
 payload[FILES[3]]=change(t,"k in ('DV_M3', 'DV3_SKIP')","k in ('DV_M3', 'DV3_SKIP', 'FNV_DV1_LIB_COFF_INDEX_V2')").encode()
 t=originals[FILES[4]].decode().replace('\r\n','\n')
 anchor="    first = active[0]; errors = []\n"
 t=change(t,anchor,anchor+"    index_metadata = any('section_index_base' in c or 'reader_sha256' in c for c in active)\n")
 anchor="        archives=c.get('archive_sha256')\n"
 added="""        if index_metadata:
            if type(c.get('section_index_base')) is not int or c['section_index_base'] not in (0, 1):
                errors.append(label + ': invalid library section index base')
            if not isinstance(c.get('reader_sha256'), str) or re.fullmatch(r'[0-9a-f]{64}', c['reader_sha256']) is None:
                errors.append(label + ': missing or invalid library reader hash')
            if c.get('section_index_base') != first.get('section_index_base') or c.get('reader_sha256') != first.get('reader_sha256'):
                errors.append(label + ': library section reader/index mode mismatch')
"""
 payload[FILES[4]]=change(t,anchor,added+anchor).encode()
 (P/'original').mkdir(parents=True);(P/'payload').mkdir()
 manifest={'status':'staged optional reader/provenance installation; defaults stay legacy','verified_suite_sha256':H((verified/'suite-acceptance.json').read_bytes()),'files':{}}
 patches=[]
 for i,p in enumerate(FILES):
  if p!=FILES[0] and b'\r\n' in originals[p]:payload[p]=payload[p].decode().replace('\r\n','\n').replace('\n','\r\n').encode()
  name=str(i)+'-'+Path(p).name;(P/'original'/name).write_bytes(originals[p]);(P/'payload'/name).write_bytes(payload[p]);ast.parse(payload[p])
  manifest['files'][p]={'artifact':name,'old':H(originals[p]),'new':H(payload[p])}
  patches.extend(difflib.unified_diff(originals[p].decode().splitlines(True),payload[p].decode().splitlines(True),fromfile=p,tofile=p))
 (P/'review.patch').write_text(''.join(patches));(P/'manifest.json').write_text(json.dumps(manifest,indent=2));print(P)
def atomic(p,b):
 fd,name=tempfile.mkstemp(prefix='.library-index-',dir=p.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
  os.replace(name,p)
 finally:
  if os.path.exists(name):os.unlink(name)
def install():
 if sys.flags.optimize:raise RuntimeError('assertions required')
 manifest=json.loads((P/'manifest.json').read_bytes());test=json.loads((P/'tests.json').read_bytes())
 if test.get('status')!='PASS actual reader equivalence and opt-in provenance/options' or test.get('manifest_sha256')!=H((P/'manifest.json').read_bytes()):raise ValueError('tests not accepted for this manifest')
 if (P/'installation.json').exists():raise FileExistsError('already installed')
 if os.environ.get('FNV_BUILD_LOCK'):raise RuntimeError('lock override refused')
 if not buildlock.acquire('install-library-index-optin',wait=0):raise RuntimeError('build lane busy')
 applied=[]
 try:
  if (RN/'direct-v1/harness.lock').exists():raise RuntimeError('gameplay active')
  for p,row in manifest['files'].items():
   if H((R/p).read_bytes())!=row['old'] or H((P/'payload'/row['artifact']).read_bytes())!=row['new']:raise ValueError('source/payload changed '+p)
  for p,row in manifest['files'].items():atomic(R/p,(P/'payload'/row['artifact']).read_bytes());applied.append(p)
  if not all(H((R/p).read_bytes())==row['new'] for p,row in manifest['files'].items()):raise RuntimeError('installation mismatch')
  (P/'installation.json').write_text(json.dumps({'status':'INSTALLED verified opt-in reader plus options/provenance; default mode and selections unchanged','manifest_sha256':H((P/'manifest.json').read_bytes()),'tests_sha256':H((P/'tests.json').read_bytes()),'files':manifest['files']},indent=2))
 except BaseException:
  for p in reversed(applied):
   row=manifest['files'][p]
   if H((R/p).read_bytes())==row['new']:atomic(R/p,(P/'original'/row['artifact']).read_bytes())
  raise
 finally:buildlock.release('install-library-index-optin')
 print('INSTALLED optional library reader; default mode remains0')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['stage','install']);a=ap.parse_args();stage() if a.action=='stage' else install()
