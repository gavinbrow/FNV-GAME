"""Local decompile targets for the FNV MCP server (no upstream service, no coordinator).

A target is one function (or static initializer) of the original image that has no recipe entry yet. The agent writes C++;
check_candidate compiles it with the compiler profile recorded on the target and compares the function with the reference
image through fnv_decomp/tools/compare.py (byte for byte, relocations resolved by name). Nothing is ever executed or uploaded.

State lives under local/mcp/local-targets/ (see LT below). Retention (hard rules, enforced here):
  * per check the compiler works in a private temp dir that is always deleted (objects, listings, compiler logs);
  * per attempt ONE small JSON record is kept in records/<target>/<candidate>.json;
  * candidate sources are kept only while the claim is live, at most MAX_SOURCES_PER_TARGET (latest) per target
    (a source that matched is also kept until submit/release); release, submit or expiry delete the rest;
  * the whole attempts/ area is capped at ATTEMPTS_CAP_BYTES (oldest candidate folders pruned first);
  * accepted matching source is written to FNV/contributions/FUN_<address>.cpp (the normal contribution path).
"""
import sys, json, os, re, shutil, subprocess, threading, time, uuid, hashlib, importlib.util, collections, hmac
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(os.environ.get('FNV_ROOT') or Path(__file__).resolve().parents[1])  # FNV_ROOT only for offline tests run from a staging folder
FN = ROOT.parent / 'fnv_decomp'
# FNV_LT_DIR / FNV_CONTRIB_DIR let an offline test instance run against a copy of the state (never set in production).
LT = Path(os.environ['FNV_LT_DIR']).resolve() if os.environ.get('FNV_LT_DIR') else ROOT / 'local/mcp/local-targets'
CATALOG = LT / 'catalog.json'
STATE = LT / 'state.json'
SYMBOLS = LT / 'symbols.json'
CONFIG = LT / 'config.json'
ATTEMPTS = LT / 'attempts'
RECORDS = LT / 'records'
NOTES = LT / 'notes'
TMP = LT / 'tmp'
CONTRIB = Path(os.environ['FNV_CONTRIB_DIR']).resolve() if os.environ.get('FNV_CONTRIB_DIR') else ROOT / 'contributions'
IMAGE = Path(os.environ['FNV_REF_IMAGE']) if os.environ.get('FNV_REF_IMAGE') else ROOT / 'work/worker1/FalloutNV.runtime-text.exe'   # decrypted reference image, read only
MAX_SOURCES_PER_TARGET = 3
ATTEMPTS_CAP_BYTES = 300 * 1024 * 1024
LEASE_SECONDS = 2 * 3600
RECORDS_CAP_BYTES = 64 * 1024 * 1024   # whole records/ area; oldest files pruned first
NOTES_CAP_BYTES = 32 * 1024 * 1024     # whole notes/ area; oldest files pruned first
RECORDS_PER_TARGET = 300               # newest attempt records kept per target
NOTES_PER_TARGET = 60                  # newest notes (checkpoints, flags, releases) kept per target
MAINTAIN_INTERVAL = 300                # seconds between throttled maintenance passes
TMP_MAX_AGE = 600                      # orphan *.tmp / scratch older than this is deleted
MAX_OUTPUT_CHARS = 2000                # compiler output returned to agents, after scrubbing
MAX_LINE_CHARS = 300
ID_RE = re.compile(r'loc_[0-9a-f]{8}')
LOCK = threading.RLock()
_cache = {}

def now():
    return datetime.now(timezone.utc)

def iso(t=None):
    return (t or now()).strftime('%Y-%m-%dT%H:%M:%SZ')

def is_local(name):
    return bool(ID_RE.fullmatch(name or ''))

def _read(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return default

def _write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex[:8] + '.tmp')
    try:
        tmp.write_text(json.dumps(value, indent=1), encoding='utf-8')
        err = None
        for i in range(8):  # Windows: os.replace fails while a reader has the target open
            try:
                os.replace(tmp, path); return
            except OSError as e:
                err = e; time.sleep(0.03 * (i + 1))
        raise err
    finally:
        try: tmp.unlink()   # gone after a successful replace; removed after any failure
        except OSError: pass

def enabled():
    cfg = _read(CONFIG, {})
    return CATALOG.exists() and cfg.get('enabled', True)

def config():
    return _read(CONFIG, {})

def catalog():
    try:
        mt = CATALOG.stat().st_mtime
    except OSError:
        return {}
    if _cache.get('cat_mt') != mt:
        _cache['cat'] = _read(CATALOG, {}).get('targets', {}); _cache['cat_mt'] = mt
    return _cache['cat']

def state():
    s = _read(STATE, {})
    s.setdefault('claims', {}); s.setdefault('requests', {})
    return s

def _expire(s):
    t = now(); changed = False
    for tid, c in list(s['claims'].items()):
        if datetime.strptime(c['expires'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) < t:
            _save_best(tid, 'claim expired without a match', c.get('agent_id'), c.get('model')); _release_files(tid); del s['claims'][tid]; changed = True
    return changed

def target(name):
    """Mirror of server.target(): returns (target dict, attempts folder). The folder holds mcp_candidates/<id>/."""
    t = catalog().get(name)
    if not t:
        raise ValueError('Unknown local target; use list_available_functions')
    return t, ATTEMPTS / name

# ---------------------------------------------------------------- compilers
EXPECT = {'sp1': ('FNV_MSVC9_ROOT', [ROOT / 'tools/vc2008']),
          'rtm': ('FNV_MSVC9_RTM_ROOT', [ROOT / 'tools/vc2008rtm']),
          'vc8': ('FNV_MSVC8_ROOT', [ROOT / 'tools/vc8sp1'])}

def _layout(root):
    root = Path(root)
    for vc in (root / 'VC', root):
        if (vc / 'bin' / 'cl.exe').exists():
            sdk = next((s for s in (root / 'SDK', vc / 'PlatformSDK', root / 'PlatformSDK') if (s / 'Include').exists() or (s / 'include').exists()), None)
            return vc, sdk
    return None, None

def _env_for(name):
    var, defaults = EXPECT[name]
    cands = ([Path(os.environ[var])] if os.environ.get(var) else []) + defaults
    for c in cands:
        vc, sdk = _layout(c)
        if not vc:
            continue
        def sub(p, *names):
            for n in names:
                if (p / n).exists(): return p / n
            return p / names[0]
        inc = [vc / 'include'] + ([sub(sdk, 'Include', 'include')] if sdk else [])
        lib = [vc / 'lib'] + ([sub(sdk, 'Lib', 'lib')] if sdk else [])
        e = os.environ.copy()
        e['INCLUDE'] = ';'.join(map(str, inc)); e['LIB'] = ';'.join(map(str, lib))
        e['PATH'] = str(vc / 'bin') + os.pathsep + e.get('PATH', '')
        return vc / 'bin' / 'cl.exe', e
    raise ValueError('compiler %s not installed (%s)' % (name, var))

# ---------------------------------------------------------------- reference + compare
def _compare_module():
    if 'cmp' not in _cache:
        if str(FN / 'tools') not in sys.path: sys.path.insert(0, str(FN / 'tools'))
        spec = importlib.util.spec_from_file_location('fnv_compare', FN / 'tools/compare.py')
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _cache['cmp'] = m
    return _cache['cmp']

def _pe():
    if 'pe' not in _cache:
        _cache['pe'] = _compare_module().Pe(IMAGE)
    return _cache['pe']

def _symbols():
    mt = SYMBOLS.stat().st_mtime if SYMBOLS.exists() else 0
    if _cache.get('sym_mt') != mt:
        _cache['sym'] = {k: int(v, 0) for k, v in _read(SYMBOLS, {}).items()}; _cache['sym_mt'] = mt
    return _cache['sym']

ADDR_RE = re.compile(r'(?<![0-9A-Za-z])(?:FUN|DAT|PTR|LAB|SUB|UNK|OFF|BYTE|WORD|DWORD|switchD|caseD|LOC)_([0-9a-f]{8})(?![0-9A-Za-z])')

DATA_NAME_RE = re.compile(r'(?<![0-9A-Za-z])(?:DAT|PTR|g)_([0-9a-f]{8})(?![0-9A-Za-z])')

def check(target_id, source, model, agent_id='', compiler='', flags='', entry=''):
    """Compile `source` and compare the target function. Returns the result dict (no original bytes unless config allows).
    flags: optional allow-listed compiler-flag overrides (see _apply_flags); entry: optional name fragment selecting which generated
    function (e.g. ??__F) is the target when the candidate defines several."""
    t, pack = target(target_id)
    started = time.monotonic()
    identity = uuid.uuid4().hex
    folder = pack / 'mcp_candidates' / identity
    folder.mkdir(parents=True)
    cand = folder / 'candidate.cpp'
    cand.write_text(source, encoding='utf-8')
    sha = hashlib.sha256(cand.read_bytes()).hexdigest()
    comp = compiler or t['compiler']
    if comp not in EXPECT:
        shutil.rmtree(folder, ignore_errors=True)
        raise ValueError('compiler must be one of sp1, rtm, vc8')
    work = TMP / identity; work.mkdir(parents=True, exist_ok=True)
    result = dict(status='tool_error', target_id=target_id, address=t['address'], size=t['size'], compiler=comp,
                  flags=t['flags'] if comp == t['compiler'] else _flags_for(comp, t), candidate_id=identity)
    try:
        if flags and flags.strip():
            try:
                result['flags'] = _apply_flags(result['flags'], flags)
            except ValueError as e:
                result.update(status='tool_error', reason=str(e)); return result
            result['flags_override'] = ' '.join(flags.split())[:200]
        if entry:
            result['entry_requested'] = str(entry)[:120]
        cl, env = _env_for(comp)
        bad = _include_violations(source, [Path(p) for p in env['INCLUDE'].split(';') if p] + [FN / 'include'])
        if bad:
            result.update(status='compile_error', errors=bad[:12]); return result
        env['TMP'] = env['TEMP'] = str(work)
        obj = work / 'c.obj'
        flags = result['flags']
        try:
            r = subprocess.run([str(cl), '/c', '/nologo'] + flags + ['/I' + str(FN / 'include'), str(cand), '/Fo' + str(obj)],
                               cwd=str(FN), env=env, capture_output=True, text=True, errors='replace', stdin=subprocess.DEVNULL, timeout=180)
        except subprocess.TimeoutExpired:
            result.update(status='tool_timeout', reason='compiler exceeded 180 s; no MATCH established'); return result
        out = (r.stdout + r.stderr)
        if r.returncode or not obj.exists():
            errs = [l.strip() for l in out.splitlines() if ' error ' in l or 'fatal error' in l]
            result.update(status='compile_error', errors=[_scrub(l) for l in errs[:12]] or [_scrub(out[-600:])]); return result
        # note: warnings/other compiler output is never returned on success
        cm = _compare_module(); pe = _pe(); coff = cm.Coff(obj)
        addr = int(t['address'], 16)
        want = 'FUN_%08x' % addr
        funcs = [s for s in coff.symbols.values() if s['section'] > 0 and s['type'] & 0x20 and not s['name'].startswith(('__catch$', '__unwind', '__ehhandler'))]
        if t['kind'] == 'text_data':   # gated: a const data object placed in a .text* section may be the entry (tables stored inside .text); only for targets of this kind
            funcs += [s for s in coff.symbols.values() if s['section'] > 0 and not s['type'] & 0x20 and s['storage'] in (2, 3) and coff.sections[s['section']]['name'].startswith('.text') and want.lower() in s['name'].lower()]
        inits = [s for s in funcs if s['name'].startswith(('??__E', '??__F'))]
        entry = (entry or '').strip()
        if entry:   # explicit selection: exact name or a fragment of it
            cands = [s for s in funcs if s['name'] == entry] or [s for s in funcs if entry.lower() in s['name'].lower()]
        else:
            cands = [s for s in funcs if want.lower() in s['name'].lower()] or [s for s in funcs if s['name'] in t.get('symbols_hint', [])]
            # A global object with a destructor yields BOTH ??__E (initializer) and ??__F (atexit stub); the target is one of
            # them, so every generated initializer function is a candidate (static_init targets, or no FUN_ name defined).
            if (len(cands) != 1 and t['kind'] == 'static_init') or (not cands and inits):
                cands = inits
        if not cands or (len(cands) > 1 and not all(s in inits for s in cands) and not entry):
            result.update(status='no_entry_function', reason=('define exactly one function whose name contains %s (any decoration, e.g. extern "C" void __cdecl %s(...) or a class member FUN_...)' % (want, want)) if t['kind'] != 'static_init' else
                          'define the global object whose compiler-generated initializer (??__E) or atexit stub (??__F) is this function (a global with a destructor produces both; the one that fits is compared automatically), or a function whose name contains %s' % want,
                          defined_functions=[s['name'] for s in funcs][:20]); return result
        mapping = dict(_symbols())
        for s in coff.symbols.values():
            if s['section'] == 0 and s['storage'] == 2 and s['name'] not in mapping:
                m = ADDR_RE.search(s['name'])
                if m: mapping[s['name']] = int(m.group(1), 16)
        # A candidate-DEFINED data object named after its original address (?DAT_011f8190@@3UT@@A, _g_011f8190, ...) binds by that
        # address whatever its C++ type mangles to. Data only (never a function), address must lie in the image's data sections; the
        # comparison still demands the reference relocation hold exactly that address (+addend), so a wrong hex mismatches.
        named_data = []
        for s in coff.symbols.values():
            if s['section'] > 0 and s['storage'] in (2, 3) and not s['type'] & 0x20 and s['name'] not in mapping                     and '$' not in s['name'] and not coff.sections[s['section']]['name'].startswith('.text'):
                m = DATA_NAME_RE.search(s['name'])
                if m and _section_name_at(pe, int(m.group(1), 16)) in ('.data', '.rdata', '.tls'):
                    mapping[s['name']] = int(m.group(1), 16); named_data.append(s['name'])
        scored = []
        for ent in cands:
            sym = ent['name']
            try:
                scored.append((_compare_entry(cm, pe, coff, t, addr, sym, mapping), sym))
            except ValueError as e:
                scored.append((dict(error=_scrub(str(e))[:300]), sym))
        good = [x for x in scored if 'row' in x[0]]
        if not good:
            result.update(status='mismatch', reason=scored[0][0]['error'], diff_bytes=None); return result
        good.sort(key=lambda x: (not x[0]['match'], x[0]['score']))
        ent, sym = good[0]
        row, diffs, rel_err = ent['row'], ent['diffs'], ent['rel_err']
        result.update(status='match' if ent['match'] else 'mismatch', diff_bytes=len(diffs) + max(0, t['size'] - row['compiled_extent']),
                      compiled_extent=row['compiled_extent'], errors=[_scrub(e) for e in row['errors'][:8]],
                      relocation_total=len(row['relocations']), relocation_mismatches=len(rel_err))
        if len(cands) > 1:
            result['entry_symbol'] = sym
            result['entries_considered'] = [dict(symbol=n, compiled_extent=e['row']['compiled_extent'] if 'row' in e else None,
                                                 diff_bytes=(len(e['diffs']) + max(0, t['size'] - e['row']['compiled_extent'])) if 'row' in e else None,
                                                 verdict='match' if e.get('match') else 'mismatch', **({} if 'row' in e else dict(error=e.get('error')))) for e, n in scored][:6]
        if named_data:
            result['bound_data_by_name'] = [dict(symbol=n, address='0x%08x' % mapping[n]) for n in named_data[:10]]
        if ent.get('bound'):
            result['bound_generated'] = ent['bound'][:20]
        if ent['eh']:
            result['eh_tail'] = ent['eh']
            if row['verdict'] == 'match' and not ent['match']:
                result['reason'] = ('function body matches, but its compiler-generated exception-handling tail (the __ehhandler$ stub and unwind funclets, '
                                    'placed in separate .text$x sections) differs: see eh_tail.errors; the unwind map follows from object lifetimes, '
                                    'try/catch structure and destructor order in your source')
        if rel_err:
            reveal = config().get('reveal_original_window')
            result['relocation_errors'] = [dict(offset=x['offset'], symbol=x.get('symbol'), yours=x.get('expected'),
                                                **({'original': x.get('observed')} if reveal else {})) for x in rel_err[:10]]
        if diffs:
            offs = [d['offset'] for d in diffs]
            ranges = []; s0 = p0 = offs[0]
            for o in offs[1:]:
                if o != p0 + 1: ranges.append([s0, p0 - s0 + 1]); s0 = o
                p0 = o
            ranges.append([s0, p0 - s0 + 1])
            result['first_difference_offset'] = offs[0]
            result['diff_ranges_offset_length'] = ranges[:40]
            result['compiled_bytes_at_first_difference'] = _compiled_window(coff, sym, offs[0])
            if config().get('reveal_original_window'):
                original = pe.read(addr, t['size']); result['original_bytes_at_first_difference'] = original[offs[0]:offs[0] + 8].hex()
        extra = {s['name'] for s in funcs if s['name'] != sym}
        if extra:
            result['note'] = 'other functions defined in the candidate were ignored: ' + ', '.join(sorted(extra)[:5])
        return result
    except ValueError as e:
        result.update(status='tool_error', reason=_scrub(str(e))[:300]); return result
    finally:
        result['elapsed_seconds'] = round(time.monotonic() - started, 2)
        result['source_sha256'] = sha
        shutil.rmtree(work, ignore_errors=True)
        _record_attempt(t, target_id, identity, sha, model, agent_id, result, folder)
        _prune(pack / 'mcp_candidates')
        _cap_attempts()
        maintain()

# ---------------------------------------------------------------- flag overrides (allow-listed)
_FLAG_GROUPS = (('/Od', '/O1', '/O2', '/Ox'), ('/Os', '/Ot'), ('/Ob0', '/Ob1', '/Ob2'), ('/Oy', '/Oy-'), ('/GS', '/GS-'),
                ('/Gy', '/Gy-'), ('/GF', '/GF-'), ('/hotpatch',), ('/EHsc', '/EHs', '/EHa'))
ALLOWED_FLAGS = {f for g in _FLAG_GROUPS for f in g}

def _apply_flags(base, text):
    """Override compiler flags with allow-listed tokens, e.g. '/Ob1', '/hotpatch', '/O2 /Oy-'. A token replaces its own group
    (optimisation level, inlining, frame pointer, GS, ...); everything else is kept. /O* flags are emitted in a fixed order so
    that /Oy- always follows the optimisation level. Anything not allow-listed (defines, includes, /link, ...) is refused."""
    toks = [x for x in re.split(r'[\s,]+', text.strip()) if x]
    bad = [x for x in toks if x not in ALLOWED_FLAGS]
    if bad:
        raise ValueError('flag(s) not allowed: %s. Allowed: %s' % (', '.join(x[:20] for x in bad[:4]), ' '.join(sorted(ALLOWED_FLAGS))))
    cur = list(base)
    for tok in toks:
        grp = next(g for g in _FLAG_GROUPS if tok in g)
        cur = [f for f in cur if f not in grp] + [tok]
    ogroups = [g for g in _FLAG_GROUPS if g[0].startswith('/O')]
    ordered_o = [f for g in ogroups for f in g if f in cur]
    other = [f for f in cur if f not in ordered_o]
    head = [f for f in other if f in ('/MT', '/MTd', '/MD', '/MDd')]
    tail = [f for f in other if f not in head]
    return head + ordered_o + tail

# ---------------------------------------------------------------- compare one entry (function + compiler EH tail)
_EH_MODULE = {}

def _bam():
    """The project's own tools/build_and_match.py: eh_sections() locates and compares the .text$x EH tails."""
    if 'm' not in _EH_MODULE:
        _compare_module()
        spec = importlib.util.spec_from_file_location('fnv_build_and_match', FN / 'tools/build_and_match.py')
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _EH_MODULE['m'] = m
    return _EH_MODULE['m']

def _eh_bindings(coff, pe, addr, size, sym):
    """Relocations of the function that point into a .text$x section (the __ehhandler$ stub it pushes) cannot be resolved by name:
    the stub is placed away from the function by the linker. Bind such a symbol to the address the ORIGINAL's relocation site holds
    (the project pipeline does the same); the stub's own bytes are then compared byte for byte by _bam().eh_sections."""
    import struct
    s0 = coff.named(sym); sec = coff.sections[s0['section']]; start = s0['value']
    original = pe.read(addr, size); out = {}
    for offset, index, kind in sec['relocs']:
        tgt = coff.symbols[index]
        if not start <= offset < start + size - 3 or tgt['section'] <= 0 or not coff.sections[tgt['section']]['name'].startswith('.text$x'):
            continue
        rel = offset - start
        if kind == 0x06:
            at = struct.unpack_from('<I', original, rel)[0] - struct.unpack_from('<I', sec['data'], offset)[0]
        elif kind == 0x14:
            at = addr + rel + 4 + struct.unpack_from('<i', original, rel)[0] - struct.unpack_from('<i', sec['data'], offset)[0]
        else:
            continue
        out.setdefault(tgt['name'], at & 0xffffffff)
    return out

# Compiler-generated / candidate-local symbols the symbol map cannot know (the generated atexit callback ??__F..., the vtable
# ??_7..., implicit ctor/dtor ??0X/??1X, __ehhandler$ stubs). A relocation to one of these is bound to the address the REFERENCE holds
# at that field, gated by the section KIND that address lies in (and, for code, by being a plausible function start).
_GEN_RE = re.compile(r'^(?:\?\?__[EF]|\?\?_7|\?\?_L|\?\?[01][A-Za-z_]|__ehhandler\$)')

def _section_name_at(pe, address):
    for (rva, vsize, _, _), name in zip(pe.sections, pe.names):
        if pe.base + rva <= address < pe.base + rva + max(vsize, 1):
            return name
    return None

def _generated_bindings(coff, pe, addr, size, sym, mapping):
    """Bind generated symbols that are not in the symbol map to the original's value at the relocation field. Accepted per symbol
    only if every reference in the function agrees on one address and that address has the right KIND: .rdata for ??_7 vtables, .text
    for the rest; ??__E/??__F/??0/??1/??_L must additionally be a function start (a known catalog/symbol-map function, or preceded by
    INT3/NOP padding). Ordinary named symbols (anything in the symbol map) are never touched. Returns ({name: address}, audit rows)."""
    import struct
    s0 = coff.named(sym); sec = coff.sections[s0['section']]; start = s0['value']
    original = pe.read(addr, size); seen = {}
    for offset, index, kind in sec['relocs']:
        tgt = coff.symbols[index]; name = tgt['name']
        if not start <= offset < start + size - 3 or name == sym or name in mapping or not _GEN_RE.match(name):
            continue
        if tgt['section'] > 0 and coff.sections[tgt['section']]['name'].startswith('.text$x'):
            continue   # handled by _eh_bindings
        rel = offset - start
        if kind == 0x06:
            at = struct.unpack_from('<I', original, rel)[0] - struct.unpack_from('<I', sec['data'], offset)[0]
        elif kind == 0x14:
            at = addr + rel + 4 + struct.unpack_from('<i', original, rel)[0] - struct.unpack_from('<i', sec['data'], offset)[0]
        else:
            continue
        seen.setdefault(name, []).append((rel, at & 0xffffffff))
    out, audit = {}, []
    known = None
    for name, refs in seen.items():
        if len({a for _, a in refs}) != 1:
            continue   # references disagree: stays unresolved, reported as a mismatch
        at = refs[0][1]; sect = _section_name_at(pe, at)
        if name.startswith('??_7'):
            ok = sect == '.rdata' and at % 4 == 0
        else:
            ok = sect == '.text'
            if ok and not name.startswith('__ehhandler$'):
                if known is None:
                    known = set(mapping.values()) | {int(c['address'], 16) for c in catalog().values()}
                try: pad = pe.read(at - 1, 1)[0] in (0xcc, 0x90)
                except ValueError: pad = False
                ok = at in known or pad
        if ok:
            out[name] = at
            audit.extend(dict(symbol=name, offset=r, address='0x%08x' % at, section=sect) for r, _ in refs)
    return out, audit

def _compare_entry(cm, pe, coff, t, addr, sym, mapping):
    """Compare one candidate entry symbol with the original. Returns dict(row, diffs, rel_err, match, score, eh)."""
    syms = {k: v for k, v in mapping.items() if k in coff.by_name}
    syms.update(_eh_bindings(coff, pe, addr, t['size'], sym))
    gen, bound = _generated_bindings(coff, pe, addr, t['size'], sym, mapping)
    syms.update(gen)
    manifest = dict(symbols=syms, functions=[dict(address=addr, symbol=sym, size=t['size'])])
    rows = cm.compare(coff, pe, manifest)
    row = rows[0]; diffs = row['byte_differences']
    rel_err = [x for x in row['relocations'] if not x.get('match')]
    eh = None; eh_ok = True
    anchored = [n for n in syms if n.startswith('__ehhandler$')]
    if anchored:
        try:
            unit = dict(functions=[dict(address='0x%08x' % addr, symbol=sym, size=t['size'])], symbols={k: hex(v) for k, v in syms.items()})
            sections, inferred, errors = _bam().eh_sections(coff, pe, unit, rows, dict(mapping))
            bad = [x for x in sections if not x[2]]
            eh_ok = not bad and not errors
            eh = dict(sections=len(sections), mismatching_sections=len(bad), errors=[_scrub(e) for e in errors[:8]])
            if bad:   # where the mismatching tails are (original address/size, the function that anchors them)
                eh['mismatching'] = [dict(original_address='0x%08x' % x[0], size=x[1] - x[0], parent=x[3]) for x in bad[:6]]
            if inferred:
                eh['callee_names_bound_from_original'] = sorted(inferred)[:6]
        except Exception as e:   # never turn a tool problem into a MATCH
            eh_ok = False; eh = dict(sections=0, mismatching_sections=0, errors=['EH tail comparison failed: ' + _scrub(str(e))[:200]])
    match = row['verdict'] == 'match' and eh_ok
    score = len(diffs) + max(0, t['size'] - row['compiled_extent']) + 4 * len(rel_err) + (0 if eh_ok else 1)
    return dict(row=row, diffs=diffs, rel_err=rel_err, match=match, score=score, eh=eh, bound=bound)

_PATH_RES = (re.compile(r'[A-Za-z]:[\\/][^\s"\'<>|]*'),            # C:\x or C:/x
             re.compile(r'(?<![\w:])\\\\[^\s"\'<>|]*'),            # \\server\share
             re.compile(r'(?<![\w.])(?:\.\.?[\\/])+[^\s"\'<>|]*'),  # ..\x  .\x
             re.compile(r'(?<![\w.:/])/(?:[A-Za-z0-9_.-]+/)+[^\s"\'<>|]*'))  # /abs/unix/path

def _scrub(text):
    text = str(text)
    text = re.sub(r'[A-Za-z]:[\\/][^\s"\'<>|]*?candidate\.cpp', 'candidate.cpp', text)  # keep "candidate.cpp(12) : error ..." usable
    for rx in _PATH_RES:
        text = rx.sub('<path>', text)
    text = '\n'.join(l[:MAX_LINE_CHARS] + ('...' if len(l) > MAX_LINE_CHARS else '') for l in text.splitlines())
    return text[:MAX_OUTPUT_CHARS] + ('...[truncated]' if len(text) > MAX_OUTPUT_CHARS else '')

_COMMENT_RE = re.compile(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'', re.S)
_DIRECTIVE_RE = re.compile(r'^[ \t]*#[ \t]*(include|import|using|pragma)\b([^\n]*)', re.M)

def _strip_comments(src):
    src = src.replace('\r\n', '\n').replace('\r', '\n')
    src = re.sub(r'\\\n', '', src)  # line splices
    def sub(m):
        t = m.group(0)
        return ' ' if t.startswith('/*') or t.startswith('//') else t
    return _COMMENT_RE.sub(sub, src)

def _include_violations(source, search_dirs):
    """Only plain #include <name> / "name" that resolves inside the compiler/project include dirs is allowed.
    Rejects absolute, drive, UNC, '..' and computed includes, #import/#using, include_alias, digraph/trigraph tricks."""
    out = []
    if '%:' in source or '??=' in source or '??/' in source:
        out.append('digraph/trigraph preprocessor forms are not allowed')
    text = _strip_comments(source)
    roots = []
    for d in search_dirs:
        try: roots.append(Path(d).resolve())
        except OSError: pass
    for m in _DIRECTIVE_RE.finditer(text):
        kind, rest = m.group(1), m.group(2).strip()
        if kind in ('import', 'using'):
            out.append('#%s is not allowed' % kind); continue
        if kind == 'pragma':
            if re.match(r'include_alias\b', rest): out.append('#pragma include_alias is not allowed')
            continue
        mm = re.fullmatch(r'<([^<>\n]+)>|"([^"\n]+)"', rest)
        if not mm:
            out.append('#include operand must be a literal <name> or "name"'); continue
        name = mm.group(1) or mm.group(2)
        if (re.match(r'^[A-Za-z]:', name) or name[0] in '/\\' or name.startswith('~') or ':' in name
                or any(seg == '..' for seg in re.split(r'[\\/]', name)) or '\0' in name):
            out.append('#include of absolute, drive, UNC or parent-relative path is not allowed'); continue
        ok = False
        for r in roots:
            try:
                cand = (r / name).resolve()
                if cand.is_file() and cand.is_relative_to(r): ok = True; break
            except (OSError, ValueError):
                continue
        if not ok:
            out.append('#include %s not found in the allowed include directories' % ('<%s>' % name if mm.group(1) else '"%s"' % name))
    return out

def _flags_for(comp, t):
    return t['flags']

def _compiled_window(coff, sym_name, offset):
    s = coff.named(sym_name); data = coff.sections[s['section']]['data'][s['value'] + max(0, offset - 4): s['value'] + offset + 8]
    return data.hex()

def _record_attempt(t, target_id, identity, sha, model, agent_id, result, folder):
    rec = dict(function=target_id, address=t['address'], agent=agent_id or '', model=(model or '')[:120], candidate_id=identity,
               finished_utc=iso(), seconds=result.get('elapsed_seconds'), result=result.get('status'), byte_diff_count=result.get('diff_bytes'),
               relocation_mismatches=result.get('relocation_mismatches'), compiler=result.get('compiler'), source_sha256=sha)
    _write(RECORDS / target_id / (identity + '.json'), rec)
    _prune_files(RECORDS / target_id, RECORDS_PER_TARGET)
    # the folder keeps only the source plus a tiny check.json
    keep = dict(status=result.get('status'), diff_bytes=result.get('diff_bytes'), compiled_extent=result.get('compiled_extent'), source_sha256=sha, compiler=result.get('compiler'),
                flags_override=result.get('flags_override', ''), entry=result.get('entry_requested', ''))
    _write(folder / 'check.json', keep)

# ---------------------------------------------------------------- retention
def _prune(cands_dir):
    """Keep the newest MAX_SOURCES_PER_TARGET candidate folders (plus any that matched). Safe for any target kind."""
    try:
        dirs = [d for d in Path(cands_dir).iterdir() if d.is_dir()]
    except OSError:
        return
    dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    for d in dirs[MAX_SOURCES_PER_TARGET:]:
        chk = _read(d / 'check.json', {})
        if chk.get('status') == 'match' and is_local(d.parent.parent.name):
            continue
        shutil.rmtree(d, ignore_errors=True)

def _dir_size(p):
    total = 0
    for dp, _, fs in os.walk(p):
        for f in fs:
            try: total += os.path.getsize(os.path.join(dp, f))
            except OSError: pass
    return total

def _cap_attempts():
    if not ATTEMPTS.exists() or _dir_size(ATTEMPTS) <= ATTEMPTS_CAP_BYTES:
        return
    folders = sorted((d for t in ATTEMPTS.iterdir() if (t / 'mcp_candidates').is_dir() for d in (t / 'mcp_candidates').iterdir() if d.is_dir()), key=lambda d: d.stat().st_mtime)
    for d in folders:
        shutil.rmtree(d, ignore_errors=True)
        if _dir_size(ATTEMPTS) <= ATTEMPTS_CAP_BYTES * 0.8:
            break

def _release_files(target_id):
    shutil.rmtree(ATTEMPTS / target_id, ignore_errors=True)

def _prune_files(d, keep, pattern='*.json'):
    """Keep only the newest `keep` files matching pattern in directory d."""
    try:
        files = sorted((f for f in Path(d).glob(pattern) if f.is_file()), key=lambda f: f.stat().st_mtime, reverse=True)
    except OSError:
        return
    files = [f for f in files if f.name != 'best.json']
    for f in files[keep:]:
        try: f.unlink()
        except OSError: pass

def _cap_tree(root, cap):
    """Delete oldest files under root until its size is <= 80% of cap (only when over cap); remove emptied folders."""
    root = Path(root)
    if not root.exists(): return
    files = []; total = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            fp = os.path.join(dp, f)
            try: st = os.stat(fp)
            except OSError: continue
            files.append((st.st_mtime, st.st_size, fp)); total += st.st_size
    if total <= cap: return
    files.sort()
    for mt, sz, fp in files:
        try: os.unlink(fp); total -= sz
        except OSError: continue
        if total <= cap * 0.8: break
    for dp, dn, fs in os.walk(root, topdown=False):
        if dp != str(root) and not dn and not fs:
            try: os.rmdir(dp)
            except OSError: pass

def _sweep_orphan_tmp():
    """Orphaned atomic-write leftovers (*.tmp) older than TMP_MAX_AGE, in LT and below records/ notes/."""
    cutoff = time.time() - TMP_MAX_AGE
    for base, deep in ((LT, False), (RECORDS, True), (NOTES, True)):
        if not base.exists(): continue
        it = base.rglob('*.tmp') if deep else base.glob('*.tmp')
        for f in it:
            try:
                if f.is_file() and f.stat().st_mtime < cutoff: f.unlink()
            except OSError: pass

_maint = dict(last=0.0, busy=False)

def maintain(force=False):
    """Throttled cap/prune pass: records/ and notes/ size caps, per-target note counts, orphan tmp files."""
    if _maint['busy'] or (not force and time.time() - _maint['last'] < MAINTAIN_INTERVAL):
        return
    _maint['busy'] = True
    try:
        _sweep_orphan_tmp()
        if NOTES.exists():
            for d in NOTES.iterdir():
                if d.is_dir(): _prune_files(d, NOTES_PER_TARGET)
        _cap_tree(RECORDS, RECORDS_CAP_BYTES); _cap_tree(NOTES, NOTES_CAP_BYTES)
    except Exception:
        pass
    finally:
        _maint['last'] = time.time(); _maint['busy'] = False

def sweep_tmp():
    """Delete stale compiler scratch (anything older than 10 minutes) and orphan state tmp files; run a full maintenance pass. Call at server start."""
    if TMP.exists():
        for d in TMP.iterdir():
            try:
                if time.time() - d.stat().st_mtime > TMP_MAX_AGE:
                    shutil.rmtree(d, ignore_errors=True)
            except OSError:
                pass
    maintain(force=True)

# ---------------------------------------------------------------- claims / listing
def _band(size):
    return '<=255' if size <= 255 else '256-511' if size <= 511 else '512-1K' if size <= 1023 else '1K-4K' if size <= 4095 else '4K+'

def list_functions(band='', limit=100, cursor=''):
    cat = catalog(); s = state()
    with LOCK:
        if _expire(s): _write(STATE, s)
    rows = []
    for tid, t in cat.items():
        if band and _band(t['size']) != band: continue
        c = s['claims'].get(tid)
        st = 'accepted' if t['address'] in s.get('accepted', {}) else ('held' if c else 'open')
        rows.append(dict(target_id=tid, address=t['address'], size=t['size'], band=_band(t['size']), kind=t['kind'], compiler=t['compiler'], state=st, working_now=1 if c else 0))
    rows.sort(key=lambda r: (-r['size'], r['address']))
    if cursor and cursor.isdigit(): rows = rows[int(cursor):]; off = int(cursor)
    else: off = 0
    page = rows[:limit]
    allopen = sum(1 for t in cat.values())
    return dict(source='local-targets', total_targets=allopen, open=sum(1 for r in rows if r['state'] == 'open'), functions=page,
                next_cursor=str(off + limit) if len(rows) > limit else None, order='size descending (largest first)',
                how_to_claim='request_function(address=<address>, model=..., agent_id=..., request_id=<32 hex>)')

def claim(request_id, model, band, agent_id, address):
    with LOCK:
        s = state()
        if _expire(s): pass
        if request_id in s['requests']:
            return s['requests'][request_id]
        if not agent_id:
            return dict(request_id=request_id, state='refused', reason='agent_id is required (a stable unique id such as claude_01); it is needed for every later call on the claim')
        cat = catalog(); agent = agent_id
        mine = [tid for tid, c in s['claims'].items() if c['agent_id'] == agent]
        if mine:
            res = dict(request_id=request_id, state='refused', reason='this agent_id already holds %s; finish it, submit_function or give_up_function first' % mine[0], target_id=mine[0])
            return res
        chosen = None
        if address:
            for tid, t in cat.items():
                if t['address'] == address.lower(): chosen = tid; break
            if not chosen:
                return dict(request_id=request_id, state='refused', reason='address is not a local target; browse list_available_functions')
            if chosen in s['claims']:
                return dict(request_id=request_id, state='refused', reason='held by another agent until %s; choose another' % s['claims'][chosen]['expires'], target_id=chosen)
            if cat[chosen]['address'] in s.get('accepted', {}):
                return dict(request_id=request_id, state='refused', reason='already accepted', target_id=chosen)
        else:
            order = sorted(cat.items(), key=lambda kv: (-kv[1]['size'], kv[1]['address']))
            for tid, t in order:
                if tid in s['claims'] or t['address'] in s.get('accepted', {}): continue
                if t['kind'] not in ('function',): continue
                if band and _band(t['size']) != band: continue
                chosen = tid; break
            if not chosen:
                return dict(request_id=request_id, state='refused', reason='no open function in that band')
        t = cat[chosen]
        s['claims'][chosen] = dict(agent_id=agent, model=model[:300], since=iso(), expires=iso(now() + timedelta(seconds=LEASE_SECONDS)), request_id=request_id)
        res = dict(request_id=request_id, state='working', target_id=chosen, address=t['address'], size=t['size'], kind=t['kind'], compiler=t['compiler'], flags=t['flags'],
                   expires_utc=s['claims'][chosen]['expires'], next='get_context(target_id, section="index"), then check_candidate(target_id, source, model, agent_id)')
        s['requests'][request_id] = res
        if len(s['requests']) > 5000:
            for k in list(s['requests'])[:1000]: del s['requests'][k]
        _write(STATE, s)
        return res

def work_status(request_id='', target_id='', agent_id=''):
    s = state(); out = {}
    if request_id: out['operation'] = s['requests'].get(request_id, dict(state='unknown'))
    if target_id:
        c = s['claims'].get(target_id)
        out['target'] = dict(target_id=target_id, state='working' if c else 'open', expires_utc=c['expires'] if c else None, yours=bool(c and agent_id and c['agent_id'] == agent_id))
    return out

def _own_claim(target_id, agent_id):
    s = state(); c = s['claims'].get(target_id)
    if not c: raise ValueError('No live claim on this target; request_function first (claims last 2 hours)')
    if not agent_id: raise ValueError('agent_id is required for this call')
    if not hmac.compare_digest(str(c['agent_id']), str(agent_id)): raise ValueError('Claim belongs to another agent_id')
    return s, c

def renew(target_id, agent_id):
    with LOCK:
        s = state(); c = s['claims'].get(target_id)
        if c and agent_id and c['agent_id'] == agent_id:
            c['expires'] = iso(now() + timedelta(seconds=LEASE_SECONDS)); _write(STATE, s)

def require_claim(target_id, agent_id):
    """check_candidate gate: the caller must hold the live claim (cheap guard against agents sharing a function)."""
    with LOCK:
        s = state()
        if _expire(s): _write(STATE, s)
        c = s['claims'].get(target_id)
        if not c: raise ValueError('Claim this function first with request_function(address=...); no live claim on %s' % target_id)
        if not agent_id: raise ValueError('agent_id is required for this call')
        if not hmac.compare_digest(str(c['agent_id']), str(agent_id)): raise ValueError('This function is claimed by another agent_id')

# ---------------------------------------------------------------- best partial source (hand-off to the next agent)
BEST_MAX_SOURCE = 24 * 1024
def _scrub_source(text):
    text = str(text)
    for rx in _PATH_RES:
        text = rx.sub('<path>', text)
    return text[:BEST_MAX_SOURCE]

def _save_best(target_id, reason, agent_id, model):
    """Before candidates are deleted: keep the closest checked candidate (fewest differing bytes) in notes/<target>/best.json.
    Replaces an existing one only if strictly closer. Never raises. (Records hold no source, so there is no startup backfill.)"""
    try:
        cands = ATTEMPTS / target_id / 'mcp_candidates'
        if not cands.is_dir(): return
        best = None
        for d in cands.iterdir():
            chk = _read(d / 'check.json', {})
            n = chk.get('diff_bytes')
            if chk.get('status') not in ('mismatch', 'match') or not isinstance(n, int) or not (d / 'candidate.cpp').exists(): continue
            key = (n, abs((chk.get('compiled_extent') or 0) - (catalog().get(target_id, {}).get('size') or 0)))
            if best is None or key < best[0]: best = (key, d, chk)
        if best is None: return
        key, d, chk = best; n = key[0]
        old = _read(NOTES / target_id / 'best.json', {})
        if isinstance(old.get('diff_bytes'), int) and (old['diff_bytes'], abs((old.get('compiled_extent') or 0) - (old.get('target_size') or 0))) <= key: return
        rec = _read(RECORDS / target_id / (d.name + '.json'), {})
        t = catalog().get(target_id, {})
        _write(NOTES / target_id / 'best.json', dict(
            kind='best', source=_scrub_source((d / 'candidate.cpp').read_text(encoding='utf-8', errors='replace')),
            status=chk.get('status'), diff_bytes=n, compiled_extent=chk.get('compiled_extent'), target_size=t.get('size'), relocation_mismatches=rec.get('relocation_mismatches'),
            compiler=chk.get('compiler'), flags_override=chk.get('flags_override', ''), entry=chk.get('entry', ''),
            agent=agent_id or rec.get('agent', ''), model=(model or rec.get('model') or '')[:120], utc=iso(), reason=_scrub(reason)[:430],
            source_sha256=chk.get('source_sha256')))
    except Exception:
        pass

def previous_best(target_id):
    """Field for request_function / get_context: kept best partial source plus the last 3 give-up reasons. None without best.json."""
    b = _read(NOTES / target_id / 'best.json', None)
    if not b or not b.get('source'): return None
    reasons = []
    d = NOTES / target_id
    if d.exists():
        rel = [v for v in (_read(f, {}) for f in d.glob('*.json') if f.name != 'best.json') if v.get('kind') == 'release']
        rel.sort(key=lambda v: v.get('utc') or '')
        reasons = [dict(utc=v.get('utc'), reason=_scrub(v.get('reason', ''))[:200]) for v in rel[-3:]]
    return dict(label='Unverified work from an earlier agent: start from it if useful, but it is not a match; every submit is rechecked.',
                source=_scrub_source(b['source']), status=b.get('status'), diff_bytes=b.get('diff_bytes'), compiled_extent=b.get('compiled_extent'), target_size=b.get('target_size'),
                relocation_mismatches=b.get('relocation_mismatches'), compiler=b.get('compiler'), flags=b.get('flags_override') or None,
                entry=b.get('entry') or None, saved_utc=b.get('utc'), model=b.get('model'), last_give_up_reasons=reasons)

def claim_owner_previous_best(target_id, agent_id):
    c = state()['claims'].get(target_id)
    if c and agent_id and hmac.compare_digest(str(c['agent_id']), str(agent_id)): return previous_best(target_id)
    return None

def give_up(target_id, reason, request_id, agent_id):
    with LOCK:
        s = state()
        if request_id in s['requests']: return s['requests'][request_id]
        s2, c = _own_claim(target_id, agent_id)
        t = catalog()[target_id]
        _write(NOTES / target_id / (uuid.uuid4().hex[:12] + '.json'), dict(kind='release', agent=c['agent_id'], utc=iso(), reason=reason[:430]))
        _prune_files(NOTES / target_id, NOTES_PER_TARGET); maintain()
        _save_best(target_id, reason, c['agent_id'], c.get('model'))
        del s['claims'][target_id]; _release_files(target_id)
        res = dict(request_id=request_id, state='released', target_id=target_id, reason=reason[:430], note='your closest checked source (if any) is kept and given to the next agent as previous_best; other candidate sources deleted; attempt records kept')
        s['requests'][request_id] = res; _write(STATE, s)
        return res

def submit(target_id, candidate_id, source_sha256, request_id, agent_id):
    # Phase 1 (locked, quick): validate ownership and the stored candidate.
    with LOCK:
        s = state()
        if request_id in s['requests']: return s['requests'][request_id]
        s2, c = _own_claim(target_id, agent_id)
        t, pack = target(target_id)
        cand = pack / 'mcp_candidates' / candidate_id / 'candidate.cpp'
        if not cand.exists(): raise ValueError('Candidate source no longer stored; check it again')
        if hashlib.sha256(cand.read_bytes()).hexdigest() != source_sha256: raise ValueError('source_sha256 does not match the stored candidate')
        source = cand.read_text(encoding='utf-8')
        owner, model, claim_req = c['agent_id'], c['model'], c['request_id']
        dest = CONTRIB / ('FUN_%s.cpp' % t['address'][2:])
        if dest.exists(): raise ValueError('a contribution for this address already exists; owner must review')
    # Phase 2 (NOT locked): fresh recheck compile, up to 180 s; other agents keep working meanwhile.
    prior = _read(cand.parent / 'check.json', {})   # the recheck uses exactly the flags/entry the candidate matched with
    fresh = check(target_id, source, model, owner, compiler=prior.get('compiler') or '', flags=prior.get('flags_override') or '', entry=prior.get('entry') or '')
    if fresh.get('status') != 'match':
        return dict(request_id=request_id, state='refused', reason='fresh recheck did not match', recheck=fresh)
    # Phase 3 (locked): re-verify the claim is still ours and the contribution is still absent, then commit.
    with LOCK:
        s = state()
        if request_id in s['requests']: return s['requests'][request_id]
        c = s['claims'].get(target_id)
        if not c or c['agent_id'] != owner or c['request_id'] != claim_req:
            raise ValueError('claim changed or expired during the recheck; nothing submitted, request_function again')
        if t['address'] in s.get('accepted', {}): raise ValueError('this address was accepted meanwhile')
        CONTRIB.mkdir(parents=True, exist_ok=True)
        try:
            with open(dest, 'x', encoding='utf-8', newline='') as fh: fh.write(source)
        except FileExistsError:
            raise ValueError('a contribution for this address already exists; owner must review')
        s.setdefault('accepted', {})[t['address']] = dict(utc=iso(), agent=owner, model=model, sha256=source_sha256, compiler=fresh['compiler'], flags=fresh.get('flags'))
        del s['claims'][target_id]; _release_files(target_id); (NOTES / target_id / 'best.json').unlink(missing_ok=True)
        res = dict(request_id=request_id, state='submitted', target_id=target_id, verified='fresh recheck MATCH', note='staged for owner review; not applied to the source tree')
        s['requests'][request_id] = res; _write(STATE, s)
        return res

def checkpoint(target_id, agent_id, request_id, **fields):
    with LOCK:
        s2, c = _own_claim(target_id, agent_id)
        notes = sorted((NOTES / target_id).glob('cp-*.json')) if (NOTES / target_id).exists() else []
        for old in notes[:-9]: old.unlink(missing_ok=True)
        entry = {k: (v[:2000] if isinstance(v, str) else v) for k, v in fields.items() if v}
        entry.update(agent=c['agent_id'], utc=iso(), request_id=request_id)
        _write(NOTES / target_id / ('cp-%s-%s.json' % (iso().replace(':', ''), uuid.uuid4().hex[:6])), entry)
        _prune_files(NOTES / target_id, NOTES_PER_TARGET); maintain()
        renew(target_id, agent_id)
        return dict(request_id=request_id, state='saved', target_id=target_id)

def history(target_id, agent_id, limit=5):
    items = []
    for d in ((NOTES / target_id), (RECORDS / target_id)):
        if d.exists():
            for f in sorted(d.glob('*.json'))[-limit:]:
                v = _read(f, {}); v.pop('source', None); items.append(v)
    items.sort(key=lambda v: v.get('utc') or v.get('finished_utc') or '')
    return dict(target_id=target_id, entries=items[-limit * 2:], note='attempt records and your notes only; no other worker data')

def flag(target_id, category, note, request_id, agent_id):
    with LOCK:
        _own_claim(target_id, agent_id)
        _write(NOTES / target_id / ('flag-%s.json' % uuid.uuid4().hex[:10]), dict(kind='flag', category=category[:80], note=note[:600], agent=agent_id, utc=iso()))
        _prune_files(NOTES / target_id, NOTES_PER_TARGET); maintain()
        return dict(request_id=request_id, state='recorded', target_id=target_id)

def summary():
    cat = catalog()
    c = collections.Counter(t['kind'] for t in cat.values())
    return dict(enabled=enabled(), targets=len(cat), by_kind=dict(c), claimed=len(state()['claims']), accepted=len(state().get('accepted', {})))
