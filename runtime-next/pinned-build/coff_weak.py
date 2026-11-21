"""Fail-closed x86 COFF weak-external auxiliary-record inspection.

A characteristic 2 fallback requires a linker library search and is not
resolved by this helper. The caller must first try its normal strong-symbol
resolution and must provide the same normal lookup for each fallback symbol.
"""
import struct

STORAGE_WEAK_EXTERNAL = 105
SUPPORTED_SEARCH = frozenset((1, 3))  # NOLIBRARY / ALIAS; library-search (2) deferred

class WeakResolutionError(ValueError):
    pass


def fallback_index(coff, index, *, allow_unsupported=False):
    """Return a validated fallback symbol index, None for a non-weak symbol.

    Invalid, cyclic or unsupported weak records raise rather than manufacture
    a reference-derived target. This reads metadata only, not executable bytes.
    """
    symbol = coff.symbols.get(index)
    if symbol is None: raise WeakResolutionError('missing symbol index')
    if symbol['storage'] != STORAGE_WEAK_EXTERNAL: return None
    try:
        symptr, count = struct.unpack_from('<II', coff.data, 8)
        if symptr < 20 or symptr + 18 * count > len(coff.data):
            raise WeakResolutionError('truncated or invalid symbol table')
        if index < 0 or index >= count: raise WeakResolutionError('symbol index outside table')
        pos = symptr + 18 * index
        raw = struct.unpack_from('<8sIhHBB', coff.data, pos)
        if (raw[1] != 0 or raw[2] != 0 or raw[3] not in (0, 0x20) or
            raw[4] != STORAGE_WEAK_EXTERNAL or raw[5] != 1 or index + 1 >= count):
            raise WeakResolutionError('invalid weak external primary or auxiliary count')
        if (symbol.get('value') != raw[1] or symbol.get('section') != raw[2] or
            symbol.get('type') != raw[3] or symbol.get('storage') != raw[4]):
            raise WeakResolutionError('parsed weak symbol differs from COFF record')
        if raw[0][:4] == b'\0' * 4:
            string_start = symptr + 18 * count
            string_len = struct.unpack_from('<I', coff.data, string_start)[0]
            string_offset = struct.unpack_from('<I', raw[0], 4)[0]
            if string_len < 4 or string_start + string_len > len(coff.data) or not 4 <= string_offset < string_len:
                raise WeakResolutionError('invalid weak symbol string table')
            end = coff.data.find(b'\0', string_start + string_offset, string_start + string_len)
            if end < 0: raise WeakResolutionError('unterminated weak symbol name')
            encoded_name = bytes(coff.data[string_start + string_offset:end])
        else:
            encoded_name = raw[0].split(b'\0', 1)[0]
        if encoded_name != symbol.get('name', '').encode('utf8'):
            raise WeakResolutionError('weak symbol name differs from COFF record')
        aux = coff.data[pos + 18:pos + 36]
        if len(aux) != 18 or any(aux[8:]):
            raise WeakResolutionError('invalid reserved weak auxiliary bytes')
        tag, characteristic = struct.unpack_from('<II', aux)
    except (struct.error, OverflowError) as exc:
        raise WeakResolutionError('truncated weak auxiliary record') from exc
    if characteristic not in (1, 2, 3):
        raise WeakResolutionError('invalid weak search characteristic %d' % characteristic)
    if characteristic == 2 and not allow_unsupported:
        raise WeakResolutionError('unsupported weak search characteristic 2')
    if tag not in coff.symbols: raise WeakResolutionError('weak fallback is invalid or auxiliary symbol')
    if coff.symbols[tag].get('storage') not in (2, STORAGE_WEAK_EXTERNAL):
        raise WeakResolutionError('weak fallback is not external')
    return tag


def validate_chain(coff, index):
    """Validate weak metadata and reject cycles without resolving a fallback."""
    visited = set()
    while True:
        if index in visited: raise WeakResolutionError('cyclic weak fallback')
        visited.add(index)
        next_index = fallback_index(coff, index, allow_unsupported=True)
        if next_index is None: return
        index = next_index


def resolve_fallback(coff, index, normal_lookup):
    """Follow weak fallbacks with cycle/ambiguity checks; return lookup result.

    `normal_lookup(symbol)` returns (source, value), or (None, None). The caller
    has already attempted the primary symbol. A defined same-name symbol in the
    object may resolve an undefined fallback, but conflicting values fail closed.
    """
    visited = set()
    while True:
        if index in visited: raise WeakResolutionError('cyclic weak fallback')
        visited.add(index)
        index = fallback_index(coff, index)
        if index is None: return None, None
        if index in visited: raise WeakResolutionError('cyclic weak fallback')
        target = coff.symbols[index]
        # A weak intermediate must itself be structurally valid, even when a
        # mapping exists under its name; malformed metadata is never accepted.
        if target.get('storage') == STORAGE_WEAK_EXTERNAL:
            fallback_index(coff, index)
        alternatives = [target] + [s for s in coff.by_name.get(target['name'], ())
                                   if s is not target and s.get('section', 0) > 0 and s.get('storage') == 2]
        matches = []
        for candidate in alternatives:
            src, value = normal_lookup(candidate)
            if src is not None and value is not None: matches.append((src, value))
        if matches:
            if len({value for _, value in matches}) != 1:
                raise WeakResolutionError('ambiguous weak fallback target')
            src, value = matches[0]
            return 'weak-fallback/' + src, value
        if target['storage'] != STORAGE_WEAK_EXTERNAL: return None, None

