"""Pure V13 combined response transform; no I/O, selection, or linking."""
import hashlib
import ntpath
import re

import application_link_diagnostic as diagnostic
import application_uuid2768 as uuid

POLICY='application-combined-response-v1'
V13_RESPONSE_SHA256='d90fe3f379b130927fc5fe98821919f7016e69d657cc2023072556ef3d60d389'

def require(ok,msg):
    if not ok:raise ValueError(msg)

def _absolute(path):
    require(type(path) is str and ntpath.isabs(path) and bool(ntpath.splitdrive(path)[0]) and
            ntpath.splitdrive(path)[1].startswith('\\') and ntpath.normpath(path)==path and
            not path.startswith(('\\\\?\\','\\\\.\\')) and ':' not in ntpath.splitdrive(path)[1] and
            not any(ord(c)<32 or ord(c)==127 or c in '<>|?*"' for c in path),
            'canonical absolute Windows path required')
    return path

def _aliases(value,count):
    require(type(value) is list and len(value)==count and all(type(x) is str and x.startswith('/ALTERNATENAME:')
       and len(x)>len('/ALTERNATENAME:') and not any(y in x for y in ('\r','\n','"')) for x in value),
       'exact inherited alias list required')
    require(len({x.casefold() for x in value})==len(value),'duplicate inherited alias')
    return value

def _parse(data):
    require(type(data) is bytes and 0<len(data)<=1024*1024,'response byte scope')
    text=data.decode('utf8');lines=text.splitlines()
    require(lines and all(len(x)>2 and x[0]=='"' and x[-1]=='"' and '"' not in x[1:-1] for x in lines),
            'one fully quoted token per line required')
    tokens=[line[1:-1] for line in lines]
    require(len(tokens)==len({x.casefold() for x in tokens}),'duplicate baseline token')
    require(diagnostic.response_text(tokens).splitlines()==lines,'baseline response rendering differs')
    return tokens

def _transform(baseline,*,old_out,new_out,batch_archive,uuid_archive,prior_iat,prior_crt,current_iat,current_crt,
               fresh_uuid_identity,qualified_uuid):
    """Private authored-fixture core; public wrapper supplies fixed V13 hash gate.

    Caller separately authenticates paths, alias proposals, fresh SDK identity,
    producer/handoff cardinality, and full cohort field/provider authority.
    """
    old_out=_absolute(old_out);new_out=_absolute(new_out);batch_archive=_absolute(batch_archive);uuid_archive=_absolute(uuid_archive)
    require(old_out.casefold()!=new_out.casefold(),'output directory unchanged')
    require(batch_archive.casefold()!=uuid_archive.casefold() and
            batch_archive.casefold().endswith('.lib') and uuid_archive.casefold().endswith('.lib'),
            'two distinct library archives required')
    inherited=_aliases(prior_iat,34)+_aliases(prior_crt,4)
    require(len({x.casefold() for x in inherited})==38,'cross-family inherited duplicate')
    require(type(current_iat) is list and type(current_crt) is list and
       all(type(x) is str for x in current_iat+current_crt) and
       len({x.casefold() for x in current_iat+current_crt})==len(current_iat)+len(current_crt) and
       set(current_iat).issubset(set(prior_iat)) and set(current_crt).issubset(set(prior_crt)),
       'current aliases must be reviewed inherited subsets')
    tokens=_parse(baseline)
    actual_aliases=[x for x in tokens if x.upper().startswith('/ALTERNATENAME:')]
    require(len(actual_aliases)==38 and set(actual_aliases)==set(inherited),'unexpected/missing baseline aliases')
    for key,name in (('OUT','diagnostic.exe'),('MAP','diagnostic.map')):
        prefix='/'+key+':'
        existing=[x for x in tokens if x.upper().startswith(prefix)]
        old=prefix+ntpath.join(old_out,name);new=prefix+ntpath.join(new_out,name)
        require(existing==[old] and new.casefold() not in {x.casefold() for x in tokens},
                'baseline destination mismatch or duplicate')
        tokens[tokens.index(old)]=new
    existing={x.casefold() for x in tokens}
    require(batch_archive.casefold() not in existing and uuid_archive.casefold() not in existing,
            'future archive already present')
    tokens=[x for x in tokens if x not in inherited]
    uuid_path=qualified_uuid['future_uuid_response_token'];_absolute(uuid_path)
    require(uuid_path.casefold() not in {x.casefold() for x in tokens} and
            len({batch_archive.casefold(),uuid_archive.casefold(),uuid_path.casefold()})==3,
            'UUID library duplicates baseline or archive')
    tokens.extend([batch_archive,uuid_archive,uuid_path]);tokens.extend(current_iat);tokens.extend(current_crt)
    require(len(tokens)==len({x.casefold() for x in tokens}),'duplicate successor token')
    gate=uuid.guard_response(tokens,fresh_uuid_identity,qualified_uuid)
    rendered=diagnostic.response_text(tokens).encode('utf8')
    require(_parse(rendered)==tokens,'render/reparse mismatch')
    return dict(kind='combined-v13-response-plan-v1',policy_id=POLICY,tokens=tokens,response_bytes=rendered,
       response_sha256=hashlib.sha256(rendered).hexdigest(),baseline_sha256=hashlib.sha256(baseline).hexdigest(),
       uuid_guard=gate,caller_baseline_authority_required=True,caller_alias_authority_required=True,
       caller_fresh_uuid_observation_required=True,caller_nonempty_accepted_batch_required=True,
       producer_or_provider_selected=False,library_loaded=False,ABI_verified=False,runtime_eligible=False,
       link_performed=False,publication_performed=False)

def transform(baseline,**kwargs):
    """Fixed public V13 baseline: no alternate hash or fixture authority override."""
    require(type(baseline) is bytes and hashlib.sha256(baseline).hexdigest()==V13_RESPONSE_SHA256,
            'fixed V13 response SHA differs')
    return _transform(baseline,**kwargs)
