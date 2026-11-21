# Phase 2 plan: web agents produce source, one local coordinator verifies

Execution update (2026-11-19): the user authorized job preparation and one local
MCP test. Both are complete; see [final tally](WEB-JOBS-TALLY-20261119.md).
The test used the unresolved unit775 caller, because the proposed unit651
migration was already installed. The test source proposal remains private;
production integration and full builds were not resumed. Paid workers are off.

Proposed on 2026-11-19 after the user stopped the four Terra workers.
Planning only: workers, compilation, full builds, gameplay and MCP claims remain
stopped. This document does not authorize their restart.

MCP service repair was separately authorized and completed later on this date.
The isolated `/phase2/mcp` endpoint passes public discovery and scoped access
checks. ChatGPT connection configuration and Phase 2 job enrollment remain next;
see [connection instructions](MCP-CONNECTION-20261119.md). Workers remain stopped.

## What we are trying to finish

The current runtime pipeline already compiles the function code. Phase 2 must
recover the C++ structure around it: real classes, members, inheritance, virtual
method order and destructors, so the compiler naturally emits the original
class-identification records (RTTI) and virtual-method tables. Constructors must
stop installing numeric vtable addresses. Existing function matching stays exact.
The roughly 849 KB of generated W placeholders also need evidence-supported
types; reproducing their bytes with anonymous structs does not complete this.

The last accepted source recipe is 825d444f...2d68. Since Phase 1, 16,758 more
initialized data bytes have been placed, including 10,356 library bytes. The
81.5% initialized-data coverage is NOT a Phase 2 completion percentage. There
is no audited count of fully recovered classes yet. Private passing experiments
are candidates, not accepted class completions.

## 1. Prove the web-agent route before scaling it

Owner: local coordinator; web agents do the source reconstruction.

1. Connect ChatGPT to the repaired isolated `/phase2/mcp` endpoint. The earlier
   HTTP 401 came from the combined endpoint's independent header-key gate.
   Discovery and worker-scoped access now pass on the isolated surface. Worker
   capabilities must be delivered privately, never in public prompts or reports.
2. Confirm curated Phase 2 job enrollment and the private evidence permitted for
   that job. Existing runtime tools support board/claim/context/progress/submit;
   submit stages replacement text and does not compile, execute or install it.
   Do not assume generic function claims target this runtime's Phase 2 backlog.
3. Publish ONE bounded pilot from P2-01 below, with exact input hashes, logical
   filenames, permitted changes, known failures and acceptance criteria. Start
   with one web worker. Prove the complete loop: claim -> read context -> submit
   source -> local comparison -> return diagnostics -> corrected submission.
4. If that loop needs server work, make only the bounded job/context/result
   change needed for this pilot. Stop and report if it needs a larger redesign;
   do not start another general tooling project. Job enrollment and a usable
   diagnostic-return path are not yet verified by the failed board request.
5. Scale to at most three independent source jobs after the pilot produces an
   accepted source change. Stay within the service's actual capacity limit.
   Keep at most two submitted packages awaiting local validation.

Web usage remains subject to the user's service allowance and limits. The
compiler and game still run locally. No paid Terra workers run continuously;
use one local coordinator for packaging, review and integration. Request paid
specialist work only if the user later chooses it for a named blocker.

## 2. First source jobs, in order

These are proposed local job IDs, not enrolled MCP jobs. Each submission is
based on the same accepted checkpoint and owns disjoint files. Shared-header
changes become dependencies and are integrated serially, never edited by two
jobs simultaneously. Rebase later packages after accepting an earlier change.

| Job | Concrete source work | Evidence already available | Required deliverable / next gate |
|---|---|---|---|
| P2-01: TESContainer | Finish the remaining TESContainer declarations and move compatible views to the canonical header. Start with the already staged unit-651 caller migration and unit-980 header dependency; then reconcile the remaining views. | Accepted unit-980 pilot; 31 functions/four table slots. Scoped inventory found 25 global declarations and eight namespace adapters, which must be distinguished. | Pilot: generator-backed 651/980 change, exact include closure, all four caller and 31 owner functions plus EH preserved. Family completion: account for every active global view, layout, constructor/destructor and slot; retain or explain distinct adapters. A pilot pass alone does not complete the class. |
| P2-02: BGSBodyPartData / BGSBodyPart | Finish the native destructor ownership transfer and class tables using the existing explicit ClearData destructor candidate. | Unit 621: 10 existing functions and eight EH checks pass; new 127-byte destructor matches donor body. Donor unit 2656: 174 functions pass. | Source/generator patch, complete new destructor EH and deleting-wrapper proofs, affected callers and class views, supported symbol ownership and exact native tables. An unresolved weak destructor symbol blocks those tables; no generic weak fallback or guessed address alias. |
| P2-03: ImageSpaceModifierInstanceDOF / DRB | Finish the class layouts and native metadata after removing the artificial allocator base. | Unit 773: 39 functions pass; both six-base graphs agree; two allocation calls have source-backed replacements. | Recover remaining virtual slots, destructor/thunk identities and table/RTTI ownership; generator-backed source and complete include closure. Preserve the six-base graph and all existing matches. Do not count padding or unmatched table tails as native metadata. |

Do not roll the broad private NiMem proposal into these jobs. Its shared-header
dependencies and EH failures need their own evidence. If a job requires that
unaccepted model, mark the exact dependency and move to independent work.

After the pilot, a separate web typing job may run when capacity is available:
replace one semantically related group of W objects, aiming for 256-4,096 bytes
where evidence supports it. Deliver actual declarations, ownership/size proof,
relocations and an exact residual partition. A smaller coherent group is valid;
inventing types to meet a byte target is not. This is typed-data progress,
not a recovered-class count. The private W103 proposal is a small salvage item,
not the main milestone.

## 3. What every web agent receives and returns

Receive only the curated job context: class IDs, exact source/header versions,
relevant compiler rules, known comparisons and blockers, authorized files and
the specific source-backed question. Reuse previous evidence; no archive-wide
rescans. A job must identify every affected source unit before integration.

Return replacement source/header text for the allowed logical files, the
deterministic generator change or precise generator specification, a short
evidence table for each layout/slot/ownership claim, exact remaining unknowns,
and the checked candidate identity when checks are available. Preserve authors.
The coordinator owns generated source application and all service mutations
that the server reserves for it. A staged submission is not acceptance.

One stable worker identity and one live assignment per worker. Reconcile the
same request after disconnects; do not acquire another overlapping claim.
Each initial job gets a 45-minute reasoning timebox and at most three checked
candidate revisions. Two failures with the same unexplained cause require a
new evidence-backed hypothesis before another trial. Otherwise checkpoint the
best candidate, report the exact blocker and release the job normally. These
limits bound an investigation, not a promise to finish a class in 45 minutes.

## 4. One local acceptance queue

1. Review the source evidence, scope and base hashes. Reject guessed aliases,
   forced layout tricks and unrelated tool changes before compiling.
2. Compile the candidate in isolation with the unchanged compiler/flags and
   matching oracle. Check every affected function, ordinary EH, required tails,
   thunks, include closure and emitted class records. Reuse hash-identical
   accepted results only when their full dependencies remain identical.
3. Return one compact diagnostic report to the owning web agent: first actual
   mismatch, affected source location, relevant checked artifact and exact
   unresolved claim. The local coordinator does not take over open-ended source
   guessing. Different failing branches remain preserved.
4. Combine three to five independently passing, compatible packages into one
   integration batch; the first pilot may stand alone. Recheck their combined
   affected closure before any full run. Source changes use guarded generators.
5. Use the existing acceptance gate: canonical executable, exact relocation
   directory, fresh applicable value/pointer mutation failures with changed
   image hashes, menu/load/play/cell change/quicksave-load/clean exit, saved-run
   verification and a clean repeat before promotion. All compiler/build/gameplay
   operations are serial. Do not do a full gameplay suite for every hypothesis.
6. Tools changed since the accepted checkpoint include the p2rv/p2rp controls
   and menu detector fix. Include their exact hashes in the next batch freeze;
   their small test passes do not replace a fresh full acceptance run.

No new generic verifier or framework unless a demonstrated gap prevents a
specific source batch from being judged. A needed tool fix must name the blocked
job and the test that proves the fix. Reuse the existing checks otherwise.

## 5. Scale through a finite class and data backlog

Use the existing census as the starting list: 2,999 recognized type descriptors,
2,833 hierarchy records and 3,268 RTTI-prefaced table leads. These are different
record counts, not 2,999 proved complete classes. Reconcile duplicates, templates,
source-only classes and classes without recognized RTTI into stable class IDs.
For each ID track: evidence, bases/layout, source views, virtual slots, native
constructor/destructor, generated records, passing checks and accepted batch.

Then process small concrete families in dependency order: simple leaf classes
first, their proven reusable bases next, then dependent subclasses and complex
multiple-inheritance/template families. Change one shared base in a dedicated
batch; do not spread competing global-header experiments across web workers.
Maintain a parallel disjoint W-typing ledger. Keep file bytes and BSS separate.
The 7,171 BSS names contribute no image bytes and need their own definition work;
they cannot improve the initialized-data coverage score.

Prioritize a ready class/family over another tiny metadata-only experiment.
After three accepted source batches, require at least one fully reconciled
class family or stop to diagnose the delivery problem before scaling further.
Expand beyond three web jobs only when the validation queue stays bounded and
accepted output demonstrates that the extra work can be integrated.

## 6. Completion and honest reporting

A class counts complete only when all its required active source views agree,
its layout/inheritance/virtual interface and destructor behavior are supported,
its constructors use the native model, and compiler-generated records plus all
affected functions/EH pass and are accepted in the executable. A renamed class,
one matching unit or a partial slot list earns partial progress only.

Report after each accepted batch, or on a blocker requiring the user's action:

- Fully recovered classes/families: accepted count and names.
- Source changes: accepted methods/slots and remaining class views.
- W bytes replaced with supported types, separately from newly placed bytes.
- Remaining produced-but-unspliced bytes: current accepted baseline 190,878.
- Submitted / validated / accepted / blocked jobs, plus measured web attempts
  and local paid usage when actually available.

Do not report a whole-Phase-2 percentage until the class/type ledger is
reconciled. Calibrate throughput after the first three accepted batches; then
estimate the remaining workload from measured class complexity and acceptance
rate. The old 4-8 week estimate is not a new delivery commitment.

Whole Phase 2 requires closing the class registry and its required source/type
work against COMPLETION.md, including the placeholder typing scope. Named
unresolved items keep it open; changing the byte-coverage percentage does not
close them. Startup ordering, TLS/exception-table integration and the standard
linked executable's Steam startup crash remain later-phase work.

The next executable action, when the user resumes, is MCP authentication and
one P2-01 pilot package. Do not restart the four paid workers by default.
