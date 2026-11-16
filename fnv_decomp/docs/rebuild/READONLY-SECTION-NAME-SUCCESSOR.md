# Read-only DATA section-name successor

The actual v3 native link diagnostic reported `LNK4078`: the two accepted small read-only DATA objects use section name `.data` while normal CRT `.data` contributions are writable. Matching names with different characteristics can cause the linker to merge incompatible contributions. This is a diagnostic finding, not a demonstrated runtime or application link. The earlier producer and its artifacts remain immutable.

A bounded read-only audit of the two existing private objects confirmed their receipt `b1a6554ad8170f06f7367a21d5b6ecd6b8b6c910e3fa3241ef8a3bde039db792`, the two saved object hashes `2243cf180e35988042c930514b7b3ae54cdab4cafa951c179312537e4000e67e` and `1b786bd7a6fbef349327851bbc8ebc350b3deabb9ca190144bf7b33f2a26f686`, and one section per object named `.data` with flags `0x40100040`, respectively 219 and 227 raw bytes, and zero relocations. The respective physical symbol counts are 11 and 9, including the existing anchors, feature records and 16 aliases. The original receipt records 20 entry fields. This observation neither re-establishes semantics of the data nor approves a provider.

`tools/rebuild/readonly_section_name_successor.py` is a separate, fixed-input proposal. It changes only the eight-byte COFF section-name field from `.data` to `.rdata`, preserving the entire rest of each object byte-for-byte, including flags, storage, symbols, indices, offsets and relocation state. The exact original hashes and receipt bind the inputs; no arbitrary COFF or game input is accepted. The new output receives a separate receipt with input/output hashes, review/source identities and unchanged counts. The name change alone cannot prove native linker behavior, input ABI, gameplay, or link readiness.

Synthetic tests use invented payloads and temporary files, and check exact byte preservation, malformed shape, stale input/review, output collisions and input drift:

```text
python -m unittest discover -s tests/rebuild -p test_readonly_section_name_successor.py
```

Source review and a separate root authorization are required before use on the actual two private objects. The review JSON must specify kind `readonly-section-name-successor-review`, nonempty `reviewer`, `approved: true`, `root_authorized: true`, the exact `source_sha256` and `input_receipt_sha256` above. After those gates only, an operator may use private placeholders:

```text
python tools/rebuild/readonly_section_name_successor.py --input-dir <private-accepted-input-directory> --review <private-exact-review-json> --output-dir <new-private-output-directory>
```

The output directory must not exist or overlap protected inputs. The tool reads and stages the two objects in memory, rechecks inputs, then exclusively creates the new directory, objects and receipt. An error removes only files created by that attempt. It never changes the old producer or inputs. Native inspection/linking and acceptance of a new diagnostic lane require their own authorization and remain future work. No actual successor objects or native operations were produced for this source proposal. The independent whole-DATA provider bridge and its binding operations are outside scope.
