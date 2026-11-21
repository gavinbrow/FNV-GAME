# BGSBodyPart declaration adoption review

The smallest evidence-supported initial cohort remains units **620 and 621**. Their candidate per-class headers have been compiled privately and their layouts, mapped functions and observed metadata checked, subject to the remaining destructor, EH/link and full-image gates. This is a bounded source proposal, not proof that every other global same-name definition has been reconciled.

For the other BGSBodyPart census leads, a comment/string-aware brace scan gives these source scopes and declaration shapes. It is lexical evidence, not a compiler-preprocessed trace; conditional compilation and includes still require actual unit validation.

| Units | Source view | Adoption implication |
| --- | --- | --- |
| 55–57 | Global `BGSBodyPart` with only `const char* GetPartName()` in `bhkcollisionobject_decls.h` | Method-only stub, not the full class; preserving emitted code after replacement needs a separate fixture. |
| 253 | `fnv_008b6df0::BGSBodyPart` enum-only view and separate global `BGSBodyPart` with `char GetByte63()` | Namespaced enum view is distinct; global method stub is not a layout match. |
| 336 | Global empty `BGSBodyPart` used as a pointer in hit-data code | Layout is absent; pointer-only evidence does not establish class compatibility. |
| 370 | `fnv_0092b830::BGSBodyPart` with `int GetLimb()` | Namespaced method view, distinct from global class. |
| 423–424 | Global method-only `const char* GetPartName()` declarations in the two fopipboymanager header variants | Same-signature view as the candidate method, but incomplete class; verify each unit and include path. |
| 425 | Global method-only `NiAVObjectS* GetPartName()` | Return type conflicts with candidate `const char*`; cannot substitute without tracing actual call and intended view. |
| 576 | `fnv_00874c10::BGSBodyPart` with two point-related methods | Namespaced adapter, not the global native class. |
| 933–936 | Global method-only `const char* GetPartName()` in speedtree source variants | Incomplete views, with distinct compiler variants; do not assume header replacement is neutral. |
| 1082 | Two distinct namespaced `BGSBodyPart` enum-only views, `fnv_00573050` and `fnv_00573110` | Both are scoped adapters rather than duplicate global definitions. |
| 2638 | Global method-only `const char* __thiscall GetPartName()` staging view | Interface lead only; verify recipe and call behavior before adoption. |

The six earlier possible duplicate-name hits are not six proven global collisions. Unit 253 has one namespaced enum view and one global method view; unit 1037 has one global and two namespaced FileEntryList views; unit 1082 has two differently namespaced BGSBodyPart enum views; unit 1117 has global and `fnv_005de700` FileEntryList views; unit 1132 has two TESModel views in separate namespaces. Unit 1038's extra TESModel hits occur in a descriptive source comment; its actual global TESModel definition is at line 166. Unit 1037's global TESModel is a small virtual-destructor/method view, not the 24-byte canonical declaration. A source namespace is not a reason to rename or merge its adapter automatically.

Class-specific integration blockers remain: `FileEntryList` has many independent source views and must preserve its 8-byte member layout and methods; `TESModel` has competing source virtual lists, special-member declarations and slot-7 const qualifications; `TESModelPSA` needs final linker ownership of its implicit destructor and RTTI/vtable; `BodyPartInfo` has typed pointer views whose semantic names need broader proof; and `BGSBodyPart` still uses a destructor adapter in the compiled split candidate. Unit 425's conflicting `GetPartName` result is a concrete blocker to any broad global substitution. Run compiler-resolved include traces, all mapped-function comparisons and ABI/EH checks for each additional unit whose source changes; do not expand solely from matching class spelling.
