# Phase 2 data accounting and W typing

Current accepted checkpoint: `out/phase2-native-source-repeat`, recipe 825d,
1,613,018 initialized bytes (81.5%) plus five physical TLS bytes. The eight new
bytes form the native BGSBodyPart table; 1,100 functions, 389 ordinary EH
sections, eight requested tails, two fresh controls and clean semantic repeat
pass. Remaining raw bytes total 366,374, including 190,878 produced/unspliced.
PSA weak E and whole-class/type recovery remain open. The paragraphs below
retain earlier checkpoint counts; use `PROGRESS.md` and
`accepted_range_partition.json` for the current disjoint partition.


The final accepted archive covers 1,596,260 of 1,979,392 raw `.data`/`.rdata` bytes. Of the remainder, 207,636 bytes are in the frozen Batch 7 produced union but outside final accepted M3/DV1 ranges and recorded builder rewrites. `phase2_accounting.json` records disjoint extents; `account_ranges.py` reproduces them. It intersects that fixed byte set with **current** `data-v3/out/produced_ranges.json` kind/unit annotations (digest recorded in JSON), which were not archived with the accepted build. These labels are overlapping metadata, not proof that a particular rejected piece owns every byte or that a particular blocker caused its rejection.

| Current annotation combination | Bytes |
|---|---:|
| Project-unit RTTI only | 65,036 |
| Project-unit vtable only | 64,872 |
| Project-unit other only | 11,813 |
| Library-unit only | 65,726 |
| Multiple annotation classes | 189 |
| Total | 207,636 |

The mixed 189 comprise RTTI+vtable 21, RTTI+other 4, vtable+other 108, vtable+library 52, and other+library 4. Original zero/nonzero values and exact ranges are recorded per extent. “Project-unit” and “library-unit” distinguish the selector's unit-number convention; they do not imply all library bytes are ready for selection. Other unspliced bytes and rewrite ranges remain separately accounted in `../BATCH8-deferrals.md`.

The accepted DV1 log's rejection counts are first-failure **piece** counts and may overlap or duplicate storage. Its `rejected_unique_uncovered` subtotals are per-reason unions, not a disjoint cross-reason partition of this category. Historical vtable figures (40,960 unresolved methods/purecall and 30,564 differing targets) are piece-byte sums, not this 207,636-byte union. A parallel source review found a small vtable triage example at `0x0103274c`; it does not establish its failure cause solely from names.

`w_candidates.json` records 23 already-selected, scalar-sized W objects (118 bytes) with matching one-scope encoded unit scalar, consistent lexical declarations and no original relocation. Scope markers and declarations are supporting evidence, not a C++ parser or proof of all aliases. The private proposal `../out/phase2-w-scalar/selection.json` conservatively replaces 22 (114 bytes) after rejecting an additional unit alias, preserving the same addresses and extents. Concrete examples are `DAT_0102efb8` in `fnv_0054c030` (const double, `fnv_decomp/src/fallout_shared/tesobjectcell.cpp:13539`) and `DAT_0104f2a8` in `fnv_00641830` (mutable float, `fnv_decomp/src/fallout_shared/sky/sun.cpp:945`). Both source files place the declaration within matching namespace markers. An independent balanced comment/string-aware source-scope review found all 22 proposal declarations in their expected namespaces with matching scalar types and constness, one captured declaration/type and no captured definition per address; unit keys are unique and no alternate address-form spelling was found in the targeted source scan. This does not evaluate preprocessing or prove all aliases; see `W-SCALAR-review.md`.

The opt-in scalar schema records exact namespace, constness and mangled key and rejects named scalars as intra-object table hosts. The original accepted generator was reconstructed byte-for-byte against the archived tooling SHA; generated legacy C++ matches for all four partitions. Six focused schema/render tests pass. An isolated VC2008 fixture passed all 22 exact native COFF names, external storage, section, reference bytes, no relocations and no dynamic initializer; its private evidence is `../out/phase2-w-scalar/isolated-fixture/result.json`. The subsequent full opt-in positive build passed; see the result below. Neither the default pinned selection nor protected source was changed.


## Generator provenance before full integration

The accepted generator baseline hash is `9d07ba5705c01ac78de276839b224b7565c209317443d37b1002ed5f4440acec`, matching the final Phase 1 archived tooling hash. The current opt-in generator hash at this checkpoint is `fbb33c47aa46dc811d4a9b147bfd4f96a63cf6f8bc9af1776863ff329c6019b9`. `check_emission.py` compares the accepted selection through both versions and found identical generated C++ hashes for partitions 0–3 respectively: `12effff96cef499ea5c3a20ad5737b03c8206d7d734b46e868302f214783fbcf`, `7920bc3cae558600cf0b983f3121e9b1c60125ab0996dbb685a9fd6e21e650eb`, `39df401d3504cd7cbadb5f26614f27b5faccb5737f38ba6d8aefd9052c6d9113`, and `da13406309987ab44b54ee28d527c6179760db355b0199f785fddef04481e421`.

The candidate selection replaces existing covered bytes and does not increase the accepted 1,596,260-byte coverage. The full opt-in positive build passed; it does not change the existing Phase 1 acceptance evidence or the default selection.


## Full opt-in W positive

`../out/phase2-w-scalar-positive` passed the full positive build with all 8,263 entries kept, zero drops, and all 22 experimental scalar definitions (114 bytes) present. The executable matches the canonical SHA-256 and exact baseline relocation bytes. The semantic harness recorded a new save, changed and restored cell IDs, 71.7 seconds of play and normal exit code 0. `../out/phase2-w-scalar-positive/evidence/root-review.json` records the independent range review: the selected address/size ranges are identical to the accepted default. These results establish this positive run; negative controls and a clean repeat were not run, and the proposal has not been promoted. The scalar types and namespace declarations are source-supported, but this does not establish all native alias identities or resolve other W objects.

## Nine W array candidates

`w_array_candidates.json` records nine source-declared `sa238a0` mutable `unsigned char[256]` objects at `0x011a7440` through `0x011a7c40`, totaling 2,304 bytes already covered by W objects. Each captured declaration has an exactly matching 256-byte W extent, one corresponding units symbol and no original relocation or symbolic field in the extent; `CharTable::FUN_00a238a0` checks the index range. The adjacent tenth declaration starts at `0x011a7d40`, but its W range is 288 bytes, so it remains deferred until the extra 32-byte tail can be independently split. Independent balanced source-scope review found all nine declarations in the expected namespace and each exact decorated symbol as an external in its original compiled unit, with no alternate address-form source spelling. The isolated `compile_array_fixture.py` exact-symbol/object fixture passed; the candidate remains opt-in. These are existing covered bytes, not additional coverage.

### Array opt-in implementation

The isolated VC2008 fixture subsequently passed all nine exact decorated symbols, external storage, `.data` sections, 2,304 reference bytes, and no relocations or dynamic initializer. The opt-in generator now validates the nine reviewed addresses, namespace, mutable element type, exact symbol, extent and alignment, raw bounds, symbolic fields and destination chunk; it rejects namespaced array objects as table hosts. The candidate `../out/phase2-w-arrays/selection.json` (SHA-256 `ce1b579d25f1cf637b02493b7499ccc282313edb779a4dd97463a33bd792303c`) retains the 22 scalar proposals and replaces nine W entries with arrays. It changes no selected byte extent and remains outside the default. Schema/render unit tests pass; full candidate build, independent generator review and integration controls remain pending.


Independent review confirms the nine-entry proposal preserves every VA, size and alignment and leaves the other 8,254 selection entries unchanged. Four array tests pass, including explicit rejection of an array used as an intra-object table host. `check_array_emission.py` confirms all four generated C++ partitions are identical before and after the array emitter change for both the Phase 1 default selection and the 22-scalar proposal. The full array-candidate positive build is queued and remains pending.

## Expanded array and source-class candidates

`array_split_candidates.json` adds the tenth 256-byte `sa238a0` character array, a 36-byte `fnv_00af4550` unsigned-int array of nine elements, and a 16-byte `fnv_009f9e50` int array of four elements. The first two replace W heads while retaining separate W tails: the 32-byte tail preserves eight original relocation cells; the 188-byte tail preserves six original relocations in twelve pointer-run slots, with the other slots remaining null. The private expanded selection contains 8,265 entries and the same selected address union as before; all legacy generated C++ partitions remain identical under the staged generator. Independent source-scope/COFF-reference review passed; The isolated five-entry VC2008 fixture passed exact symbols, sections, 528 bytes and all 14 original tail relocations; full-image checks remain pending. The two `int[1000]` declarations that span numerous unrelated known names remain deferred, as does an `int[7]` declaration whose W head contains pointer relocations.

`point3_candidate.json` separately records the first 12 bytes of `fnv_005c25f0::NiPoint3 DAT_011a9c30` and a 252-byte W tail preserving the original float and pointer runs and two original relocations. Independent review confirmed the source class has three public floats, the namespace and one corresponding unresolved COFF symbol. The private `compile_point3_fixture.py` passed the exact class symbol, 12 head bytes, preserved 252-byte tail and both original relocations, with no dynamic initializer. Full generator integration and image verification remain pending. Neither candidate establishes native identity or ownership for the retained W tails.

## Further private source-view experiments

The expanded array fixture passed: three additional bounded arrays and their two retained W tails totaled 528 bytes, with 14 original tail relocations preserved. A private `NiPoint3` generator and 8,266-entry selection are staged under `../out/phase2-point3-proposal`; the range union exactly equals the accepted default. Its earlier head/tail COFF fixture passed and the staged generator rejects NaN, infinity and denormal head values. It remains unintegrated and has not passed a full candidate build or controls.

The source's two namespace-local `__m128` declarations at `0x010cb620` and `0x010cb630` explicitly carry 16-byte alignment. They are not treated as 4- or 8-byte-aligned substitutes. Private staged support under `../out/phase2-align16` extends destination validation and pseudo-unit alignment to 16, requires 16-byte-aligned symbol offsets and COFF section flags, and checks the translated image address. Four synthetic file-backing, destination/overlap and alignment tests pass; `simd_candidates.json` and `compile_simd_fixture.py` describe two 16-byte heads and the retained four-byte W tail. Compiler, image and gameplay validation remain pending. The staged changes do not alter the active default.


## Source-view Cost245 aggregate

The standalone VC2008 feasibility fixture for `fnv_004a8bb0::Cost245 DAT_011886a0[16]` passed: its 320-byte source-view head has the exact native symbol, reference bytes and all 58 original DIR32 sites, and its separately retained 64-byte W tail preserves one more site; no dynamic initialization was emitted. The fixture asserts `sizeof(Cost245)==20` and member offsets. The source-declared integer fields containing relocations are not asserted to be semantically native pointer fields.

An uninstalled private generator and combined selection are staged under `../out/phase2-cost245-proposal`. The selection replaces W384 with Y320 + W64, preserving its selected address union; the generator validates the explicit identity, bounds, per-record bool/padding and 58 relocation positions before emitting the source view. The staged-generator compiler fixture, independent generator review, targeted controls and full image validation are pending. No default coverage or class-completeness claim changes.


## Accepted next-data default (2026-11-19)

The fresh no-overrides default passed the independent full gate in `../out/phase2-next-data-default-verified/evidence/root-default-review.json`. `generate_accepted_range_partition.py` computes the current disjoint partition from the archived actual M3/DV1 ranges, frozen produced inventory, rewrite ranges and reference bytes; it preserves the previous record in `accepted_range_partition.before-next-data.json`.

Of 1,979,392 raw `.data`/`.rdata` bytes, 1,613,010 are covered: 1,062,973 M3 and 550,037 DV1. Five TLS bytes are separate. The remaining 366,382 comprise 190,886 produced but unspliced, 67,551 uncovered nonzero, 100,045 uncovered zero, and 7,900 builder-rewritten bytes. Produced-range annotation does not identify the cause of every blocker. The four new source-view heads improve 364 previously covered W bytes and preserve the selected range union; their types do not by themselves establish complete native class identity.

Earlier proposal, fixture and opt-in status sections above are historical snapshots.
