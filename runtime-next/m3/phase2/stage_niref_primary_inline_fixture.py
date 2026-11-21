"""Stage private inline NiRef hypothesis after saved out-of-line experiment."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;R=M.parent.parent;F=R/'fnv_decomp';O=M/'out';P=O/'phase2-nimem-next-source-composed';OLD=O/'phase2-niref-primary-owner-fixture';D=O/'phase2-niref-primary-inline-fixture';sys.path.insert(0,str(H));import baseformcomponent_core_stage as core
h=lambda b:hashlib.sha256(b).hexdigest()
def replace_once(text,old,new):
 old=old.replace('\n','\r\n') if '\r\n' in text else old;new=new.replace('\n','\r\n') if '\r\n' in text else new
 if text.count(old)!=1:raise ValueError('ambiguous source anchor')
 return text.replace(old,new,1)
def main():
 if D.exists():raise FileExistsError(D)
 pm=(P/'manifest.json').read_bytes();fm=(OLD/'manifest.json').read_bytes();cmp=(OLD/'lane-comparison.json').read_bytes()
 if h(pm)!='c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53' or h(fm)!='81cc3c7b15fd142f1284d91b16c72dc435e67ba273a340dbc88ca3dfbdc83d53':raise ValueError('frozen fixture changed')
 result=json.loads(cmp);r=result['results']['1503']
 if r['original']['matches']!=11 or r['candidate']['matches']!=10 or [x['address'] for x in r['candidate']['failures']]!=['0x00aa05a0']:raise ValueError('prior failure differs')
 parent=json.loads(pm);ov={k:(P/'payload'/k).read_bytes() for k in parent['source_payload_sha256']}
 for k,v in parent['source_payload_sha256'].items():
  if h(ov[k])!=v:raise ValueError('parent overlay differs')
 for rel in ('src/fallout_shared/animation_decls.h','src/fallout_shared/animation.cpp','src/gamebryo2.2/corelibs/nimain/nishaderfactory.cpp'):
  ov[rel]=(OLD/'overrides'/rel).read_bytes()
 hdr='include/NiRefObject.h';data=(F/hdr).read_bytes()
 if h(data)!='f60c8cf83d4fc0e60ab50a987c096cd9325cfb00c4e1a160ac6e491a561ce2eb':raise ValueError('header differs')
 ov[hdr]=replace_once(data.decode('utf8'),'    virtual ~NiRefObject();','    virtual ~NiRefObject()\n    {\n        NiAtomicSubtract(ms_lObjectCount);\n    }').encode()
 src='src/fallout_shared/animation.cpp';s=ov[src].decode('utf8');s=replace_once(s,'NiRefObject::~NiRefObject()\n{\n    FinishScriptRunLock((void*)&ms_lObjectCount);\n}','');s=replace_once(s,'struct FUN_004968e0_shell : EBase','struct FUN_004968e0_shell : NiRefObject');s=replace_once(s,'    this->EBase::~EBase();','    this->NiRefObject::~NiRefObject();');ov[src]=s.encode()
 units=json.loads((OLD/'units.original').read_bytes())['units'];candidate=(OLD/'units.generated').read_bytes();mirrors={}
 baseline={k:(P/'payload'/k).read_bytes() for k in parent['source_payload_sha256']}
 for i in (612,1503):
  source=units[i]['source'];a=core.walk(F,source,baseline);b=core.walk(F,source,ov);mirrors[str(i)]={'source':source,'flags':units[i]['flags'],'functions':len(units[i]['functions']),'original':a,'candidate':b}
 D.mkdir();(D/'units.original').write_bytes((OLD/'units.original').read_bytes());(D/'units.generated').write_bytes(candidate)
 for rel in (hdr,src,'src/fallout_shared/animation_decls.h','src/gamebryo2.2/corelibs/nimain/nishaderfactory.cpp'):
  q=D/'overrides'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(ov[rel])
 for i,z in mirrors.items():
  for tag,overrides in (('original',baseline),('candidate',ov)):
   for rel,digest in z[tag]['files'].items():
    b=overrides[rel] if rel in overrides else (F/rel).read_bytes()
    if h(b)!=digest:raise ValueError('closure changed')
    q=D/i/tag/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
  q=D/i/'mirror-manifest.json';q.write_text(json.dumps({'unit':int(i),'source':z['source'],'flags':z['flags'],'original':z['original'],'candidate':z['candidate'],'parent_manifest_sha256':h(pm),'prior_fixture_sha256':h(fm)},indent=2))
 out={'status':'private uncompiled inline hypothesis; no dummy emission or forced alias','parent_manifest_sha256':h(pm),'prior_fixture_manifest_sha256':h(fm),'prior_comparison_sha256':h(cmp),'recipe_original_sha256':h((D/'units.original').read_bytes()),'recipe_candidate_sha256':h(candidate),'modified_source_sha256':{k:h(ov[k]) for k in (hdr,src,'src/fallout_shared/animation_decls.h','src/gamebryo2.2/corelibs/nimain/nishaderfactory.cpp')},'mirrors':mirrors,'failure_trigger':'unit1503 destructor at 0x00aa05a0: 277-byte inline body became 269-byte tail call','limits':['612 native G/dtor emission not established; absence is a failed hypothesis','original source use is explicitly typed as NiRefObject in a private surrogate; native ownership is not assumed','inline helper code under /Od may emit different call shape; no noinline or reference-only alias','public header affects at least 118 known recipe closures; actual full cohort revalidation required','unit2725 physical 18-byte optimized owner remains untouched','no compiler, installation, final provider or runtime proof']}
 (D/'manifest.json').write_text(json.dumps(out,indent=2));print(json.dumps({'manifest_sha256':h((D/'manifest.json').read_bytes()),'recipe_sha256':h(candidate),'closure':{k:[len(v['original']['files']),len(v['candidate']['files'])] for k,v in mirrors.items()}}))
if __name__=='__main__':main()
