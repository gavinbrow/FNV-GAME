# V8 negative root context selection

`tools/rebuild/comdat_any_frontier_contexts.py` is a pure, opt-in metadata
selector. Its entry point is
`select_candidates(frontier, registry, new_receipt, new_receipt_sha256)`.
It accepts the exact V8 profile: 467 CODE demands, the distinct-authority
269-root registry, and the new-frontier-v3 receipt covering 259 new roots.
It opens no files and does not inspect a native object, reference image, source
body, or contract body. The caller must authenticate the accepted artifact pins
and their independent reviews before calling it. A self-consistent synthetic
receipt is useful for testing and is not production authority.

The selector accounts for every demand and every new singleton and recipe union.
It joins ten-field physical roots and canonical demand names, typed cached
summary/source locators, the three distinct historical receipt/request
authorities, and the new receipt's registry/frontier/request hashes. Exact
envelopes and boolean/integer types are checked. Cached contract identity stays
`null`, bound through the exact record hash until an authenticated body is read.
The new authority additionally retains the details-file hash and record ordinal.
No summary-derived substitute contract digest is created.

The document hashes intentionally follow two different frozen producers.
`base.save_json` writes sorted compact JSON plus LF as binary bytes for registry,
frontier, and request. `finite.publish_summary` writes insertion-order compact
JSON through a Windows UTF-8 text stream, producing a terminal CRLF for the new
receipt. Preserve parsed dictionary insertion order and use the actual receipt
file SHA. Reformatting or changing the receipt key order is rejected. This
Windows producer profile does not silently accept another newline convention.

The result contains sorted `roots`, `candidates` carrying the exact root,
summary, authority, and demand identity, and an `audit` entry for all 467 demands.
Only negative singleton summaries with
`UNSUPPORTED_OR_PARTIAL_ROOT_SECTION` and an authenticated certificate digest
are selected. All other blocker names and their multiplicities remain intact.
Positive new summaries are preserved without selection. The 3 prepared skips,
25 unselected or unproved demands, and the reference-group quarantine at
`0x0086beb0` remain excluded. The quarantine's supplied digest remains a demand
input; it is not replaced by a policy inference.

A selection means an exact original body is needed for further assessment.
It does not establish that Selection 2 caused the root blocker. The separately
reviewed native census preflight and COMDAT witness must freshly establish that
fact, preserving the original negative certificate and every independent
blocker. No census, native form, namespace, provider, link, serialization,
materialization, or runtime approval follows from this selector.

The authored fixture in `tests/rebuild/test_comdat_any_frontier_contexts.py`
constructs the complete metadata counts without any original inputs. Independent
authority negatives live in
`tests/rebuild/test_comdat_any_frontier_contexts_authority.py`. These tests do not
authorize actual input observation or emission.
