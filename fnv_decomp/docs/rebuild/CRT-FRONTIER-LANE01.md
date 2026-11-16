# CRT frontier lane 01: finite provider proposals

This lane retains 46 original executable targets and 658 physical fields from
the shared 190-target frontier. This is an application-entry graph inventory,
not 46 actual LINK failures. Every original base, source hash, physical COFF
symbol, signed addend and binding proof remains in the private lane packet and
metadata report. No provider, alias, runtime ABI, object, or executable is
approved by this proposal. The matching recipe and oracle are unchanged.

The metadata-only collector is `tools/rebuild/crt_frontier_lane01.py`. It uses
the existing bounded archive index reader and the three doctor-selected SP1,
RTM and VC8 `libcmt.lib` files. It does not run LIB/LINK or read an original
image. Temporary selected members are removed. Export names below identify
actual installed library exports, but their association with an original
target remains a hypothesis until the exact-target observation and caller
contract are independently joined. The normal provider proposal is one fresh
SP1 CRT; RTM/VC8 template evidence does not select additional CRT instances.

## Concrete candidates and boundaries

| Original target | Named normal export candidates | Material remaining contract |
|---|---|---|
| `0x00406d50` | `_strcat_s` via already observed wrapper/delegate | Reuse the accepted finite main proposal; other 386 physical fields do not inherit main's three-field approval. Capacities, termination, overlap and ignored/result-consuming aliases need review. |
| `0x00ec7230` | `_memcpy`, `_memmove` | Source uses three arguments and pointer results; overlap behavior distinguishes the candidates. Neither a recovered name nor identical-sized library sections chooses it. |
| `0x00ec6cde` | `_fabs` | Normal cdecl double input and x87 double result; preserve NaN/sign behavior and floating environment. |
| `0x00ec6e30` | `_strrchr` | NUL-terminated borrowed byte string, promoted integer character, nullable pointer into that same live input. |
| `0x00ec67aa` | `_tolower`, `__tolower` | Public `tolower` versus public `_tolower` are different functions. Argument range and locale policy must be resolved; the installed header even provides an unchecked `_tolower` macro. |
| `0x00ec8d5f` | `_strncpy_s` | Four-argument copy source passes destination capacity `count+1` and count. Prove count, buffer extent, truncation policy, termination, overlap and invalid-parameter behavior. Recovered void returns can ignore errno_t, but do not prove it. |
| `0x00ec4835` | `_memcmp` | Full installed executable section is 5,760 bytes in all three libraries. It exceeds the 4 KiB per-target cap and is excluded from observation; no prefix-only equality establishes identity. One physical pointer-return alias also conflicts with ordinary integer-result comparison. |
| `0x00ec7595` | `__finite` | Source consumes zero/nonzero for promoted float angles. Preserve cdecl double input, integer result, infinities and NaNs. |
| `0x00eca573` | `_atof` | NUL-terminated input and cdecl double result; chosen locale, conversion failure and errno belong to the fresh CRT. |
| `0x00ec9907` | `_fclose`, `__fclose_nolock` | Preserve the distinction between locking and caller-held locking. Recovered void aliases ignore a result; `_fclose_nolock` spellings do not prove the original target actually omitted locks. |
| `0x00ec9a47` | `_fopen` | Two terminated byte strings and returned `FILE*`; mode strings, error path, close, descriptor and lock state must share one CRT owner. |
| `0x00ec62f6` | `__ftol2` | Symbol is at offset 54 in a 171-byte section with four function symbols. Full-section comparison begins at the explicit candidate base, accounting for peer entries. Compiler-emitted register/x87/integer-result ABI remains separate from C prototypes. |
| `0x00ecbc5b` | `__strlwr_s` | Source lowercases a mutable buffer with capacity; int and void recovered declarations coexist. Locale, termination, invalid parameters and result use remain material. |
| `0x00462d40` | `__splitpath_s` | Nine source arguments fit split-path shape, but an application wrapper is possible. No elision without argument/result forwarding evidence and all four output-buffer capacity contracts. |
| `0x00ec825b` | `__makepath_s` | Six-argument destination/capacity/drive/directory/name/extension shape. Prove optional null components and readable input/output extents. |
| `0x00ec9650`, `0x00ec9610` | `__CIasin`, `_asin` | Same 326-byte native section; entry offsets 64 and zero respectively. Compare the complete shared section at each exact entry mapping; the entrypoints retain distinct ABIs. Source also has a recovered float-result/double-input alias. |
| `0x004b7580` | `_memcpy_s` | Source supplies destination remaining capacity and prefix length. This application-range target may be a wrapper; explicit forwarding proof is required. |
| `0x00ec77e0` | `__allshr` | Compiler helper's register count and 64-bit pair result require generated-call proof, including count ranges and signed shifts. |
| `0x00ec86e1` | `_isalpha` | int argument/result does not establish valid argument range or chosen ctype/locale state. |
| `0x00ecadda` | `__time64` | Installed public `_time64` returns a 64-bit time and optionally stores through a 64-bit pointer. Recovered `___time64` is retained as an absent export hypothesis; it is not silently normalized. |
| `0x00ecd291`, `0x00eccf5d` | `_free`, `_realloc` | Every consumed allocation must originate from the chosen compatible heap owner. Null/zero/failure semantics, alignment and preserved original allocation on realloc failure need review across the allocating family. |
| `0x00ec8244` | `__mbscmp` | Source is only a two-pointer/int wrapper. Byte versus multibyte semantics, codepage, termination and invalid-input handling remain unresolved. |
| `0x00ec913a` | `__CIfmod` | Entry is offset ten in a 50-byte section shared with ordinary `_fmod`; preserve compiler x87 argument order and result boundary. |
| `0x00eca6bd` | `_atol` | Borrowed terminated string and signed 32-bit long result; locale, range and error policy remain material. |
| `0x00ecddf1` | `__vsnprintf` | Source forwards a `va_list` built with `va_start`; normal x86 va-list representation, format/argument agreement, size, termination and return semantics require proof. Never substitute a secure or C99 variant merely because its name is similar. |

## Explicit unresolved targets

The append target's physical symbol spellings narrow its ABI workload: 379
fields encode cdecl `int(char*, unsigned int, const char*)`, three encode the
corresponding void result, three are main's variadic cdecl int declaration,
and four are undecorated unknowns. These 389 fields span 53 recipe/function
callers in 38 source paths. That is useful review scope, not proof of the
arguments' buffer lifetime or a blanket alias approval.

`0x00ec30b0` has a length-error-helper source lead, but its recovered `__Xlen`
spelling is absent from all three named `libcmt` indexes. Exception class,
destructor and C++ library ownership remain unknown; no fabricated no-return
stub or guessed libcmt export is proposed.

No specific normal CRT provider is supported for application/middleware methods
`0x004e4470`, `0x00447300`, `0x00cb26e0`, `0x00aa1810`, `0x004f6e40`,
`0x009fead6`, or `0x00aa8660`. Float cosine/arccosine-looking wrappers need
actual forwarding evidence; thiscall methods cannot be replaced with a cdecl
math API. `NiFile::WriteBytesToFile` remains its source-owned method, not an
automatic `_fwrite` alias.

`0x00ec3bda`, `0x00ecb849`, and `0x00ecbf20` remain unknown. Their observed
one-, three-, or two-pointer source shapes do not establish a named CRT body.
The latter two were deliberately not assigned adjacent stream/string exports.

The eight targets `0x00fcaf50`, `0x00fd7810`, `0x00fd9b90`, `0x00fdad80`,
`0x00fdbfe0`, `0x00fdc3e0`, `0x00fdcc80`, and `0x00fddd40` are unresolved
static-cleanup/callback identities. A normal atexit registry does not create
their source-owned destructors, live object storage, ordering or lifetime.

## Family and observation gates

Stream APIs must use fresh streams from the same selected CRT, including
buffering, descriptor, lock, EOF/error and close state. Never copy old `FILE`
storage. Heap APIs require compatible allocations across malloc/new/realloc/
free/delete, not a per-name successful link. Locale/ctype/multibyte/conversion
APIs need one explicit fresh locale and per-thread errno/invalid-parameter
policy. Their old state addresses are evidence to record, not storage aliases
to apply. Math compiler helpers retain their generated-call ABI, FPU control
and error support; C++ EH helpers retain exception and destruction ownership.

The finite observation request excludes memcmp's oversized native section and
reuses the earlier append identity receipts. It covers 25 target hypotheses,
5,695 bytes across distinct alternative spans, coalesced to 4,233 requested
bytes. Root's bounded-after-review delegation and one metadata lease covered
one original observation after independent source and request review. Every
span lay in checked reference `.text`, at most 4 KiB per target and within the
root aggregate budget. Positive reports compare all
non-relocation bytes of the complete native span and account for every field,
including intra-member definitions, section-symbol addends, peer entries and
original numeric dependency destinations. Unknown old dependency identities
stay unknown. A reviewed functional substitution may use normal fresh CRT
dependencies; template equality alone does not approve caller or state ABI.

## Observed outcome and refined proposals

The once-only observation completed with 84 native template alternatives,
59 complete non-relocation-span matches, and all 738 relocation fields
retained, including failed alternatives and their errors. Twenty-three of the
25 target hypotheses have a matching SP1/RTM complete native section. The
direct `_memcpy_s` hypothesis at `0x004b7580` and direct `__splitpath_s`
hypothesis at `0x00462d40` fail all three libraries; they remain unapproved
application-wrapper investigations. No short prefix or nearest-address result
replaces either failed full-span comparison.

The comparisons distinguish actual normal `tolower` (COFF `_tolower`) at
`0x00ec67aa` from the unchecked `_tolower` export (COFF `__tolower`), which
fails. They distinguish normal locking `fclose` at `0x00ec9907` from the
`_fclose_nolock` templates, which fail. Thus the conflicting recovered
spellings remain caller-declaration evidence, not competing provider choices.

At `0x00ec7230`, the full 869-byte SP1/RTM/VC8 `_memcpy` and `_memmove`
sections have identical fixed bytes and all 48 corresponding relocation
templates. Every same-section computed destination agrees; the two external
dependencies remain original numeric witnesses with unproved old identities.
The old historical export name cannot be uniquely recovered from this
evidence. A concrete normal `_memmove` functional substitution can nevertheless
be proposed for the three-argument pointer-result boundary, retaining overlap
handling; no unique old-name claim is needed. The normal CRT supplies its own
SSE2 dispatch and vector-copy dependency/state.

The complete `_strrchr`, `__finite` and `__allshr` native spans match without
relocations. The remaining successful families retain every external or
same-member field. The two asin entries and the fmod compiler entry retain
their native section offsets and peer functions; helper ABI is not converted
to a guessed ordinary C signature. Fresh heap, FILE, locale, errno, math and
invalid-parameter ownership remains the material integration gate even when
all template comparisons pass. No alias, object, library, LINK invocation or
runtime execution was produced by this lane.

The final private proposal retains 23 new exact-span functional candidates,
the existing narrow append-wrapper proposal, and 22 blocked targets. Its
selected SP1 templates contain 178 dependency fields: 46 same-section fields
and 132 external or other-section fields covering 68 symbol/destination
identities. Fifteen fields have an exact numeric same-family template witness
in this lane's or lane 04's saved positive observations. Those joins are
explicitly unverified dependency evidence; none approves old data ownership
or recursively closes CRT state. Every remaining destination is retained.

Lane 04 independently reconciled the saved outcome and final projection:
25 targets, 4,233 requested bytes, 84 alternatives, 59 fixed-byte matches and
all 738 relocation rows. The 276 same-section alternative rows and 78 rows
with recorded relocation errors remain visible, including failed templates.
The review reread no original code or library payload. Five lane-specific
offline observer tests passed. ABI, provider selection and runtime eligibility
remain false after review.

Private metadata v1 and v2 remain separately preserved; v2 adds the actual
`__time64` export while retaining the absent recovered spelling. The metadata,
finite request, peer review and later observation receipts remain under the
ignored rebuild tree. No game code, library payload, or disassembly belongs in
this document or publishable source.
