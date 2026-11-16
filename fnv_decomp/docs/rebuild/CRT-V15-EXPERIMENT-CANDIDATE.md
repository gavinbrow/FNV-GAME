# V15 normal-CRT alias experiment candidate

Source-only proposal for independent review. This is not an executed link,
provider adoption, runtime ABI approval, or evidence of an executable/window.
It changes neither the reference oracle nor any V14 artifact. The owner has
requested a potentially crashing runtime-first experiment; the unresolved
compatibility risks below remain material and are not converted to facts by
that request.

For a separately versioned diagnostic response, retain the four accepted CRT
aliases and every other inherited input exactly as independently reviewed, and
consider adding only these two x86 LINK alias tokens:

```text
/alternatename:_fnv_undefined_86b5006e5d6d2a0348c632bbd16e24c66b0a3804def721a1235e0f2a4af3c7e9=___CxxFrameHandler3
/alternatename:_fnv_undefined_d9896c4c820aa59aae9e417910a0bfa1c7374957003b682c2810dddb89febb3d=___RTDynamicCast
```

The proposed right-hand sides are real native COFF symbol names, not wrappers,
new definitions or fabricated providers. Bind to the same single pinned SP1
static CRT family already used by the diagnostic. Before any adoption, review
that exact response, its existing CRT directives and exact archive identity;
confirm LINK will resolve each alias against the intended library rather than a
conflicting definition. Do not add another CRT family or `/FORCE`. This
proposal deliberately does not modify the existing four-key validator or
response generator: a new, separately reviewed consumer must validate exact
canonical symbols, complete current field census, role, provider and inherited
alias set. Fail closed on collisions, unreviewed inputs or changed evidence.
A new response and operation require the established independent reviews and
owned lease; this document authorizes no native operation.

## Evidence and limits

The accepted V14 `application-link-diagnostic-v14-combined/unresolved-groups-v1.json`
records two `crt-contract` groups, both zero-addend REL32. Its included
provenance is not proof of linker extraction. The frame-handler group at
`0x00ec3d33` identifies compiler-generated `___CxxFrameHandler3`: EHFile
recipe 2656, physical section 242 +31, and ModelLoader-EH recipe 2633,
physical section 421 +71. Both include `EXACT_GENERATED_EH_FIELD_RESOLUTION`.
The saved normal SP1 original-EH fixture maps that symbol to `LIBCMT` member
`_trnsctrl_.obj`; its handler/registration coordinate evidence is for a
different parent, not either V14 parent. The frame, FuncInfo, unwind action,
receiver lifetime, SafeSEH and CRT exception-family compatibility remain
unverified. See [frame-handler triage](CRT-FRAME-HANDLER-TRIAGE.md).

The dynamic-cast group at `0x00ec43fb` contains 126 included field records,
not 126 proven loaded calls. Saved recipe 0576 `src/fallout/misc/main.cpp`
contains two generated pointer casts with physical symbol 1211
`___RTDynamicCast`, zero-addend REL32 at function offsets 205 and 332. The
normal SP1 provider is `libcmt.lib` member `rtti.obj`, archive SHA-256
`bd9700d126d378f31f32736abc0c88cb08a8e0f0914acb6e2c8cbfd1ab99f411`, member
SHA-256 `1adc1a40f30de4870fbbbee9686ec46663240bd8a46503c69716415a60cc260f`.
The compiler helper has a five-word cdecl boundary; this proposal does not add
a handwritten declaration. Retained RTTI descriptors, object layouts, vfptrs,
hierarchies, exception paths and cross-family interoperability remain unverified.
The distinct `(0x00ec43fb, code)` identity is not covered by this alias. See
[dynamic-cast triage](CRT-V7-RTDYNAMICCAST-TRIAGE.md) and
[CRT integration inventory](CRT-INTEGRATION-PROPOSAL.md).

These two substitutions cannot close the V14 link alone: its accepted result
also reports 626 CODE groups, 393 DATA groups and one Steam import group.
Normal startup, initialization order and real state ownership remain required;
this proposal does not omit initializers or introduce zero-filled guessed data.
A successful later link would not prove runtime compatibility, original-image
matching, or a working window.
