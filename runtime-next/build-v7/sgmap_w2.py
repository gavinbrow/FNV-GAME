"""w2: bind string-literal labels ($SGnnnn) by content, not by number.

units.json 'symbols' names each string literal of a unit by the compiler's label ($SG<n>) and gives the address the original
placed it at. A source edit that adds or removes code before a string (for example a sized operator delete, which changes the
unwind code the compiler emits) renumbers every later label although the strings themselves are unchanged, so the by-name
binding fails. This module re-binds the labels of the recompiled object by what they contain:

  sidecar (made once from the object compiled before the edit + the recipe's symbols):
      {content_hex: [address, ...]}   addresses in label-number order, one entry per label with that content
  remap(coff, symbols, sidecar):
      every $SG label of the new object gets the address of the same content, taking the k-th label with that content to the k-th address.

Nothing is read from the reference image. A label whose content is not in the sidecar is left unbound.
"""
import re
_SG = re.compile(r'^\$SG(\d+)$')

def sg_labels(coff):
    """[(number, name, content_bytes)] for the object's $SG labels, in number order. Content is the symbol's bytes up to the next symbol of its section."""
    by_sec = {}
    for s in coff.symbols.values():
        if s['section'] > 0: by_sec.setdefault(s['section'], []).append(s['value'])
    out = []
    for s in coff.symbols.values():
        m = _SG.match(s['name'])
        if not m or s['section'] <= 0: continue
        sec = coff.sections[s['section']]; data = sec['data']
        nxt = sorted(v for v in by_sec[s['section']] if v > s['value'])
        end = nxt[0] if nxt else len(data)
        out.append((int(m.group(1)), s['name'], bytes(data[s['value']:end])))
    out.sort()
    return out

def make_sidecar(coff, symbols, global_symbols=None):
    """global_symbols: the recipe-wide {name: address} map the assembler falls back to when a unit's own map lacks the label"""
    side = {}
    for num, name, content in sg_labels(coff):
        if name in symbols: a = int(symbols[name], 0)
        elif global_symbols and name in global_symbols: a = int(global_symbols[name])
        else: continue
        side.setdefault(content.hex(), []).append(a)
    return side

def remap(coff, symbols, sidecar):
    new = {k: v for k, v in symbols.items() if not _SG.match(k)}
    used = {}
    for num, name, content in sg_labels(coff):
        addrs = sidecar.get(content.hex())
        if not addrs: continue
        k = used.get(content.hex(), 0); used[content.hex()] = k + 1
        if k < len(addrs): new[name] = '0x%08x' % addrs[k]
    return new
