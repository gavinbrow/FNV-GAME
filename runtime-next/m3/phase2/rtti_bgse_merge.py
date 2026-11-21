"""Create a private BGSEncounterZone override+destructor merge hypothesis."""
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;M3=HERE.parent;PROJECT=M3.parent.parent;FN=PROJECT/'fnv_decomp';PRIOR=M3/'out/phase2-bgsencounterzone-overlay';OUT=M3/'out/phase2-bgsencounterzone-combined'
SRC_SHA='30208087bcd67f1183736ce74dfdd8d35afd76fb924eb7c7f9eabe7ea6a031ee';HDR_SHA='4016f5fee6890cfca0035f1d9cfe33f7da34db8f90a38edd2f67a9036c9bf7b1';UNIT_SHA='ae4182c8062cf566210935d284b6663a83ab63e077b41d8e147fa66cb7aca70e'
OVERRIDE_SRC_SHA='3fb70b0fdb9bd9844f6cd437ffc45c6065cd1389b32aba1c130e9230b52ca4df';OVERRIDE_HDR_SHA='d000c5fb3ebed95971f5a83279a4a96c400fc8a4ae955374bb27c682af110c03'
OLD='''struct Base5a
{
    virtual ~Base5a();
};
struct FUN_00525ce0 : Base5a
{
    virtual ~FUN_00525ce0();
};
// @fnv 0x00525ce0
FUN_00525ce0::~FUN_00525ce0()
{}'''
NEW='''// @fnv 0x00525ce0
BGSEncounterZone::~BGSEncounterZone()
{}'''


def sha(data):return hashlib.sha256(data).hexdigest()


def merge_destructor(data):
    if data.count(OLD)!=1:raise ValueError('surrogate destructor block must occur exactly once')
    if re.search(r'\bBGSEncounterZone\s*::\s*~\s*BGSEncounterZone\s*\(',data):raise ValueError('native destructor definition already exists')
    return data.replace(OLD,NEW,1)


def include_closure(path):
    todo=[path];seen={};external=set()
    while todo:
        p=todo.pop().resolve()
        if p in seen:continue
        if not p.is_relative_to(FN.resolve()):raise ValueError('include escapes source tree')
        data=p.read_bytes();seen[p]=sha(data)
        for style,name in re.findall(rb'^\s*#\s*include\s*(["<])([^">\r\n]+)[">]',data,re.M):
            include=name.decode('ascii')
            if style==b'<':external.add(include);continue
            choices=[p.parent/include,FN/'include'/include]
            found=next((x for x in choices if x.is_file()),None)
            if found is None:raise ValueError('unresolved quoted include '+include)
            todo.append(found)
    return [{'path':p.relative_to(FN.resolve()).as_posix(),'sha256':d} for p,d in sorted(seen.items(),key=lambda x:str(x[0]))],sorted(external)


def main():
    src=FN/'src/bgsencounterzone.cpp';hdr=FN/'src/bgsencounterzone_decls.h';up=FN/'build/units.json';pri=json.loads((PRIOR/'manifest.json').read_text());s=src.read_bytes();h=hdr.read_bytes();ub=up.read_bytes();os=(PRIOR/'bgsencounterzone.cpp').read_bytes();oh=(PRIOR/'bgsencounterzone_decls.h').read_bytes()
    if (sha(s),sha(h),sha(ub),sha(os),sha(oh))!=(SRC_SHA,HDR_SHA,UNIT_SHA,OVERRIDE_SRC_SHA,OVERRIDE_HDR_SHA):raise ValueError('input digest mismatch')
    if pri['source_overlay_sha256']!=OVERRIDE_SRC_SHA or pri['header_overlay_sha256']!=OVERRIDE_HDR_SHA:raise ValueError('prior manifest mismatch')
    if len(re.findall(rb'\bclass\s+BGSEncounterZone\s*:\s*public\s+TESForm\b',oh))!=1:raise ValueError('native class header ambiguous')
    merged=merge_destructor(os.decode('utf8')).encode('utf8');units=json.loads(ub)['units'];u=units[2]
    if u['source']!='src/bgsencounterzone.cpp' or u['compiler']!='sp1':raise ValueError('unit recipe mismatch')
    original='??1FUN_00525ce0@@UAE@XZ';native='??1BGSEncounterZone@@UAE@XZ';f=[x for x in u['functions'] if x['address']=='0x00525ce0']
    if len(f)!=1 or f[0]['symbol']!=original or u['symbols'].get('??1Base5a@@UAE@XZ')!='0x00483630':raise ValueError('destructor recipe mapping mismatch')
    sources=[{'unit':i,'source':x['source'],'address':x['symbols']['??1TESForm@@UAE@XZ']} for i,x in enumerate(units) if '??1TESForm@@UAE@XZ' in x.get('symbols',{})]
    if len(sources)!=2 or {x['address'] for x in sources}!={'0x00483630'}:raise ValueError('TESForm destructor alias not unique')
    closure,external=include_closure(src)
    proposal=pri['functions']+[{'address':'0x00525ce0','before':original,'after':native,'size':f[0]['size']}]
    OUT.mkdir(parents=False,exist_ok=False)
    with (OUT/'bgsencounterzone.cpp').open('xb') as f:f.write(merged)
    with (OUT/'bgsencounterzone_decls.h').open('xb') as f:f.write(oh)
    meta={'schema_version':1,'scope':'private exploratory existing-class merge and two override hypotheses; no native ABI or coverage claim',
          'input_sha256':{'source':SRC_SHA,'header':HDR_SHA,'units':UNIT_SHA,'prior_override_source':OVERRIDE_SRC_SHA,'prior_override_header':OVERRIDE_HDR_SHA},
          'unit_index':2,'source':u['source'],'compiler':u['compiler'],'flags':u['flags'],'proposed_function_symbol_changes':proposal,
          'proposed_external_symbol_alias':{'before':'??1Base5a@@UAE@XZ','after':'??1TESForm@@UAE@XZ','address':'0x00483630','independent_unit_evidence':sources},
          'source_overlay_sha256':sha(merged),'header_overlay_sha256':sha(oh),'original_include_closure':closure,'system_includes':external,
          'known_risks':['the same native name has differing definitions in other translation units','base method and virtual slot semantics require full reference checks','no source or units.json is modified','original TD is already DV1-owned; no byte gain claimed'],
          'status':'uncompiled; requires all 24 function and relocations checks, original hierarchy and full slot audit'}
    with (OUT/'manifest.json').open('x',encoding='utf8') as f:json.dump(meta,f,indent=2)
    print(json.dumps({'source_overlay_sha256':meta['source_overlay_sha256'],'header_overlay_sha256':meta['header_overlay_sha256'],'include_closure_count':len(closure),'proposed_function_symbol_changes':len(proposal)}))

if __name__=='__main__':main()
