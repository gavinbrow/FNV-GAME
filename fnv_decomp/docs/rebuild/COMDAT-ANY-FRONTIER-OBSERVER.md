# Finite V8 COMDAT witness observer

`comdat_any_frontier_observer.py` is an evidence-only operational adapter.
Development and review initially use source and authored fixtures only. Actual
use requires an independently reviewed exact request/context and root-delegated
observation authorization. The adapter does not read a reference image, call a
native tool, emit a COFF or library, or adopt a provider/application manifest.

The CLI takes `--request`, `--request-sha256`, `--context`,
`--context-sha256`, `--review`, `--review-sha256`, and `--out`. The request is
the entire saved output of the independently accepted V8 negative context
selector, including every candidate and its 467-demand audit. It is not a
hand-picked subset or a truncated count. The adapter freshly reruns the selector
against the hash-bound V8 frontier, 269-root registry, and new259 receipt.

The context has exact keys:

```
schema_version: 1
kind: finite-comdat-any-frontier-observer-context
epoch: an explicit ASCII observation label
request_sha256: exact request file digest
artifacts: frontier, registry, new_receipt, manifest, retained, selection,
           recipes, prepared_epoch, epoch_review
acceptances: selector_freeze, selector_review, comdat_source_review,
             comdat_authority_review, metadata_review, new_receipt_review
sources: [{kind, receipt, request, details: [{lane, path, sha256}]}]
provider_selected: false
runtime_eligible: false
emission_performed: false
reference_image_read: false
```

Each artifact, acceptance, receipt, and request reference is exactly
`{path, sha256}`. Paths resolve inside the project; metadata/detail paths stay
under private `build/rebuild`, while the original recipe manifest may resolve
elsewhere inside the project. Central detail references name only the selected
lanes (integer 1 through 8). Frontier details use `lane: null`. There is one
source entry for each distinct selected receipt/request authority, with no
additional lanes or authorities. The actual finite candidate count comes from
the complete selector output.

The accepted V8 artifact and source-review hashes are pinned in the adapter.
The original manifest/retained/selection/recipe hashes retain their immutable
native epoch. Their original raw files are hashed before JSON parsing; the
adapter does not guess their original pretty-printing or newline convention.
The known compact V8 metadata formats follow the selector's exact binary-LF
versus Windows-text-CRLF document rules.

The prepared epoch is the immutable upstream V8 planning epoch with 14,403
ordinary and 14,409 collision entries. It is used only to preserve the historical
request exclusion boundary. This evidence-only observer makes no latest
prepared-namespace claim. Any future projection must independently reconstruct
the current prepared exclusions, including subsequently accepted cohorts, and
authenticate the complete planned provider map.

An exact independent input/source review is mandatory. The review schema in
`review_gate` binds the complete request/context hashes, all owned source/test/doc
hashes, producer pins, named reviewer, and delegated authorization. It explicitly
permits original object observation and source hashing while denying reference
reads, native tools, and code emission. Context acceptance files are hash-bound
inputs; their independent outcome interpretation belongs to that input review.

For each authority, receipt/request roots and selected summaries/ordinals are
joined without borrowing an epoch or lane. Only selected detail rows are parsed.
Unselected lines in those exact hash-bound gzip files are bounded-skipped to
reach locators and verify the declared extent; no owner/binding stream, archive,
directory glob, or global object scan is used. The reader caps each uncompressed
line at 64 MiB and each selected source file's expanded extent at 4 GiB.

Each original row must match its source-record hash, full ten-field physical
root, negative certificate, contract hash, request provenance, blocker counts,
and typed closure/graph state. The original selection, recipe, and complete
retained unit proof are rejoined. The original source file is freshly hashed,
and the requested original COFF is freshly read with a 16-MiB bound. The native
census preflight freshly replays the frozen ordinary negative graph. Unsupported
native ownership forms produce explicit no-policy evidence with every original
blocker retained. Schema, hash, source, physical identity, or graph contradictions
are fatal and cannot become a normal unsupported result.

A qualified native census feeds the unchanged Selection-2 witness producer and
new COMDAT composer. The original negative certificate remains negative and is
included unchanged. Only the exact root-conjunct policy can discharge; all other
blockers remain. No Selection 2 to 1 normalization or fake positive ordinary
certificate is introduced. A complete composition establishes evidence for
separate consumer review, with every provider/runtime/namespace/link/emission
approval flag still false. Future projection additionally needs fresh field
operand/HIGHLOW checks and ordinary before/after plain MATCH.

Outputs are private `observations.jsonl.gz`, source snapshots, a durable journal,
and a terminal metadata receipt. The frozen resource/publication helpers retain
sampled 900-second, 1-GiB peak-memory, and 128-MiB owned-output limits, exclusive
output creation, pre/post input hashes, journal closure before terminal receipt,
and rollback of the attempt's terminal receipt link after failed postgates.
Completed evidence and source snapshots are registered in that same stable hash
gate, so their drift also prevents a successful terminal receipt.
An abort or incomplete run has no successful terminal receipt. The observer's
`emitted` count is always zero.

The owned tests construct original authored COFF/negative records and temporary
gzip files. Independent tests cover source/body authority and reader/native
boundaries. No actual input observation is authorized by those synthetic passes.

The accepted finite V8 observation covered all nine candidate roots across five recipes. All nine qualified for the original native-definition census; only 0x008d8520 had a complete typed COMDAT composition. Eight retained independent blockers. Original negative certificates and blocker occurrences were preserved, with zero code emission and no reference image or native execution. Independent saved-outcome reviews accepted the evidence. Its historical upstream epoch was planning evidence, not a claim of current provider or application selection.
