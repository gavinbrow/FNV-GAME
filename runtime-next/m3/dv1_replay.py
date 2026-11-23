r"""Batch 10 step C: data-v1 piece selection WITHOUT the reference image (opt-in FNV_M3_DV1_REPLAY=<replay.json>, written by dv1_splice.py with FNV_M3_DV1_FREEZE=<path>).
The replay file freezes, per accepted piece, only its identity (sha256 of the data-v1 section key: unit/section/definitions/content of our compiled object), its VA, tier, kind, chunk
and target VAs.  The bytes always come from OUR compiled objects (the data-v1 state), never from the reference; every piece is checked against its frozen content hash and its
relocations are re-resolved by data-v1 and compared with the frozen targets, so a changed compile, a changed placement or a changed resolution fails loudly.
Outputs (m3\gen): dv1_pieces.json (must reproduce the normal run byte for byte: sha256 pinned in the replay file), dv1_skip_ranges.json, skip_ranges_b5.json, dv1_log.json,
rtti-name-field-proof.json (RTTI literal mode; reference hash field is null: the three pinned descriptors were validated at freeze time)."""
import os, sys, json, struct, collections, pickle, hashlib, re, bisect
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation'
RN = os.path.join(PROJ, 'runtime-next')
GEN = os.path.join(HERE, 'gen')
M32 = 0xffffffff


def keyhash(k): return hashlib.sha256(repr(k).encode('utf8')).hexdigest()


def main(pkl, replay_path):
    sys.path.insert(0, os.path.join(RN, 'data-v1'))
    import place as PL
    EXT = os.environ.get('FNV_M3_DV1_EXT') == '1'
    rp = json.load(open(replay_path))
    st = pickle.load(open(pkl, 'rb')); SECS, placed = st.SEC, st.placed
    byhash = {keyhash(k): k for k in SECS}

    def resolve2(s):
        res, src = st.resolve(s)
        if not EXT: return res, src
        u = s['units'][0]
        for r in s['relocs']:
            off, kind, nm, tsec, tval, tstor, addend, rsrc, rexp = r
            if rsrc == 'b' and kind == 6 and tsec > 0 and addend is not None:
                tk, a0 = st.tkey(u, tsec, tval + addend)
                if tk is not None and tk in placed:
                    v = (placed[tk][0] + (tval + addend) - a0) & M32
                    if res.get(off) != v: res[off] = v; src[off] = 'placed-section-pref'
        return res, src
    acc = []; nfrozen = [0]
    for r in rp['pieces']:
        k = byhash.get(r['kh'])
        if k is None: raise SystemExit('replay: piece identity not found (compiled object changed): va %08x kind %s unit %s' % (r['va'], r['kind'], r['unit']))
        s = SECS[k]; data = bytes(s['data'])
        if k not in placed or placed[k][0] != r['va'] or placed[k][1] != r['tier']: raise SystemExit('replay: placement differs for va %08x: %s vs %s' % (r['va'], placed.get(k), (r['va'], r['tier'])))
        if len(data) != r['size'] or hashlib.sha256(data).hexdigest() != r['dsha']: raise SystemExit('replay: compiled bytes differ for va %08x' % r['va'])
        res, src = resolve2(s) if s['relocs'] else ({}, {})
        rl = []
        for (off, tgt, add) in r['relocs']:
            rec = next((x for x in s['relocs'] if x[0] == off), None)
            if rec is None or rec[1] != 6 or off + 4 > len(data): raise SystemExit('replay: relocation %d of piece %08x missing' % (off, r['va']))
            if res.get(off) is None: nfrozen[0] += 1               # EH-table unwind-funclet addresses: phase0 learns them from the reference's EH tables; the frozen target VA (placement metadata) is used
            elif res[off] & M32 != tgt: raise SystemExit('replay: relocation %d of piece %08x resolves to %08x, frozen %08x' % (off, r['va'], res[off] & M32, tgt))
            a2 = struct.unpack_from('<i', data, off)[0]
            if a2 != add: raise SystemExit('replay: addend differs at %08x+%d' % (r['va'], off))
            rl.append((off, tgt, add, src.get(off)))
        if len(rl) != len([x for x in s['relocs']]): raise SystemExit('replay: unfrozen relocations in piece %08x' % r['va'])
        c = dict(va=r['va'], size=r['size'], kind=r['kind'], tier=r['tier'], unit=r['unit'], nunits=r['nunits'], section=r['section'], chunk=r['chunk'], names=r['names'], ext=r['ext'], data=data, relocs=rl)
        if r.get('library_opt_in'): c['library_opt_in'] = True
        acc.append(c)
    m3skip = json.load(open(os.path.join(GEN, 'skip_ranges.json'))); m3rng = sorted((a, a + n) for a, n in m3skip)
    dv1skip = sorted([c['va'], c['size']] for c in acc)
    merged = sorted(m3skip + dv1skip)
    for x, y in zip(merged, merged[1:]): assert x[0] + x[1] <= y[0], ('overlap in merged skip ranges', x, y)
    pieces = [dict(va=c['va'], size=c['size'], section=c['section'], chunk=c['chunk'], kind=c['kind'], tier=c['tier'], unit=c['unit'], nunits=c['nunits'], names=c['names'], ext=c['ext'],
                   data=c['data'].hex(), relocs=[[o, t, a] for o, t, a, sr in c['relocs']], **({'library_opt_in': True} if c.get('library_opt_in') else {})) for c in sorted(acc, key=lambda c: c['va'])]
    payload = json.dumps(dict(note='M3 batch 5: data-v1 placed pieces of our unit objects (bytes as compiled, relocation fields hold the object addend); relocs = [offset, resolved target VA, object addend]', pieces=pieces), separators=(',', ':')).encode('utf8')
    psha = hashlib.sha256(payload).hexdigest()
    if psha != rp['payload_sha256']: raise SystemExit('replay: dv1_pieces.json differs from the frozen normal run (%s != %s)' % (psha, rp['payload_sha256']))
    # library provenance (hashes of the archives actually used; the selection digest pins the member contents)
    lib_meta = None
    lib_selection = os.environ.get('FNV_M3_LIB_SELECTION')
    if lib_selection:
        sys.path.insert(0, os.path.join(RN, 'data-v2')); import libsecs
        raw = open(lib_selection, 'rb').read(); dg = hashlib.sha256(raw).hexdigest()
        if dg != os.environ.get('FNV_M3_LIB_SHA256', '').lower(): raise SystemExit('library selection digest mismatch')
        ah = {n: hashlib.sha256((libsecs.LIB / n).read_bytes()).hexdigest() for n in ('libcmt.lib', 'libcpmt.lib')}
        libp = [c for c in acc if c.get('library_opt_in')]
        lib_meta = dict(selection_sha256=dg, selected=len(libp), bytes=sum(c['size'] for c in libp), archive_sha256=ah)
        if (lib_meta['selected'], lib_meta['bytes']) != (rp['library']['selected'], rp['library']['bytes']): raise SystemExit('replay: library overlay differs from the frozen run')
        if ah != rp['library']['archive_sha256']: raise SystemExit('replay: library archives differ from the frozen run')
    with open(os.path.join(GEN, 'dv1_pieces.json'), 'wb') as f: f.write(payload)
    if os.environ.get('FNV_M3_RTTI_NAME_LITERAL') == '1':
        sys.path.insert(0, os.path.join(HERE, 'phase2')); import selector_bridge as RB
        D = RB.D; sha = RB.sha
        proof = dict(rp['rtti_proof_template'])
        proof.update(removed_value_fields=sorted(proof['removed_value_fields']), objects_sha256={p: sha(p) for p in proof['objects_sha256']}, recipe_sha256=sha(os.path.join(PROJ, 'fnv_decomp', 'build', 'units.json')),
                     reference_sha256=None, dv1_pieces_sha256=psha, placement_sha256=sha(pkl), bridge_sha256=sha(RB.__file__), validator_sha256=sha(D / 'validate_type_name_literal.py'), allowlist_sha256=sha(D / 'rtti-descriptor-allowlist.json'), replay=True)
        tmp = os.environ['TEMP']
        if os.path.exists(os.path.join(tmp, 'rtti-name-field-proof.json')): raise FileExistsError('RTTI proof already exists')
        with open(os.path.join(tmp, 'rtti-name-field-proof.json'), 'x') as f: json.dump(proof, f, indent=2)
    json.dump(dv1skip, open(os.path.join(GEN, 'dv1_skip_ranges.json'), 'w'))
    json.dump(merged, open(os.path.join(GEN, 'skip_ranges_b5.json'), 'w'))
    bykind = collections.defaultdict(lambda: [0, 0, 0]); bytier = collections.Counter()
    for c in acc:
        b = bykind[c['kind']]; b[0] += 1; b[1] += c['size']; b[2] += len(c['relocs']); bytier[c['tier']] += c['size']
    log = dict(selected=len(acc), bytes=sum(c['size'] for c in acc), relocs=sum(len(c['relocs']) for c in acc), kinds_filter=None, library_opt_in=lib_meta,
               by_kind={k: dict(pieces=v[0], bytes=v[1], relocs=v[2]) for k, v in sorted(bykind.items())}, bytes_by_tier=dict(bytier),
               by_section={s_: sum(c['size'] for c in acc if c['section'] == s_) for s_ in ('.data', '.rdata', 'CONST', '.tls')},
               rejected={}, rejected_bytes_by_reason={}, rejected_sub={}, rejected_unique_uncovered={},
               ext=dict(enabled=EXT, stats={}, placed_by_kind={}, selected_pieces=sum(1 for c in acc if c['ext']), selected_bytes=sum(c['size'] for c in acc if c['ext']), selected_relocs=sum(len(c['relocs']) for c in acc if c['ext'])),
               replay=dict(source=os.path.basename(replay_path), reference_reads=0, relocs_resolved_by_data_v1=sum(len(c['relocs']) for c in acc) - nfrozen[0], relocs_with_frozen_target=nfrozen[0]), pieces_sha=psha[:16])
    json.dump(log, open(os.path.join(GEN, 'dv1_log.json'), 'w'), indent=1)
    print(json.dumps({k: log[k] for k in ('selected', 'bytes', 'relocs', 'bytes_by_tier', 'by_section')}, indent=1))
    print('dv1 replay: %d pieces, dv1_pieces.json reproduced (sha256 %s), no reference read; %d relocation targets taken from the frozen map (EH funclet addresses)' % (len(acc), psha, nfrozen[0]))
