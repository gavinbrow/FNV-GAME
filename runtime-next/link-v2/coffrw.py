r"""link-v2 coffrw.py: minimal COFF symbol-table rewriter (rename external symbols, keep symbol indexes, so relocations stay valid).
rewrite(src_bytes, rename: dict old->new) -> (new_bytes, count_renamed)"""
import collections
import struct


def parse(b):
    machine, nsec, ts, symptr, nsym, optsz, chars = struct.unpack_from('<HHIIIHH', b, 0)
    return dict(machine=machine, nsec=nsec, symptr=symptr, nsym=nsym, optsz=optsz)


def symbols(b):
    """yield (index, name, value, section, type, storage, naux, entry_offset)"""
    h = parse(b)
    strt = h['symptr'] + 18 * h['nsym']
    i = 0
    while i < h['nsym']:
        o = h['symptr'] + 18 * i
        raw = b[o:o + 8]
        if raw[:4] == b'\0\0\0\0':
            off = struct.unpack_from('<I', raw, 4)[0]
            e = b.index(b'\0', strt + off)
            name = b[strt + off:e].decode('latin1')
        else:
            name = raw.rstrip(b'\0').decode('latin1')
        value, sec, ty, sc, naux = struct.unpack_from('<IhHBB', b, o + 8)
        yield i, name, value, sec, ty, sc, naux, o
        i += 1 + naux


def rewrite(b, rename):
    h = parse(b)
    buf = bytearray(b)
    strt = h['symptr'] + 18 * h['nsym']
    oldlen = struct.unpack_from('<I', b, strt)[0] if strt + 4 <= len(b) else 4
    add = bytearray(); n = 0
    for i, name, value, sec, ty, sc, naux, o in symbols(b):
        new = rename.get(name)
        if new is None or new == name or sc not in (2, 3, 105): continue
        if sc == 3 and not (sec > 0 and (ty & 0x20)): continue
        if sc == 3: buf[o + 16] = 2          # static function made external under its address name
        nb = new.encode('latin1')
        if len(nb) <= 8:
            buf[o:o + 8] = nb.ljust(8, b'\0')
        else:
            off = oldlen + len(add)
            buf[o:o + 8] = struct.pack('<II', 0, off)
            add += nb + b'\0'
        n += 1
    if add:
        total = oldlen + len(add)
        buf = buf[:strt] + struct.pack('<I', total) + buf[strt + 4:strt + oldlen] + add + buf[strt + oldlen:]
    return bytes(buf), n


def sections(b):
    """list of dicts: index (1-based), name, flags, hdr_off, size, nreloc, relptr"""
    h = parse(b); out = []
    base = 20 + h['optsz']
    for i in range(h['nsec']):
        o = base + 40 * i
        nm = b[o:o + 8].rstrip(b'\0').decode('latin1')
        vs, va, size, rptr, relptr, lnp, nrel, nln, fl = struct.unpack_from('<IIIIIIHHI', b, o + 8)
        out.append(dict(index=i + 1, name=nm, flags=fl, hdr=o, size=size, nrel=nrel, relptr=relptr))
    return out


def comdat_info(b):
    """{section index: (selection, associated section index or 0, external symbol names defined in it)}"""
    h = parse(b); secs = sections(b); info = {}
    ext = {}
    for i, name, value, sec, ty, sc, naux, o in symbols(b):
        if sc == 3 and naux >= 1 and sec > 0 and value == 0 and (secs[sec - 1]['flags'] & 0x1000):
            length, nr, nl, cksum, num, sel = struct.unpack_from('<IHHIHB', b, o + 18)
            info[sec] = [sel, num, []]
        if sc == 2 and sec > 0: ext.setdefault(sec, []).append((name, ty))
    for s, l in ext.items():
        if s in info: info[s][2] = l
    return info


def set_flags(buf, sec, add=0x800):
    fl = struct.unpack_from('<I', buf, sec['hdr'] + 36)[0]
    struct.pack_into('<I', buf, sec['hdr'] + 36, fl | add)


def strip_unplaced(b, keep_prefix='C_'):
    """mark code COMDAT sections whose external symbols are not all recipe (C_<va>) names as LNK_REMOVE, plus their associative children. returns (bytes, removed, kept_code_comdats, noncomdat_code_sections)"""
    secs = sections(b); info = comdat_info(b); buf = bytearray(b)
    rem = set(); kept = 0
    for k, (sel, num, ex) in info.items():
        s = secs[k - 1]
        if not (s['flags'] & 0x20) or sel == 5: continue          # code, primary comdat
        if any(n.startswith(keep_prefix) for n, ty in ex): kept += 1
        else: rem.add(k)
    changed = True
    while changed:
        changed = False
        for k, (sel, num, ex) in info.items():
            if sel == 5 and num in rem and k not in rem: rem.add(k); changed = True
    rem |= {s['index'] for s in secs if s['name'] == '.sxdata'}
    nb2 = drop_sections(b, rem) if rem else b
    noncomdat = sum(1 for s in secs if (s['flags'] & 0x20) and not (s['flags'] & 0x1000) and s['name'].startswith('.text') and s['size'] > 0)
    return nb2, len(rem), kept, noncomdat


def drop_sections(b, rem):
    """physically remove sections (1-based indexes in rem): renumber sections, defined external symbols of removed sections become undefined, other symbols of them become absolute"""
    h = parse(b); secs = sections(b)
    keep = [s for s in secs if s['index'] not in rem]
    newidx = {s['index']: k + 1 for k, s in enumerate(keep)}
    base = 20 + h['optsz']
    out = bytearray(b[:base])
    hdr_end = base + 40 * len(keep)
    body = bytearray(); hdrs = []
    pos = hdr_end
    for s in keep:
        o = s['hdr']; raw = bytearray(b[o:o + 40])
        size = s['size']; rptr = struct.unpack_from('<I', raw, 20)[0]; relptr = struct.unpack_from('<I', raw, 24)[0]; nrel = struct.unpack_from('<H', raw, 32)[0]
        if size and rptr:
            struct.pack_into('<I', raw, 20, pos + len(body)); body += b[rptr:rptr + size]
        else: struct.pack_into('<I', raw, 20, 0)
        if nrel and relptr:
            nb = 10 * nrel
            struct.pack_into('<I', raw, 24, pos + len(body)); body += b[relptr:relptr + nb]
        else: struct.pack_into('<I', raw, 24, 0)
        hdrs.append(bytes(raw))
    symptr = pos + len(body)
    sym = bytearray(b[h['symptr']:h['symptr'] + 18 * h['nsym']])
    strtab = b[h['symptr'] + 18 * h['nsym']:]
    i = 0
    while i < h['nsym']:
        o = 18 * i
        value, sec, ty, sc, naux = struct.unpack_from('<IhHBB', sym, o + 8)
        if bytes(sym[o:o + 8]).rstrip(b'\x00') == b'@feat.00': struct.pack_into('<I', sym, o + 8, value & ~1)
        if sec > 0:
            if sec in rem:
                if sc == 2: struct.pack_into('<I', sym, o + 8, 0); struct.pack_into('<h', sym, o + 12, 0)
                else: struct.pack_into('<h', sym, o + 12, -1)
            else:
                struct.pack_into('<h', sym, o + 12, newidx[sec])
                if sc == 3 and naux >= 1:
                    num = struct.unpack_from('<H', sym, o + 18 + 12)[0]
                    if num in newidx: struct.pack_into('<H', sym, o + 18 + 12, newidx[num])
        i += 1 + naux
    out[2:4] = struct.pack('<H', len(keep))
    out[8:12] = struct.pack('<I', symptr)
    return bytes(out) + b''.join(hdrs) + bytes(body) + bytes(sym) + strtab


def rebuild(b, drop, newnames, relnames=None):
    """drop: set of 1-based section indexes to remove; newnames: {old symbol index: new external name}. Relocations that reference an old symbol are redirected to an appended
    undefined external symbol with the new name. The symbol table is compacted: symbols that belonged to dropped sections or are undefined and no longer referenced by a kept
    relocation are removed (this linker reports unreferenced undefined externals), relocation symbol indexes are renumbered."""
    h = parse(b); secs = sections(b)
    keep = [s for s in secs if s['index'] not in drop]
    newidx = {s['index']: k + 1 for k, s in enumerate(keep)}
    base = 20 + h['optsz']; nsym0 = h['nsym']
    old = bytes(b[h['symptr']:h['symptr'] + 18 * nsym0]); strtab0 = b[h['symptr'] + 18 * nsym0:]
    # appended names
    entries = []                                 # (old index or None, bytes of entry+aux, name for new)
    ents = {}
    i = 0
    while i < nsym0:
        value, sec, ty, sc, naux = struct.unpack_from('<IhHBB', old, 18 * i + 8)
        ents[i] = (old[18 * i:18 * (i + 1 + naux)], sec, sc, naux, value)
        i += 1 + naux
    # referenced symbols after redirect
    redirect = {}
    names_new = {}
    for oi, nm in newnames.items():
        if nm not in names_new: names_new[nm] = len(names_new)
        redirect[oi] = nm
    relnames = relnames or {}
    for (_k, _r), nm in relnames.items():
        if nm not in names_new: names_new[nm] = len(names_new)
    ref_old = set(); ref_new = set()
    relbytes = {}
    for s in keep:
        nrel = s['nrel']
        if not nrel: continue
        rel = bytearray(b[s['relptr']:s['relptr'] + 10 * nrel])
        for r in range(nrel):
            si = struct.unpack_from('<I', rel, 10 * r + 4)[0]
            if (s['index'], r) in relnames: continue
            if si in redirect: ref_new.add(redirect[si])
            else: ref_old.add(si)
        relbytes[s['index']] = rel
    for oi, (raw, sec, sc, naux, value) in ents.items():
        if sc == 105 and naux and oi in ref_old: ref_old.add(struct.unpack_from('<I', raw, 18)[0])
    keep_old = []
    for oi, (raw, sec, sc, naux, value) in ents.items():
        indrop = sec > 0 and sec in drop
        if indrop and oi not in ref_old: continue
        if sec > 0 and not indrop: keep_old.append(oi); continue
        if oi in ref_old: keep_old.append(oi); continue
        if sec == 0 and sc in (2, 105) and value == 0: continue            # unreferenced undefined external / weak external
        if sec == -1 and sc == 3 and False: continue
        keep_old.append(oi)
    # new symbol table
    strt = bytearray(struct.pack('<I', 4)) + bytearray(strtab0[4:]) if len(strtab0) >= 4 else bytearray(struct.pack('<I', 4))
    newtab = bytearray(); idxmap = {}; n = 0
    for oi in keep_old:
        idxmap[oi] = n; n += 1 + ents[oi][3]
    n = 0
    for oi in keep_old:
        raw, sec, sc, naux, value = ents[oi]
        e = bytearray(raw)
        if sc == 105 and naux: struct.pack_into('<I', e, 18, idxmap[struct.unpack_from('<I', raw, 18)[0]])
        if sec > 0 and sec in drop:
            if sc == 2: struct.pack_into('<I', e, 8, 0); struct.pack_into('<h', e, 12, 0)
            else: struct.pack_into('<h', e, 12, -1)
        elif sec > 0:
            struct.pack_into('<h', e, 12, newidx[sec])
            if sc == 3 and naux >= 1:
                num = struct.unpack_from('<H', e, 18 + 12)[0]
                if num in newidx: struct.pack_into('<H', e, 18 + 12, newidx[num])
        if bytes(e[:8]).rstrip(b'\x00') == b'@feat.00': struct.pack_into('<I', e, 8, struct.unpack_from('<I', e, 8)[0] & ~1)
        n += 1 + naux; newtab += e
    nameidx = {}
    for nm in names_new:
        e = bytearray(18); nb = nm.encode('latin1')
        if len(nb) <= 8: e[0:8] = nb.ljust(8, b'\x00')
        else: struct.pack_into('<II', e, 0, 0, len(strt)); strt += nb + b'\x00'
        struct.pack_into('<IhHBB', e, 8, 0, 0, 0, 2, 0)
        nameidx[nm] = n; n += 1; newtab += e
    struct.pack_into('<I', strt, 0, len(strt))
    out = bytearray(b[:base]); pos = base + 40 * len(keep); body = bytearray(); hdrs = []
    for s in keep:
        o = s['hdr']; raw = bytearray(b[o:o + 40])
        size = s['size']; rptr = struct.unpack_from('<I', raw, 20)[0]
        if size and rptr: struct.pack_into('<I', raw, 20, pos + len(body)); body += b[rptr:rptr + size]
        else: struct.pack_into('<I', raw, 20, 0)
        rel = relbytes.get(s['index'])
        if rel is not None:
            struct.pack_into('<I', raw, 24, pos + len(body))
            for r in range(len(rel) // 10):
                si = struct.unpack_from('<I', rel, 10 * r + 4)[0]
                ni = nameidx[relnames[(s['index'], r)]] if (s['index'], r) in relnames else (nameidx[redirect[si]] if si in redirect else idxmap[si])
                struct.pack_into('<I', rel, 10 * r + 4, ni)
            body += rel
        else: struct.pack_into('<I', raw, 24, 0)
        hdrs.append(bytes(raw))
    out[2:4] = struct.pack('<H', len(keep)); out[8:12] = struct.pack('<I', pos + len(body)); out[12:16] = struct.pack('<I', n)
    return bytes(out) + b''.join(hdrs) + bytes(body) + bytes(newtab) + bytes(strt)


def rewrite_idx(b, idxnames):
    """rename symbols by table index (new names; static symbols become external)"""
    h = parse(b); buf = bytearray(b)
    strt = h['symptr'] + 18 * h['nsym']
    oldlen = struct.unpack_from('<I', b, strt)[0] if strt + 4 <= len(b) else 4
    add = bytearray(); n = 0
    for i, name, value, sec, ty, sc, naux, o in symbols(b):
        new = idxnames.get(i)
        if new is None or sc not in (2, 3): continue
        nb = new.encode('latin1')
        if len(nb) <= 8: buf[o:o + 8] = nb.ljust(8, bytes(1))
        else:
            buf[o:o + 8] = struct.pack('<II', 0, oldlen + len(add)); add += nb + bytes(1)
        if sc == 3: buf[o + 16] = 2
        n += 1
    if add:
        buf = buf[:strt] + struct.pack('<I', oldlen + len(add)) + buf[strt + 4:strt + oldlen] + add + buf[strt + oldlen:]
    return bytes(buf), n


def add_symbols(b, adds):
    """append external symbols (name, section number, value, type); existing symbol indexes unchanged"""
    h = parse(b); buf = bytearray(b)
    strt = h['symptr'] + 18 * h['nsym']
    oldlen = struct.unpack_from('<I', b, strt)[0] if strt + 4 <= len(b) else 4
    new = bytearray(); add = bytearray()
    for name, sec, value, ty in adds:
        e = bytearray(18); nb = name.encode('latin1')
        if len(nb) <= 8: e[0:8] = nb.ljust(8, bytes(1))
        else: struct.pack_into('<II', e, 0, 0, oldlen + len(add)); add += nb + bytes(1)
        struct.pack_into('<IhHBB', e, 8, value, sec, ty, 2, 0)
        new += e
    out = bytearray(b[:h['symptr'] + 18 * h['nsym']]) + new + struct.pack('<I', oldlen + len(add)) + b[strt + 4:strt + oldlen] + add
    struct.pack_into('<I', out, 12, h['nsym'] + len(adds))
    return bytes(out)


def split_packs(b, names=('.text$x',)):
    """Split COMDAT code packs (default .text$x: compiler funclet packs) at the offsets of their symbols into separate COMDAT sections (same selection / associative parent), one per piece.
    The symbol table is re-ordered so every new COMDAT starts with its section symbol followed by its own symbols (this linker takes the first symbol after the section symbol as
    the COMDAT leader); relocation symbol indexes are renumbered. returns (new_bytes, number of packs split)"""
    h = parse(b); secs = sections(b); info = comdat_info(b)
    ents = list(symbols(b)); nsym0 = h['nsym']
    raw_all = bytes(b[h['symptr']:h['symptr'] + 18 * nsym0]); strtab = bytearray(b[h['symptr'] + 18 * nsym0:])
    bysec = collections.defaultdict(set)
    for i, nm, value, sec, ty, sc, naux, o in ents:
        if sec > 0 and not (sc == 3 and naux >= 1 and nm.startswith('.')): bysec[sec].add(value)
    plans = {}
    for s in secs:
        k = s['index']
        if s['name'] not in names or k not in info or not (s['flags'] & 0x20): continue
        offs = sorted(bysec.get(k, ()))
        if len(offs) < 2 or offs[0] != 0: continue
        plans[k] = list(zip(offs, offs[1:] + [s['size']]))
    if not plans: return b, 0
    nsec0 = len(secs); newsecs = []; slice_of = {}
    for k, pl in plans.items():
        s = secs[k - 1]; raw = b[struct.unpack_from('<I', b, s['hdr'] + 20)[0]:][:s['size']]
        rel = [(struct.unpack_from('<I', b, s['relptr'] + 10 * r)[0], struct.unpack_from('<I', b, s['relptr'] + 10 * r + 4)[0], struct.unpack_from('<H', b, s['relptr'] + 10 * r + 8)[0]) for r in range(s['nrel'])]
        for a, e in pl:
            slice_of[(k, a)] = len(newsecs)
            newsecs.append((s['name'], s['flags'], raw[a:e], [(o - a, si, ty) for o, si, ty in rel if a <= o < e], k, a))
    # new symbol order
    new_entries = []; idxmap = {}; deferred = collections.defaultdict(list); n = 0
    for i, nm, value, sec, ty, sc, naux, o in ents:
        raw = bytearray(raw_all[18 * i:18 * (i + 1 + naux)])
        if sec in plans:
            if sc == 3 and naux >= 1 and nm.startswith('.'): continue                  # old pack section symbol dropped
            a = max(x for x, e in plans[sec] if x <= value)
            struct.pack_into('<I', raw, 8, value - a); struct.pack_into('<h', raw, 12, nsec0 + 1 + slice_of[(sec, a)])
            deferred[slice_of[(sec, a)]].append((i, raw, 1 + naux)); continue
        new_entries.append((i, raw, 1 + naux))
    for idx_s, (nm, fl, data, rel, k, a) in enumerate(newsecs):
        e = bytearray(36); e[0:8] = nm.encode('latin1')[:8].ljust(8, bytes(1))
        struct.pack_into('<IhHBB', e, 8, 0, nsec0 + 1 + idx_s, 0, 3, 1)
        struct.pack_into('<IHHIHB', e, 18, len(data), len(rel), 0, 0, info[k][1], info[k][0])
        new_entries.append((None, e, 2)); new_entries.extend(deferred[idx_s])
    out_sym = bytearray()
    for i, raw, cnt in new_entries:
        if i is not None: idxmap[i] = n
        n += cnt; out_sym += raw
    # old symbols that vanished (pack section symbols) map to the first slice's section symbol
    first_sec_sym = {}
    nn = 0
    for i, raw, cnt in new_entries:
        if i is None: first_sec_sym.setdefault(len(first_sec_sym), nn)
        nn += cnt
    for i, nm, value, sec, ty, sc, naux, o in ents:
        if i not in idxmap: idxmap[i] = 0
    # weak external tags
    j = 0
    while j < len(out_sym):
        # walk entries
        v, sec_, ty_, sc_, na_ = struct.unpack_from('<IhHBB', out_sym, j + 8)
        if sc_ == 105 and na_: struct.pack_into('<I', out_sym, j + 18, idxmap.get(struct.unpack_from('<I', out_sym, j + 18)[0], 0))
        j += 18 * (1 + na_)
    total = len(secs) + len(newsecs)
    base = 20 + h['optsz']
    out = bytearray(b[:base]); pos = base + 40 * total; body = bytearray(); hdrs = []
    def remap_rel(relb):
        r = bytearray(relb)
        for q in range(len(r) // 10): struct.pack_into('<I', r, 10 * q + 4, idxmap[struct.unpack_from('<I', r, 10 * q + 4)[0]])
        return bytes(r)
    for s in secs:
        raw = bytearray(b[s['hdr']:s['hdr'] + 40])
        if s['index'] in plans:
            struct.pack_into('<I', raw, 36, (struct.unpack_from('<I', raw, 36)[0] & ~0x1000) | 0x800); struct.pack_into('<I', raw, 16, 0); struct.pack_into('<I', raw, 20, 0); struct.pack_into('<I', raw, 24, 0); struct.pack_into('<H', raw, 32, 0)
        else:
            rptr = struct.unpack_from('<I', raw, 20)[0]; relptr = struct.unpack_from('<I', raw, 24)[0]; nrel = struct.unpack_from('<H', raw, 32)[0]
            if s['size'] and rptr: struct.pack_into('<I', raw, 20, pos + len(body)); body += b[rptr:rptr + s['size']]
            if nrel and relptr: struct.pack_into('<I', raw, 24, pos + len(body)); body += remap_rel(b[relptr:relptr + 10 * nrel])
        hdrs.append(bytes(raw))
    for nm, fl, data, rel, k, a in newsecs:
        raw = bytearray(40); raw[0:8] = nm.encode('latin1')[:8].ljust(8, bytes(1))
        struct.pack_into('<IIIIIIHHI', raw, 8, 0, 0, len(data), pos + len(body), pos + len(body) + len(data) if rel else 0, 0, len(rel), 0, fl)
        body += data
        for o, si, ty in rel: body += struct.pack('<IIH', o, idxmap[si], ty)
        hdrs.append(bytes(raw))
    out[2:4] = struct.pack('<H', total); out[8:12] = struct.pack('<I', pos + len(body)); out[12:16] = struct.pack('<I', n)
    return bytes(out) + b''.join(hdrs) + bytes(body) + bytes(out_sym) + bytes(strtab), len(plans)
