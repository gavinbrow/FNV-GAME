# Whole raw DATA with exact undefined address demands

November 3, 2026. This is a separate source/synthetic implementation of
[DATA-ADDRESS-DEMANDS.md](DATA-ADDRESS-DEMANDS.md). No actual larger DATA object
has been produced. The old arena planner, frozen 446-byte objects/projector,
policies, original source and comparison tools remain unchanged. No compiler,
linker, native inspection or executable is invoked by this tool.

The fixed scope is one complete existing raw writable nonexec fragment:
`374b2034599e26fb66895c38ed20cdebd079783c94fde6c9ba470cacb54e88b4`,
original interval `0x01183000..0x011c16bc`, 255,676 bytes, alignment 4,096,
exactly 13,869 HIGHLOW fields. No slicing, virtual-zero extension, cookie cell,
original code or target allocation is included.

## Fixed metadata and input contract

`runtime/data-arenas/address-demands-original-v1.json` pins the exact candidate
field receipt, owner ledger detail, v4/detail, binding detail and planning
evidence, plus original coordinate/image identities and strict-reader helpers.
It records the complete source arena geometry and legacy field-sequence hash.
Its default action is verify-only; actual private projection requires a separate
independent source review and explicit root authorization. Runtime/provider/
materialization/link approval flags remain false and semantic fixup approval zero.

`metadata(paths, policy, root)` consumes only those exact files. It loads the
bounded 34 MB candidate metadata and streams the original owner/v4 gzip detail;
it does not read the 1 GB observation or repeat its producer. Each of the 13,869
fields must match its full original owner row and ordinal, source domain, exact
site and target, raw backing and v4 record identity. Complete field counts,
unique sites and the pinned legacy sequence must agree. No missing row is
replaced by an overlay or a nearest-symbol inference.

The actual-operation gate rehashes all saved inputs and dependencies before and
after, with chunked hashing. Owned and compatible reference full-image hashes
are pinned. Their section geometry must agree, and the fixed span must be wholly
raw-backed in the expected `.data` arena, writable and nonexec. The exact raw
payload hash is derived only inside that guarded operation from the full-image
identity and fixed geometry; owned/reference bytes must compare equal. The
private receipt captures the payload hash for independent recomputation. No
payload or private absolute path enters tracked code/policy/tests.

## Positive address classification

Every field needs positive target-section and complete known storage-domain
evidence. `assess_fields` rejects the whole plan for an unknown or ambiguous
section, unsupported/special domain, selected source-owner conflict, unmapped
target, malformed site/addend proof or overlapping/cross-boundary source field.
No unknown-to-data fallback or partial successful field set is returned.

Mapped nonexec `.rdata`, `.data` and `CONST` addresses can be exact storage demands
with separately recorded raw/virtual-zero backing. Any intersecting known claim
must be an explicitly unselected source-projection alternative. These claims
are retained as alternatives, not allocated or selected as providers. Known
CRT/TLS/IAT/loader/resource/selected-state claims reject. The two selected scalar
literal ranges remain excluded by exact policy. No target data is emitted.

Mapped `.text` addresses can be exact executable-address demands, retaining an
explicit source-built-provider requirement. No instruction bytes are read and
no function-entry, EH/frame, helper, callable ABI or CRT owner is inferred.
Packaging/binding sections and unsupported executable domains reject.

The existing 1,387 provider-related quarantines are addressed by this new
contract, not silently changed inside the old classifier. All 13,869 actual
target admissions still await the separately authorized operation; synthetic
success is not a claim that an actual input has passed.

## New identity and relocation representation

`demand_identity(space, target, role)` implements a distinct namespace:

```text
_fnv_address_v1_ + SHA256(compact_sorted_ASCII_JSON({
  version: 1,
  address_space: <coordinate ID>,
  original_target: "0x........",
  representation: "absolute32",
  role: "original-nonexec-storage-address-v1"
      | "original-executable-address-v1"
}))
```

The coordinate ID hashes the exact owned/reference image identities, nonexec
identity digest and authoritative recipe hash. These role names cannot be
substituted with existing `data`, `code`, `iat-cell` or `crt-contract` roles.
The old four-role CODE namespace and producers remain unchanged. Fields sharing
one exact identity may share an undefined symbol while retaining distinct sites.

Original COFF bases/addends remain null where unknown. Every admitted original
word is checked against its exact target, then replaced with four zero bytes and
one DIR32 to the new undefined address symbol. The zero addend describes the new
exact-target expression, not an inferred original symbol. Numeric non-fields
remain unchanged, including address-shaped integers. No original pointer word,
numeric fallback, original process-VA definition or dummy provider survives.

## COFF output and independent checks

`coff_bytes` emits one standard i386 `.data` section with read/write/nonexec flags
and explicit 4,096 alignment, one arena anchor, understood `@feat.00=1` metadata
and only undefined address-demand targets. No target aliases, typed extents,
COMDATs, constructors, special runtime storage, imports or code are introduced.

`validate_object` uses the separately pinned strict COFF reader. It checks exact
section geometry/protection, complete symbols and absence of auxiliary/type
records, every relocation kind/site/name/zero addend, and all non-field bytes.
It restores the expected original target words only in a private comparison
buffer to verify complete raw payload equality. The returned map records the
actual serialized symbol indices and all physical field offsets, independently
of the writer's index construction.

`project(paths, policy_path, owned, reference, root, review_path, out)` requires
review kind `whole-raw-address-projection-review`, phase
`private-whole-fragment-projection`, independent reviewer, approval, root
authorization and exact tool/policy hashes before reading actual metadata or
payload. It verifies the actual PE HIGHLOW set equals all 13,869 fields, including
boundary-crossing rejection, before staging any object. Only after complete
positive classification, original-word checks, strict reparse and input stability
does it publish exclusively. Existing outputs/input aliases fail; a failed final
check removes only newly created outputs. Private receipts bind the full field
and namespace maps, original ledger ordinals, raw/object/input hashes and false
runtime states. No native tool, executable or link is a side effect.

## Provider and fulfillment limits

The output deliberately assembles dependencies without resolving them. Source
literal alternatives are not duplicated allocations. Original virtual-zero
targets are not materialized, and no raw/zero adjacency or cross-arena arithmetic
is claimed. RVA/encoded content, typed bounds, initialization and lifetime remain
unresolved obligations even when address identity is exact.

Later verified CODE, DATA or fresh CRT fulfillment needs its own contract. A
bridge must preserve the exact address identity and one physical allocation.
For old `B + a = T`, the exact-target demand for `T` has addend zero and must
alias the provider at base-offset plus `a`; it cannot alias directly to `B` or
add `a` twice. No bridge or provider alias is applied here, and no compatible
four-role name is guessed from an address or source spelling.

## Synthetic validation and next gate

Thirteen offline tests pass using invented payloads and metadata. Coverage includes
known address/unknown provider separation, coordinate/role identity, special and
selected-source exclusions, mixed/resource/TLS/binding targets, raw bounds and
overlap, unreviewed base/addend bridges, preservation of numeric bytes, original
word mismatch and fallback rejection, strict COFF mutation/relocation rejection,
disabled observation/projection gates and protected input drift. Full-size tests
exercise all 13,869 invented fields and the corresponding saved-ledger/v4 joins;
a missing last v4 row or unsupported last target fails the whole operation.

```text
python -m unittest discover -s tests/rebuild -p test_data_address_projection.py
```

Independent source/schema review precedes any actual field admission or data
projection. Root must separately authorize the exact private whole-fragment
operation afterward. Native COFF conformance, provider fulfillment, link closure
and every runtime behavior remain future gates. This source phase proves no
actual application startup or game subsystem.
