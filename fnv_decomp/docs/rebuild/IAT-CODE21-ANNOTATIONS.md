# Additive CODE21 IAT evidence annotations

`tools/rebuild/iat_code21_annotations.py` selects only CODE21 IAT fields and
reuses the frozen CODE59 full-proof validator. Its pure API is
`annotate(mapped_fields, full_proofs, catalog_plan, expected_locations)`.
Locations are `(component, member, root, physical_section,
physical_symbol_index, offset, kind, field_proof_sha256)`. The declared set and
full-proof registry must exactly cover the selected fields without duplicates.
Original physical locations, recipe, canonical cell, zero-addend DIR32 operand
and catalog import identity must agree; conflicts fail closed.

The returned copy adds unchanged `original_field_proof`, `IAT_annotation` and
top-level `import_id`/`classification`. Compact proofs and all other rows remain
unchanged. `census_view(all_fields, catalog_plan)` requires hydrated CODE21
proofs, then delegates through the frozen CODE56 census chain, retaining the
earlier CODE59, CODE68 and CODE56 checks. The published ledger is never modified by a
temporary census view.

The bounded private collector authenticates the saved CODE21 member ledger,
all 21 normative full-proof wrappers and 46 ordered fields, handoff ordinals,
authorities, roots, certificate/contract identities and output hashes. It reads
no object, archive, original image, source body or context. The selected cohort
has two IAT fields and 44 other fields. Existing 34 native pointers are compared
by original cell/DLL/export identity only; this does not activate an alias or
prove a complete caller census.

Private artifacts under `build/rebuild/code21-iat-annotations-v1` are
`proof-bundle.json`, `annotated-code21-fields.json` and `receipt.json`, followed
by an independent outcome review. The bundle kind is
`code21-exact-IAT-fullproof-bundle`, schema 1, with `full_proofs`,
`expected_locations`, `normative_wrappers`, `inputs`, `source_dependencies`
and `annotator_source_sha256`. The receipt kind is
`code21-IAT-annotation-metadata-receipt`, schema 1, status
`collected-pending-independent-review`. Source/input review, coordinator
metadata capacity and actual independent reconciliation precede adoption by a
later full-cohort observer.

No new library, alias, DLL load, provider, ABI, runtime, compiler or executable
action is authorized by these annotations. Unknown original cells remain
explicitly unaliased.

```powershell
python tests/rebuild/test_iat_code21_annotations.py -v
```
