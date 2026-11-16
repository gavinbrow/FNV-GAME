# Lane 04 CRT frontier evidence

This lane owns 48 exact unknown executable targets and 657 physical fields
from the full entry graph. It is not a census of actual failed LINK names.
The packet's actual-v4 unresolved groups remain attached without reinterpretation.
Reference source, include files, units, oracle, runtime aliases and provider
selection are unchanged.

The metadata producer `tools/rebuild/crt_frontier_lane04.py` reuses the lane01
named-member collector and the existing archive/COFF parsers. It validates the
fixed dispatch index, packet, doctor-all, three libcmt libraries and all 206
exact source input hashes. It records complete named native sections, every
relocation (including defined member symbols), every same-section function peer
and every original physical field. Four offline tests pass. The source and
metadata received independent lane01 review.

The finite request proposes 29 original targets, 90 native section alternatives
and 6,222 bytes after coalescing each target's overlapping alternative spans.
The sum of distinct alternative span lengths is 9,132 bytes; it is not the
coalesced payload budget. Every coalesced target span is at most 4 KiB. The
normal libraries are evidence candidates, not selected game providers.

| Original target | Fields | Named library hypothesis |
|---|---:|---|
| `0x00ec782f` | 167 | `??_L@YGXPAXIHP6EX0@Z1@Z` |
| `0x00ec6130` | 109 | `_strlen` |
| `0x00ec44d0` | 83 | `_memcpy`, `_memmove` |
| `0x00ec43fb` | 56 | `___RTDynamicCast` |
| `0x00ec7d40` | 34 | `_abs` |
| `0x00ec9774` | 27 | `_fprintf` |
| `0x00ec9f70` | 21 | `__CIcos` |
| `0x00ecadb8` | 17 | `_rand` |
| `0x00ec75b1` | 15 | `__isnan` |
| `0x00ec68e4` | 14 | `__stricmp` |
| `0x00eca0a0` | 13 | `__CIsin` |
| `0x00eca4a6` | 10 | `_sscanf` |
| `0x00ec7810` | 9 | `__allshl` |
| `0x00ecc6e6` | 8 | `_strtok` |
| `0x00ec658f` | 6 | `_atexit` |
| `0x00ec62c0` | 5 | `__ftol2_sse` |
| `0x00eca1d0` | 5 | `__CIacos` |
| `0x00ec6f20` | 4 | `_qsort` |
| `0x00eca7f4` | 4 | `_toupper` |
| `0x00ec7c66` | 3 | `_memcpy_s` |
| `0x00ec9130` | 3 | `_fmod` |
| `0x00ec85e3` | 2 | `__errno` |
| `0x00ec923c` | 2 | `__stat64` |
| `0x00ecada6` | 2 | `_srand` |
| `0x00ecd1c7` | 2 | `_malloc`; recovered `__malloc` is absent |
| `0x00eca5d0` | 1 | `__CItan` |
| `0x00ecb562` | 1 | `_ftell` |
| `0x00ecc8e0` | 1 | `__except_handler4` |
| `0x00ecdacc` | 1 | `_feof` |

Four hypotheses are explicit source-contract leads rather than literal aliases:
the stream-plus-format variadic caller at `0x00ec9774`, the four-word buffer
copy at `0x00ec7c66`, the int-pointer return at `0x00ec85e3` and the path/stat
structure pair at `0x00ec923c`. No similar-looking original function was searched
for. A different native version or failed comparison remains visible.

## Caller and family constraints

The 167 vector-construction uses retain the decorated stdcall compiler-helper
spelling and the conflicting recovered constructor/destructor iterator labels.
The selected normal helper's register, callback convention, unwind cleanup,
element stride/count and exception behavior need review; generic C++ function
casts are not machine ABI proof. The dynamic-cast target similarly retains all
int, pointer and opaque recovered aliases and remains role-distinct from an
explicit `crt-contract` use. Its RTTI ownership, multiple-inheritance adjustment
and exception policy are not established by a section match.

The native `_memcpy` and `_memmove` candidates share a complete section and entry
in the observed libraries. Both candidate names and every source alias remain
recorded. The source has pointer-return and ignored/void-return declarations;
source labels alone do not prove overlap or valid buffer extents. `_memcpy_s`
source callers pass destination, capacity, source and count. Two secure-char
traits implementations ignore its result and return the destination themselves;
another wrapper declares a pointer result but also discards it. These uses do
not justify exporting a pointer-return implementation or ignoring the chosen
CRT's range/error/invalid-parameter policy.

The FILE family requires one CRT to create, use, lock, buffer, inspect, seek and
close each stream. The renderer's 27 variadic output calls pass the pointer from
an opener at another frontier address and later call the corresponding closer;
neither pointer layout nor stream ownership follows from the variadic signature.
The selected NiFile caller tests a signed tell result for failure, seeks and
restores position, and has a recovered int result compatible in width with x86
long but still requiring unified stream provenance. The EOF caller operates on
a freshly opened stream and loops before reading; EOF/error and loop behavior
remain the retained source's responsibility. No standalone FILE substitute or
borrowed old CRT state is proposed.

The stat callers supply source-defined output structures. One accesses the mtime
field, and another compares a timestamp; their field widths, packing and exact
selected stat variant need source-layout proof before adopting `__stat64`.
The library candidate is an identification test, not permission to overwrite a
recovered structure with a guessed modern layout.

`_rand` and `_srand` must share the chosen CRT's per-thread random state;
`__errno` must refer to that same runtime's per-thread error storage. String
comparison, character conversion, scanning and tokenization require explicit
normal locale/invalid-input policy. `_strtok` additionally owns per-thread
continuation state. `_malloc` needs the allocation/reallocation/free family and
new-handler/heap policy reviewed together. `_atexit` requires the same fresh
normal exit registry and a known callback lifetime, rather than old registry
storage. No old data cell or numeric dependency target is adopted.

The `__CI*` helpers have nonzero native entry offsets inside sections shared with
other math functions. The request starts at target minus that exact value and
compares the entire section. The x87 argument/result/stack contracts and the
`__ftol2_sse` and `__allshl` register contracts remain separate ABI obligations.
The exception handler additionally depends on frame tables, cookie and EH
ownership. A handwritten recovered prototype cannot close any of those facts.

Nineteen targets have no finite named CRT candidate, including application
constructors, wrappers and late static-destructor callbacks. They remain
unresolved in the metadata and receive no original payload observation.

## Fixed observation gate

`tools/rebuild/crt_lane04_observer.py` reuses the existing PE reader, relocation
observer and named-member collector. Before any original payload read it checks
the pinned metadata/request and libraries, re-collects each exact named member,
preflights all coalesced spans and requires an independent review bound to its
source/test/dependency hashes and reference fingerprint. Five offline tests
cover full-span comparison, relocation masking, invalid placement and review
rejection. It does not search, recurse into dependency bodies, invoke native
tools, emit game bytes or execute anything.

The report preserves all nonrelocation comparisons and every observed relocation
destination. Same-section defined targets also retain the exact expected native
section-relative destination and equality result. Undefined and other-section
symbols retain unknown identity. All provider, ABI, full relocation-identity and
runtime eligibility flags stay false. Independent outcome reconciliation remains
separate from source approval.

## Observed finite result

The independently source-reviewed observer completed one fixed pass: 29 targets,
6,222 executable bytes requested and 90 complete named native alternatives.
Seventy-three alternatives pass every nonrelocation byte comparison. Twenty-eight
targets have both an SP1 and an RTM passing alternative. Fifteen VC8 alternatives
fail and fifteen pass (the copy target has two names per family). These are
alternative comparisons, not independent function or original compiler counts.

The `__stat64` candidate at `0x00ec923c` fails all three families. Its source
layout and exact stat variant remain unresolved; the failure is retained without
searching for another original address or assigning a neighboring provider.
The other nineteen targets still have no named candidate or original observation.

All 964 alternative relocation records are saved. The 276 same-section native
target comparisons agree with their exact section-relative expected targets.
Every passing nonrelocation alternative also has no relocation geometry error.
There are 103 relocation records with errors among failed alternatives; those
operands are retained as failed-template diagnostics, not promoted dependency
destinations. Matching undefined and other-section destinations remain unverified
identities, even when several candidates resolve to the same original number.

The private outcome basename is `crt-lane04-observation-v1.json`, SHA-256
`fcca50ae0ec7c9183b567716ef8c4ec276807d43ca16e51ad6cb8890ba0e1334`.
The independent source-review receipt is
`crt-lane04-observer-source-review-lane01-v1.json`, SHA-256
`4f7773b12109aa11bf6e21e893497de3f3bc20e7e0e7bc5baa503a316eacbb6e`.
Exact invocation, original delegation scope and successful exit are retained in
separate private operation records. The protected input hashes were stable
before/after the pass. No executable was produced or executed, and all adoption
and ABI flags remain false. Independent saved-outcome review reconciled the
90 alternatives, 964 relocation records and 276 same-section fields without
another original or native-library read. Its receipt is
`crt-lane04-outcome-review-lane01-v1.json`, SHA-256
`3f3978eea791725b504b0b87f47eef3d6e0fbfa3228c4ca21ab691bdf51efea3`.
