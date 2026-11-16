# V13 cached CODE metadata inventory

`tools/rebuild/cached_code_frontier_inventory_v13.py` reconciles the fixed, accepted
V13 frontier of 593 CODE demands. It preserves the four original observation
authorities (528 singletons) and adds the accepted cached-native observation's
180 distinct singleton summaries. All 77 union summaries remain evidence only.
Their whole 257-record census, original native and qualified ordinals, record,
contract, certificate and qualified metadata hashes are retained separately.
Qualification created no certificate. An unsupported native format may retain a
negative summary with no certificate; it cannot become a positive candidate.

The accepted collision epoch is reconstructed by the frozen
`prepared_code56_successor.from_bytes` from the exact parent, handoff and member
ledger bytes and compared with the accepted saved epoch. Historical record
order and namespace roles are preserved. Its 14,528 ordinary names and 14,534
collision names do not establish an application selection. The absent adoption
flag stays absent; no false value is invented. All six canonical reference-group
quarantines remain distinct from prepared and negative observations.

Each of the 593 demands receives one planning state. Prepared, quarantined,
namespace-unproved and cached-negative demands are ledger-only. Only genuinely
unobserved selected roots and unprepared ordinary positives request fresh cached
metadata. The 72 additions in the LINK delta are not assumed to be the hydration
count. No old observation detail stream, original object, source body, archive,
reference image, global binding stream or owner stream is reopened.

The immutable lossless-cache adapter reads each selected full recipe frame once
and preserves full-unit incoming, missing and omission evidence. Root field,
missing, parent-EH and omission counts overlap; one primary planning state is
reported without adding these counts into an unlock forecast. Zero binding rows
remain `NO_BINDING_ROWS_NATIVE_COVERAGE_UNKNOWN`. Contracts have new metadata
identities and explicitly require a future native observation. No certificate,
provider, serialization, application, ABI or runtime approval is created.

The frozen selected-range guard, compressed bounded sink and atomic publisher
are reused. Selected compressed ranges are freshly verified before and after
publication; whole-cache hash and unrequested frame verification remain false.
Known source and saved JSON identities are checked separately. Limits remain
900 seconds, 1 GiB peak memory and 128 MiB private output; exceeding a cap aborts
without truncation or a cap increase. The exclusive output is
`build/rebuild/cached-code-frontier-inventory-v13-v1`.

Source and authored tests precede independent main and authority reviews, an
exact saved-input gate, a metadata lease, one coordinated run and independent
saved-output review. No actual V13 metadata or cache-frame read has occurred in
the source implementation stage.
