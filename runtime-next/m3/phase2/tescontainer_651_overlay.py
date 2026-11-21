"""Prepare, but do not install or compile, the unit-651 TESContainer experiment."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;F=M.parent.parent/'fnv_decomp';sys.path.insert(0,str(H));import tescontainer_experiment as pilot
UNIT=651;SRC=F/'src/fallout_shared/bgsloadedreferencecollection.cpp';HDR=F/'include/TESContainer.h';RECIPE=F/'build/units.json';OUT=M/'out/phase2-tescontainer-651'
EXPECTED={'source':'84d6cb550ad8c12f138f4d019ac806cfbd73fdd0004d9dbc9f4ed3a0a619a710','header':'fa04e82ae34b60fbb75e97fc100bd791b7b490a213496b9478c1b07daeeef0f0','units':'e883ac21f25808a7ebba172006e09ae803ae640bf12d389ad2c10641ddba1576'}
OLD='struct TESContainer\n{\n    static bool __cdecl IsValidContainerType(unsigned char type);\n};'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 data={k:p.read_bytes() for k,p in (('source',SRC),('header',HDR),('units',RECIPE))}
 if any(sha(data[k])!=v for k,v in EXPECTED.items()):raise ValueError('input digest changed')
 unit=json.loads(data['units'])['units'][UNIT]
 if unit['source']!='src/fallout_shared/bgsloadedreferencecollection.cpp' or len(unit['functions'])!=4 or '?IsValidContainerType@TESContainer@@SA_NE@Z' not in unit.get('symbols',{}):raise ValueError('recipe changed')
 text=data['source'].decode('utf-8-sig').replace('\r\n','\n')
 if text.count(OLD)!=1:raise ValueError('source shell changed')
 header=data['header'].decode('utf-8-sig')
 if header.count('static bool IsValidContainerType(unsigned char type);')!=1:raise ValueError('canonical static signature changed')
 transformed=text.replace(OLD,'#include "TESContainer.h"',1).encode('utf-8');closure=pilot.closure(SRC)
 OUT.mkdir(exist_ok=False);(OUT/'bgsloadedreferencecollection.cpp').write_bytes(transformed)
 meta={'unit_index':UNIT,'source':unit['source'],'source_sha256':EXPECTED['source'],'units_sha256':EXPECTED['units'],'canonical_header_sha256':EXPECTED['header'],'overlay_sha256':sha(transformed),'original_include_closure':closure,'mapped_functions':[{'address':f['address'],'symbol':f['symbol']} for f in unit['functions']],'source_symbol':'?IsValidContainerType@TESContainer@@SA_NE@Z','classification':'static-method-only hypothesis; no complete class layout equivalence asserted','status':'private uncompiled; compare all emitted code/relocs and all four mapped functions against original and reference; evaluate duplicate type/include side effects'}
 (OUT/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8');print('prepared unit',UNIT,'mapped_functions',len(meta['mapped_functions']),'source and dependency guards',len(closure))
if __name__=='__main__':main()
