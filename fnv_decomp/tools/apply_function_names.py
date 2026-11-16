"""Apply docs/function-names.json to a COPY of src/ (e.g. the public export staging dir).

Usage: python tools/apply_function_names.py <dir-containing-copied-sources>

Replaces whole-identifier occurrences of FUN_<addr> with the new name in .cpp/.h/.inl files.
Refuses to run on the live src/ tree (the build keys on the FUN_<addr> identifiers).
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target = os.path.abspath(sys.argv[1])
if os.path.normcase(target).startswith(os.path.normcase(os.path.join(ROOT, 'src'))) or \
   os.path.normcase(target) == os.path.normcase(ROOT):
    sys.exit('refusing to rewrite the live source tree; pass a copy')
rows = json.load(open(os.path.join(ROOT, 'docs', 'function-names.json')))
sub = {r['old']: r['new'] for r in rows}
pat = re.compile(r'(?<![0-9A-Za-z_])(' + '|'.join(map(re.escape, sub)) + r')(?![0-9A-Za-z_])')
n = 0
for d, _, fs in os.walk(target):
    for fn in fs:
        if fn.endswith(('.cpp', '.h', '.inl')):
            p = os.path.join(d, fn)
            t = open(p, encoding='latin1', newline='').read()
            t2, k = pat.subn(lambda m: sub[m.group(1)], t)
            if k:
                open(p, 'w', encoding='latin1', newline='').write(t2)
                n += k
print('replaced', n, 'identifiers')
