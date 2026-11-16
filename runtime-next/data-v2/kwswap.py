import re


def swap_keyword(raw, old, kw_ours, kw_orig):
    """class <-> struct for the definition of `old` (and its forward declarations) keeping default access and inheritance access."""
    nl = '\r\n' if '\r\n' in raw else '\n'
    m = re.search(r'\b' + kw_ours + r'\s+' + re.escape(old) + r'\b(?!\s*;)([^{;]*)\{', raw)
    if not m:
        return None
    head = m.group(1)
    if '<' in head:
        return None
    if kw_ours == 'struct':      # struct -> class: bases need explicit public, members need public:
        if ':' in head:
            pre, bases = head.split(':', 1)
            parts = [b.strip() for b in bases.split(',')]
            parts = [b if re.match(r'(public|private|protected)\b', b) or re.match(r'virtual\s+(public|private|protected)\b', b) else ('public ' + b) for b in parts]
            head2 = pre + ': ' + ', '.join(parts) + ' '
        else:
            head2 = head
        body_ins = nl + 'public:'
    else:                         # class -> struct: members need private:
        head2 = head
        body_ins = nl + 'private:'
    out = raw[:m.start()] + kw_orig + ' ' + old + head2 + '{' + body_ins + raw[m.end():]
    out = re.sub(r'\b' + kw_ours + r'(\s+' + re.escape(old) + r'\s*;)', kw_orig + r'\1', out)
    return out
