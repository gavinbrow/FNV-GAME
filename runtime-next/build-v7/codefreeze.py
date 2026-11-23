r"""Batch 12: the code stage without the reference image.

FNV_CODE_NOREF=1 (implied by FNV_M3_NOREF2=1 in build_all.py): build-v7 never opens the reference. Everything the reference used to supply as LAYOUT
(EH funclet addresses, CRT/STL placement, import slots, binding-overlay decisions, ICF map) is read from m3/frozen/code_*.json; no section byte is frozen.
FNV_CODE_FREEZE=1 (normal run, reference present): writes those files (assemble_v7.py / verify_v7.py call write()/merge()).
Files (m3/frozen/): code_eh.json code_crt.json code_contrib.json code_overlay.json code_meta.json code_icf_map.json (see m3/frozen/README.md)."""
import os, json, struct, hashlib
RN = os.path.join(os.environ.get('FNV_PROJ_ROOT') or r'C:\path\to\Decompilation', 'runtime-next')
FZDIR = os.environ.get('FNV_CODE_FROZEN_DIR') or os.path.join(RN, 'm3', 'frozen')
NOREF = os.environ.get('FNV_CODE_NOREF') == '1'
FREEZE = os.environ.get('FNV_CODE_FREEZE') == '1'
if NOREF and FREEZE: raise SystemExit('FNV_CODE_NOREF and FNV_CODE_FREEZE are exclusive')
_cache = {}


def path(name): return os.path.join(FZDIR, name)


def load(name):
    if name not in _cache:
        with open(path(name), 'r') as f: _cache[name] = json.load(f)
    return _cache[name]


def write(name, obj):
    os.makedirs(FZDIR, exist_ok=True)
    with open(path(name), 'w') as f: json.dump(obj, f, separators=(',', ':'), sort_keys=True)


def sha_file(name):
    with open(path(name), 'rb') as f: return hashlib.sha256(f.read()).hexdigest()


class PeMeta:
    """Stand-in for compare.Pe: header constants of the image from m3/frozen/pe_meta.json (no section bytes). read() always fails."""
    data = None

    def __init__(self):
        with open(os.path.join(FZDIR, 'pe_meta.json')) as f: m = json.load(f)
        self.base = m['base']; self.sections = []; self.names = []
        for s in m['sections']:
            self.sections.append((s['rva'], s['vs'], s['rs'], s['raw'])); self.names.append(s['name'])
        self.image_size = (max(r + v for r, v, _, _ in self.sections) + 0xfff) & ~0xfff

    def tls_start(self):
        for (rva, _, _, _), name in zip(self.sections, self.names):
            if name == '.tls': return self.base + rva
        return None

    def secrel(self, address):
        start = self.tls_start()
        for (rva, vs, _, _), name in zip(self.sections, self.names):
            if self.base + rva <= address < self.base + rva + max(vs, 1):
                if name != '.tls': raise ValueError('SECREL target is not thread-local (section %s)' % name)
                return address - start
        raise ValueError('SECREL target outside the image')

    def read(self, address, size):
        raise OSError('FNV_CODE_NOREF: the reference image must not be read (read of 0x%x+%d)' % (address, size))


def imports_thunks():
    m = load('code_meta.json')
    return dict(m['imports']), {int(k): v for k, v in m['thunks'].items()}


def refuse_reference(what):
    """Fail loudly when a no-ref run reaches a reference reader."""
    raise OSError('FNV_CODE_NOREF=1: %s would open the reference image' % what)
