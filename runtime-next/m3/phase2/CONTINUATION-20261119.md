# Phase 2 continuation checkpoint — 2026-11-19

Workspace C:/path/to/Decompilation; explicit workdir always. Goal remains active:
finish Phase 2 with four existing Terra workers. Luna unavailable. No commits,
push/export/downloads, reference/game files read-only. Protected fnv_decomp
source/include/units edits generator-only, approval already given. Serialize
all builds/private compilers/gameplay through verification worker.

## Accepted now

Recipe 825d444f16df19589bf9f10764b064f4dee5cae44dc2f50b47ad1bc5c6ce2d68.
Guard combined_source_apply.py, manifest9422dd1642f66ddca78a1b161b040cdb55847afd3ad447fbf66e86a6ed47e9da.
Native seven-unit source batch ACCEPTED by audit_native_source_acceptance.py:
actual positive/repeat 1100 functions,389 located EH,8 requested tails; source
freeze12710/5497 source paths/10pins; canonical image c267a197...a0f and
reloc734884 SHA364b83a3...6057. Two fresh controls a8cc.../f60a... actual
COFF+PE proofs pass. Gameplay70.1/70.0s, restored cells/new saves/clean exits.
Dirs phase2-native-source-{positive,p2av,p2wp,repeat}; actual11 objects archived.
Acceptance out/phase2-native-source-acceptance.json. No weak resolver enabled.

Coverage1613018/1979392 (81.5%), TLS5 separate. New8BGSBodyPart table at1045400.
Accepted partition SHAfacf9bc45e5e97148b27256fff20db75f642c303fd4380b55abf0f90017d5efa,
backup accepted_range_partition.before-native-source.json. Remaining366374 =
190878 produced/unspliced+67551 uncovered nonzero+100045 zero+7900 rewrite.
Selection a0a8...9c3a/library74e3...9700 unchanged. Most W types/classes open.

## Next source proposal, NOT installed

out/phase2-nimem-next-source-composed/manifest.json SHA
c1289a7009ada0218ae60bf4d9851ed39512f508e72b8bcf063185c53b40ef53;
38 source payloads, recipe13350f07...7876. Includes27 kind headers merged with
NiMem API/new+delete owner defs,7 API compatibility fixes and TESFile995global.
Calendar-only revision out/phase2-nimem-calendar-binding-v1 manifest1b15812e...
recipe92b5d4058d196208672a6479f1d5e33414c2e022172fa3f3674d1d8e12ede9b8;
adds source-owner574 GetDayOfMonth binding to368,123/123. No new compiler needed.

Dynamic scope752 =135 fresh contexts (old133+620+995) +617 unchanged kind-only
reuses. IMPORTANT:129 already in old128 API archive and133run;620 was missing
from old750/133 because new825d headers introduced layout_support. Fresh620
joint check closes this gap. Source snapshots/context must remain exact.

Old133 run out/phase2-nimem-combined-825d-run:96pass30review7candidate compile
fails. Resolved separately by global ::new for1203/1271/1598, ordinary native
new for200 (fixes real0x38c AA1460 unwind), adapter using for128/129/191/773.
Preserve all failed fixtures. Ten composed joint run out/phase2-nimem-next-source-joint-ten
(all candidate functions strict); legitimate raw differences200 nativeowner,
773 samepool SG,995 true global replacement+SG. 995 all4tails need2634outside
owner proof. 62016 PSA-related sections exactly equal accepted producer.

Proof index out/phase2-nimem-next-source-proof-index-v4.json SHAf02c075f...
125 source-identical candidates3428/3432 before Calendar; Calendar fixes3,
remaining1592 PTR_010bffe4 unbound (source extern only), exact before/after
function bytes+reloc identity. Earlier25EH failed sections/18 errors exactly
unchanged,136 associated fields none changed; Calendar lowers25 to23. All
remaining baseline errors explicit, no forced aliases. 44 historical immediate
proofs remain field-scoped, never unitwide. Production labels need reproof.
Source field 995 replaces3 false TOFTQ literals with unsigned DAT_011873c8,
independent owner587; no startup initialization semantics claim.

## NiRef primary experiment, NOT installed

Public header originally already OUT-OF-LINE declaration (old summary wrong).
Native primary612 dtor is33B at496910, wrapper46B4968e0. Optimized separate
physical18B owner A5D3D0 in2725 MUST stay separate; do not bytealias collapse.
Private out-of-line fixture81cc... above38parent:612154/154,natural33/G46;
1503real277B AA05A0 becomes269B externaltailcall (10/11), not acceptable.
Private inline fixture84940a...: canonicalinlineheader, removes local1503body;
source-backed atomic helper4019a0 from accepted633 actual15B fixesunitlocal
NiAtomicSubtract symbol. Both612154+1503 11 pass, no EH failures.
Counter11f4400 declaration+address known, storage/initialization owner unknown.

Broader119cohort out/phase2-niref-inline-cohort completed session55471:
all119 pairs/reports,2080 functions,76 listed tails unionallpass/no conflicts.
BUT candidate2061/2080 vsparent2079/2080. Seven SG shifts54fields;612 expected
owner transitions. FIVE REAL inline code regressions111/1200/1433/1598/1630.
These five originally call separate optimized18 atA5D3D0, NOT primary33!
1503 NiShaderFactory destructor uses inline cleanup; original RTTI confirms
NiShaderFactory->NiRefObject->NiMemObject. Universalinline OR universalexternal
model does not preserveall6contexts. No arbitrary noinline/forceinline patches.
Source visibility/identity/provider model unresolved; keep independent of38.
Out-of-line612 dtor33 COMDAT NODUPLICATES1/G46ANY2; inline612 dtor33/G46 and
1503dtor18/G44ANY2, Eweakmode2->G. Never assume provider fromsameName.
Notes NIREF-PRIMARY-OWNER-REVIEW.md,NIREF-VISIBILITY-AND-OWNER-REVIEW.md.

## W103 native metadata proposal, NOT installed

out/phase2-psa-metadata-ownership-proposal; final selection v3 starts06250fe5...
Five accepted620 native sections COL20/CHD16/basearray13/BCD28/TD26 =103 bytes.
Basearray13 includes3ptrcells+compilertrailingbyte; next3padding NOT native.
Replace two W1602B with native103 + residual1499 (gap3,prefix2,tail1494).
All61relocsites=9native+52residual; retain all incoming M3D tags. PSA vtable E/T
excluded; E unresolved mode2, no native weak switch.

First fixture v2 failed prefix2 mutablezero landed .bss. Existing schema
file_backed:true fixes to writable.data; NO productiongenerator modification.
Distinct v3 hardened lock/env/input/output guards; compiled session24167 PASS:
M3 8269/8269,no drops; prefix writable file-backed; COLtag UNDEF resolves orig
110fbe8 by existing regex (address marker,notstorage). Full selector actual
compiledskip adds exactly5single620pieces, removes none, library405/16730same.
compiled-proof-v3.json proves exactunion/61sites. No freshphase0/image/runtime.
Scripts psa_m3_compiled_fixture_v3.py,psa_compiled_selector_replay_v3.py,
psa_compiled_ownership_verify_v3.py; all outputs private, oldfailuresretained.
ToolchainDLL/SDK closure limit documented. 620 metadata matches composed38.

## Workers / next

Reuse existing /root/{other_names,conflicting_types,zero_accounting,verification}.
All last operations terminal; inspect status before assignments; followup_task
starts completed agents, send_message alone does not. No running compiler.
Verification owns compiler lane. Next: independent review38+Calendar source
transaction readiness with explicit unchanged baseline gaps, generated/wrapper
ownership and full image gates. Can compose W103 data opt-in after complete
artifact review, preserving rawunion and keeping unsupported E excluded.
NiRef119 experiment is a separate unresolved native-class model; no install.
Never mark wholePhase2 complete based on these bounded batches. No goal pause
or blocked status requested. Avoid giant JSON dumps and forbidden scans under
FNV/work,FNV/local,fnv_decomp/build/rebuild; reference exactpath reads permitted.


## W103 full gate started; live opt-in tools (2026-11-19)

The five-file W103 control tool transaction is now applied, default selection
unchanged. Proposal manifest e1151c84a099a09b2acc021f93fd8d458bcb77baef66d412f5840b1885b3e107;
transaction cd1971f4edf3d6c98d0da55fc8018ce910db22cf81ecee4dd0b097c9e8a02f71,
applier phase2/psa_w103_control_transaction.py SHA
e06059618314f9560e3f3d26e0f60ebfe80ccebc0e80d056a4dd6865e36ed2cd.
Private originals/payloads remain out/phase2-psa-w103-control-patch.
Root and zero_accounting independent review; 4 targeted controls, 3 guarded
transaction tests pass, owner/reviewer also ran 11 legacy checker cases.
Early driver refuses p2rv/p2rp without M3/DV1/fresh data-v1. Exact native TD/COL
producer/name/extent/bytes/sites and alternate TESModel descriptor are checked.
Saved checker demands exact recorded ID and exact VA/old/new for new controls.

Verifier started positive operation session3413, sole compiler/build/gameplay
lane. Outputs out/phase2-psa-w103-positive and sibling -freeze, preflight nine
required pins +5497 source/include; catalog out/phase2-psa-w103-inputs.json.
Opt-in package selection06250fe537e1f34eae3488444927e909acc64a04ec3ac46cf1af5b2cf9b931a4,
recipe still825d. No default promotion. After positive archive actual620/M3/DV1/
phase0/placed/layout before any next compiler; root review before p2rv/p2rp.
phase2/w103_capture_run.py does immediate capture; root independent audits are
w103_positive_artifact_audit.py and w103_control_artifact_audit.py.
All assertions-enabled only; audit failures remain failures.

Source1592 local PTR diagnostic now has sibling matched factory c2d180 source
relocation evidence matching c2d240 field; original RTTI NiPSysColorModifier.
Proof out/phase2-nimem-1592-psys-color-pointer-proof.json SHA
5b7c3ca71cd48d1050d23c46091cb151f8f78072b3ddd956dc8f6632ceb730bb.
Private overlay out/phase2-nimem-psys-pointer-binding-v1 manifest
df79066878d3112c4cdf00de7e5163088ca6ecb25789e9ee831bfa2b77ba295b;
recipe5a51705361ab8a9f2947f815a86c935a195fe82cecd3de7b43a2e7db362a74ad.
10/10 strict+ordinaryEH pass; no native hierarchy/slots/data ownership claim.
23 unchanged EH sections /18 errors remain after Calendar. Unit211 is real
funclet stack displacement mismatch EBP-104c versus original1048, not alias.

Next focused compiler fixtures queued after W103 suite: local149/194 NiMem
unsized-to-sized declaration hypothesis, class extents192/100 agree original
EH pushed sizes c0/64 and source allocator1664 AA1460. Private manifest
out/phase2-nimem-149-194-sized-eh-v1/manifest.json SHA
dca9aece504241d985be62def30a1e2eb67ad08cf2bab3dc9eac8ee167fa0948;
mirrors -u0149/-u0194; comparator nimem_149_194_sized_eh_compare.py SHA
a772bbdbafba45662a4156676470b1fc2b0b784ff92fc6533125c66d8b73bfca.
No fixture compiled yet; no live source change.


## W103 diagnostic rejected and corrected v2 launch (newest)

Original out/phase2-psa-w103-positive finished canonical image/gameplay/freeze
in529s, but verifier capture caught omitted FNV_M3_LIB=1. Explicit custom
selection disables automatic library defaults, so this IS NOT accepted gate
evidence. Preserve all old output and partial capture; never overwrite/move.
New suite stem out/phase2-psa-w103-v2-{positive,p2rv,p2rp,repeat}. Corrected
preflight explicitly sets LIB=1, LIB_SELECTION absolute canonical path and
LIB_SHA256=74e381... with selection06250... and weak0; configure/driver
validation confirms effectiveM3/DV1/EXT=1. Root reviewed and GRANTED v2positive
only after provider archive; verifier should report new operation. No next
compiler until actual620/M3/DV1/scratch/layout capture+positive root review.
Rootaudits now use v2stem, require LIB1, and w103_frozen_proof.py pins exact
9distinct productionpaths/digests, package manifest65b12a3744550167f48c4af749fbe92a13624c265dadf7d0c408741d54207374,
controlpatch e115..., all5497sourcefiles equal fixed accepted snapshot48ef88bb8a247d5d09cd633964052c2ce2dd79cc98c6bc787e66d673cb008c96.

New source-provider index from rejected diagnostic (source-only evidence,
NOT gate acceptance): out/phase2-psa-w103-provider-index.json covers all2995
successful exactrecipe compiled objects, start/end hashes equal. Provider
archive out/phase2-psa-w103-provider-archive retains620/621/2656, index,
compilelogs, recipe, freeze. No strong E found forPSA/BGSBodyPartData in this
bounded namespace. CRTcode/index, V7/ICF/overlays/M3/DV1 remain separate.

Further queued/private source fixtures: unit773 allocator mixin graph
(original7bases including stateless NiMemObjectAllocation at+32 vsreference6;
classvsstructNiMemObject), source generator unit773_allocator_hypothesis_stage.py
and fixture prepare/compare scripts. Complete fixture nowprepared,39functions
plusordinaryEH, sourceowner2734new/1664delete andcomplete6basegraphs required;
compile command nimem_combined_825d_compile.py --unit773 --out
out/phase2-unit773-allocator-fixture. Mirrors/compare pinned; diagnosticonly.
No90B nativeCHD/basearray ownership claim from original773 graph.

BGSBodyPartData621 emitted implicitdtor86B is genuinely incomplete vsnative
sourceowner2656 dtor127B: missing ClearData andnaturalvptrtransitions. Private
reproducible mirror out/phase2-bgsbodypartdata-native-dtor-v1 adds explicit
virtualdtor calling sourceClearData; requires10native621+174donor2656 funcs/EH,
ownertransfer/ODR/RTTI/weakproof. No forcedvptrstores orrecipechanges.

Unit211 originalfuncletownership verified viahandlerf2918b/FuncInfo1175a04/
unwindmap11759fc ->f29180. Real sourcegap: originalonewordAutoMemContext
cleanup atEBP-1048 calling source47 dtor404ee0 versuscurrent2wordinline
WaterShaderMemScope atEBP-104c. Parent5647B matches, prolog1050same; local
type/lifetimehypothesis beingprepared byother_names, cannotaliascleanup.
