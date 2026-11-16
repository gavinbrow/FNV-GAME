# Exact normal CRT bindings for a diagnostic successor

The reviewed CRT integration has four linker bindings: three functions
and the cookie data consumed by the generated callers. It is a separate
diagnostic successor proposal. The fixed V5 input set and response remain
unchanged. No application execution, old-code forwarding, fake provider,
forced link or runtime ABI approval is part of this work.

| Original base / role | Normal SP1 export | Current V4 input fields | Planned expanded input fields |
|---|---|---:|---:|
| `0x00ec408c` / `crt-contract` | `@__security_check_cookie@4` | 58 | 99 |
| `0x011c16bc` / `data` | `___security_cookie` | 54 | 93 |
| `0x00ecc071` / `code` | `__wcsicmp` | 1 | 1 |
| `0x00406d50` / `code` | `_strcat_s` | 3 | 3 |

These four exact canonical names occur in the actual V4 unresolved set.
The current input cohort has 37,282 fields; the planned expanded cohort has
44,353 after excluding the eleven IOTask EH fields. Their binding use sets
contain 116 and 196 fields respectively. These are complete input-site
censuses, including every included use of a globally aliased canonical name.
They are not claims that the linker extracted every input member. Reported
LINK callers and included physical provenance remain separate evidence.

The source planner, `tools/rebuild/crt_provider_adoption_plan.py`, reads exact
pinned saved JSON artifacts and the recipe metadata only. It never opens an
image, library or object, invokes native tools, or applies an alias. It emits
a new private plan and an exact four-line `/ALTERNATENAME` proposal. Nine
synthetic tests cover role separation, physical versus serialized symbol
indices, duplicate fields, addends, data/function relocation kinds, unique
cookie recipe identity and response injection/conflicts. Independent source
review accepted this saved-metadata planning scope.

## Provider and ABI basis

The two main function models reuse the accepted complete native comparison
and transparent-wrapper observations. The wide comparison has the ordinary
cdecl two-pointer/signed-int boundary. The append wrapper forwards three
stack words unchanged and returns the delegate's result unchanged, supporting
elision to ordinary cdecl `strcat_s`. Main uses three local 260-byte
destinations and ignores the append result. The wide string placeholder's
extent and the buffers' termination, overlap and source lifetime remain
runtime data-contract gates. Those gates are explicit without making
diagnostic link identity conditional on matching old CRT data addresses.

The compiler-generated cookie check uses the x86 ECX-word helper boundary.
Binding only its function would leave callers reading a distinct cookie
cell. Every included recipe independently names `___security_cookie` at the
original cell, with zero-addend DIR32 fields. The companion data binding
supplies the normal four-byte SP1 cookie. The accepted bootstrap evidence
identifies its actual `libcmt.lib` member `gs_cookie.obj`, its member hash,
and the matching normal cookie/complement/init ownership. The normal CRT
initializes its own fresh cookie before protected source-owned frames.
No old cookie storage or value is copied. Actual game-frame compatibility
and startup order remain runtime gates.

All providers use the same pinned normal SP1 static CRT. Its internal
`errno`, invalid-parameter, locale and math dependencies resolve through its
own normal library symbols and state. Old numeric dependency destinations
are retained observations, not requirements that fresh CRT addresses equal
original addresses. This does not authorize aliases to old locale or errno
storage. The cookie companion is different: generated application callers
directly reference that canonical data identity, so it needs an explicit
fresh normal owner alongside the helper.

## Whole-family contracts and retained frontier

The four independently reviewed lane outcomes and their typed model
supplements remain bound inputs. All 190 original frontier targets and all
2,631 physical source fields are retained, including failed comparisons,
excluded spans and unknown providers. Their names do not add response-file
aliases. A positive source-built normal function model is distinct from a
claim that old transitive CRT code and data identities are fully recovered.

Stream integration uses one normal CRT for open, read, write, seek, tell,
buffering, descriptors, locks, EOF/error and close. It requires fresh streams
from that owner rather than copied old FILE objects. The earlier source-owned
read component and its accepted bounded test remain evidence for that
component; no current `_fread` alias is added without an included caller.

Heap integration uses a coherent malloc/new/calloc/realloc/free/delete
family with explicit alignment, zero-size and failure policy. Locale,
ctype, multibyte, parsing and formatting functions share the same fresh
locale, per-thread errno and invalid-parameter policy. Compiler math helpers
retain their generated x87/register ABI. EH, RTTI and callback models retain
their frame, descriptor, destruction, order and lifetime gates. None of those
future models becomes an executable provider merely because the current
four linker names resolve.

## Diagnostic consumption and required observation

After independent plan review, root delegates a separate diagnostic-only
consumer through the startup owner. That consumer must freeze and rehash
its actual input cohort, reproduce the complete four-key field census, and
reject any stronger canonical definition that could override an alternate
name, especially the cookie data cell. It must preserve original base and
role, every physical and serialized site, kind, addend and source proof.
The future expanded census is prospective evidence until that exact selected
successor has independently passed its freeze review.

The consumer adds only the four reviewed alternate-name tokens and the
chosen normal CRT. It retains the command, response, native result, log and
map. Review checks that the four old names disappear, accounts for any new
dependencies and distinguishes successful namespace resolution from a
completed link. When map evidence exists, it must identify the actual normal
archive members and shared state owners. A failed link is retained honestly;
no executable may be run by this diagnostic scope.

## Reviewed preparation checkpoint

The saved-metadata pass completed once in 0.99 seconds with all bound inputs
and producer/test hashes stable. Independent artifact review reconciled the
four response tokens, both complete field censuses, the paired cookie member
and recipe evidence, all 190 frontier targets and all four model supplements.
Private artifacts are `application-crt-adoption-plan-v1.json`,
`application-crt-adoption-v4-proposal-v1.rsp`, and
`application-crt-adoption-plan-peer-lane04-v1.json` under the ignored rebuild
tree. The plan and response are frozen. This checkpoint authorizes preparation
review of a separate consumer. At that checkpoint no native application
diagnostic or runtime adoption had occurred through the plan.

The separate pure helper `tools/rebuild/crt_adoption_consumer_contract.py`
is ready for the startup owner's consumer. It opens no files or native tools:
the caller supplies the exact plan, review and response bytes, its complete
observed selected fields, and every selected strong definition. The helper
checks the exact raw payload hashes, the complete cohort snapshot, every
per-canonical field and source identity, cookie/function role pairing and
definition collisions, then returns exactly four reviewed tokens. Unknown
scopes, changed metadata or incomplete use sets fail. Its return grants no
native permission or runtime approval.

Independent review passed seven synthetic tests, including the actual
Windows CRLF response format, and exercised the helper successfully against
both complete saved cohorts and the accepted provider namespace. A metadata
change caused by a future native format repair requires a newly reviewed
cohort contract rather than silent field normalization. At that checkpoint,
the separate actual consumer's input freeze, native operation and result review
remained required; the completed V6 observation follows.

## Actual four-binding diagnostic result

The separately reviewed V6 CRT successor used the accepted 44,353-field
cohort and all 196 affected physical uses. Its one native LINK attempt removed
exactly the four reviewed canonical names: unresolved groups fell from 277
to 273, with no added unresolved names. Independent startup and CRT outcome
reviews accepted that namespace delta. The link still failed; the result
does not establish a complete application, final-map provider closure or
runtime ABI. No application was executed.

The exact private V6 receipts are in `application-link-diagnostic-v6-crt`:
`link-receipt.json`, `independent-outcome-review.json`, and
`crt-plan-independent-outcome-review.json`. This observed linker progress
leaves the frozen 44,353-field consumer contract intact. Adding source
components requires a separate complete field census and new review before
those same global alternate names can be carried into the larger cohort.
