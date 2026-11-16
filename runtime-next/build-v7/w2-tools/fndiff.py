import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0,'.'); sys.path.append(r'C:\Users\cjhub\AppData\Roaming\Python\Python312\site-packages')
import ehdiag as D
from capstone import *
md = Cs(CS_ARCH_X86, CS_MODE_32)
def lines(code, at): return [f"{i.address:x} {i.mnemonic} {i.op_str}" for i in md.disasm(code, at)]
if __name__ == '__main__':
    U = D.setup(); i = int(sys.argv[1]); addr = int(sys.argv[2], 16)
    if not U[i].get('eh_tails'): U[i]['eh_tails'] = [{'address': '0x0', 'size': 0, 'dummy': True}]
    r = D.A.process((i, U[i])); pe = D.A.G['pe']
    for rec in r['fn']:
        if rec['address'] == addr:
            print(rec['symbol'], rec['verdict'], rec['reason'], rec['size'])
            if rec['data'] is None: continue
            ref = pe.read(addr, rec['size']); d = rec['data']
            diff = [k for k in range(len(d)) if d[k] != ref[k]]
            print('ndiff', len(diff), diff[:10])
            if diff:
                a = max(0, diff[0] - 24)
                for x, y in zip(lines(d[a:], addr + a)[:14], lines(ref[a:], addr + a)[:14]): print('%-40s | %s' % (x, y))
