# TESForm getter hypotheses

The four proposed bodies agree with their source views and the original x86 instructions: each reads the 32-bit field at `this + 8`, masks it, and returns a Boolean in `AL`, with no explicit stack arguments. The reference BGSEncounterZone vtable rooted at `0x0102cbbc` has original relocation entries at the following zero-based slots:

| Slot | Code address | Mask | Source evidence |
| --- | --- | --- | --- |
| 38 (`0x26`) | `0x00549580` | `0x40` | `fallout_shared/tesform.cpp:1832` |
| 43 (`0x2b`) | `0x004011f0` | `0x80000` | `fallout_shared/tesform.cpp:1030` |
| 44 (`0x2c`) | `0x00401210` | `0x2000000` | `fallout_shared/tesform.cpp:1363` |
| 46 (`0x2e`) | `0x00401250` | `0x200` | `fallout_shared/tesform.cpp:1376` |

The neighboring slots 37–47 resolve to `0x00401190`, `0x00549580`, `0x004011b0`, `0x004011b0`, `0x004011d0`, `0x004011d0`, `0x004011f0`, `0x00401210`, `0x00401230`, `0x00401250`, and `0x004849d0`, respectively. Both candidate TESForm headers declare the four positions as parameterless virtual `bool` functions. Slot number and target support those bindings for the observed BGSEncounterZone vtable; they do not alone prove the same implementation is the original base-class definition or establish a historical method name.

The original source shells for `0x00549580` and `0x00401210` declare `const`; the candidate changes them to match the existing non-const `TESForm` virtual declarations. The original machine bodies do not write the object, but they cannot distinguish a const from non-const C++ declaration. Constness affects the decorated symbol and override compatibility even where the x86 calling sequence is identical. Keep non-const as an explicit current-header ABI hypothesis, not recovered original source semantics. The two non-const source shells are likewise layout views, not proof of original qualifiers. Targeted TESForm/BGSEncounterZone source searches did not establish a call-site contract for these specific slots; unrelated `Unk_` names in other classes are not evidence.

No compiler, vtable placement, inheritance-completeness or source-name result is implied by this review. Require the full 128-function reference and relocation comparison, explicit original/candidate COFF vtable slot and target checks, and independent class-hierarchy/override review before integration.
