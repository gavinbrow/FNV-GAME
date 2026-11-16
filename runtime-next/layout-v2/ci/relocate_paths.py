"""Rewrite hard-coded absolute paths in the build-path scripts into env-overridable expressions with today's value as default.
  python relocate_paths.py [--apply]      (dry run by default; --apply writes, with a .bak-wA copy next to each file)
Each STRING token that starts with a known root becomes  (__import__('os').environ.get('<VAR>', <default>) + <rest>)  - no imports needed, works under python -I.
Roots (longest first): FNV_MSVC9_RTM_ROOT, FNV_MSVC9_ROOT (SP1 toolchain), FNV_REF_IMAGE (decrypted reference image, read only), FNV_GAME_DIR, FNV_PY_SITE, FNV_PROJ_ROOT."""
import tokenize, io, os, sys, json, re
BS = chr(92)
def W(p): return p.replace('/', BS)
P = 'C:' + BS + 'Projects' + BS + 'Decompilation'
ROOTS = [  # (default path, env var)
    (P + BS + 'FNV' + BS + 'work' + BS + 'worker1' + BS + 'FalloutNV.runtime-text.exe', 'FNV_REF_IMAGE'),
    (P + BS + 'FNV' + BS + 'tools' + BS + 'vc2008rtm', 'FNV_MSVC9_RTM_ROOT'),
    (P + BS + 'FNV' + BS + 'tools' + BS + 'vc2008', 'FNV_MSVC9_ROOT'),
    ('C:' + BS + 'Program Files (x86)' + BS + 'Steam' + BS + 'steamapps' + BS + 'common' + BS + 'Fallout New Vegas', 'FNV_GAME_DIR'),
    ('C:' + BS + 'Users' + BS + 'cjhub' + BS + 'AppData' + BS + 'Roaming' + BS + 'Python' + BS + 'Python312' + BS + 'site-packages', 'FNV_PY_SITE'),
    (P, 'FNV_PROJ_ROOT'),
]
def match_root(body):
    nb = body.replace('/', BS).replace(BS + BS, BS)
    for root, var in ROOTS:
        if nb.lower().startswith(root.lower()):
            rest_start = len(body)
            # find how many raw chars of body correspond to root (body may use / or doubled backslashes)
            i = 0; j = 0
            while j < len(root):
                c = body[i]
                if c == BS and i + 1 < len(body) and body[i + 1] == BS: i += 2
                else: i += 1
                j += 1
            return root, var, body[i:]
    return None
def rewrite(src):
    out = []; toks = list(tokenize.generate_tokens(io.StringIO(src).readline)); changes = []
    lines = src.split('\n'); edits = []
    for t in toks:
        if t.type != tokenize.STRING: continue
        s = t.string; m = re.match(r'^([rRbBuU]*)(\'\'\'|"""|\'|")', s)
        if not m or m.group(2) in ("'''", '"""') or 'f' in m.group(1).lower(): continue
        pre, q = m.group(1), m.group(2); body = s[len(pre) + len(q):-len(q)]
        r = match_root(body)
        if not r: continue
        root, var, rest = r
        if "environ.get('" in lines[t.start[0] - 1][:t.start[1]][-60:]: continue   # already an env default
        israw = 'r' in pre.lower(); fwd = '/' in body.split(root[3:8])[0] if False else (body.find('/') >= 0 and body.find(BS) < 0)
        d = repr(root) if not israw else 'r' + "'" + root + "'"
        env = "__import__('os').environ.get('%s', %s)" % (var, d)
        if fwd: env = env + ".replace(%s, '/')" % repr(BS)
        if rest:
            lit = (pre + q + rest + q)
            new = '(%s + %s)' % (env, lit)
        else: new = '(%s)' % env
        edits.append((t.start, t.end, new, s))
    # apply from the end
    for (sr, sc), (er, ec), new, old in sorted(edits, reverse=True):
        assert sr == er, 'multiline string'
        ln = lines[sr - 1]; assert ln[sc:ec] == old, (ln[sc:ec], old)
        lines[sr - 1] = ln[:sc] + new + ln[ec:]
    return '\n'.join(lines), len(edits)
if __name__ == '__main__':
    apply = '--apply' in sys.argv
    files = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scan_deps.json')))
    tot = 0
    for f, hits in files.items():
        if not hits: continue
        src = open(f, encoding='utf-8', errors='surrogateescape', newline='').read()
        crlf = '\r\n' in src
        new, n = rewrite(src.replace('\r\n', '\n'))
        if crlf: new = new.replace('\n', '\r\n')
        left = [m.group(0)[:80] for m in re.finditer('C:[' + BS + BS + '/]+(?:Projects|Users|Program)[^' + chr(39) + chr(34) + ']*', new) if "environ.get" not in new[max(0, m.start() - 60):m.start()]]
        print(os.path.relpath(f, P), 'edits', n, 'remaining literals', len(left), left[:2])
        tot += n
        if apply and n:
            import shutil; shutil.copy2(f, f + '.bak-wA'); open(f, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(new)
    print('total edits', tot, '(applied)' if apply else '(dry run)')
