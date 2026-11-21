"""Read-only audit of archived M3 and DV1 overlay ranges against an output PE.

Inputs must be archived from the same positive build; global generated files can
be overwritten by subsequent builds. This checks metadata consistency and PE
bounds, not whether an object was actually spliced or produced matching bytes.
"""
import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

TYPES = {'H': 4, 'I': 4, 'M': 4, 'N': 8, 'J': 4, 'K': 4,
         'F': 2, 'G': 2, 'D': 1, 'E': 1, '_N': 1, 'C': 1}
REWRITTEN = [(0xfdf000, 0xfdf000 + 1188), (0x118062c, 0x118062c + 6688), (0x110147c, 0x110147c + 24)]

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def fail(msg):
    raise ValueError(msg)

def pe_sections(path):
    data = Path(path).read_bytes()
    if data[:2] != b'MZ' or len(data) < 64: fail('not a PE file')
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    if data[pe:pe+4] != b'PE\0\0': fail('bad PE signature')
    machine, count = struct.unpack_from('<HH', data, pe+4)
    optsize = struct.unpack_from('<H', data, pe+20)[0]
    opt = pe+24
    if machine != 0x14c or struct.unpack_from('<H', data, opt)[0] != 0x10b: fail('not PE32 x86')
    base = struct.unpack_from('<I', data, opt+28)[0]
    sections = {}
    for i in range(count):
        off = opt+optsize+40*i
        name = data[off:off+8].split(b'\0',1)[0].decode('ascii')
        vs, va, raw, fp = struct.unpack_from('<IIII', data, off+8)
        if name in sections: fail('duplicate section name '+name)
        if raw and (fp == 0 or fp+raw > len(data)): fail('invalid raw bounds '+name)
        sections[name] = (base+va, base+va+raw, vs)
    if not all(n in sections for n in ('.data','.rdata')): fail('missing data sections')
    return sections

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('exe','selection','manifest','pieces','log'):
        p.add_argument('--'+arg, required=True)
    p.add_argument('--expected-selection-sha256', required=True)
    p.add_argument('--section-metadata', required=True)
    a = p.parse_args()
    selection_bytes = Path(a.selection).read_bytes()
    digest = hashlib.sha256(selection_bytes).hexdigest()
    if digest.lower() != a.expected_selection_sha256.lower(): fail('selection digest mismatch')
    selection = json.loads(selection_bytes.decode('utf-8-sig'))['entries']
    manifest = load(a.manifest)['entries']; pieces = load(a.pieces)['pieces']; log = load(a.log)
    if len(manifest) != len(selection) or log['kept'] != len(selection) or log['dropped']:
        fail('selection, manifest or kept/drop counts disagree')
    def selected_size(e):
        return 4 if e['tc']=='P' else TYPES[e['tc']] if e['tc'] in TYPES else e['size']
    selected = sorted((e['va'],selected_size(e)) for e in selection)
    emitted = sorted((e['va'],e['size']) for e in manifest)
    if selected != emitted: fail('manifest ranges do not exactly match selection')
    sections = pe_sections(a.exe); claims=[]; totals=Counter()
    original = {e['name']: (int(e['va'],16), int(e['raw_end'],16)) for e in load(a.section_metadata)['meta']['sections']}
    for name in ('.data','.rdata','.tls'):
        if name not in original or name not in sections or sections[name][1]-sections[name][0] < original[name][1]-original[name][0]: fail('output PE raw section too small')
    for source, entries in (('m3',manifest),('dv1',pieces)):
        for e in entries:
            start=e['va']; end=start+e['size']; name=e['section']
            if e['size']<=0 or name not in ('.data','.rdata','.tls'): fail('invalid range')
            lo,hi=original[name]
            if not lo<=start<end<=hi: fail('range outside raw PE section')
            if any(x<end and start<y for x,y in REWRITTEN): fail('range intersects recorded builder rewrite')
            claims.append((start,end,source))
            if name in ('.data','.rdata'): totals[source]+=end-start
            totals[source+'_'+name]+=end-start
    claims.sort()
    for left,right in zip(claims,claims[1:]):
        if left[1]>right[0]: fail('overlapping overlay ranges %s %s' % (left,right))
    for sec in ('.data','.rdata'):
        if totals['m3_'+sec] != log['bytes_by_section'].get(sec,0): fail('manifest and generator log section bytes disagree')
    raw_total=sum(original[n][1]-original[n][0] for n in ('.data','.rdata'))
    out={'selection_sha256':digest,'m3_records':len(manifest),'dv1_records':len(pieces),
         'section_raw_bytes':raw_total,'coverage':dict(totals),
         'union_bytes':totals['m3']+totals['dv1'],'remaining_raw_bytes':raw_total-totals['m3']-totals['dv1'],
         'limitations':'Archived range metadata only; no byte or relocation validation and no proof the archived inputs were used for this executable.'}
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()


