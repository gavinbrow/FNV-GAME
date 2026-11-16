"""Bind actual emitted archive bytes to the exact semantic member ledger.

Pure COFF parsing only; authenticated producer receipt and source review remain
external prerequisites. Never selects providers or authorizes a link.
"""
import coff_code_archive as coff


def require(ok,message):
    if not ok: raise ValueError(message)


def bind(*, archive_bytes, archive_sha256, members, member_count, member_bytes):
    require(type(archive_bytes) is bytes and type(archive_sha256) is str and
            coff.digest(archive_bytes)==archive_sha256, 'actual archive byte identity differs')
    require(type(member_count) is int and member_count > 0 and type(members) is list and
            len(members)==member_count and type(member_bytes) is dict, 'actual emitted census required')
    expected=[row['name'] for row in members]
    require(len(set(expected))==member_count and set(expected)==set(member_bytes), 'member ledger identities differ')
    parsed=coff.read_archive(archive_bytes)
    require([name for name,_ in parsed['members']]==expected, 'archive complete ordered members differ')
    for row,(name,data) in zip(members,parsed['members']):
        require(type(member_bytes[name]) is bytes and data==member_bytes[name] and
                coff.digest(data)==row['projection']['output_sha256'], 'archive member bytes differ')
    return {'archive_sha256':archive_sha256, 'member_count':member_count,
            'member_names':expected, 'admission_approved':False, 'link_approved':False}
