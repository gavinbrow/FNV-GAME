"""Pure directive candidate checks with caller-authenticated finite profiles.

This module performs no IO and grants no closure, provider, projection, linker
or runtime authority. The calling boundary must independently authenticate the
registry and review hashes; internally consistent documents are not an approval.
"""
import copy
import hashlib
import json
import ntpath
import re
import unicodedata

POLICY='directive-candidate-v1'
BASELINE_LIBRARIES=frozenset(('LIBCMT','OLDNAMES'))
TOKEN=re.compile(r'/DEFAULTLIB:"([A-Za-z0-9_.-]+)"\Z',re.ASCII)
SHA=re.compile(r'[0-9a-f]{64}\Z',re.ASCII)
HEADER_KEYS={'index','name','size','flags','virtual_size','virtual_address','object_size','raw_data_offset',
 'section_count','optional_header_size','relocation_count','relocation_pointer','line_number_count','line_number_pointer'}


def _require(ok,message):
    if not ok:raise ValueError(message)


def _canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def _digest(value):return hashlib.sha256(_canonical(value)).hexdigest()


def _sha(value):return type(value) is str and SHA.fullmatch(value) is not None


def _full_path(path,library):
    _require(type(path) is str and ntpath.isabs(path) and bool(ntpath.splitdrive(path)[0]) and
       ntpath.splitdrive(path)[1].startswith('\\') and ntpath.normpath(path)==path and
       not path.startswith(('\\\\?\\','\\\\.\\')) and ':' not in ntpath.splitdrive(path)[1] and
       all(ord(c)>=32 and ord(c)!=127 and c not in '<>|?*"' for c in path) and
       ntpath.basename(path).casefold()==library.casefold(),'exact full library path required')
    drive,tail=ntpath.splitdrive(path)
    if drive.startswith('\\\\'):
        prefix=drive[2:].split('\\')
        _require(len(prefix)==2 and all(prefix),'complete UNC share required')
    else:
        _require(len(drive)==2 and drive[0].isascii() and drive[0].isalpha() and drive[1]==':',
                 'drive-rooted path required')
        prefix=[]
    parts=prefix+tail.lstrip('\\').split('\\')
    for part in parts:
        normalized=unicodedata.normalize('NFKC',part).casefold()
        _require(bool(part) and not part.endswith((' ','.')) and
          re.fullmatch(r'(con|prn|aux|nul|conin\$|conout\$|clock\$|com[1-9]|lpt[1-9])(?:\..*)?',normalized) is None,
          'reserved or ambiguous library path component')


def qualify(*,root,contract,negative,raw_section,header,registry,registry_review,
            registry_sha256,registry_review_sha256,declarations):
    """Produce evidence only, for an exact independently authenticated registry.

    Registry/review digest arguments are external authority inputs, not evidence
    that this pure function authenticated a reviewer or read physical files.
    Each nonbaseline library requires its own separately reviewed full-path
    declaration; the response token remains an obligation for the future caller.
    """
    _require(_sha(registry_sha256) and _sha(registry_review_sha256) and
       _digest(registry)==registry_sha256 and _digest(registry_review)==registry_review_sha256,
       'registry authority pin differs')
    _require(type(registry) is dict and set(registry)=={'schema_version','kind','profiles'} and
       type(registry['schema_version']) is int and registry['schema_version']==1 and
       registry['kind']=='directive-candidate-finite-registry-v1' and type(registry['profiles']) is list and
       0<len(registry['profiles'])<=256,'finite registry required')
    _require(type(registry_review) is dict and set(registry_review)=={'kind','status','registry_sha256','reviewer'} and
       registry_review['kind']=='independent-directive-registry-review-v1' and registry_review['status']=='accepted' and
       registry_review['registry_sha256']==registry_sha256 and type(registry_review['reviewer']) is str and
       bool(registry_review['reviewer'].strip()),'registry review differs')
    _require(type(root) is dict and bool(root) and type(contract) is dict and type(negative) is dict and
       type(raw_section) is bytes and 0<len(raw_section)<=65536 and type(header) is dict,'typed input required')
    root_keys={'original_address','recipe_id','recipe_index','symbol','symbol_index','section','value','size',
               'object_sha256','source_sha256'}
    _require(set(root)==root_keys and all(type(root[k]) is int for k in ('recipe_index','symbol_index','section','value','size')) and
       all(type(root[k]) is str and root[k] for k in ('original_address','recipe_id','symbol')) and
       _sha(root['object_sha256']) and _sha(root['source_sha256']) and root['recipe_index']>=0 and
       root['symbol_index']>=0 and root['section']>0 and root['value']==0 and root['size']>0,
       'complete typed source root required')
    native={k:root[k] for k in ('original_address','symbol','symbol_index','section','value','size')}
    provenance=contract.get('provenance')
    _require(type(provenance) is dict and all(type(provenance.get(k)) is type(root[k]) and provenance.get(k)==root[k] for k in
       ('recipe_id','recipe_index','object_sha256','source_sha256')) and
       contract.get('recipe_id')==root['recipe_id'] and _canonical(contract.get('roots'))==_canonical([native]) and
       negative.get('recipe_id')==root['recipe_id'] and _canonical(negative.get('roots'))==_canonical([native]) and
       negative.get('contract_identity_sha256')==_digest(contract),'root source/contract/negative binding differs')
    before=_digest(dict(root=root,contract=contract,negative=negative,raw=raw_section.hex(),header=header,
                        registry=registry,registry_review=registry_review,declarations=declarations))
    profiles=registry['profiles'];_require(all(type(p) is dict and set(p)=={'root','contract_sha256','negative_sha256',
       'section_sha256','header_sha256','tokens','blockers','declarations'} for p in profiles),'profile schema differs')
    identities=[_digest(p['root']) for p in profiles]
    _require(len(identities)==len(set(identities)),'duplicate profile root')
    matches=[p for p in profiles if _canonical(p['root'])==_canonical(root)]
    _require(len(matches)==1,'exact registered root required');profile=matches[0]
    _require(all(_sha(profile[k]) for k in ('contract_sha256','negative_sha256','section_sha256','header_sha256')) and
       _digest(contract)==profile['contract_sha256'] and _digest(negative)==profile['negative_sha256'] and
       hashlib.sha256(raw_section).hexdigest()==profile['section_sha256'] and _digest(header)==profile['header_sha256'],
       'exact evidence digest differs')
    _require(all(negative.get(k) is False for k in ('closure_observed','graph_observation_complete','root_closure_candidate')),
       'original negative promoted')
    _require(set(header)==HEADER_KEYS and header['name']=='.drectve' and
       all(type(header[k]) is int and 0<=header[k]<=0xffffffff for k in HEADER_KEYS-{'name'}) and
       header['size']==len(raw_section) and header['flags']==0x100a00 and
       header['virtual_size']==header['virtual_address']==header['optional_header_size']==0 and
       header['relocation_count']==header['relocation_pointer']==header['line_number_count']==header['line_number_pointer']==0 and
       1<=header['index']<=header['section_count']<=65535 and root['section']<=header['section_count'] and
       root['section']!=header['index'] and
       header['raw_data_offset']>=20+40*header['section_count'] and
       header['raw_data_offset']+header['size']<=header['object_size'],'unsupported directive section')
    tokens=profile['tokens'];_require(type(tokens) is list and 0<len(tokens)<=64,'finite directive tokens required')
    names=[];spans=[];pos=0
    for ordinal,token in enumerate(tokens,1):
        _require(type(token) is str and TOKEN.fullmatch(token) is not None,'unsupported directive vocabulary')
        names.append(TOKEN.fullmatch(token).group(1))
        while pos<len(raw_section) and raw_section[pos] in b' \t\r\n':pos+=1
        start=pos;encoded=token.encode('ascii');pos+=len(encoded)
        _require(raw_section[start:pos]==encoded and (pos==len(raw_section) or raw_section[pos] in b' \t\r\n'),
                 'directive bytes or boundary differ')
        spans.append(dict(ordinal=ordinal,start=start,end=pos,token=token))
    _require(all(ch in b' \t\r\n' for ch in raw_section[pos:]),'unknown trailing directive')
    blockers=profile['blockers'];_require(type(blockers) is list and 0<len(blockers)<=128 and
       type(negative.get('blockers')) is list and len(blockers)==len(negative['blockers']),'blocker scope differs')
    occurrences=[]
    for ordinal,(entry,actual) in enumerate(zip(blockers,negative['blockers']),1):
        _require(type(entry) is dict and set(entry)=={'blocker','directive_ordinals'} and type(entry['blocker']) is dict and
          _canonical(entry['blocker'])==_canonical(actual) and type(entry['directive_ordinals']) is list and
          entry['directive_ordinals'] and all(type(i) is int and 1<=i<=len(tokens) for i in entry['directive_ordinals']) and
          type(actual) is dict and _sha(actual.get('blocker_id')),
          'blocker occurrence differs')
        indices=entry['directive_ordinals'];code=actual.get('code')
        _require((code=='UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE' and len(indices)==1 and actual.get('evidence')==tokens[indices[0]-1]) or
          (code=='DIRECTIVE_CONTRACT_DIFFERS' and indices==list(range(1,len(tokens)+1)) and actual.get('evidence')==tokens),
          'unsupported blocker or occurrence mapping')
        occurrences.append(dict(ordinal=ordinal,blocker=copy.deepcopy(actual),blocker_sha256=_digest(actual),
                                directive_ordinals=copy.deepcopy(indices)))
    unsupported=[i for i,name in enumerate(names,1) if name not in BASELINE_LIBRARIES]
    _require(bool(unsupported) and [o['blocker']['code'] for o in occurrences]==
       ['UNSUPPORTED_IMPLICIT_LINKER_DIRECTIVE']*len(unsupported)+['DIRECTIVE_CONTRACT_DIFFERS'] and
       [o['directive_ordinals'][0] for o in occurrences[:-1]]==unsupported,
       'directive occurrence coverage differs')
    required={name.casefold() for name in names if name not in BASELINE_LIBRARIES}
    _require(type(declarations) is list and type(profile['declarations']) is list and
       len(declarations)==len(profile['declarations'])==len(required),'exact dependency declarations required')
    obligations=[];seen=set()
    for record,pin in zip(declarations,profile['declarations']):
        _require(type(record) is dict and set(record)=={'declaration','review'} and type(pin) is dict and
          set(pin)=={'declaration_sha256','review_sha256'} and _sha(pin['declaration_sha256']) and _sha(pin['review_sha256']) and
          _digest(record['declaration'])==pin['declaration_sha256'] and _digest(record['review'])==pin['review_sha256'],
          'dependency authority differs')
        d=record['declaration'];r=record['review']
        _require(type(d) is dict and set(d)=={'kind','library_name','absolute_path','sha256','required_response_token'} and
          d['kind']=='explicit-normal-sdk-library-dependency-v1' and type(d['library_name']) is str and
          _sha(d['sha256']) and d['required_response_token']==d['absolute_path'],'declaration differs')
        _full_path(d['absolute_path'],d['library_name']);key=d['library_name'].casefold()
        _require(key in required and key not in seen,'unexpected or duplicate dependency');seen.add(key)
        _require(type(r) is dict and set(r)=={'kind','status','declaration_sha256','reviewer'} and
          r['kind']=='independent-normal-dependency-declaration-review-v1' and r['status']=='accepted' and
          r['declaration_sha256']==_digest(d) and type(r['reviewer']) is str and bool(r['reviewer'].strip()),
          'independent dependency review differs')
        obligations.append(dict(library_name=d['library_name'],sha256=d['sha256'],
            declaration_sha256=pin['declaration_sha256'],review_sha256=pin['review_sha256'],
            required_response_token=d['absolute_path']))
    _require(seen==required,'dependency coverage differs')
    _require(before==_digest(dict(root=root,contract=contract,negative=negative,raw=raw_section.hex(),header=header,
                                 registry=registry,registry_review=registry_review,declarations=declarations)),'input mutated')
    return dict(schema_version=1,kind='finite-directive-candidate',policy_id=POLICY,root=copy.deepcopy(root),
       original_negative=copy.deepcopy(negative),original_negative_sha256=_digest(negative),original_negative_unchanged=True,
       contract_sha256=_digest(contract),registry_sha256=registry_sha256,registry_review_sha256=registry_review_sha256,
       raw_section_sha256=hashlib.sha256(raw_section).hexdigest(),raw_section_hex=raw_section.hex(),header=copy.deepcopy(header),
       directive_occurrences=spans,blocker_occurrences=occurrences,required_future_dependencies=obligations,
       caller_authority_authentication_required=True,SDK_identity_freshly_observed=False,response_token_observed=False,
       ordinary_graph_closure=False,certificate_rewritten=False,composition_proved=False,projection_performed=False,
       provider_selected=False,runtime_eligible=False,ABI_verified=False,library_selected=False,library_loaded=False,
       duplicate_linker_semantics_proved=False,admission_approved=False,emission_performed=False)
