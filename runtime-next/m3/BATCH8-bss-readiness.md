# Batch 8 BSS definition readiness

The 7,171 distinct DAT-containing units symbol addresses in the `.data` virtual-only tail `[0x011c3200, 0x01271a9c)` have no file bytes. `inventory/b8_bss_definition_candidates.json` records a reproducible classification and exact scalar evidence; regenerate with `python -I runtime-next/m3/tools/b8_bss_readiness.py`. It does not infer an object's extent from the next address.

| Classification | Addresses |
|---|---:|
| Scalar metadata candidates | 1,584 |
| Complex or unsupported declaration | 3,949 |
| Alias, namespace or symbol-type mismatch | 935 |
| C linkage requiring review | 83 |
| No captured extern declaration | 320 |
| Inconsistent captured declarations | 222 |
| Existing captured source definition | 38 |
| No source inventory entry | 20 |
| Fixed-size array; symbol encoding unverified | 20 |

The scalar candidate evidence sums to 5,494 bytes of **virtual storage**, not file data. Each has a single consistent, simple non-const scalar extern, a matching global C++ symbol encoding, no captured definition, a naturally aligned exact scalar extent contained in the virtual tail, and no known interior units/inventory symbol or data label. A source scan of `fnv_decomp/src` and `include` found no alternate `_DAT`/PTR/OFF/UNK/BYTE/WORD/DWORD spelling at these candidates. This is lexical evidence; declaration scopes and previous object extents are not fully established. Three otherwise scalar candidates were deferred for C linkage. Candidate alignments reflect scalar natural alignment and require compiler confirmation.

The 20 bounded arrays have explicit source element types and counts, recorded separately with their unit symbol keys. Their keys are pointer-shaped, so the source declaration and binary linkage need careful reconciliation before treating the full array bound as a storage definition. Complex declarations include pointer, aggregate, array and other forms; they are not all class or phase-2 work. Namespace and alias cases, conflicts and missing declarations need individual resolution. Aggregate/class definitions or vtable-dependent storage may require Phase 2; the present lexical categories do not prove how many.

A plausible Phase 1 route is a generator-owned translation unit with exact-type, uninitialized scalar definitions and a separate memory-layout manifest of name, virtual address, size and alignment. Compile isolated fixtures first, inspect COFF symbol linkage, `.bss` section size, zero raw-data pointer and absence of dynamic initialization, and verify that generated definitions neither duplicate existing ones nor exceed the PE virtual bounds. Extend placement to claim those virtual ranges without copying file bytes, preserving the existing `.data` virtual size and alignment. Current file-backed M3 splice/placement machinery is not itself evidence of such virtual placement, and no end-to-end BSS definition, link, or runtime test has been performed. Phase 1 remains open.
