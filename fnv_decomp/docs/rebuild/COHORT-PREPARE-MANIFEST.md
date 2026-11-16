# Authored cohort preparation prototype

`cohort_prepare_manifest.py` is an off-side, prepare-only prototype for reducing
per-cohort CLI, path and response-edit source forks. It exercises the unchanged
V8 and V9 response-token validators through one fixed entrypoint:

```text
python tools/rebuild/cohort_prepare_manifest.py --manifest PATH --manifest-sha256 SHA256
```

This stage reads authored fixture packages only. It produces
`prepared-response.rsp` and `synthetic-preparation.json`, with status
`synthetic-response-prepared-unqualified`. It produces no production receipt,
command, native permission, provider selection or full-proof admission. No
actual cohort, archive, game object or executable is read by the tests. Full
namespace, MATCH, native-conformance and provenance admission remain mandatory
in the existing validators and must be integrated by a separately reviewed
qualification adapter before any production use.

The exact manifest schema has these fields:

| Field | Fixed meaning |
|---|---|
| `schema_version`, `kind` | Version 1 authored response prototype |
| `phase`, `scope` | Literal `prepare-only`, `authored-synthetic-only` |
| `validator_id` | One of two closed frozen V8/V9 response profiles |
| `entrypoint_sha256`, `kernel_sha256` | Exact working source bytes; kernels cannot be selected by metadata |
| `baseline_output_relative`, `output_relative` | Distinct bounded output names in the fixture package |
| `inputs` | Role-to-relative-path mapping with full physical identities |
| `baseline_roles`, `addition_roles`, `replacements` | Exact consumed input roles, with no unused or substituted role |
| `aliases` | Literal prior/allowed/enabled IAT and CRT token facts, admitted by the frozen profile |
| `expected_response_sha256` | Authored expected output byte hash |

An input identity includes requested path, resolved path, file SHA-256, byte
size, device and inode. Each selected baseline input token must appear exactly
once. A byte-identical original library at a different path cannot replace the
physically selected library. Path lookup uses no basename, regular expression
or global string replacement. Paths must remain in the authored fixture
package; unknown members, duplicate JSON keys, path escapes, arbitrary modules,
templates, phase choices and new linker options are rejected.

The V8 profile retains its existing two-addition and alias-subset rules. The V9
profile retains its exact two-library replacement, one-addition and expanded
alias rules. Those rules live in pinned Python, not in executable metadata.
The original frozen response serializer still rejects prohibited linker policy
and unsafe token quoting. Counts are checked by those profiles; a new proof
schema or broader policy is not admitted by increasing manifest numbers.

File SHA-256 values always cover raw bytes. They are not substituted with JSON
semantic digests. Response output matches the frozen preparers' UTF-8 and
native-newline conversion; the resulting physical bytes are hashed explicitly.
The prototype checks manifest, kernel, entrypoint and input stability before
and after publication. Output is exclusive, and a failed final gate removes
the apparent completed prototype report.

The authored tests create two different temporary V8/V9 packages. Both use the
same CLI and identical entrypoint bytes, match manually expected response
bytes, and agree with the public frozen response kernels. Adversarial cases
cover the selected-library copy mistake, requested/resolved/file identity
changes, duplicate tokens, raw-byte newline changes, unsafe aliases/options,
schema and profile drift, CLI startup, exclusive output and final input drift.

## Qualification boundary

1. Independently review and freeze this source, test and document group.
2. Separately review a narrow adapter from existing complete validator results
   to manifest input roles. It must preserve every original source, namespace,
   full-field proof, MATCH, native and review identity; manifest booleans cannot
   stand in for any admission proof.
3. Under a separately approved bounded metadata lease, shadow a known accepted
   cohort and compare response bytes and complete input/proof provenance against
   the frozen preparer. The active V10 tools remain untouched.
4. Measure setup and review effort for a later unchanged-policy cohort with no
   Python changes. Until then, no timing reduction or faster playability is
   claimed.

Stop if the two authored cohorts require different entrypoint bytes, if a new
module/template field is needed, or if a production adapter merely transfers
proof semantics into metadata. Source changes for genuinely new proof policies
remain independently reviewed work; this prototype does not remove them.
