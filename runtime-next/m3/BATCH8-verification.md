# Batch 8 verification

Status: **Phase 1 acceptance gate complete with explicit deferrals; Batch 8 defaults promoted and verified.**

The accepted full no-overrides run is `out/batch8-promoted-default-verified`: status `ok`, canonical SHA-256,
exact baseline relocation bytes, 8,263 selected/kept definitions, zero drops, new quicksave, changed then restored
cell IDs and normal QuitGame exit 0. Its range audit confirms 1,596,260 initialized `.data`/`.rdata` bytes from
objects (80.6%). One recognized console-close action restored the HUD; no pause recovery was recorded.
The earlier failed attempts remain failed and archived. Earlier HUD-only PASS flags below are historical;
they did not establish quickload restoration with the profile's F6 binding. The final semantic runs do.
Remaining source types, aliases, BSS and later-phase ranges are explicit in `BATCH8-deferrals.md`;
The user subsequently authorized Phase 2 generator-backed source changes on
2026-11-18; protected source still uses generators and the unchanged matching gates.

Read-only final evidence check, from `runtime-next/m3`:

```powershell
python tools/verify_saved_runs.py --positive out/batch8-promoted-default-verified/build-summary.json --default out/batch8-baseline/build-summary.json --control out/batch8-final-negctl-b8v/build-summary.json --control out/batch8-final-negctl-b8p/build-summary.json --verdict out/batch8-promoted-default-verified/harness-verdict.json --check-control-logs --require-extended-mode --expected-selection batch8_final_selection.json --expected-control b8v --expected-control b8p --expected-selection-sha256 42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7 --require-cell-state
```

## Builder rewrite audit

The audit follows every mutation in `layout-v2/make_image.py` after M3/DV1 overlays. General data relocation cells are rewritten from object relocations at lines 301–317; they are part of the overlay's pointer semantics and are not wholesale exclusions. The only unconditional writes into data chunks after that loop are the import-region and IAT `put_data` calls at lines 318–335. Running `build_imports.build` on the current checked-in `iat_spec.json` yielded these original VA ranges, exactly matching the selector exclusions:

| Range | Size | Builder action |
|---|---:|---|
| `[0x00fdf000, 0x00fdf4a4)` | 1,188 | Rebuilt IAT |
| `[0x0118062c, 0x0118204c)` | 6,688 | Rebuilt import region |
| `[0x0110147c, 0x01101494)` | 24 | Conservative TLS directory exclusion; builder computes the relocated directory address and handles its pointer cells in the general relocation loop. |

The nearby TLS comment states `0x112147c`, but the executable expression `BASE + 0xd0147c` evaluates to `0x110147c`, matching the exclusion. Code rewrites apply to the separately assembled `.text`; resources and `.reloc` are generated in separate sections; directory fields are written to the PE header. This audit applies to the current builder/spec and original data ranges; it is not a guarantee against future changes. Selector integration must independently check the effective Batch 8 selection against all three ranges.

## Serialized run plan and recorded results

The plan required a fresh legacy baseline, selected positives, value/pointer controls with round-trip failure and changed image hashes, repeat builds, exact relocation-byte comparisons and full gameplay/clean exit. The required image SHA-256 is `c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`. Builds and gameplay were serialized; independent snapshots, commands, summaries and failures were preserved. The ledger below records that sequence, including the final stronger semantic acceptance run.

Baseline operation: `runtime-next/build-all.cmd --out runtime-next/m3/out/batch8-baseline --no-harness` from repository root, with all `FNV_M3*`, `DV_M3`, and `DV3_SKIP` environment variables removed from this process. Output identity: `runtime-next/m3/out/batch8-baseline`. Started 2026-11-18; no prior matching output or visible build/harness lock.

Baseline result: exit 0, status `ok-harness-skipped`; executable SHA-256 `c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f`. Exact PE base-relocation directory bytes match `out/batch7-restore/FalloutNV_selfbuilt.exe`: RVA `0xf40000`, length 734884, SHA-256 `364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057`. Baseline was built with `--no-harness`. Batch 7 strict saved-evidence checks pass after checker changes; synthetic Batch 8 label checks accept both labels and reject an identifier mismatch.

Positive operation: `build-all.cmd --out C:\path\to\Decompilation\runtime-next\m3\out\batch8 --require-harness --play 60` with FNV_M3=1, FNV_M3_SEL=batch8_selection.json, FNV_M3_DV1=1, FNV_M3_DV1_EXT=1, FNV_M3_NEGCTL cleared, DV_M3 and DV3_SKIP cleared. Selection SHA-256 f0539b28be3c58729bb994534e19bc1d1410f80b88e027bdea9363878129990b. Output did not exist; no visible build or harness lock.

Pilot `out/batch8` passed extended harness (69.6 seconds, menu/load/cell/quicksave-load/clean exit). Generator retained all 8260 selected entries, zero dropped. It used the pre-fail-closed generator; final selection is larger and separately tested. M3 snapshot objects/manifest, DV1 pieces, selection and generator report archived under pilot evidence before subsequent builds.

Final positive operation: `build-all.cmd --out C:\path\to\Decompilation\runtime-next\m3\out\batch8-final --require-harness --play 60`, clean FNV_M3* and DV_M3/DV3_SKIP then FNV_M3=1, FNV_M3_SEL=batch8_final_selection.json, FNV_M3_DV1=1, FNV_M3_DV1_EXT=1. Selection SHA-256 42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7; no prior output or visible locks.

Final positive PASS: 8263 selected=kept, no drops; M3 section bytes .data 191622 and .rdata 871351. SHA-256 c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f; exact relocation bytes equal baseline (734884 bytes, SHA-256 364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057). Extended gameplay passed with 69.7s play, cell, quicksave/load, exit 0. Frozen snapshot, selection, and logs archived out/batch8-final/evidence.

Value control operation: build-all.cmd --out C:\path\to\Decompilation\runtime-next\m3\out\batch8-final-negctl-b8v --no-harness with final selection SHA 42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7 and FNV_M3=1, FNV_M3_DV1=1, FNV_M3_DV1_EXT=1, FNV_M3_NEGCTL=b8v, after clearing inherited M3/DV variables.

Value control passed: expected round-trip failure and value diagnostic; SHA-256 75a6950b1151c3c7741759e5224502e8153a7e4c3f7837418350a1165ea43e25 differs; 8263 selected=kept, no drops. Evidence archived out/batch8-final-negctl-b8v/evidence.

Pointer control operation: build-all.cmd --out C:\path\to\Decompilation\runtime-next\m3\out\batch8-final-negctl-b8p --no-harness with final selection SHA 42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7 and FNV_M3=1, FNV_M3_DV1=1, FNV_M3_DV1_EXT=1, FNV_M3_NEGCTL=b8p, after clearing inherited M3/DV variables.

Pointer control passed: expected round-trip failure and pointer diagnostic; SHA-256 3c02a6eef0f28722d01ebfd9640807ea0cd5aeeae0c84d430eb1c3f4b06116eb differs; 8263 selected=kept, no drops. Both controls' exact relocation bytes equal baseline (734884 bytes, SHA-256 364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057). Evidence archived out/batch8-final-negctl-b8p/evidence.

Repeat operation: build-all.cmd --out C:\path\to\Decompilation\runtime-next\m3\out\batch8-final-repeat --require-harness --play 60 with final selection SHA 42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7, FNV_M3=1, FNV_M3_DV1=1, FNV_M3_DV1_EXT=1, control unset after clearing inherited M3/DV variables.

Repeat PASS: SHA-256 c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f; 8263 selected=kept, no drops; exact relocation directory equals baseline (734884 bytes, SHA-256 364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057). Extended gameplay passed with 69.7s play, cell, quicksave/load and clean exit 0. Evidence archived out/batch8-final-repeat/evidence. Strict saved checker passed against legacy baseline, final repeat, both controls, selection SHA and identifiers. Separate exact relocation byte comparisons passed for baseline, final positive, both controls and repeat.

Promoted default operation: build-all.cmd --out C:\path\to\Decompilation\runtime-next\m3\out\batch8-promoted-default --require-harness --play 60, after clearing all FNV_M3*, DV_M3 and DV3_SKIP variables; no explicit M3 settings. Expected automatic final selection SHA 42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7.

Promoted default first attempt FAILED harness rc=1 after 520s: 70.1s play but no new save and world-after-cell/time/load false, despite clean process exit 0. Unique tag build-all-937740-1795049441781226400; verdict archived evidence/failed-harness-verdict.json. Image SHA canonical c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f; no gameplay pass claimed. Snapshot evidence archived.

Direct repaired-harness operation: python runtime-next/direct-v1/harness.py C:\path\to\Decompilation\runtime-next\m3\out\batch8-promoted-default\FalloutNV_selfbuilt.exe --extended --play 60 --tag batch8-guard-check-20261118; canonical image SHA c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f; output log out/batch8-harness-guard-check/harness.log. Prior failed verdict retained.

Direct repaired harness FAILED rc1 at console_after_coc: world HUD not detected, after 71.5s play and successful new quicksave; exception caused forced kill. Screenshot and verdict archived out/batch8-harness-guard-check. No fresh full build started.

Second repaired direct harness: python runtime-next/direct-v1/harness.py C:\path\to\Decompilation\runtime-next\m3\out\batch8-promoted-default\FalloutNV_selfbuilt.exe --extended --play 60 --tag batch8-guard-check2-20261118. Canonical image unchanged; first two failures retained.

Second repaired direct harness FAILED rc1: 71.8s play, new quicksave and world-after-cell/time/load all true; exit fallbacks exhausted, forced kill and no clean exit. Verdict/log archived out/batch8-harness-guard-check2. No fresh full build started.

Third repaired direct harness: python runtime-next/direct-v1/harness.py C:\path\to\Decompilation\runtime-next\m3\out\batch8-promoted-default\FalloutNV_selfbuilt.exe --extended --play 60 --tag batch8-guard-check3-20261118. Canonical image unchanged; prior failures retained.

Third direct semantic harness PASS rc0: 71.8s, configured scans 63/64, saved cell 1291213 -> coc 1073541 -> quickload 1291213, new quicksave, console_quitgame exit 0 clean; strict cell-state checker passed. Verdict/log archived out/batch8-harness-guard-check3. Earlier failures remain documented.

Fresh verified promoted default: build-all.cmd --out C:\path\to\Decompilation\runtime-next\m3\out\batch8-promoted-default-verified --require-harness --play 60; all inherited FNV_M3*, DV_M3, DV3_SKIP cleared, no explicit M3 overrides.

Fresh promoted-default VERIFIED PASS: status ok, rc0; SHA-256 c267a197492f7d53b3592ff47ea6de3d7daf45afd7893701c0d32822f1d49a0f; exact relocation bytes match baseline (734884 bytes, SHA-256 364b83a38aae50e6faf0a4f0512fdfa8b338bd1dab47b39fec0bd7b03fd26057). Automatic selection batch8_final_selection.json SHA-256 42d84f21776429e139502ebe391302d7c8b36f1833a6403d96009a99bbabcfe7, DV1/EXT enabled, 8263 selected=kept, zero drops, M3 1062973 bytes. Unique accepted harness tag build-all-936352-1795052857227733200: 71.8s play, quick scans 63/64, saved cell 1291213 -> coc 1073541 -> quickload 1291213, new quicksave, console_quitgame exit 0 clean; one confirmed console-close recovery at console_after_set restored the HUD; no pause recovery. Strict checker with --require-cell-state passed using legacy baseline and both controls. Snapshot objects/manifest, selection, generator logs and tooling SHA-256 archived out/batch8-promoted-default-verified/evidence. Earlier failed runs are retained as failures.
