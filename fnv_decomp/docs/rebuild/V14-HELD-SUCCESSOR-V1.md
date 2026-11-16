# Held factory successor v1: review candidate

Owner: `/root/sol_bootstrap_terra_failure`, explicitly assigned as the limited
Sol fallback after the Terra bootstrap task failed. This is implementation, not
factory or native launch evidence. The frozen old smoke launcher is unchanged.

`tools/rebuild/factory_held_launcher_v1.py` owns both the parent launch and the
child guard. `factory_held_child_v1.py` only reads one canonical bounded stdin
frame, verifies the parent source bytes, and enters that source's child path.
`tests/rebuild/test_factory_held_launcher_v1.py` uses synthetic Python fixtures;
it does not create processes, invoke Windows APIs, compile, or read game inputs.

The exact external profile SHA is supplied by a separately reviewed once-only
root command, not by a payload command, environment variable or approval boolean.
No actual profile or actual command is configured here. The external command
pins the parent bytes before executing them in a fresh `-I -S -B` interpreter;
`parent_command` constructs this command but does not execute it. The profile
pins the parent, child, interpreter image, complete project source closure and
metadata whitelist. It binds the fixed driver `held_entry(profile, guard)`,
operation paths/hashes, output roles, exact phase sequence, owner/slot and exact
canonical existing lease row (all fields except granted/running state).
External profile pinning avoids a profile/parent self-hash cycle.

The child now registers its verified bootstrap module under
`_fnv_verified_held_bootstrap_v1` and issues one process-local capability for its
actual Guard, profile object, session digest and operation digest. A matching
duck-typed object or a newly constructed Guard has no capability. Before its
protected accesses the driver pins the exact reviewed bootstrap source hash,
reads only that fixed sibling tool source, and executes it into an independent
verifier. `authenticate_runtime` compares the registered Guard/verifier method
code and globals to those independent definitions before invoking
`require_held_guard`. The real runtime then consumes the sole issued entry once
and performs another complete live source/profile/session/PID/Job/lease check.
The child rejects a result if the driver did not claim that capability and clears
the capability after entry completes. A forged no-op fixed-name verifier is
rejected. This is a cooperative process integrity check, not security against
arbitrary hostile Python memory rewriting or copying live interpreter state.

The parent creates a new named Job with queried 1 GiB aggregate committed-memory
limit, kill-on-close and no breakaway flags. It creates a suspended process with
atomic Job-list assignment and an explicit inherited-handle list containing
only the stdin pipe reader. Before resume it verifies actual membership, exact
initial census, creation FILETIME, interpreter and current lease. The parent
keeps its noninherited Job handle until the process and Job census drain. It
supervises the 900-second wall deadline and output allowlist. An independent
reviewed outer watchdog remains a prerequisite; synchronous OS calls do not
establish a hard wall-time bound on the parent itself.

The child verifies session nonce, parent/child PID plus FILETIME and image,
actual parent PID, durable started/intent records, exact profile/source/runtime
and metadata hashes, and current lease. Each check queries the named Job's
actual limits, membership and census. It closes its temporary Job handle before
any payload and rechecks live identities and lease after closure. An uncertain
close is terminal, with no retry of the numeric handle. Parent pipe EOF before
a complete session fails; parent loss after bootstrap fails subsequent guards
and closes the sole long-lived Job owner. Creator-death behavior is unproved.

Project modules load from verified private byte snapshots before any project
import. The fresh interpreter excludes cwd, script directory, environment and
site; the finder also rejects an unlisted project import if reviewed code later
adds a project directory to the import path. The known interpreter installation
and standard library are trusted. This does not claim hostile same-user,
interpreter-installation, filesystem, kernel or cryptographic server attestation.

`guard.check(phase)` consumes the exact next scheduled phase; skipped/reordered
checks or missing completion fail. `guard.refresh()` performs all authority
checks without advancing the sequence, for publisher stability callbacks.
The fixed 15-selection sequence includes metadata, source snapshots, reference,
15 source/object pairs, final stability, publication and entry completion.
The driver owns the readable C++, official compiler/image/span/hash/plain
before/after MATCH gates. This transport does not replace or weaken them.

A driver result with blocked selections exits 3. Unknown statuses, incomplete
censuses and late post-publication guard failures fail. A published file can
remain after a late failure: it is quarantined, never admitted merely because
it exists. Admission requires a successful control terminal and independent
outcome review. Owned failure artifacts remain for reconciliation; there is no
automatic replay or cleanup of another operation's outputs.

Lease and filesystem checks are samples under a cooperative trusted local
single-writer, stable-tree model. Revocation followed by undetectable same-value
restoration between samples is not detected. A random nonce binds a session;
it is not signed authentication. The existing schema need not gain an invented
monotonic generation to implement this cooperative protocol.

Resource review is still open. The driver reports 163,213,297 bytes in twenty
known metadata inputs, excluding a future operation/review. Root approved the
bounded source implementation for review: exactly 22 metadata files, at most
64 MiB per file and 192 MiB aggregate, freshly streamed in 1 MiB chunks on each
check. This preserves full hashes and does not cache freshness across phases.
The successful path performs 84 full metadata sweeps: four parent pre/post
checks, one initial child authority check, 73 scheduled child guard checks,
five publisher guard refreshes and one entry-capability refresh. The existing
twenty files alone contribute 13,709,916,948 bytes (13.71 decimal GB). This is not total IO: add the future
operation/review files, interpreter image, parent/child/project source pins on
each sweep, the extra import snapshot, and profile/control/lease reads. Driver
metadata reads and protected reference/source/object reads (including its four
full stability sweeps) are additional. The exact full read schedule and resource review remain
prerequisites; source-cap approval is not execution approval or a 900 s/1 GiB
waiver. No native test or production read is authorized by this document.
