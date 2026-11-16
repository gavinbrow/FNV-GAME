# Versioned COMDAT ANY integration

`comdat_any_root_composer.py` and `comdat_any_code_projection.py` are separate
opt-in producer APIs for the reviewed COMDAT Selection 2 candidate witness.
The earlier witness, ordinary observer, composer, parser, serializers and
global writer stay frozen. Initial validation uses authored synthetic COFF;
real input observation and production require the exact wave input gate.

The composer accepts original raw bytes, the full contract, original negative
ordinary certificate, and exactly one wrapper:

```text
{kind: "typed-comdat-any-code-witness",
 definition_census: <exact accepted witness census>,
 observation: <accepted witness producer result>}
```

`compose(..., policy_id=composer.POLICY)` freshly replays the accepted witness
and original graph. Canonical JSON identity checks reject boolean/numeric
coercions and changed or extended wrappers. A complete witness census must
equal `reconstruct_definition_census(raw, contract, requested_root)`: the exact
whole original native root with one storage-2 definition and its planned
canonical physical identity. This is a source-bound singleton census, not a
claim about prepared archives, linker uniqueness, ABI or runtime providers.
Operational input gates authenticate the complete current prepared epoch and
the selected-provider map independently.

`assess_native_definition(raw, contract, negative_base, requested_root,
policy_id=...)` provides a fresh structured native-census preflight. Its
`eligible` result means only that an exact native singleton census can be
constructed. Valid partial, aliased or unsupported ownership/auxiliary forms
return no census and explicit reasons. Raw/schema/hash failures, a declared
physical identity contradicting the object, or a changed negative graph remain
fatal. It does not catch arbitrary exceptions or evaluate the witness policy.
Clean Selection 1 with a positive ordinary result is outside this negative-only
API; Selection 1 in an original negative view is reported as unsupported.

Only the one unambiguous original `UNSUPPORTED_OR_PARTIAL_ROOT_SECTION`
occurrence bound to that root may be discharged. A blocked witness produces an
incomplete composition that preserves every original blocker occurrence.
There is no DATA/LABEL fallback, fabricated positive ordinary certificate,
Selection 2-to-1 normalization or mutation of original proof inputs.

`summarize_unsupported` freshly replays the composition and reports ordered
original, discharged and remaining blocker IDs with occurrence counts. It
distinguishes native Selection 2 being observed from a proved root-conjunct
discharge. The accepted witness's conservative profile withholds discharge
when other unsupported contexts remain; the summary never invents a discharge
to make that state eligible. Assessment carries the same bound summary.

Consumer APIs are `assess_member` and `project_member`, taking original bytes,
contract, negative base, wrappers, new composition, ten-field requested roots
and original three-key selected-provider identities. Both require the complete
current `existing_exports` and explicit consumer `policy_id`. Assessment reports
`eligible=False` for a valid incomplete composition; malformed identity,
independent field/namespace policy and integrity failures remain fatal.
Projection never accepts a cached assessment as authority.

The consumer freshly recomputes composition, checks prepared canonical export
exclusion, and uses the unchanged global writer's field classifier. Only its
exact original-root `UNSUPPORTED_ROOT_COMDAT` auxiliary observation can be
discharged; every other legacy blocker is fatal. Full field geometry, source
proof, original operand target, ordinary function TYPE and provider identity
are checked. External callable references require exact selected entries, or
remain unresolved CODE/explicit CRT obligations. A reference to the same
retained function symbol plus a checked interior addend stays local to that
owned root; it creates no interior provider or additional definition.

The original-index namespace helper and unchanged serializer retain Selection
2 and its complete auxiliary bytes, flags, payloads and relocation addends.
Explicit section, symbol and auxiliary bijections preserve each original
relocation target. Only the selected original physical root is exported.
Receipts bind original-negative/composed/census hashes, maps, canonical bases,
field proof hashes and unchanged auxiliary facts. All approval and runtime
flags remain false; actual production, original before/after MATCH, independent
readers, recovered archives, stable input pins and resource gates are separate.
Projection reports in-memory serialization separately from disk publication;
the pure API performs no artifact disk write.

```text
python -m unittest discover -s tests/rebuild -p test_comdat_any_code_projection.py
python -m unittest discover -s tests/rebuild -p test_comdat_any_integration_independent.py
```

Authored comparator tests exercise nonzero DIR32 and negative REL32 addends
before and after projection with the unchanged comparator. They do not read
original game inputs, adopt cached observations, link an executable or execute
game code.
