"""Pure post-V14 successor composition; fixed wrapper authenticates every input.

This module never loads files, launches tools, publishes or approves a link.
Independent peers and a fixed authenticated operation wrapper are mandatory.
"""
import application_actual_cohort_assembly_v4 as assembly
import application_response_successor_v2 as response
import post_v14_iat_crt_census_v5 as census


def compose(*, baseline_bytes, semantic_inputs, iat_inputs, crt_inputs,
            response_bytes, response_inputs):
    built=assembly.assemble(baseline_bytes=baseline_bytes, semantic_inputs=semantic_inputs)
    baseline_count=built['baseline_observation']['complete_field_count']
    old=built['fields'][:baseline_count]
    namespace=list(built['report']['successor_namespace']['symbols'])
    iat=census.iat_census(baseline=old,fields=built['fields'],namespace=namespace,**iat_inputs)
    crt=census.crt_census(baseline=old,fields=built['fields'],namespace=namespace,**crt_inputs)
    rargs=dict(response_inputs)
    rargs['current_aliases']=iat['tokens']+crt['tokens']
    rendered=response.transform(response_bytes,**rargs)
    return dict(kind='post-v14-composed-evidence-v5', assembly=built, iat=iat, crt=crt,
                response=rendered, admission_approved=False, link_approved=False,
                execution_approved=False)
