"""Private fail-closed BGSE weak resolution proposal; not integrated in builders.

Call only after independently recomputing each input check for the active run.
This function has no filesystem access and never interprets a vtable target as a
function address. Candidate placement comes from a source recipe owner proof.
"""
PRIMARY='??_EBGSEncounterZone@@UAEPAXI@Z'
FALLBACK='??_GBGSEncounterZone@@UAEPAXI@Z'
def propose(primary,field_va,normal_result,proof):
 if normal_result is not None:return normal_result
 if primary!=PRIMARY or field_va!=0x0102cbcc:raise ValueError('unsupported weak relocation')
 required=('snapshot_current','weak_metadata_valid','fallback_unique','source_owner_unique','body_and_reloc_equal','strict_reference_match','recipe_primary_absent','placed_global_absent','v7_name_absent','icf_primary_absent','name_overlay_absent','field_overlay_absent','relevant_provider_cohort_checked')
 if not isinstance(proof,dict) or any(proof.get(k) is not True for k in required):raise ValueError('effective namespace proof incomplete')
 if proof.get('characteristic')!=2 or proof.get('fallback')!=FALLBACK:raise ValueError('weak fallback differs')
 if proof.get('owner_symbol')!='?Destroy@FUN_00525cb0_shell@@QAEPAU1@I@Z' or proof.get('owner_size')!=44 or type(proof.get('owner_address')) is not int or proof['owner_address']!=0x00525cb0:raise ValueError('source owner differs')
 return ('private-bgse-fallback',proof['owner_address'])
