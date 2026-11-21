"""Narrow opt-in validation of three literal RTTI name-tail fields.

This private helper performs no writes and does not alter production selection.
Call only after ordinary selector relocation/source ownership checks; on success
return the one value-rule address that must be excluded from ghost reloc counts.
"""
import hashlib,struct

def validate(record, section_bytes, relocs, value_fields, original_relocs, original_bytes, source_key, chunk_ranges, claims, rewrites, pin):
    if (record['va'],record['size'],record['unit'],record['kind'],record['section'],record['tier']) != (pin['va'],pin['size'],pin['unit'],'rtti0','.data','B'):
        raise ValueError('candidate identity differs')
    a,n=record['va'],record['size']; b=a+n
    if source_key != (pin['unit'],pin['unit_section_index']): raise ValueError('unit/section mismatch')
    if record['names'] != [pin['symbol']]: raise ValueError('definition or alias mismatch')
    if len(section_bytes)!=n or hashlib.sha256(section_bytes).hexdigest()!=pin['coff_data_sha256']: raise ValueError('COFF data mismatch')
    if len(original_bytes)!=n or hashlib.sha256(original_bytes).hexdigest()!=pin['reference_sha256']: raise ValueError('reference bytes mismatch')
    if original_relocs != [a] or relocs != [(0,6,'??_7type_info@@6B@',0,0x010f1ee0)]: raise ValueError('DIR32 provenance mismatch')
    if section_bytes[4:8]!=bytes(4) or not section_bytes[8:].startswith((b'.?AV',b'.?AU')) or not section_bytes[8:].endswith(b'@@\x00') or b'\x00' in section_bytes[8:-1]:raise ValueError('RTTI name shape')
    if pin['symbol'][5:-2].encode('ascii')!=section_bytes[9:-1]:raise ValueError('RTTI symbol/name mismatch')
    field=pin['excluded_value_field']['va']
    if value_fields != [(field,'value-rule','?FUN_00404040@@YAMM@Z')] or not (a+8<=field and field+4==b):raise ValueError('heuristic field mismatch')
    if section_bytes[field-a:field-a+4]!=b'@@@\x00' or any(x<=field+3 and field<=x+3 for x in original_relocs):raise ValueError('not an unrelocated name tail')
    if len([c for c in chunk_ranges if c[0]<=a and b<=c[1] and c[2]=='.data'])!=1:raise ValueError('chunk ambiguity')
    if any(x<b and a<y for x,y in claims+rewrites):raise ValueError('competing ownership')
    linked=bytearray(section_bytes);struct.pack_into('<I',linked,0,0x010f1ee0)
    if bytes(linked)!=original_bytes:raise ValueError('full reference mismatch')
    return field
