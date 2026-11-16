#!/usr/bin/env python3
"""Read-only triage of the V81 LINK output. Writes only into its own directory.

Usage: python -I triage.py   (no arguments; paths are pinned below)
Outputs: unresolved.csv, summary.json (same directory as this script)
"""
import bisect, collections, csv, gzip, hashlib, json, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = r'C:\Projects\Decompilation\fnv_decomp\build'
STDOUT = R + r'\rebuild\v81-inventory-lookup-control-20261114-v1\stdout.log'
RSP = R + r'\rebuild\v81-inventory-lookup-response-plan-v1\link.rsp'
UNITS = R + r'\units.json'
POOL = R + r'\rebuild\bulk-code-pool-all-current-v1\production'
EXE = r'C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\FalloutNV.exe'
IMAGECHECK = R + r'\image_check.json'

# ---------------------------------------------------------------- PE
class PE:
    def __init__(s, path):
        s.d = open(path, 'rb').read()
        d = s.d
        pe = struct.unpack_from('<I', d, 0x3c)[0]
        assert d[pe:pe+4] == b'PE\0\0'
        (s.machine, s.nsec, _, _, _, s.optsz, s.chars) = struct.unpack_from('<HHIIIHH', d, pe+4)
        o = pe + 24
        s.magic = struct.unpack_from('<H', d, o)[0]
        s.entry = struct.unpack_from('<I', d, o+16)[0]
        s.imagebase = struct.unpack_from('<I', d, o+28)[0]
        s.secalign, s.filealign = struct.unpack_from('<II', d, o+32)
        s.sizeofimage = struct.unpack_from('<I', d, o+56)[0]
        s.dllchars = struct.unpack_from('<H', d, o+70)[0]
        nd = struct.unpack_from('<I', d, o+92)[0]
        s.dd = [struct.unpack_from('<II', d, o+96+8*i) for i in range(nd)]
        so = o + s.optsz
        s.secs = []
        for i in range(s.nsec):
            nm, vs, va, rs, rp = struct.unpack_from('<8sIIII', d, so+40*i)
            fl = struct.unpack_from('<I', d, so+40*i+36)[0]
            s.secs.append((nm.rstrip(b'\0').decode('latin1'), s.imagebase+va, vs, rp, rs, fl))
    def sec_of(s, va):
        for nm, a, vs, rp, rs, fl in s.secs:
            if a <= va < a + max(vs, 1):
                return nm
        return None
    def read(s, va, n):
        for nm, a, vs, rp, rs, fl in s.secs:
            if a <= va < a + vs:
                off = rp + va - a
                return s.d[off:off+n]
        raise ValueError
    def imports(s):
        """returns (iat_ranges, {slot_va: 'dll!name'})"""
        rva, sz = s.dd[1] if len(s.dd) > 1 else (0, 0)
        slots = {}
        if not rva:
            return slots
        def rd(va, n): return s.read(s.imagebase+va, n)
        def cstr(va):
            b = b''
            while True:
                c = rd(va+len(b), 64); i = c.find(b'\0')
                if i >= 0: return (b+c[:i]).decode('latin1')
                b += c
        p = rva
        while True:
            ot, _, _, nm, ft = struct.unpack('<IIIII', rd(p, 20))
            if not (ot or nm or ft): break
            dll = cstr(nm); t = ot or ft; k = 0
            while True:
                v = struct.unpack('<I', rd(t+4*k, 4))[0]
                if not v: break
                fn = ('#%d' % (v & 0xffff)) if v & 0x80000000 else cstr((v & 0x7fffffff)+2)
                slots[s.imagebase+ft+4*k] = dll + '!' + fn
                k += 1
            p += 20
        return slots

def reloc_stats(pe):
    rva, sz = pe.dd[5]
    d = pe.read(pe.imagebase+rva, sz) if sz else b''
    p = 0; by = collections.Counter(); ptr_to_text = collections.Counter(); n = 0; types = collections.Counter()
    text = [x for x in pe.secs if x[0] == '.text'][0]
    while p + 8 <= len(d):
        page, bs = struct.unpack_from('<II', d, p)
        if bs < 8: break
        for k in range((bs-8)//2):
            v = struct.unpack_from('<H', d, p+8+2*k)[0]; t = v >> 12; off = v & 0xfff
            types[t] += 1
            if t == 3:
                va = pe.imagebase + page + off; sec = pe.sec_of(va) or 'outside'; by[sec] += 1; n += 1
                try:
                    val = struct.unpack('<I', pe.read(va, 4))[0]
                    if text[1] <= val < text[1]+text[2]: ptr_to_text[sec] += 1
                except Exception: pass
        p += bs
    return dict(highlow=n, by_section=dict(by), highlow_values_pointing_into_text_by_section=dict(ptr_to_text), types=dict(types))

# ---------------------------------------------------------------- log parse
LOGRE = re.compile(r'^(?P<obj>.+?) : error LNK(?P<code>2019|2001): unresolved external symbol (?P<rest>.*)$')
def split_sym(rest):
    """returns (raw_decorated, undecorated or '', referenced_in or '')"""
    ref = ''
    m = re.search(r' referenced in function (.*)$', rest)
    if m:
        ref = m.group(1); rest = rest[:m.start()]
    und = ''
    if rest.startswith('"'):
        i = rest.rfind('" (')
        und = rest[1:i]; raw = rest[i+3:-1]
    else:
        raw = rest.strip()
    return raw, und, ref

def parse_log():
    refs = collections.OrderedDict(); und = {}
    nrec = 0
    for line in open(STDOUT, encoding='latin1'):
        m = LOGRE.match(line.rstrip('\r\n'))
        if not m: continue
        raw, u, ref = split_sym(m.group('rest'))
        nrec += 1
        refs.setdefault(raw, []).append((m.group('obj'), ref))
        if u: und[raw] = u
    return refs, und, nrec

# ---------------------------------------------------------------- link inputs / defined symbols
def parse_rsp():
    objs, libs, alts = [], [], {}
    for line in open(RSP, encoding='latin1'):
        t = line.strip().strip('"')
        if t.startswith('/ALTERNATENAME:'):
            a, b = t[len('/ALTERNATENAME:'):].split('=', 1); alts[a] = b
        elif t.lower().endswith('.lib'): libs.append(t)
        elif t.lower().endswith('.obj'): objs.append(t)
    return objs, libs, alts

def lib_symbols(path):
    d = open(path, 'rb').read()
    if d[:8] != b'!<arch>\n': return set()
    p = 8; hdr = d[p:p+60]; size = int(hdr[48:58]); body = d[p+60:p+60+size]
    if hdr[:2] != b'/ ': return set()
    n = struct.unpack_from('>I', body, 0)[0]
    strs = body[4+4*n:]
    return {x.decode('latin1') for x in strs.split(b'\0')[:n]}

def obj_symbols(path):
    """(defined_external, undefined_external) from a COFF object"""
    d = open(path, 'rb').read()
    mach, nsec, ts, symp, nsym = struct.unpack_from('<HHIII', d, 0)
    if mach != 0x14c: return set(), set()
    stro = symp + 18*nsym; defs, undefs = set(), set(); i = 0
    while i < nsym:
        e = d[symp+18*i:symp+18*i+18]
        nm = e[:8]
        if nm[:4] == b'\0\0\0\0':
            off = struct.unpack('<I', nm[4:])[0]; end = d.index(b'\0', stro+off); name = d[stro+off:end].decode('latin1')
        else: name = nm.rstrip(b'\0').decode('latin1')
        val, sec, typ, sc, aux = struct.unpack('<IhHBB', e[8:])
        if sc == 2:
            (undefs if sec == 0 and val == 0 else defs).add(name)
        i += 1 + aux
    return defs, undefs

# ---------------------------------------------------------------- hash identity maps
def load_pool_identity():
    """canonical name -> dict(original_base, role, classification, import_id). Also pool exports/undefined."""
    ident = {}; exports = set(); undefs = set(); members = 0
    export_addr = {}
    with gzip.open(POOL + r'\unions.jsonl.gz', 'rt') as g:
        for line in g:
            r = json.loads(line)
            if r.get('event') != 'EMITTED_RECIPE_UNION': continue
            members += 1
            rc = r['receipt']
            for o in rc['plan']['obligations']:
                ident.setdefault(o['canonical_name'], dict(original_base=o['original_base'], role=o['role'],
                                 classification=o['classification'], import_id=o['import_id']))
            exports.update(r['member']['exports'])
            for c in rc['after_comparison']:
                export_addr[c['symbol']] = c['address']
            undefs.update(rc['undefined'])
    return ident, exports, undefs, members, export_addr

def load_coverage():
    cov = {}
    with gzip.open(POOL + r'\coverage.jsonl.gz', 'rt') as g:
        for line in g:
            r = json.loads(line)
            pid = r['physical_identity']
            nm = '_fnv_code_' + hashlib.sha256(json.dumps(pid, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            cov[nm] = (r['original_address'], r['status'])
    return cov

def undef_name(base, role):
    return '_fnv_undefined_' + hashlib.sha256(json.dumps(dict(original_base=base, role=role), sort_keys=True,
                                                         separators=(',', ':')).encode()).hexdigest()

# ---------------------------------------------------------------- main
def main():
    pe = PE(EXE)
    chk = json.load(open(IMAGECHECK)); ok = 0
    for a, n, h in chk['probes']:
        try: ok += hashlib.sha256(pe.read(int(a, 16), n)).hexdigest() == h
        except Exception: pass
    iat = pe.imports()
    iat_lo, iat_hi = (min(iat), max(iat)+4) if iat else (0, 0)

    units = json.load(open(UNITS))['units']
    fstart = {}; fsyms = {}
    for ui, u in enumerate(units):
        for f in u['functions']:
            a = int(f['address'], 16); fstart[a] = (f['size'], ui, f['symbol'])
    starts = sorted(fstart)
    sym_addr = collections.defaultdict(set)
    for u in units:
        for n, a in u.get('symbols', {}).items(): sym_addr[n].add(int(a, 16))

    refs, und, nrec = parse_log()
    objs, libs, alts = parse_rsp()
    ident, pool_exports, pool_undefs, nmem, export_addr = load_pool_identity()
    cov = load_coverage()
    selfcheck = sum(1 for n in pool_exports if n in cov)

    # defined external symbol index over linked inputs
    defined = set();
    for l in libs:
        if os.path.exists(l): defined |= lib_symbols(l)
    for o in objs:
        if os.path.exists(o): defined |= obj_symbols(o)[0]
    key = lambda n: n[:n.index('@@')] if n.startswith('?') and '@@' in n else n
    dkey = collections.defaultdict(list)
    for n in defined:
        if n.startswith('?'): dkey[key(n)].append(n)

    # brute-force reverse of unmapped _fnv_undefined hashes: sha256(canonical json(original_base, role))
    want = {n[len('_fnv_undefined_'):]: n for n in refs if n.startswith('_fnv_undefined_') and n not in ident}
    brute = {}
    lo = min(x[1] for x in pe.secs if x[0] == '.text'); hi = max(x[1]+x[2] for x in pe.secs if x[0] in ('.tls', 'CONST'))
    for role in ('data', 'iat-cell', 'code'):
        pre = '{"original_base":"0x'; suf = '","role":"%s"}' % role
        for a in range(lo, hi):
            h = hashlib.sha256(('%s%08x%s' % (pre, a, suf)).encode()).hexdigest()
            if h in want: brute[want[h]] = (a, role)
    for n, (a, role) in brute.items():
        ident[n] = dict(original_base='0x%08x' % a, role=role, classification='brute-force-sha256', import_id=None)
    funaddr = collections.defaultdict(list)
    first = collections.defaultdict(list)
    for n in defined:
        if n.startswith('?'):
            for m in re.finditer(r'FUN_([0-9a-f]{8})', n): funaddr[m.group(1)].append(n)
            first[n[1:].split('@')[0]].append(n)
    rows = []
    for raw, rl in refs.items():
        fam = ('fnv_code' if raw.startswith('_fnv_code_') else 'fnv_undefined' if raw.startswith('_fnv_undefined_')
               else 'cpp-FUN' if re.search(r'FUN_[0-9a-f]{8}', raw) else 'cpp-DAT' if re.search(r'DAT_[0-9a-f]{8}', raw)
               else 'cpp-other' if raw.startswith('?') else 'other')
        addr = None; asrc = ''; role = ''; note = ''
        if fam in ('fnv_code', 'fnv_undefined'):
            i = ident.get(raw)
            if i:
                addr = int(i['original_base'], 16); asrc = 'pool-obligation'; role = i['role']; note = i['classification']
            elif raw in cov:
                addr = int(cov[raw][0], 16); asrc = 'pool-coverage'; role = 'code'
        else:
            m = re.search(r'(?:FUN|DAT)_([0-9a-f]{8})', raw)
            if m: addr = int(m.group(1), 16); asrc = 'name'
            elif raw in sym_addr and len(sym_addr[raw]) == 1:
                addr = next(iter(sym_addr[raw])); asrc = 'units.symbols'
            elif raw in sym_addr:
                note = 'multi-address:' + ','.join('0x%08x' % a for a in sorted(sym_addr[raw])[:4]); asrc = 'units.symbols(ambiguous)'
            m2 = re.match(r'__imp__(.+?)(@\d+)?$', raw)
        # address class
        cls = 'no-address'; sec = ''; rf = ''
        if addr is not None:
            sec = pe.sec_of(addr) or 'outside-image'
            if iat_lo <= addr < iat_hi and addr in iat:
                cls = 'iat-slot'; rf = iat[addr]
            elif addr in fstart:
                cls = 'recipe-function-start'; rf = fstart[addr][2]
            else:
                j = bisect.bisect_right(starts, addr) - 1
                if j >= 0 and starts[j] <= addr < starts[j] + fstart[starts[j]][0]:
                    cls = 'recipe-function-interior'; rf = fstart[starts[j]][2] + '+0x%x' % (addr - starts[j])
                elif sec == '.text': cls = 'code-not-in-recipe'
                else: cls = 'data-not-in-recipe'
        # decoration mismatch
        variants = []; loose = []; weak = []
        if raw.startswith('?'):
            variants = [v for v in dkey.get(key(raw), []) if v != raw]
        loose = []
        if raw.startswith('?'):
            m = re.search(r'FUN_([0-9a-f]{8})', raw)
            if m: loose = [v for v in funaddr.get(m.group(1), []) if v != raw]
            fn = raw[1:].split('@')[0]
            weak = [v for v in first.get(fn, []) if v != raw] if not fn.startswith('?') or True else []
        alt = alts.get(raw, ''); altdef = ''
        if alt: altdef = 'yes' if alt in defined else 'no'
        # bucket
        if variants or loose: bucket = 'decoration-mismatch'
        elif cls == 'recipe-function-start': bucket = 'bind-to-matched-code-by-address'
        elif cls == 'recipe-function-interior': bucket = 'code-interior-of-matched-function'
        elif cls == 'iat-slot': bucket = 'bind-to-import-slot'
        elif cls == 'data-not-in-recipe': bucket = 'bind-to-original-data-by-address'
        elif cls == 'code-not-in-recipe': bucket = 'code-address-not-in-any-recipe'
        else: bucket = 'unresolvable-no-address'
        rows.append(dict(raw_name=raw, undecorated=und.get(raw, ''), family=fam, ref_count=len(rl),
                         ref_first3=' || '.join('%s @ %s' % (o, f) for o, f in rl[:3]),
                         embedded_or_mapped_address=('0x%08x' % addr) if addr is not None else '', address_source=asrc,
                         role=role, pe_section=sec, address_class=cls, recipe_function_or_import=rf,
                         decoration_variants_defined=' | '.join(variants[:3]), same_FUN_address_other_decoration_defined=' | '.join(loose[:3]), same_first_segment_defined_count=len(weak) if raw.startswith('?') else 0, alternatename=alt, alternatename_target_defined=altdef,
                         bucket=bucket, note=note))
    rows.sort(key=lambda r: (r['family'], r['raw_name']))
    with open(os.path.join(HERE, 'unresolved.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    # ---- pool frontier (names the whole pool references but nothing in the pool defines)
    front = pool_undefs - pool_exports
    fam_of = lambda n: 'fnv_code' if n.startswith('_fnv_code_') else 'fnv_undefined' if n.startswith('_fnv_undefined_') else 'other'
    # ---- unit-graph closure from the code-bindable unresolved names
    owner = {}
    for ui, u in enumerate(units):
        for f in u['functions']: owner[int(f['address'], 16)] = ui
    seeds = set()
    for r in rows:
        if r['bucket'] == 'bind-to-matched-code-by-address':
            seeds.add(owner[int(r['embedded_or_mapped_address'], 16)])
    seen = set(seeds); stack = list(seeds); ext = collections.Counter(); extaddr = set()
    while stack:
        ui = stack.pop(); u = units[ui]
        own = {int(f['address'], 16) for f in u['functions']}
        for n, a in u.get('symbols', {}).items():
            a = int(a, 16)
            if a in own: continue
            if a in owner:
                if owner[a] not in seen: seen.add(owner[a]); stack.append(owner[a])
            else:
                extaddr.add(a)
    ext_cls = collections.Counter()
    for a in extaddr:
        if a in iat: ext_cls['iat-slot'] += 1
        elif (pe.sec_of(a) or '') == '.text': ext_cls['code-not-in-recipe'] += 1
        else: ext_cls['data/other:' + (pe.sec_of(a) or 'outside')] += 1

    cnt = collections.Counter((r['family'], r['bucket']) for r in rows)
    summ = dict(
        parsed_records=nrec, distinct=len(rows), equals_1512=len(rows) == 1512,
        family_totals=collections.Counter(r['family'] for r in rows),
        family_x_bucket={'%s | %s' % k: v for k, v in sorted(cnt.items())},
        family_x_section=dict(collections.Counter('%s | %s' % (r['family'], r['pe_section'] or 'none') for r in rows)),
        address_source=dict(collections.Counter(r['address_source'] or 'none' for r in rows)),
        alternatename_present=sum(1 for r in rows if r['alternatename']),
        alternatename_target_defined=sum(1 for r in rows if r['alternatename_target_defined'] == 'yes'),
        pe=dict(sha256=hashlib.sha256(pe.d).hexdigest(), relocs=reloc_stats(pe), brute_resolved=len(brute), imagebase=hex(pe.imagebase), entry=hex(pe.imagebase+pe.entry), dllcharacteristics=hex(pe.dllchars), file_characteristics=hex(pe.chars),
                reloc_dir_rva_size=pe.dd[5], reloc_stripped_flag=bool(pe.chars & 1), sections=[(s[0], hex(s[1]), hex(s[2]), hex(s[5])) for s in pe.secs],
                iat_slots=len(iat), iat_range=(hex(iat_lo), hex(iat_hi)), image_probe_ok='%d/%d' % (ok, len(chk['probes'])), size=len(pe.d)),
        link_inputs=dict(objs=len(objs), libs=len(libs), alternatenames=len(alts), defined_external_symbols=len(defined)),
        pool=dict(members=nmem, exports=len(pool_exports), refs_undefined=len(pool_undefs), frontier=len(front),
                  frontier_by_family=dict(collections.Counter(fam_of(n) for n in front)), identity_names=len(ident), selfcheck_code_hash_matches=selfcheck, of=len(pool_exports)),
        closure=dict(seed_units=len(seeds), reachable_units=len(seen), total_units=len(units), external_addresses_without_function_owner=len(extaddr), by_class=dict(ext_cls)),
        recipe_functions=len(fstart))
    json.dump(summ, open(os.path.join(HERE, 'summary.json'), 'w'), indent=1, default=dict)
    print(json.dumps(summ, indent=1, default=dict))

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
