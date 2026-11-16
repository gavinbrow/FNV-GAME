# Entry CRT aliases and the source-owned file component

This is the next candidate plan after the independently accepted
[entry CRT provider inventory](ENTRY-CRT-PROVIDERS.md). It proposes two useful
normal functional substitutions for actual main, and a bounded source-owned
file component. It applies no alias, emits no object, invokes no compiler or
linker and executes no original code. The existing observer, provider inventory
and reference sources remain frozen. Runtime compatibility and provider
adoption require separate review.

## Actual main: concrete functional candidates

Propose function-to-function aliases, subject to the caller and state contracts
below:

| Original base / role | Normal SP1 CRT export | Initial field scope |
|---|---|---|
| `0x00ecc071` / `code` | `__wcsicmp` | Main `0x0086a850` +768, recipe0576, physical symbol1420 |
| `0x00406d50` / `code` | `_strcat_s` | Main +893/+964/+1134, recipe0576, physical symbol1409 |

The first export is the x86 COFF spelling of public `_wcsicmp`. The second
proposal deliberately elides a semantically transparent wrapper; it does not
create a new C++ stub or forward into the original image. Other uses of these
original bases do not inherit approval from main's finite field scope.

The owner authorized one checked-text observation of up to 4 KiB at each of
the two original targets, then a separate up-to-4-KiB observation of the append
wrapper's exact delegate. The private reference's complete hash was checked
before and after each pass. Only named SP1/RTM/VC8 library sections were compared;
original bytes and disassembly remain private. No image byte was put in a game
build, and no original function was called.

At `0x00ecc071`, all **131 non-relocation bytes** of the complete 147-byte
SP1/RTM `__wcsicmp` section agree. The section's only callable public export is
that named function at value zero. Every relocation was accounted for:

| Section field | Kind | Library dependency | Observed original destination |
|---|---|---|---|
| +11 | DIR32 | `___locale_changed` | `0x0126fdf4` |
| +25 | REL32 | `__errno` | `0x00ec85e3` |
| +41 | REL32 | `__invalid_parameter` | `0x00ec7c30` |
| +136 | REL32 | `__wcsicmp_l` | `0x00ecbf60` |

All four library addends are zero. Their original destination bodies/storage
are not proved by this comparison, and full relocation-identity equivalence
remains false. No optional original function index exists to supply an
independent boundary record. The exact named section-entry shape and complete
field accounting support this functional candidate rather than an inferred
nearest-address assignment. The VC8 section does not pass the same comparison.

At `0x00406d50`, the bounded observation finds a 25-byte function-shaped wrapper
with a normal frame, exactly three stack-word arguments, a call to
`0x00ec6bd2`, caller stack cleanup, and a plain return. All three arguments are
forwarded unchanged; the delegated EAX result is returned unchanged. This
wrapper does not match the CRT `_strcat_s` section directly.

The separately authorized `0x00ec6bd2` observation agrees at all **104
non-relocation bytes** of the full 116-byte SP1/RTM `_strcat_s` section. Its
only callable public export is `_strcat_s` at value zero. Its complete field
set is REL32 +25/+96 to `__errno`, both observed at `0x00ec85e3`, and REL32
+40 to `__invalid_parameter`, observed at `0x00ec7c30`; every addend is zero.
Again, the old dependency identities are unresolved, not silently ignored.
Independent source metadata reinforces the identity: the delegate has 63
reachable field uses, including 45 exact C `_strcat_s` spellings. Conflicting
void/pointer/C++ aliases remain visible.

These are **normal functional substitutions**, not claims that the new CRT
must retain old dependency addresses or reproduce old helper bytes. Normal SP1
CRT code supplies its own compatible errno, invalid-parameter and locale
implementation and fresh state. Old state must not be copied or aliased to
preserve those original numeric destinations. Review must approve the retained
call interface and chosen behavior, not mistake non-relocation equality for a
complete original-body identity proof.

### Main's caller and lifetime contracts

Main's existing checked source declares both calls as variadic cdecl `int`
functions. The actual typed uses and checked physical field identities narrow
the proposed substitutions without editing those declarations:

- The wide comparison passes `unsigned short* option6`, a 16-bit argument view
  derived from `CommandLineToArgvW`, plus a second pointer, and tests the signed
  integer result against zero. Public `_wcsicmp` supplies the required cdecl
  two-pointer/int-result boundary and case-insensitive comparison. Main's
  second operand has an `unsigned char` placeholder declaration, so its extent,
  null termination and lifetime must be supplied by the data owner as a
  readable 16-bit string. That placeholder is not a typed string proof.
- The three append calls pass a local `char[260]` destination, capacity 260,
  and a borrowed source pointer; main ignores the result. The wrapper's
  observed stack forwarding and EAX preservation support elision to normal
  `_strcat_s`. The destination must already be terminated, both buffers must
  be valid for the call, and source/destination overlap must not violate the
  normal CRT contract. Source-pointer providers remain a data/lifetime gate.
- The chosen CRT supplies normal case/locale and invalid-parameter/errno
  policy. Public compatibility assumes those standard semantics, with one
  fresh normal locale/runtime state; it does not preserve arbitrary old hook
  or locale state. Other callers with pointer-return, void or differing type
  declarations need their own review before expanding the finite scope.

The existing public API/header evidence is in
[the provider proposal](ENTRY-CRT-PROVIDERS.md). No generic handwritten helper
prototype or caller cast is used as proof of the x87/RTTI/EH contracts.

## Concrete role-keyed candidate metadata

`tools/rebuild/entry_crt_link_plan.py` reads nine exact saved metadata artifacts,
with fixed hashes, and emits an exclusive new candidate report. It reads no
game image, library, source body or retained object. It preserves each actual
source physical field, original base, signed addend, compiler/source/object
provenance and binding ordinal/hash. It joins every candidate source to the
selected native recipe/symbol/span and derives the canonical undefined name
from the frozen `(original_base, role)` convention.

The fixed scope has eleven role keys and 2,123 observed fields: six explicit
CRT-helper candidates, `_fread`, the two main target candidates, the direct
append delegate and the separately unresolved **code-role** uses of dynamic
cast. The ten keys with observed normal exports are provisional candidates.
The second dynamic-cast role remains unmapped; a `crt-contract` proposal never
silently resolves the same original address's `code` obligations. The direct
append delegate has no initial preparation subset, and the file package starts
with only the exact read leaf's one `_fread` field. Main append starts with
only its three listed fields, preserving the other observed aliases.

All provider/adoption/ABI/link/emission flags stay false. Exact exported SP1
archive/member identities come from the accepted metadata; this tool does not
invent providers for unobserved exports. The full original relocation-identity
flag remains false as historical evidence, and is explicitly not a prerequisite
to selecting a reviewed functional normal-CRT substitution.

## Bounded source-owned file component

The initial real source-backed CODE root is `ReadOrMarkFailed`, original
`0x00d2bcd0`, selected recipe `1821-ead65709d249dd91`, physical symbol8,
section3/value0, 39 bytes. It has exactly one field: REL32 +20, physical
undefined symbol9 `_fread`, original base `0x00ecb3a8`, zero addend. The expected
canonical obligation is
`_fnv_undefined_0c4e496a4a88850bf6d891c83171901bbbf2c62066442d845d0fb5bdd4787b0c`.
The selected object identity is
`c768b253bc216a32ff93300d2cd488a33c6c726c7aa01d9fb0e230fa7e396e4b`.

Its current sole blocker is recipe-wide `SAFESEH_REQUIRES_CLOSURE`, identifying
section22. There are no same-parent EH pieces or original missing fields for
this root. It needs its **own** reviewed ordinary-root exclusion certificate;
main/allocator certificates and the expanded IOTask producer do not cover it.
The symbol owner confirmed that a later fixed collector extension, rather than
changing the frozen ordinary-root producer, is the appropriate separate scope.

The bounded consumer would call the actual retained source body through its
existing C++ member boundary, not a rewritten implementation. That boundary is
thiscall, two explicit arguments `(void* buffer, unsigned count)`, a borrowed
stream pointer at receiver+12 and a mutable validity byte at receiver+16.
The declared source class has other unused prefix fields; the observable
minimum 17-byte access range does not prove a full original allocation size,
dynamic type or C++ lifetime. A consumer must construct its reviewed source
receiver representation, not allocate an arbitrary 17-byte fake game object.

For this first bounded preparation, original source-owned host code creates
and closes a fresh stream with the chosen normal SP1 CRT and borrows it into
that receiver only during calls. No game vtable/data/import is required by the
leaf itself. Normal CRT libraries and their OS dependencies are still required.
Actual map checks must bind the exact canonical CODE export and the one
canonical `_fread` obligation to its normal archive provider, and prove normal
startup, stream/descriptor/lock/error state ownership, without duplicate CRTs.
No preparation or execution is authorized by this plan.

This is a limited actual source-backed component, not a claim to have closed
the original Havok file object's complete lifecycle. The source and saved
binding stream expose the following remaining concrete routes:

| Source owner | Exact fields | Remaining obligation |
|---|---|---|
| Open `0x00d2bd60` | +13 read mode `0x0106e79c`; +30 vtable `0x010ce6c0`; +39 `_FUN_00ec9a47` | Source calls a two-string opener and stores the result at +12. Original target has four `_fopen` recipe aliases; actual provider and mode/vtable ownership remain open. |
| Read `0x00d2bcd0` | +20 `_fread` → `0x00ecb3a8` | Four total source callers bind exact `_fread`; initial package contains this one selected leaf. |
| Seek `0x00d2bd30` | +15 `?_fseek@@YAHPAXJH@Z` → `0x00ecb65a` | Pointer/long/int cdecl lead; retained source returns `result != 0`, so preserve its failure polarity. |
| Tell `0x00d2bd50` | +5 `?_ftell@@YAJPAX@Z` → `0x00ecb562` | Pointer/long cdecl lead, including signed error result. |
| Close `0x00d2bda0` | +8 vtable `0x010ce6c0`; +18 `?_fclose@@YAHH@Z` → `0x00ec9907`; +27 vtable `0x0102e388` | Source changes vtables and closes the nonzero handle. Recovered int/pointer/void/nolock aliases conflict; typed owner and provider need review. |

All five saved owner assessments and nine exact field records are retained in
the candidate report. Full lifecycle integration additionally needs the three
data providers, actual opener/seek/tell/close contracts and method/receiver
lifetime agreement. Do not manufacture vtables or discard those methods to
claim the whole original object closed. No original-method write path was
identified in this named source file; a writable-stream component would add an
explicit separate write contract rather than assume it from `_fread`.

After separate source/metadata review, root may authorize a preparation that
retains the exact leaf, supplies its reviewed alias and binds a source-owned
normal-CRT file consumer. Later execution needs independent artifact/ABI review
and its own go. Finite behavior checks should include positive read, zero count,
positive short read and EOF, with the owner inspecting count/position/EOF/error
separately. The retained body clears its validity byte only when `(int)fread`
is not positive, so a positive short read keeps the flag and zero-result EOF
and error are conflated. Bound the count within signed-int range. These are
tests of the actual retained component, not another generic CRT fixture.

## Private evidence and source review gate

The first two-target receipt is 20,815 bytes, SHA-256
`1e9b4fb0280518a61904a779aad0fa62fa2d807186782c2b286208b2bef3ae09`;
the separate append-delegate receipt is 7,011 bytes, SHA-256
`2e85d99790a64a1a7d488514d47f15d1db96367e9e2f3c8c952bc9df2c0fc1b0`.
Their private basenames are `entry-direct-crt-identification-v1.json` and
`entry-append-crt-identification-v1.json`. They contain private disassembly and
must not be published. They retain every compared member/hash, mismatch result,
field/addend and original resolved dependency destination, with no full
relocation-identity or ABI promotion. The checked reference hash is
`df1788907c6e26ef4df0b448ead526825336356b5606650165a1ce0825097eb7`.

The new candidate tool and synthetic tests require independent review before
the saved metadata report is emitted. Planned private output is
`entry-crt-link-plan-native-v1.json`. Input hashes and the caller-supplied
implementation hash are checked before and after planning; output creation is
exclusive and restricted to the ignored checkout `build/rebuild` tree. Resolved
paths cannot redirect it into tracked/public directories. It has no
alias-emission, native-preparation or execution command.

```powershell
python -m unittest discover -s tests/rebuild -p test_entry_crt_link_plan.py -v
```

## Emitted candidate plan and actual inclusion census

After independent source/privacy review and 14 passing synthetic tests, root
authorized one saved-metadata pass. It completed in 6.16 seconds, exit zero,
with all nine inputs and implementation stable before/after planning. The
accepted source/test/then-current document hashes remained unchanged through
that observation. No image, library or object was reopened and no native tool
was invoked. Private `entry-crt-link-plan-native-v1.json` is 1,223,449 bytes,
SHA-256 `99e16d2120d7b8249136fde98a78fb2c08f1c268f8cb4d424ab33216dad57082`.
It contains eleven role keys, ten provisional export candidates, 2,123 physical
field references and the five-owner/nine-field source lifecycle evidence.
Independent outcome reconciliation was requested separately.

The source is SHA-256
`dbb8a2abfea00eef6965b5c229d653faa8ee54c42ae58e928dc7c12dad99e196`;
the 14-test file is
`c295f41d3dec6e362ab4c2a2d03610e223b449361c86460b64d424d6692b5c9c`.
This subsequent documentation update does not alter that producer checkpoint.

An initial field subset is preparation/test coverage, not a mechanism that
limits a global linker alias. Canonical aliases resolve every included use of
the same `(original_base, role)` name. Before applying one, the actual selected
CODE set needs an inclusion census and an explicit reviewed function contract.
A verified whole-function functional model can eventually cover all compatible
callers under its material state and lifetime assumptions; it need not prove
old transitive CRT addresses or treat every future caller as a different
function. Caller tests and declaration contradictions remain evidence about
coverage and compatibility rather than an indefinite ban on integration.

The current bounded census joins the accepted **incomplete** all-current CODE
production (12,946 emitted owners; 3,913 union-blocked candidates; 51,798
historically blocked owners) and the separately emitted one-owner main
projection. Their union has 12,947 selected owners. These are retained bodies,
not a linked/extracted/executed function set. Across the eleven candidate keys:

| Base / role | Included fields | Distinct selected callers | In initial plan field subset |
|---|---:|---:|---:|
| `0x00ec408c` / `crt-contract` | 58 | 54 | 30 |
| `0x00ec43fb` / `crt-contract` | 55 | 45 | 15 |
| `0x00ec6040` / `crt-contract` | 54 | 35 | 9 |
| `0x00ec62c0` / `crt-contract` | 22 | 14 | 2 |
| `0x00ecc071` / `code` | 1 | 1 | 1 |
| `0x00406d50` / `code` | 3 | 1 | 3 |
| `0x00ec6bd2` / `code` | 5 | 3 | 0 |
| `0x00ec43fb` / `code` | 2 | 2 | 0 |
| `0x00ec658f` / `crt-contract`; `0x00ec7894` / `crt-contract`; `0x00ecb3a8` / `code` | 0 each | 0 each | 0 each |

Thus the two main aliases currently have exactly their four initial fields in
this concrete retained set; the current bulk pool supplies no other included
users of either name. A later larger component can change that fact. Helper
fields outside the plan's observed entry closure are visible in the census,
rather than silently treated as tested by the original 1,610-field helper scope.

The five included direct-delegate fields preserve three uses with a void C++
spelling, one exact C `_strcat_s` use and one int C++ spelling. The two code-role
dynamic-cast fields preserve an int/opaque five-argument alias and
`_FNV_DynamicCast`; they remain distinct from the 55 explicit helper-role fields.
Different names alone do not prove different machine ABIs, but these recovered
types are not approved public prototypes and must not disappear from review.
No `_fread` owner is currently emitted in this cohort, confirming the need for
the new ordinary-root certificate rather than pretending the source component
already links. Whole-game stream adoption still requires unified creation,
use, seek/tell/write where applicable, close, descriptor and lifetime ownership.

The census uses only exact saved receipts/coverage/selection/manifest and the
pinned complete binding stream. All seven inputs were rehashed after the join;
there was no archive or object traversal. Private
`entry-crt-inclusion-census-v1.json` is 267,478 bytes, SHA-256
`3485973616caa132364c053d43e61eb71ff84c92e70ea69f47aab80cdf90dece`.
It retains separate bulk/main/union cohorts and every physical site/spelling.
The all-current CODE receipt is
`ad870815321b42485378b0f896340bfd0b70cd52aea0dd27ffc39725bd93ce14`,
its coverage stream is
`e29cef9c0169ea19ac39724d3acb33163b101d9f21e8eed970c8071253d4ec16`,
and the main projection receipt is
`b46ffd72903c4363f545884d3dbb5cbb3bcf355d1ef8e84171c8fae1861eeb6b`.
This remains an inclusion and compatibility plan: no aliases have been applied.
