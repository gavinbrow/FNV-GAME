# Exact binding stability selection

`tools/rebuild/exact_binding_stability.py` is an opt-in caller utility. It does
not alter `application_link_diagnostic.stable`, any frozen caller, or the full
`input_bindings` ledger retained in a receipt. Callers keep that ledger verbatim.

`stable_phase(bindings, phase='pre' or 'post', stable_fn=authenticated_delegate)`
selects the first occurrence of each exact complete six-field identity dictionary
and calls the delegate once with copies. Each invocation builds its own selection;
there is no cache across pre/post phases or other invocations. Exceptions propagate
without retries. After return, both the selected snapshot and original ledger are
checked for mutation before completion metadata is returned.

Deduplication skips repeated observations within a phase. It can miss transient
file drift between duplicate occurrences that the old repeated pass might catch;
neither pass is atomic. Pre and post remain independent complete unique checks.
This observation-frequency limit must be retained in any adoption decision.

The schema is closed: requested_path, path and lowercase SHA-256 are nonempty
strings; size, device and inode are nonnegative integers, excluding booleans.
Dictionary insertion order does not affect equality. No path normalization,
case-folding, basename substitution or physical-origin substitution occurs.
Distinct requested aliases remain separate checks even when they resolve to the
same file. A requested path with conflicting complete identities, or a resolved
path with conflicting hash/size/device/inode expectations, fails before delegation.
Unknown fields fail rather than being silently removed.

The utility cannot authenticate an arbitrary callable. A production caller must
bind the actual immutable diagnostic stable function, its loaded source and
closure using the existing source/provenance gates. Returned counts/digests are
selection metadata, not admission, MATCH, native provenance or runtime authority.
Namespace, full proof, lease and publication checks remain the caller's work.

`select_exact_bindings` is the pure selection interface for a separately reviewed
saved-only qualification. Such qualification may read only its exact approved
derived receipt and must not invoke identity or read historical library/object
paths. It can measure selection CPU cost and check-count reduction. It cannot
establish actual storage I/O savings or fresh historical file stability.

Owner tests use authored identity dictionaries and temporary authored text files.
No V13 adoption, original/archive read, native call, or performance claim follows
from source tests. Actual saved-only qualification requires independent source
and exact-input review and the coordinator's bounded metadata lease.
