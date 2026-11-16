import json,collections
p=json.load(open('../build-v7/progress.json'));print('borrowed B',p['borrowed_relocation_field_bytes'],'rebase',p['rebase_test']['text_bytes_differing'],p['rebase_test']['remaining_diff_fields_by_cause'],p['coverage_pct_of_nonpadding_text'],p['filled_equals_reference'],p['ours_bytes'])
print(p['relocation_fields']['by_status'])
print(p['pieces']['fn_reject_reasons'])
bc=p['relocation_fields']['borrowed_by_cause']
c=collections.Counter()
for k,v in bc.items(): c[':'.join(k.split(':')[:2]) if not k.startswith('crt') else 'crt:'+k.split(':')[1]]+=v
print(c)
