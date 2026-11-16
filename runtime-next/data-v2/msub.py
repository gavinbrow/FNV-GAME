import re


def mangle_sub2(s, old, new, kw_from=None, kw_to=None):
    """rename class `old` -> `new` inside mangled names; if the class keyword changed, the V/U type letter changes too"""
    o = re.escape(old)
    if kw_from and kw_to and kw_from != kw_to:
        lf = 'V' if kw_from == 'class' else 'U'
        lt = 'V' if kw_to == 'class' else 'U'
        s = re.sub(lf + o + '@', lt + new + '@', s)
    out = re.sub(r'(?<![A-Za-z_$])' + o + '@', new + '@', s)
    out = re.sub(r'(?<=\?\?_[GE])' + o + '@', new + '@', out)
    out = re.sub(r'(?<=[VU])' + o + '@', new + '@', out)
    return out
