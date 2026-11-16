# Saved static reference index

`tools/rebuild/static_reference_graph.py` builds a conservative planning index
from the saved planned physical-provider map and complete selected-function
binding metadata. It never opens native objects, original source, the game image,
archives or services. The first source version intentionally does not interpret
the DATA-owner stream, prepared overlays, callbacks or initializer ownership.

The provider map supplies physical identities `(recipe_id, object_sha256,
symbol_index)` and source-field geometry. Each saved field joins its exact
recipe, selected address, function name and physical section. A known static
CODE reference additionally requires exact own-source resolution, one
nonoverlapping field contained in the selected function, ordinary DIR32/REL32
with zero addend, one unambiguous selected target owner at offset zero, and equal
selected/base/expected/observed target identities. IAT names, absolute migration
conflicts and special classes cannot become CODE edges.

Every other field stays an explicit unknown with a category. Literal tolerance
does not merge addresses. Unselected and interior CODE targets do not become
providers. DATA, TLS, EH, imports and normal CRT candidates do not acquire
ownership from this index. Nodes with no saved field rows remain unknown; they
are not established dependency-free leaves.

Output is restricted to names and typed physical source/target field identities.
Original operand values, addends, literal payloads and code bytes are never
copied. One compressed-byte hashing reader authenticates the saved binding
stream while parsing it. Summary event, classification, proof and relocation
censuses must reconcile exactly. The historical producer hash is recorded from
the pinned summary; current producer source is not asserted identical.

The index reports known-edge strongly connected groups, explicit-seed known
closure lower bounds and unknown frontier categories. A seed is an exact
physical identity supplied in the reviewed manifest. A diagnostic entry seed
does not establish the executable entry point or Game reachability. Known static
references can include address-taking and do not establish execution or calls.
Indirect calls, vtables, dynamic loading, callbacks, initializer execution, DATA
pointer graphs and missing metadata remain open mechanisms. No playable ETA,
complete remaining-work total, provider choice, alias, MATCH or runtime approval
is derived.

Production requires an independently reviewed exact manifest and resource lease.
Its only allowed inputs are three exact saved files under `build/rebuild`: the
provider map, binding summary and gzip JSONL binding detail. Public tool and
manifest hashes are checked before and after publication. Saved input hashes are
verified in their single read pass; file identity, size and modification time are
checked afterward. This is deliberately not a claim of a second post-read
cryptographic input scan. Inputs must remain frozen during the operation.

Bounds are 900 seconds, 1 GiB peak process memory and 128 MiB total retained output;
rows, line sizes, decompressed size, nodes and admissible field identities also
have fixed caps. Outputs use a new ignored directory, exclusive files and owned
inode cleanup on failure. A failed or incomplete pass publishes no success
manifest. There is no automatic retry. Only derived outputs are rehashed.

The source, exact inputs and bounded launcher passed independent review. All 22
index tests and ten launcher tests passed, including an authored Python-only
suspended-process/Windows-Job smoke case. Existing planners remain unchanged.

One approved saved-metadata pass completed in 17.344 seconds, with 251,805,696
bytes peak working set and about 27.3 MB retained output. It accounted for 68,657
planned physical identities and 490,801 field/migration rows. There are 288,731
known selected CODE field references and 181,549 distinct static edges; 202,070
field records remain in explicit unknown categories. The 7,550 nodes without
field rows retain unknown coverage.

For the explicit diagnostic seed, the known static subgraph contains at least
16,838 identities in 13,265 strongly connected groups, plus 58,806 unknown field
records. These are not counts of unimplemented functions or unique unfinished
contracts. Prepared cohorts were not joined, references can take addresses, and
dynamic mechanisms remain unknown. The index does not establish a playable ETA.

An independent derived-only review recomputed all node/field counters, known
edges, groups and seed lower bounds. It did not reread the original provider map
or binding stream. The accepted manifest is the ignored
`build/rebuild/static-reference-index-v1/manifest.json`; the independent outcome
review has SHA-256
`1b82947817ad7917a7b7f99a49a18751d67096d2806c4f704e2b77607618d886`.

The projected reference stream preserves the original binding stream's pinned
hash and each row's one-based ordinal as a raw-authority locator. It does not
preserve full binding payloads or per-row hashes. Full root contracts must still
come from accepted contract caches or a separately reviewed bulk collection;
the planning index cannot replace that evidence. Do not repeatedly hydrate the
original global stream for individual workers.
