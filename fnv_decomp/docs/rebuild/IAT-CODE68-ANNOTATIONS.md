# Additive CODE68 IAT proof annotations

`tools/rebuild/iat_code68_annotations.py` adds the CODE68 component to the
immutable annotation workflow. It leaves the frozen CODE59 helper and all V9
artifacts unchanged. The new adapter calls the accepted full-proof validator
and catalog identity join, while selecting only CODE68 IAT fields.

`annotate(mapped_fields, full_proofs, catalog_plan, expected_locations)` has
the same inputs as the earlier annotation helper. Each expected location is
`(component, member, root, physical_section, physical_symbol_index, offset,
kind, field_proof_sha256)`. The exact declared set and proof map must cover all
new CODE68 IAT fields without missing, extra or duplicate records. Each full
original payload must match its compact proof hash and physical source record,
original operand/base/target, zero-addend DIR32 representation and exact catalog
identity. Conflicts and runtime-promotion claims reject the input.

The returned copy adds `original_field_proof`, `IAT_annotation` and top-level
`import_id`/`classification`. Original compact witnesses, full original proof
payloads and all other rows stay unchanged. No API is selected from a source
spelling. `census_view(annotated_fields, catalog_plan)` requires every CODE68 IAT
row to have its original proof and annotation, then delegates to the frozen
validator to produce a temporary evaluation copy. Existing CODE59 annotations
continue through that same validator; the published ledger is never mutated.

The bounded producer joins the accepted 68-member projection ledger, all 68
normative JSONL full-proof wrappers, handoff ordinals/digests, original catalog
and existing 31-pointer native mapping. Wrapper roots, authorities, contract and
certificate identities, output hashes, ordered field-list hashes and every
compact/full proof hash must agree. The actual selection contains 629 fields,
including four IAT fields. All 625 other rows remain unchanged.

The new private bundle kind is `code68-exact-IAT-fullproof-bundle`, schema 1,
with `full_proofs`, `expected_locations`, source/input hashes and normative
wrapper provenance. The receipt kind is `code68-IAT-annotation-metadata-receipt`,
schema 1, status `collected-pending-independent-review`, binding the bundle and
annotated fields. An independent outcome must be accepted before the later
observer publishes its complete immutable ledger.

Existing pointer membership is an exact identity join only. New cells remain
unaliased, including vendor DLL identities. The module and collector invoke no
native tools, read no original objects/images or source-built archives, and
approve no DLL provider, ABI, extraction completeness, runtime use or execution.

```powershell
python tests/rebuild/test_iat_code68_annotations.py -v
```
