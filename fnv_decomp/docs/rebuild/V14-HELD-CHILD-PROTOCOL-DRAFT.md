# V14 held-child protocol: design draft, not authority

This draft is not an implementation, review, launch authorization, or evidence
that a factory run is safe. The current launcher has no held-child protocol.
The V14 factory entry remains closed.

## Scope and trust

The protocol assumes the reviewed launcher, child, Python runtime and operating
system cooperate, the private control and lease directories have stable trusted
owners, and no hostile same-user process substitutes files or handles. It does
not prove safety against a hostile process. All paths and source/runtime closure
must be independently reviewed and pinned before an actual operation. No generic
caller-supplied approval, dynamic module substitution, CLI-selected operation,
or cross-operation/global authority is acceptable.

The child's reviewed policy must bind the exact operation, inputs, outputs,
launcher/runtime identities, lease scope, phase sequence, and bounds. To avoid a
self-hash cycle, that policy need not contain the child's final source hash: the
parent's independently reviewed binding must pin the final child source hash,
and the child must check its current source against that binding. A parent
binding alone is not a substitute for independent operation-policy approval.
Pin exact process image paths and hashes as well as complete interpreter/import
closure. The operation must give each output an exclusive role and ownership;
the phase list and its order are part of the reviewed policy.

## Proposed protocol

1. Parent verifies its exact reviewed binding, source/runtime closure, lease and
   all prelaunch conditions. It generates independent unpredictable session and
   Job identifiers, creates a unique named Job, and rejects an existing name.
   It checks the exact factory profile (1 GiB, 900 s, kill-on-close and no
   breakaway), and creates a unique named-pipe server. No Job handle is inherited.
2. Parent durably records a new immutable prelaunch intent with the operation
   and policy digest, full input/output and source bindings, exact lease grant,
   parent PID and creation FILETIME, session nonce, and exact Job/pipe identities.
   It creates the child suspended and atomically in that Job, recording its PID
   and creation FILETIME in an immutable started record before resuming it.
   Record stable file identity as well as exact bytes for both control records;
   recheck both on every phase. The lease must have a unique immutable grant
   identity/generation, not merely mutable fields that could be revoked and
   recreated with the same values. The current registry has not been shown to
   provide that identity; this remains a prerequisite.
   The child's only inherited handle is the explicit read-capable pipe client.
3. Parent sends one bounded, framed session message over the held pipe. The
   child must reject truncation, EOF, duplicate JSON keys, noncanonical values,
   stale or additional frames, and every mismatch with its reviewed policy and
   durable records. The child's pipe endpoint must verify the server PID using
   the Windows API; it then independently verifies the live parent's PID,
   creation FILETIME and image, its own PID, creation FILETIME and image, and
   the actual parent relationship. PID alone never establishes identity.
4. Child opens the exact named Job for query only, verifies its own membership,
   the exact census and queried kernel profile, and closes that Job handle on
   every path. A failed or uncertain close is terminal. Child checks parent
   liveness and current exact lease again after the close before any work.
   Parent retains its Job handle throughout the child lifetime. A crash during
   the temporary child query can delay kill-on-last-handle; this is not a proof
   of race-free crash containment.
5. Before and after *each* separately enumerated protected source, object,
   reference and publication phase, the child rechecks the complete binding,
   session and immutable control records, parent/child identities and process
   image paths/hashes, exact named
   Job membership and limits, current lease grant/state/scope/expiry, and policy
   pins. No authority result is cached across phases. Each query handle is
   closed successfully before returning from the guard; the parent and lease
   are checked again after closure. Failure is terminal and must prevent the
   following protected read or publication. Phase checks do not make a
   protected action atomic with lease revocation or filesystem mutation.
6. Preserve a durable ledger of session, phase checks, failures and publication
   outcome. The parent supervises the process, retains the held endpoint and
   Job until process exit, and records terminal reconciliation. Neither a smoke
   result nor an unverified checkpoint grants factory authority.

## Remaining implementation and review

The precise schemas, pipe creation and inherited-handle allowlist, full x64
Windows API bindings, control-file durability, stable-path handling, lease
interface, source/runtime import closure, and phase integration must be built
and jointly reviewed. Tests need adversarial parent and PID-reuse, nonce,
operation, policy/source/interpreter, Job/census/limit, lease expiry/revocation,
control drift, close failure, and pipe EOF cases. A separately reviewed finite
authored fixture and fresh lease are prerequisites for any live Windows smoke.
The existing 64 MiB smoke profile is mechanism evidence only and is not the
1 GiB/900 s factory profile. No original, reference, compiler or game input is
authorized by this draft.
