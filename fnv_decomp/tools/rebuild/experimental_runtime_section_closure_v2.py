"""Experimental in-memory runtime COFF section closure; not a MATCH or provider.

No filesystem, compiler, linker, or publication API. Callers must independently
review exact source, object identity, root selection, and application-level roots.
Conservatively retain every SafeSEH handler, initializer/TLS section and local
relocation dependency. Unsupported structures fail closed.
"""
import re
import struct
import coff_code_archive as coff

POLICY = 'experimental-runtime-section-closure-v2'


def _need(condition, message):
    if not condition:
        raise ValueError(message)


def project(raw, root_index, expected_sha256):
    _need(type(raw) is bytes and coff.digest(raw) == expected_sha256, 'object identity mismatch')
    obj = coff.parse(raw)
    sections, symbols = obj['sections'], obj['symbols']
    _need(type(root_index) is int and root_index in symbols, 'root symbol absent')
    root = symbols[root_index]
    _need(root['storage'] == 2 and root['section'] > 0 and root['type'] == 32 and
          root['value'] == 0 and not root['aux_count'], 'unsupported root identity')
    # Weak fallback edges and unknown classes can create implicit roots.
    _need(not any(s['storage'] == 105 for s in symbols.values()), 'WEAK_EXTERNAL_UNSUPPORTED')
    _need(all(s['storage'] in (2, 3, 6, 103) for s in symbols.values()), 'UNKNOWN_SYMBOL_CLASS')
    for s in symbols.values():
        if s['aux_count'] and s['storage'] != 103:
            _need(s['storage'] == 3 and s['section'] > 0 and s['type'] == 0 and s['aux_count'] == 1 and s['name'] == sections[s['section']]['name'], 'UNKNOWN_AUXILIARY_RECORD')
        if s['storage'] == 103:
            _need(s['section'] == -2, 'UNKNOWN_FILE_RECORD')
    assoc = {}
    section_definitions = {}
    for i, s in symbols.items():
        if s['storage'] == 3 and s['section'] > 0 and s['type'] == 0 and s['aux_count']:
            _need(s['aux_count'] == 1 and s['name'] == sections[s['section']]['name'], 'UNKNOWN_SECTION_AUX')
            length, nr, nl, checksum, parent, selection, reserved, high = struct.unpack('<IHHIhBBH', s['aux'])
            sec = sections[s['section']]
            _need(s['section'] not in section_definitions, 'DUPLICATE_SECTION_DEFINITION')
            section_definitions[s['section']] = (i, selection, checksum)
            _need(bool(sec['flags'] & 0x1000) == bool(selection), 'COMDAT_FLAG_SELECTION_MISMATCH')
            _need(length == sec['size'] and nr == len(sec['relocs']) and not nl and not reserved and not high,
                  'BAD_SECTION_AUX')
            if selection == 5:
                _need(parent in sections and parent != s['section'], 'BAD_ASSOCIATION')
                _need(s['section'] not in assoc, 'DUPLICATE_ASSOCIATION')
                assoc[s['section']] = parent
            else:
                _need(selection in (0,1,2,3,4,6,7) and parent == 0, 'UNKNOWN_COMDAT_POLICY')
    _need(set(section_definitions) == set(sections), 'MISSING_SECTION_DEFINITION')
    for sec in sections.values():
        n = sec['name'].lower()
        _need(n in ('.text', '.data', '.bss', '.rdata', '.xdata', '.debug$s', '.drectve', '.sxdata', '.tls', '.crt') or any(n.startswith(p+'$') for p in ('.text', '.data', '.bss', '.rdata', '.xdata', '.tls', '.crt')), 'UNKNOWN_SECTION_METADATA')
    for child in assoc:
        seen = set(); node = child
        while node in assoc:
            _need(node not in seen, 'ASSOCIATION_CYCLE')
            seen.add(node); node = assoc[node]
    # An object contributes all non-COMDAT sections when loaded.
    roots = {root['section']} | {i for i in sections if section_definitions[i][1] == 0}
    sx_indices = []
    for i, sec in sections.items():
        n = sec['name']
        if n == '.drectve':
            _need(not sec['relocs'], 'DIRECTIVE_RELOCATIONS_UNSUPPORTED')
            text = sec['payload'].decode('ascii', 'strict')
            tokens = re.findall(r'/DEFAULTLIB:"[^"\r\n]+"', text, re.I)
            remaining = re.sub(r'/DEFAULTLIB:"[^"\r\n]+"', '', text, flags=re.I)
            _need(not remaining.strip() and tokens, 'DIRECTIVE_OPERATION_UNSUPPORTED')
            roots.add(i)
        elif n.lower().startswith(('.crt', '.tls', '.ctors', '.init', '.fini')):
            roots.add(i)
        elif n == '.sxdata':
            _need(not sx_indices and not sec['relocs'] and sec['size'] == len(sec['payload']) and
                  sec['size'] % 4 == 0, 'SAFESEH_SECTION_UNSUPPORTED')
            sx_indices.append(i); roots.add(i)
    registrations = []
    if sx_indices:
        sx = sx_indices[0]; sec = sections[sx]
        registrations = list(struct.unpack('<' + 'I' * (sec['size']//4), sec['payload']))
        _need(len(registrations) == len(set(registrations)), 'SAFESEH_DUPLICATE')
        for index in registrations:
            _need(index in symbols, 'SAFESEH_ABSENT_SYMBOL')
            s = symbols[index]
            _need(s['section'] > 0 and s['type'] == 32 and s['storage'] in (2,3) and
                  not s['aux_count'] and s['value'] < sections[s['section']]['size'], 'SAFESEH_HANDLER_UNSUPPORTED')
            roots.add(s['section'])
    keep = set(roots)
    while True:
        before = len(keep)
        for child, parent in assoc.items():
            if child in keep or parent in keep:
                keep.update((child, parent))
        for i in list(keep):
            for _, target, kind in sections[i]['relocs']:
                _need(kind in (6,20), 'RELOCATION_KIND_UNSUPPORTED')
                s = symbols[target]
                _need(s['storage'] in (2,3) and not (s['section'] == 0 and s['value']),
                      'RELOCATION_TARGET_UNSUPPORTED')
                if s['section'] > 0:
                    keep.add(s['section'])
                else:
                    _need(s['section'] == 0, 'ABSOLUTE_TARGET_UNSUPPORTED')
        if len(keep) == before:
            break
    _need(all(len(sections[i]['payload']) == sections[i]['size'] for i in keep), 'UNBACKED_SECTION_UNSUPPORTED')
    chosen = {i for i,s in symbols.items() if s['section'] in keep}
    for i in keep:
        chosen.update(target for _,target,_ in sections[i]['relocs'])
    chosen.update(registrations)
    # Compiler metadata constants are preserved where they are supported.
    chosen.update(i for i,s in symbols.items() if s['section'] == -1 and s['storage'] == 3 and
                  s['name'] in ('@feat.00','@comp.id'))
    _need(all(symbols[i]['storage'] in (2,3) for i in chosen), 'SELECTED_SYMBOL_CLASS_UNSUPPORTED')
    intermediate, maps = coff.serialize(raw, sorted(keep), sorted(chosen))
    final = bytearray(intermediate)
    if sx_indices:
        sx = sx_indices[0]; mapped = maps['section_map'][sx]
        # Keep the complete table and update each physical symbol index only.
        pos = struct.unpack_from('<I', intermediate, 20 + 40*(mapped-1) + 20)[0]
        for ordinal, old in enumerate(registrations):
            _need(old in maps['symbol_map'], 'SAFESEH_HANDLER_OMITTED')
            struct.pack_into('<I', final, pos + 4*ordinal, maps['symbol_map'][old])
        sx_symbol, sx_selection, old_checksum = section_definitions[sx]
        _need(sx_selection == 0, 'SAFESEH_COMDAT_UNSUPPORTED')
        aux_slot = maps['auxiliary_map'][sx_symbol + 1]
        mapped_obj = coff.parse(intermediate)
        checksum_pos = mapped_obj['symbol_pointer'] + 18*aux_slot + 8
        # Existing parent-EH extractor clears this advisory field after a table rewrite.
        struct.pack_into('<I', final, checksum_pos, 0)
        allowed = set(range(pos, pos + 4*len(registrations))) | set(range(checksum_pos, checksum_pos+4))
        _need(all(a == b or i in allowed for i,(a,b) in enumerate(zip(intermediate,final))),
              'UNEXPECTED_SAFESEH_MUTATION')
        after = coff.parse(bytes(final)); expected = [maps['symbol_map'][x] for x in registrations]
        _need(list(struct.unpack('<'+'I'*len(expected), after['sections'][mapped]['payload'])) == expected,
              'SAFESEH_REMAP_FAILED')
        _need(struct.unpack_from('<I', after['symbols'][maps['symbol_map'][sx_symbol]]['aux'], 8)[0] == 0, 'SAFESEH_CHECKSUM_CLEAR_FAILED')
    else:
        coff.parse(bytes(final))
    return bytes(final), dict(policy=POLICY, input_sha256=expected_sha256, output_sha256=coff.digest(bytes(final)),
        root_index=root_index, root_section=root['section'], retained_sections=sorted(keep),
        retained_safe_seh_indices=registrations, safeseh_checksum_policy='zero-after-index-remap' if sx_indices else None, section_map=maps['section_map'], symbol_map=maps['symbol_map'],
        auxiliary_map=maps['auxiliary_map'], original_byte_match_claimed=False,
        application_initializer_closure_proved=False, provider_or_ABI_approved=False, runtime_ready=False)
