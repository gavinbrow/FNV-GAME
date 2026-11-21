# W scalar declaration and COFF review

This read-only review covers all 22 selected candidates (114 bytes) in `m3/out/phase2-w-scalar/selection.json`. `w_scalar_scope_audit.py` produces metadata-only `w_scalar_scope_audit.json`; it strips comments and string/character literals, tracks balanced braces and namespace declarations, checks source DAT inventory declarations, inspects all unit symbol mappings containing the same address, and reads the matching existing unit COFF symbol table. It does not evaluate preprocessor branches, prove runtime ownership, emit code, or compile.

For every row, the captured source line is exactly a simple `extern` scalar declaration at namespace scope with the stated type and constness. The comment/literal-aware brace stack has exactly the listed namespace open. The source DAT inventory lists that one matching declaration/type and no definition. A targeted `rg` scan of `fnv_decomp/src` and `include` for DAT/PTR/OFF/UNK/BYTE/WORD/DWORD spellings at each address found one extern line and no alternate spelling for any candidate. Across `units.json`, each address has exactly one corresponding mapped symbol, and its pinned object contains that exact decorated symbol as an undefined external (COFF section 0, storage 2). There are no conflicting unit-map aliases or captured declaration types for these 22; none was rejected for that reason. Undefined symbols establish original object reference spelling, not a compiled definition or linkage equivalence.

| Address | Namespace | Declared type | Unit |
|---|---|---|---:|
| `0x0102efb8` | `fnv_0054c030` | `const double` | 1059 |
| `0x0102f080` | `CellShadow` | `const double` | 1059 |
| `0x0104f2a8` | `fnv_00641830` | `float` | 928 |
| `0x0106b4f4` | `PathDebugRender` | `const float` | 2670 |
| `0x0106b50c` | `PathDebugRender` | `const float` | 2670 |
| `0x0106ef4c` | `fnv_0070a130` | `const float` | 439 |
| `0x01071c84` | `fnv_007539a0` | `const float` | 457 |
| `0x01073488` | `fnv_00771700` | `const double` | 467 |
| `0x010734f8` | `fnv_00778b80` | `double` | 467 |
| `0x01074ffc` | `fnv_0079b8e0` | `float` | 479 |
| `0x01084d88` | `fnv_008a4810` | `float` | 253 |
| `0x01088140` | `fnv_008df1e0` | `double` | 362 |
| `0x01092508` | `fnv_009e8000` | `double` | 388 |
| `0x010da2a8` | `ConstraintInit` | `const double` | 2290 |
| `0x010da2b0` | `ConstraintInit` | `const double` | 2290 |
| `0x011a0120` | `fnv_00774090` | `int` | 467 |
| `0x011a3014` | `fnv_0086a0a0` | `unsigned char` | 2690 |
| `0x011a3b30` | `fnv_0094df80` | `unsigned char` | 396 |
| `0x011ad11c` | `fnv_00b06c10` | `float` | 2622 |
| `0x011ad120` | `fnv_00b06c10` | `float` | 2622 |
| `0x011ad7f8` | `fnv_00b4e490` | `float` | 115 |
| `0x011ad868` | `fnv_00b5e870` | `int` | 193 |


The scanner is more precise than nearest-namespace-marker matching, but remains lexical and does not interpret preprocessor conditions, macros, linker folding, or all possible undeclared numeric aliases. The private isolated VC2008 fixture result in `m3/out/phase2-w-scalar/isolated-fixture/result.json` records PASS for all 22 entries and 114 bytes: exact generated symbol, external storage, expected section, reference bytes, no relocations and no dynamic initializer. This is an isolated object check. A subsequent full opt-in positive matched the canonical image and exact relocation-directory hashes and passed semantic gameplay; its archived `m3/out/phase2-w-scalar-positive/evidence/root-review.json` records all 22 scalar identities, 114 bytes, 8,241 unchanged entries and unchanged coverage ranges. This is positive-only evidence: new-selection negative controls and a clean repeat have not been run. The proposed selection remains opt-in; zero candidates are promoted by this report. No game reference byte sequences are stored in this report or audit JSON.

## Selection and default review

The current promoted `batch8_final_selection.json` retains its pinned SHA-256 `42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7`. The experimental selection has 8,263 entries in the same address order: exactly 22 W entries totaling 114 bytes are replaced with scalar entries at the same addresses and widths; the other 8,241 entries are unchanged. The candidate digest is `0e0efb67b2a89260e5e78c7e49646aab4fdd252dd4b0a24116549b0f4c51596a`, matching the isolated fixture report. `m3/config.py` still selects the existing promoted file by default. The generator diff is conditional on explicit scalar identity fields; its fail-closed table-host check prevents an unsupported namespaced reference. A separate emission comparison reports unchanged generated C++ for all four promoted-selection partitions. No coverage increase is implied by replacing the existing W-owned ranges.
