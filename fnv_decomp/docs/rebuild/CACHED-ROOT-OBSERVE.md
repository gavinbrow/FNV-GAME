# Fresh observations from qualified binding contexts

`cached_root_observe.py` observes the exact 180 newly requested selected owners
across 77 recipes using the 257 accepted singleton and recipe-union metadata
contracts. It preserves each qualified contract and its V11 request provenance
unchanged. The current V12 frontier is a separate input: its only change is removal
of an already prepared owner. Qualification supplied field authority, not a prior
positive or negative certificate.

The new policy is `cached-context-root-observation-v1`. Its finite operation names
15 hash-bound metadata artifacts, the observer source digest, an explicit epoch,
and fixed limits of 900 seconds, 1 GiB measured peak process memory, and 128 MiB
combined output. An unavailable memory counter fails closed. Limits are sampled
checks, not operating-system quotas. No request truncation or automatic cap
increase is supported.

The pure `observe_recipe_contracts` seam validates exact selected and retained
section/value/symbol identities, metadata-only view schemas, full-unit shared
evidence, singleton partitions and the final union. It hashes and parses one
fresh original COFF byte buffer per requested recipe, then invokes the unchanged
ordinary observer. Only unsupported COFF parsing produces a structured format
blocker; contradictory identity, relocation or authority evidence aborts the
whole operation. Empty field or EH lists establish no independent closure.

The runner hashes the exact compressed qualified bytes consumed by its gzip
reader and validates all original row ordinals and singleton metadata hashes.
It streams one output detail gzip without retaining duplicate full-contract
copies. It requires all 257 views and the compressed EOF/hash before publication.
Named source files are hash-checked and named objects are read once for fresh
observation; both are rehashed for stability. It reads no binding or owner stream,
cache frames, original image, archives, or historical native roots.
The receipt counts observation reads separately and explicitly records the
additional physical reads used by stability rehashes.

Each detail envelope contains the unchanged contract and its hash, qualified row
identity, fresh observation provenance, and the fresh ordinary certificate when
parsing succeeds. The base observer's result is preserved. EH, SafeSEH, TLS,
directives, aliases, local labels, data and missing fields receive no waiver.
Graph completeness and ordinary closure are reported separately from the
always-false runtime, provider, namespace, ABI and serialization flags.

Outputs are exclusive summary/detail files and a crash-persistent progress
journal. Publication checks source/input stability and optional-index absence
before and after both writes. Failure removes only outputs created by that
attempt whose current filesystem identity still matches; an exclusive-create
race or foreign replacement cannot delete another process's file. Both output
hashes are checked after the final gates and journal close. The bounded journal
has reserved space within the combined output limit. The
original inputs and frozen collectors are never modified. A failed or partial
journal is not a completed receipt.

The CLI takes `--operation`, `--operation-sha256`, `--out` and `--details`.
The journal path is the summary path followed by `.progress.jsonl`. Independent
source/input review and the coordinated metadata lease precede actual input
observation; independent saved-output reconciliation follows it. This mechanism
does not emit COFF, compile, link, execute, adopt providers, or admit game code.

Authored tests cover direct frozen-observer equivalence, one parse per recipe,
the complete 180/77/257 shape, borrowed identities, exact metadata-only schemas,
strict integer and digest types, field/union partitions, compressed-byte
authentication and EOF, resource-counter failure, exclusive publication races
and post-publication drift cleanup. Test fixtures contain original synthetic
COFF, not game bytes.
