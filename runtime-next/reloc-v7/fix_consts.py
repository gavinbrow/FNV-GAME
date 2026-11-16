"""Source fix for the rebase residue 'we-shift-a-field-the-original-does-not-relocate': integer constants that the decompiled source wrote as the
address of a DAT_/FUN_/g_*_arg1 extern ((unsigned int)&DAT_00ffffff). Replaced by the literal constant. Backs each file up (.bak-20261116-wB).
usage: python -I fix_consts.py [--apply]   (dry run lists the edits)"""
import sys, json, re, bisect, collections, shutil, os
sys.dont_write_bytecode = True
FN = 'C:/Projects/Decompilation/fnv_decomp/'
R = 'C:/Projects/Decompilation/runtime-next/'
units = json.load(open(FN + 'build/units.json'))['units']
ranges = sorted((int(f['address'], 16), int(f['address'], 16) + f['size'], i) for i, x in enumerate(units) for f in x['functions'])
ks = [r[0] for r in ranges]
rr = json.load(open(R + 'reloc-v7/rebase_base.json'))['we-shift-a-field-the-original-does-not-relocate']
need = collections.defaultdict(dict)   # source -> {name: value}
for e in rr:
    f = int(e['field'], 16); r = ranges[bisect.bisect_right(ks, f) - 1]; assert r[0] <= f < r[1]
    m = re.match(r'\??_?(DAT_[0-9a-f]+|FUN_00a00000|g_[0-9a-f]+_arg1)', e['symbol'])
    if not m: print('skip (manual)', e); continue
    need[units[r[2]]['source']][m.group(1)] = int(e['value'], 16)
apply = '--apply' in sys.argv
touched = []
for src, names in sorted(need.items()):
    raw = open(FN + src, 'rb').read().decode('latin1'); new = raw; n = 0
    for name, val in names.items():
        lit = '0x%x' % val
        if name.startswith('g_'):
            pat = re.compile(r'(?<![\w])' + re.escape(name) + r'(?![\w])')
            def sub(m):
                return '((const char*)%s)' % lit
            # only the constructor-argument use (not 'extern' declarations)
            lines = new.split('\n'); out = []
            for l in lines:
                if pat.search(l) and not re.match(r'\s*(extern|//)', l) and '&' not in l:
                    l2 = pat.sub(sub, l); n += (l2 != l); l = l2
                elif pat.search(l) and re.search(r'&\s*' + re.escape(name), l) and not re.match(r'\s*(extern|//)', l):
                    l2 = re.sub(r'&\s*' + re.escape(name), '((char const* const*)%s)' % lit, l); n += (l2 != l); l = l2
                out.append(l)
            new = '\n'.join(out); continue
        mt = re.search(r'extern\s+(?:"C"\s+)?([\w\s\*:]+?)\s+' + re.escape(name) + r'\s*;', new)
        ty = (mt.group(1).strip() if mt else 'int')
        lines = new.split('\n'); out = []
        pat = re.compile(r'&\s*' + re.escape(name) + r'(?![\w])')
        for l in lines:
            if pat.search(l) and not re.match(r'\s*(extern|//)', l):
                l2 = pat.sub('((%s*)%s)' % (ty, lit), l); n += (l2 != l); l = l2
            out.append(l)
        new = '\n'.join(out)
    print(src, names, 'edits', n)
    if apply and new != raw:
        if not os.path.exists(FN + src + '.bak-20261116-wB'): shutil.copy(FN + src, FN + src + '.bak-20261116-wB')
        open(FN + src, 'wb').write(new.encode('latin1')); touched.append(src)
json.dump([i for i, u in enumerate(units) if u['source'] in touched], open(R + 'reloc-v7/edited_units_consts.json', 'w'))
