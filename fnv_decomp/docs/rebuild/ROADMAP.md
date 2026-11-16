# Playable rebuild roadmap

The goal is a separately built runtime that can eventually launch and play with owned, compatible inputs. **No playable build or complete game link has been demonstrated.** Preserve the existing reference matcher, recipe variants and official checks independently throughout.

| Milestone | Current evidence | Exit gate |
|---|---|---|
| Reference and full recipe | 2,988 retained recipes compiled; separate full reference and retained checks reported parity. | Preserve compiler identities, recipe variants and original matching gates. |
| Code, data and EH ownership | The accepted V14 cohort observation preserves 14,555 namespace entries, 46,292 fields and the full 58,914-binding ledger; it does not establish provider or ABI readiness. Data lifetimes, local EH diagnostics and provider/ABI contracts remain open. | Reconcile every selected identity, data lifetime, relocation and EH dependency without guessed providers. |
| Startup and private link | Diagnostic links have run. The independently reviewed canonical V18 link reported 1,009 unresolved symbols and 1,338 records; it removed five DATA keys from V17 and produced no executable or window. | Independently review exact inputs and resolve all dependencies in a private link, without weakening the oracle. |
| Menu and gameplay | Not demonstrated. | Repeat isolated launches to a responsive menu, then exercise a documented gameplay route and broader scenarios. |
| Save/load and reproducibility | Not demonstrated. | Verify isolated save/load round trips and reproduce the workflow in an independently prepared environment. |

The immediate milestone is a source-built executable that compiles and starts, even if it is buggy or crashes. A responsive menu, gameplay, full ABI and stability remain later milestones; the reference matcher and official checks continue independently.

## Next concrete gates

1. Resolve remaining import and provider contracts with evidence, including the unaliased Steam import.
2. Continue resolving selected CODE, DATA and EH dependencies with evidence-backed ownership and bounded conformance; a prepared object alone does not prove a callable ABI or runtime provider.
3. Establish startup, CRT, TLS and initialization contracts, then achieve a private application link without weakening the oracle.
4. Verify an isolated launch and responsive menu before estimating gameplay or save/load milestones. No reliable date for a first buggy game is established.

The [work ledger](AGENT-WORK.md) tracks owners and current review status. Detailed previous evidence and test counts are preserved in [evidence history](EVIDENCE-HISTORY.md); current validation and private-output rules are in [VALIDATION.md](VALIDATION.md).
