# V7 generated dynamic-cast obligation

The accepted V7 diagnostic reports one unresolved `crt-contract` identity for
original target `0x00ec43fb`. Its extraction witness is the generated CODE12
member for `0x00706320`, not a new code-role identity. The complete included
ledger contains **125 physical fields** for this canonical obligation; the
new member contributes two. One LNK2019 report does not limit a global alias
to those two fields.

The saved source and metadata pass is `crt-lane03-V7-RTDynamicCast-triage-v1.json`,
SHA-256 `4c3ddf0e6aa4db150608ad8c6dfc78e8a355d0ef50f1a1581d547b97f8d1375b`.
It retains the complete 125-field ledger census, exact two new fields, all
normal-member and saved observation evidence, source excerpts and the separate
code-role frontier. No current V7 producer, consumer, contract or input changed;
there was no native operation or image/object/archive read.

## Exact generated caller

Recipe `0576-dd603b7071c482c6` uses `src/fallout/misc/main.cpp`, source SHA-256
`89d09f8b4ba6d9758fca0ac3ebd32e18c9cc82c68a739c044457ed5c005ae3c5`.
Its SP1 `/MT /Od /Oy- /GS /EHsc /Gy /GF` function `FUN_00706320(int)` has a
retained extent of 661 bytes. The original source-object identity is
`a6c310961921f70eea2c70b9c18dba3d85ac19bffdfe3164922e9c3462ab425b`.

Both exact call fields are zero-addend REL32 references to physical symbol
1211 `___RTDynamicCast`, source section 195. They occur at function offsets
205 and 332, and serialize to section 2, symbol 27 in
`typed-composed-003-00706320.obj`. The saved projected member hash is
`3da7e361246dcd377e26ae24586729525f369bb4962cb4a243950d25bd4aab38`.
The before/after comparison metadata reports both original targets as matching.

Source lines 6054 and 6061 are compiler-generated pointer dynamic casts from
`Menu*` to `SPECIALBookMenu*` and `LoveTesterMenu*`. Each result is tested for
null. The calls originate from actual C++ casts, rather than a recovered
handwritten helper declaration. The source declares a polymorphic Menu base
and empty derived classes; that declaration alone does not prove complete
runtime object layout or RTTI ownership.

The exact nearby caller DIR32 fields are:

| Offset | Source physical descriptor | Original identity |
|---|---|---|
| 184 | `SPECIALBookMenu` TypeDescriptor | `0x0119f47c` |
| 189 | `Menu` TypeDescriptor | `0x0119f34c` |
| 311 | `LoveTesterMenu` TypeDescriptor | `0x0119f45c` |
| 316 | `Menu` TypeDescriptor | `0x0119f34c` |

These are exact metadata identities, not descriptor extent or content proofs.
The immediate vfptr displacement and reference-mode words were not independently
read during this source/metadata pass. Pointer-cast behavior is established at
the source level; runtime safety still requires the generated call boundary.

## Normal model and role separation

The normal candidate is SP1 `___RTDynamicCast` in `libcmt.lib` member `rtti.obj`.
Its saved archive hash is
`bd9700d126d378f31f32736abc0c88cb08a8e0f0914acb6e2c8cbfd1ab99f411`;
member hash is
`1adc1a40f30de4870fbbbee9686ec46663240bd8a46503c69716415a60cc260f`.
The native section is 213 bytes, section 36, entry value zero. Accepted lane04
observations agree at all 153 non-relocation bytes and account for all 15
relocation fields in each of SP1, RTM and VC8. Their old dependency identities
remain unverified. Equal observations do not select a runtime family or prove
interoperability with retained RTTI and exception frames.

The normal helper boundary is cdecl, returning a pointer, with five x86 words:
object pointer, signed vfptr displacement, source TypeDescriptor pointer, target
TypeDescriptor pointer and reference-mode integer. Pointer failure returns null;
valid RTTI, adjustment and normal exception policy remain part of the contract.

The actual V7 key is `(0x00ec43fb, crt-contract)`, canonical suffix
`d9896c4c820aa59aae9e417910a0bfa1c7374957003b682c2810dddb89febb3d`.
The separately saved `(0x00ec43fb, code)` key has canonical suffix
`41e7f4592199bcdfa4bb2104fa2e9217b741ea28fc963e3da047a00dcd021c89`.
Its 56 entry-frontier fields retain recovered int/pointer/opaque aliases and
need their own caller review. The actual V7 unresolved ledger has no group for
that code-role key. A shared original VA does not merge these obligations.

## Concrete blockers before another binding proposal

The actual included census must be reviewed as 125 fields. The exact three
caller TypeDescriptors additionally need compatible `type_info` ownership,
vftables, complete-object locators, hierarchy/base arrays and member displacement
graphs. Live Menu objects must have the expected vfptr and complete-object
representation throughout list removal and destruction.

Normal `rtti.obj` brings SEH prolog/epilog support, hierarchy search, `bad_cast`
and `__non_rtti_object` metadata, and `CxxThrowException`. Pointer-cast syntax
does not waive invalid-RTTI exception paths or cross-family EH requirements.
Those dependencies should use the chosen normal CRT's own implementations and
state; old numeric destinations are witnesses and are not required to equal
new provider addresses.

This triage proposes zero aliases. Diagnostic binding eligibility, provider
selection, runtime ABI approval and runtime eligibility remain false. It leaves
all current V7 frozen inputs intact.
