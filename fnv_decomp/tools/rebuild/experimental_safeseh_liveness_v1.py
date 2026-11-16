"""Read-only experimental SafeSEH liveness comparison; emits no COFF object.

Cross-object demand completeness is an external obligation. A candidate omission
is not an authorization to remove a registration or a runtime/link proof.
"""
import re
import struct
import experimental_runtime_section_closure_v5 as baseline
import coff_code_archive as coff


def analyze(raw, root_index, expected_sha256, demanded_names):
    _need=coff.require
    _need(type(demanded_names) in (list,tuple,set,frozenset) and all(type(x) is str and x for x in demanded_names), 'invalid demands')
    # Validate the exact object with the existing reviewed full-registration path.
    _,full=baseline.project(raw,root_index,expected_sha256)
    obj=coff.parse(raw); secs=obj['sections']; syms=obj['symbols']; assoc={};roots={syms[root_index]['section']};weak={};directive_names=set();sx=None
    for i,s in syms.items():
        if s['storage']==105:weak[i]=struct.unpack_from('<I',s['aux'])[0]
        if s['storage']==3 and s['section']>0 and s['type']==0 and s['aux_count']==1 and s['name']==secs[s['section']]['name']:
            aux=struct.unpack('<IHHIhBBH',s['aux']);
            if aux[5]==0:roots.add(s['section'])
            if aux[5]==5:assoc[s['section']]=aux[4]
    for i,sec in secs.items():
        n=sec['name']
        if n.startswith(('.CRT','.tls')):roots.add(i)
        if n=='.sxdata':_need(sx is None,'multiple safeseh sections');sx=i
        if n=='.drectve':
            text=sec['payload'].decode('ascii')
            for a,b in re.findall(r'/alternatename:([^\s=]+)=([^\s]+)',text,re.I):directive_names.update((a,b))
    _need(sx is not None,'no safeseh table')
    regs=list(struct.unpack('<'+'I'*(secs[sx]['size']//4),secs[sx]['payload']))
    demand=set(demanded_names)|directive_names
    live=set(weak)|set(weak.values())|{i for i,s in syms.items() if s['name'] in demand}
    keep=set(roots)
    while True:
        before=(len(keep),len(live))
        for i in list(live):
            s=syms[i]
            if i in weak:live.add(weak[i])
            if s['section']>0:keep.add(s['section'])
            if s['storage'] in (2,105):live.update(j for j,t in syms.items() if t['name']==s['name'] and t['section']>0)
        for child,parent in assoc.items():
            if child in keep or parent in keep:keep.update((child,parent))
        for i in list(keep):
            for _,t,_ in secs[i]['relocs']:
                live.add(t)
                if syms[t]['section']>0:keep.add(syms[t]['section'])
        if before==(len(keep),len(live)):break
    baseline_set=set(full['retained_sections'])
    handler_rows=[]
    for index in regs:
        s=syms[index];section=s['section']; handler_rows.append(dict(symbol_index=index,section=section,
            parent_section=assoc.get(section),retained=section in keep,symbol_live=index in live,
            local_name=s['name'],storage=s['storage']))
        _need(section in keep or index not in live,'live handler cannot be omitted')
    reloc_count=lambda selection:sum(len(secs[i]['relocs']) for i in selection)
    return dict(kind='experimental-safeseh-local-liveness-analysis-v1',input_sha256=expected_sha256,root_index=root_index,
        full_sections=len(baseline_set),candidate_sections=len(keep),candidate_section_indices=sorted(keep),
        full_relocations=reloc_count(baseline_set),candidate_relocations=reloc_count(keep),
        removed_from_full=sorted(baseline_set-keep),added_to_full=sorted(keep-baseline_set),
        handler_count=len(regs),retained_handler_count=sum(r['retained'] for r in handler_rows),handlers=handler_rows,
        demanded_names_count=len(set(demanded_names)),retained_noncomdat_count=len(roots),
        all_initializer_and_cross_object_demands_proved=False,archive_demands_proved=False,
        omission_approved=False,native_link_conformance=False,runtime_eligible=False)
