# Unit 370 source-view split diagnostic

The private split compiles to identical bytes and equivalent scoped relocations for all 178 mapped functions. Normalization is restricted to constructor `0x00913fe0`, where the two pointer-view constructor and method names changed, and to the compiler-generated literal label in `0x008f36c0`. Applying the method normalization to unrelated functions would incorrectly transform their already-matching PtrA96/PtrB96 calls.

The candidate label `$SG27297` and old `$SG27267` refer to the same offset 148 in byte-identical 2,588-byte `.rdata` pools across archived production, original mirror and candidate; the original recipe maps `$SG27267` to `0x01088220`. The existing BFC cohort evidence independently supplies `$SG58544 -> 0x010898c0`. With those source-backed local bindings, archived production, original mirror and candidate each pass all 178 strict reference comparisons.

The unchanged ordinary EH oracle locates 81 sections for both mirrors. The original has one failed section for the single surrogate destructor name that denotes two different original targets. The split candidate has zero failed sections and zero errors; four other inferred EH names remain reported separately. These results are machine-recorded and input-hashed in `out/phase2-bfc-370-pointer-split-mirror/diagnostic-proof.json`; `bfc_370_pointer_split_diagnostic.py` reproduces them without compiling.

This is a private source-view experiment, not an installed fix or full placement/runtime proof. The new constructor aliases, typed pointer method shapes and per-unit source integration still require independent review, and final image, EH ownership and gameplay gates remain separate.
