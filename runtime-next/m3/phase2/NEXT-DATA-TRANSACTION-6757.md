# Private next data transaction

`out/phase2-next-data-transaction6757` contains one private review payload with exact current and proposed bytes for the cumulative generator, hardened Cost245 helper, splice alignment, pseudo-unit alignment, image placement check, and split-library hook. The generator `next_data_batch_transaction.py` refuses to create it unless all six live code preimages equal their recorded staged baselines, accepted 6757 archive inputs and source hashes match, saved fixture evidence is consistent, and the selection/range accounting succeeds. It does not install files or change the accepted defaults.

Against the archived flags-script positive, 8,265 accepted and 8,268 proposed M3 entries have the same disjoint range union. The proposed library set has 405 pieces / 16,730 bytes: 370 / 6,374 are identical to accepted DV1 pieces, while 35 / 10,356 are disjoint incremental pieces, with 4,014 zero and 6,342 nonzero reference bytes. The staged library hook's read-only dry run also accepted the 405 entries against the saved placement SHA `43345111a3ff1fc11d4d1ffc837fa8163fbf4e5027fad208a1ecab9854c43756`, with libcmt and libcpmt archive hashes matching the selection. That dry run uses earlier claims internally; the accepted-archive union check is separate.

The recorded NiPoint3, SIMD and hardened Cost245 isolated fixture results are pinned in the transaction manifest. They do not constitute a cumulative production build. Cost245 relocation-bearing source integers remain integer transports, not established native pointer types; the atan selection retains unresolved overlapping unselected annotations. Review the six changes together, then run fresh placement, targeted controls, full positive, repeat and gameplay before any promotion. No class-source changes are included.

The separate `next_data_batch_apply.py` supplies the actual install/build-lock,
rollback and recovery logic; the packaging script above does not install.
Independent review and six isolated tests passed before the coordinator applied
the six exact code payloads. Both accepted defaults and recipe 6757 remain
unchanged. The opt-in full positive is `out/phase2-next-data-positive-v2`;
its earlier preflight rejected a mistyped expected library hash before any
compilation. No candidate coverage or promotion is accepted yet.
