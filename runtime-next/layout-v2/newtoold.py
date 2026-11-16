import sys, numpy as np
m = np.load(sys.argv[1]); bs, be, NS, nb = m['bs'], m['be'], m['NS'], int(m['nbva'][0])
for a in sys.argv[2:]:
    v = int(a, 16) - nb; i = np.where((NS <= v) & (v < NS + (be - bs)))[0]
    print(a, '->', hex(0x401000 + int(bs[i[0]]) + v - int(NS[i[0]])) if len(i) else None)
