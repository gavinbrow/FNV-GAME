r"""Source fix for 'call resolves to a different function than the original calls': the original constructs the object with the (address-named) constructor FUN_xxxxxxxx.
Adds `struct FUN_xxxxxxxx : public Base { FUN_xxxxxxxx(); };` before the enclosing function(s) and constructs that type at the given lines (the constructor itself is the
recipe function `??0FUN_xxxxxxxx@@QAE@XZ`, already placed). Backs the file up once (.bak-20261116-wB).
derive(rel_to_src, [(line_of_original_file, BaseName, NewName), ...])"""
import re, shutil, os
FN = 'C:/Projects/Decompilation/fnv_decomp/src/'


def derive(rel, uses, maxup=600):
    p = FN + rel
    if not os.path.exists(p + '.bak-20261116-wB'):
        shutil.copy(p, p + '.bak-20261116-wB')
    raw = open(p, 'rb').read().decode('latin1')
    nl = '\r\n' if '\r\n' in raw else '\n'
    L = raw.split(nl)
    decls = []
    for line, base, new in uses:
        i = line - 1
        pat = re.compile(r'\bnew\s+' + re.escape(base) + r'\b(?!\s*\[)')
        assert pat.search(L[i]), (rel, line, L[i])
        L[i] = pat.sub('new ' + new, L[i], count=1)
        d = 'struct %s : public %s { %s(); };' % (new, base, new)
        if d not in decls:
            decls.append(d)
    j = uses[0][0] - 1
    while j > 0 and not L[j].startswith('// @fnv'):
        j -= 1
    assert uses[0][0] - 1 - j < maxup, (rel, 'no @fnv marker')
    while j > 0 and L[j - 1].startswith('//'):
        j -= 1
    L[j:j] = decls
    open(p, 'wb').write(nl.join(L).encode('latin1'))
    print('ok', rel, [(u[0], u[2]) for u in uses])
