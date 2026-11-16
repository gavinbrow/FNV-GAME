import sys, io, contextlib, pickle, json
sys.dont_write_bytecode = True
sys.path.insert(0, '.')
from concurrent.futures import ProcessPoolExecutor
import autosized as AS, w2lib as L
def job(i):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): AS.run(i)
    except Exception as e: buf.write('EXC %r\n' % (e,))
    open('auto/%04d.log' % i, 'w').write(buf.getvalue())
    return i, buf.getvalue().splitlines()[:1]
if __name__ == '__main__':
    rows = pickle.load(open(sys.argv[1], 'rb'))
    units = sorted({r['i'] for r in rows})
    if len(sys.argv) > 2: units = [u for u in units if u in set(map(int, sys.argv[2:]))]
    print(len(units), 'units', flush=True)
    with ProcessPoolExecutor(8, initializer=L.setup) as ex:
        for i, l in ex.map(job, units): print(i, l, flush=True)
