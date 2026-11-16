# Proven literal labels and two-unit continuation

The v1 batch stopped on the fifth TU's complete original comparison. Its first
four TUs verified 190 original rows and eleven proposed fields. The fifth TU
compiled and passed its selected-owner geometry, but only 147 of 148 rows
matched: unrelated row `0x009aa150` could not resolve compiler label `$SG7468`.
The sixth TU was never compiled. No final runtime-overlay manifest was emitted.
The failed fifth object is evidence, not an accepted repair.

The exact failure is preserved in private
`entry-relocation-batch-native-v1/result.json`, SHA-256
`1459952e1a79284b5dd11c555f8b90e96f5b8aecd33b0ee40becebcbf19a9a4d`.
The operation took three seconds; observer peak memory was 362,479,616 bytes.
The saved error receipt correctly lacks a successful terminal stability claim.
A separate read-only reconciliation then verified all 64 protected input hashes
and all 28 completed-unit artifact hashes, SHA-256
`729ff5f6625efa99f913f104e42d293adbf9b9413085ec3a5d5fc5aaadd8405e`.
Neither failed attempt nor its frozen producer/policy was changed or rerun.

Two early copied declarations changed the compiler's generated literal name
from `$SG7466` to `$SG7468`. Moving those declarations nearer their use would
still precede the affected source literal and retain that renumbering problem.
No unrelated source declaration is removed to manipulate the compiler counter.
The original recipe and ordinary comparator remain unchanged.

## Exact binding supplement

The new `literal_symbol_migration.py` derives supplemental resolver bindings
for an alternate object, using positive original/fresh physical evidence. It
does not compute label numbers or search for a nearby/equal string to choose
an identity. Each changed compiler label must have:

- One unique original and new static compiler symbol, with the same exact
  native value in an identical read-only, nonexecuting, relocation-free section.
  The complete section payload hash and all section/COMDAT geometry agree.
- An exact full compiler-literal extent bounded by its next primary symbol or
  section end. Both full payloads, terminator/padding and extents agree. The
  complete original bound image extent is read-only, has no intersecting HIGHLOW
  field and equals that complete payload.
- A bijective old/new name relationship and a complete equal set of physical
  uses throughout both objects. Every use has the same section/offset/kind,
  four-byte DIR32 addend and complete checked function/address/relative-field
  context. Original field operands resolve to that exact original recipe
  literal binding plus addend. Unowned or unmatched uses reject the supplement.

Identical payloads elsewhere do not select a target. They are acceptable only
when this complete physical-use provenance independently closes the exact label
identity; any split, competing mapping, changed placement, absent use context,
payload difference or pointer-bearing/writable extent rejects it.

The read-only preview on the preserved failed fifth object found exactly one
witness: `$SG7466` to `$SG7468`, original binding `0x01012600`, full extent eight
bytes, one exact physical use in `0x009aa150`. The complete payload hash is
`e480454cc3c8ae65409e347cf7dc94a07149d6a80e7cd4be5ffacbd92cbfe916`.
Private `entry-relocation-literal-preview-v1.json` SHA-256 is
`1f3325d129984e07e34ce80790d93b8eac8a1a94c388dd691eb7b6bee70d4267`.
This preview performed no new compile or comparison and accepts no failed row.

The supplement creates a separate private resolver recipe with the exact
original function rows, profile and other keys. Only witnessed compiler-label
bindings can be added or explicitly replaced in its `symbols` map. Its original
recipe hash, alternate resolver hash and complete witnesses are recorded.
The unchanged comparator must then check every original function row with that
explicit alternate resolver. Fresh source bindings also cite the supplement's
hash, so they cannot silently borrow the old source/object namespace. Original
`build/units.json`, sources and comparison implementation remain unchanged.

## One finite continuation contract

`entry_relocation_continue.py` is a new producer with a separate fixed policy,
`runtime/source-overlays/entry-nineteen-continuation.json`, SHA-256
`76ce3b2b8bfe92ea5ca138006adf8a08e7c55a110211b44648d9923d9a0a38e4`.
It pins the v1 producer, policy, failure/reconciliation and preview evidence.
It rechecks every original input and all completed artifacts before use.
The four completed source transformations and complete comparison sets are
reconciled against the original fixed policy and original recipes. Their
compiler/header context remains pinned by the original input ledger.

After independent review and explicit root go, it compiles only recipes 2709
and 2757, once each, with the same frozen source transformations. It derives
the literal supplement afresh for each new object, checks all 429 newly compiled
rows, all eight new fields and the four remaining owner spans, and preserves
all prior geometry, migration, full physical inventory and fresh binding gates.
An empty supplement is valid if no compiler labels migrate. No guessed alias
rescues an unmatched function.

The final 619-row count combines 190 reused terminal rows and 429 new rows;
it is explicitly not a claim of six new compiles. A v2 manifest records each
unit's `reused_v1_verified_terminal` or `compiled_v2` operation, original artifact
root, per-artifact hashes, separate source/object lanes and supplemental resolver
evidence. The original failed fifth object stays separate and the earlier sixth
remains recorded as unattempted. No original selection or runtime provider is
adopted. The original 47/88 missing censuses remain historical unchanged inputs.

The continuation uses a fresh exclusive private output directory. The wrapper
requires explicit compile-only intent and reviewed implementation hash, writes
durable operation starts, preserves failures and does not retry them. It checks
terminal protected-input hashes even on failure. A ten-minute wall limit and
one-GiB observer/100-MiB output checkpoints constrain this modest continuation;
compiler-child memory is not independently measured. No linker or executable
operation is present.

Five synthetic literal-proof tests and two continuation scope/census tests pass;
the original eight fixed-batch tests also remain unchanged. Negative cases
include identical payloads with unmatched uses, wrong placement, altered payload,
writable/pointer containers, intersecting original HIGHLOW, wrong original field
target/payload, absent origin, unowned uses, cached failed/extra/omitted units and
wrong combined row, repair or operation counts. Independent source review passed
all seven tests and independently reconciled the prior failure/reuse evidence
and bounded original/fresh-object/image literal witness before the root go.

## Actual two-TU continuation

The one authorized continuation compiled exactly recipes 2709 and 2757 once
each. All 148 and 281 new original function rows MATCH with the unchanged plain
comparator and the explicitly recorded resolver supplement. The selected four
owners retain their original extents, non-field bytes and other references;
their eight fields have the exact expected DIR32 targets and zero addends.
The first four terminal units were reused with their checked 190 rows and
eleven fields. The combined ledger therefore has 619 rows and 19 repairs,
including nine code-address and ten dispatch-header fields, rather than six
new compiles.

Recipe 2709 has exactly the one freshly proved `$SG7466` to `$SG7468` witness;
recipe 2757 requires no literal aliases. All six TUs' original missing-field
sets reconcile from 25 to six in these alternate candidates: the two archive
code-address fields and four AI setting-object fields stay unresolved. The
original 47 reachable / 88 global censuses remain unchanged. No other blocked
field is silently synthesized.

Private `entry-relocation-batch-v2/result.json` SHA-256 is
`ec32d68580b62b225cd9e9e90e450a9915a39ab859b2c652105441d25b6ea9fb`;
`runtime-overlays.json` SHA-256 is
`5728021d6d5796f377bd3fbf02873db1d2b2d50e8d4bf2b2bfdff80409e97bec`.
Both protected-input and generated-artifact stability checks passed. The new
operation took 2.703 seconds, recorded observer peak memory 324,743,168 bytes
and produced 8,849,325 private output bytes. Compiler-child peak memory was not
measured. No executable, linking, callback execution or runtime provider adoption
occurred. Independent actual-artifact review accepted all 19 raw COFF fields,
ten-owner geometry, 619 saved comparison rows, exact source transformations,
100 input hashes, fresh source-binding/lane identities, the 25-to-six missing
census and the literal supplement. The reviewer did not recompile or rerun the
original comparator. Neither manifest is an automatic runtime selection or
authorization to modify a busy consumer.
