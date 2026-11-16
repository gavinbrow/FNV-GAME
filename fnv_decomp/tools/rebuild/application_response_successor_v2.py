"""Pure V14 response successor transform. No I/O, selection or native link."""
import hashlib
import ntpath
import application_combined_response as previous
import application_link_diagnostic as diagnostic
import application_uuid2768 as uuid

V14_RESPONSE_SHA256='7fe58875f18f1bb542c151b4c3c62dc86903c5633a6ac9ef331028ac60ce26e6'


def require(ok,message):
    if not ok: raise ValueError(message)


def transform(baseline, *, old_out, new_out, new_archive, inherited_aliases,
              current_aliases, fresh_uuid_identity, qualified_uuid):
    require(type(baseline) is bytes and hashlib.sha256(baseline).hexdigest()==V14_RESPONSE_SHA256,
            'fixed V14 response differs')
    old_out=previous._absolute(old_out); new_out=previous._absolute(new_out)
    new_archive=previous._absolute(new_archive)
    require(old_out.casefold()!=new_out.casefold() and new_archive.casefold().endswith('.lib'),
            'distinct output and one new library required')
    tokens=previous._parse(baseline)
    aliases=[x for x in tokens if x.upper().startswith('/ALTERNATENAME:')]
    require(type(inherited_aliases) is list and aliases==inherited_aliases and
            type(current_aliases) is list and all(type(x) is str for x in current_aliases) and
            len({x.casefold() for x in current_aliases})==len(current_aliases) and
            set(current_aliases).issubset(set(inherited_aliases)), 'reviewed inherited alias subset required')
    for key,name in (('OUT','diagnostic.exe'),('MAP','diagnostic.map')):
        prefix='/'+key+':'
        old=prefix+ntpath.join(old_out,name);new=prefix+ntpath.join(new_out,name)
        require([x for x in tokens if x.upper().startswith(prefix)]==[old], 'baseline destination differs')
        tokens[tokens.index(old)]=new
    require(new_archive.casefold() not in {x.casefold() for x in tokens}, 'library already present')
    tokens=[x for x in tokens if x not in inherited_aliases]
    tokens.append(new_archive);tokens.extend(current_aliases)
    require(len({x.casefold() for x in tokens})==len(tokens), 'duplicate successor response token')
    uuid.guard_response(tokens,fresh_uuid_identity,qualified_uuid)
    rendered=diagnostic.response_text(tokens).encode('utf8')
    require(previous._parse(rendered)==tokens, 'response roundtrip differs')
    return dict(response_bytes=rendered, response_sha256=hashlib.sha256(rendered).hexdigest(),
                baseline_sha256=V14_RESPONSE_SHA256, admission_approved=False,
                link_approved=False, execution_approved=False)
