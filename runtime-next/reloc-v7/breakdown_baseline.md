
### Baseline: by cause

| group | fields | bytes |
|---|---:|---:|
| EH funclet: callee name defined nowhere in our sources | 2674 | 10696 |
| CRT/STL library code | 1576 | 6304 |
| EH funclet: call to identical-body copy, ICF picked another copy | 230 | 920 |
| accepted web contribution (EH piece) | 91 | 364 |
| EH funclet: name bound by symbol map to another copy | 90 | 360 |
| recipe function: call resolves to a different function (source bug) | 48 | 192 |
| accepted web contribution (function body) | 21 | 84 |
| recipe function: float/string pool copy or literal | 20 | 80 |
| total | 4750 | 19000 |

### Baseline: by origin / status

| group | fields | bytes |
|---|---:|---:|
| ('tail', 'borrow', 'None') | 2671 | 10684 |
| ('crt', 'borrow', 'unresolved') | 1529 | 6116 |
| ('tail', 'disagree', 'icf-fold') | 228 | 912 |
| ('contrib-eh', 'borrow', 'None') | 91 | 364 |
| ('tail', 'disagree', 'c') | 90 | 360 |
| ('fn', 'disagree', 'a') | 48 | 192 |
| ('crt', 'disagree', 'member-section') | 30 | 120 |
| ('contrib', 'borrow', 'None') | 21 | 84 |
| ('fn', 'disagree', 'c') | 20 | 80 |
| ('crt', 'disagree', 'symbol-map') | 13 | 52 |
| ('crt', 'disagree', 'lib-matched') | 4 | 16 |
| ('tail', 'borrow', 'icf-fold') | 2 | 8 |
| ('tail', 'disagree', 'sized-delete-rule') | 1 | 4 |
| ('tail', 'borrow', 'sized-delete-rule') | 1 | 4 |
| ('tail', 'disagree', 'a') | 1 | 4 |

### Baseline: by owner (source file of the placing unit; CRT and contributions have no source file)

| group | fields | bytes |
|---|---:|---:|
| (crt) | 1576 | 6304 |
| src/staging/blk_00aa0000_od_ob1_variant.cpp | 148 | 592 |
| src/staging/blk_00ac0000_od_ob1_variant.cpp | 118 | 472 |
| (contrib-eh) | 91 | 364 |
| src/speedtree/frondengine_ob1_variant.cpp | 86 | 344 |
| src/staging/blk_00c40000_od_ob1_variant.cpp | 85 | 340 |
| src/speedtree/speedtreert_ob1_variant.cpp | 84 | 336 |
| src/fallout/interface/menus/specialbookmenu.cpp | 77 | 308 |
| src/generated/setting_eh_initializers.cpp | 71 | 284 |
| src/staging/blk_00440000_od.cpp | 63 | 252 |
| src/fallout_shared/tesobject_ob1_variant.cpp | 58 | 232 |
| src/staging/blk_00ba0000_o2.cpp | 58 | 232 |
| src/staging/blk_00b20000_od_ob1_variant.cpp | 56 | 224 |
| src/staging/blk_00b60000_o2.cpp | 49 | 196 |
| src/bsaudio/bsaudiomanager_ob1_variant.cpp | 47 | 188 |
| src/bsmenu/font.cpp | 43 | 172 |
| src/fallout/ai/actor_o2_nood_variant.cpp | 43 | 172 |
| src/speedtree/indexedgeometry_ob1_variant.cpp | 38 | 152 |
| src/fallout_shared/inventorychanges.cpp | 37 | 148 |
| src/staging/blk_009e0000_o2.cpp | 36 | 144 |
| src/bsmenu/tile_ob1_variant.cpp | 36 | 144 |
| src/staging/blk_00ca0000_o2.cpp | 36 | 144 |
| src/bsshader/shadowscenenode.cpp | 35 | 140 |
| src/staging/blk_00c60000_o2.cpp | 34 | 136 |
| src/staging/blk_006e0000_od.cpp | 31 | 124 |
| src/staging/blk_00cc0000_o2.cpp | 31 | 124 |
| src/staging/blk_00c80000_o2.cpp | 26 | 104 |
| src/staging/blk_00c60000_od_ob1_variant.cpp | 25 | 100 |
| src/staging/blk_00c20000_od_ob1_variant.cpp | 24 | 96 |
| src/fallout_shared/modelloader.cpp | 23 | 92 |
| (contrib) | 21 | 84 |
| src/speedtree/libspline_source/idvspline_ob1_variant.cpp | 21 | 84 |
| src/bsshader/shadowscenelight.cpp | 21 | 84 |
| src/staging/blk_00b20000_od.cpp | 20 | 80 |
| src/staging/blk_00cc0000_od_o2_nood_variant.cpp | 20 | 80 |
| src/staging/blk_00b40000_od_ob1_variant.cpp | 19 | 76 |
| src/staging/blk_00bc0000_o2.cpp | 19 | 76 |
| src/bsshader/bsshaderaccumulator.cpp | 18 | 72 |
| src/fallout_shared/tesobjectrefr.cpp | 17 | 68 |
| src/staging/blk_006a0000_od.cpp | 16 | 64 |

### Baseline: EH-funclet callee names (top 25)

| group | fields | bytes |
|---|---:|---:|
| ??3BkItemBase@@SAXPAX@Z | 75 | 300 |
| ??1SettingBase_01012120@@UAE@XZ | 71 | 284 |
| ??1Setting@@QAE@XZ | 68 | 272 |
| ??3@YAXPAX0@Z | 63 | 252 |
| ??1GlobalObject_0096a2d0@@QAE@XZ | 60 | 240 |
| ??1MemContextGuard@@QAE@XZ | 21 | 84 |
| ??1FUN_0044a4c0@@QAE@XZ | 18 | 72 |
| ??1?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@QAE@XZ | 16 | 64 |
| ??1VB9@@QAE@XZ | 13 | 52 |
| ??1?$NiPointer@VNiRefObject@@@@QAE@XZ | 13 | 52 |
| ??1?$WriterVectorVal@DU?$Allocator@D@TriWriterRework@@@TriWriterRework | 12 | 48 |
| ??1FUN_00b31270@@QAE@XZ | 12 | 48 |
| ??1RefPtr@@QAE@XZ | 11 | 44 |
| ??1LayoutString@fnv_00a17390@@QAE@XZ | 10 | 40 |
| ??1?$FGVal@M@@QAE@XZ | 10 | 40 |
| ??1FGContainer@@QAE@XZ | 10 | 40 |
| ??1VA9@@QAE@XZ | 10 | 40 |
| ??1?$WXPointer@UWXObject@@@@QAE@XZ | 9 | 36 |
| ??1String@@QAE@XZ | 9 | 36 |
| ??1MemberD@fnv_00b2e810@@QAE@XZ | 9 | 36 |
| ??3ImageSpaceShaderParam@@SAXPAX@Z | 9 | 36 |
| ??1TlsGuard_t@@QAE@XZ | 9 | 36 |
| ??3FUN_00a12020@FontManagerInitialization@@SAXPAX@Z | 8 | 32 |
| ??1FgStore@fnv_00aac820@@QAE@XZ | 8 | 32 |
| ??1?$VectorVal@D@fnv_00ab5ec0@@QAE@XZ | 8 | 32 |

### Baseline: CRT symbols (top 25)

| group | fields | bytes |
|---|---:|---:|
| __errno | 280 | 1120 |
| ___pioinfo | 72 | 288 |
| ___doserrno | 46 | 184 |
| __unlock | 33 | 132 |
| _tzinfo | 27 | 108 |
| ___use_sse2_mathfcns | 22 | 88 |
| ___fastflag | 21 | 84 |
| __inc | 19 | 76 |
| ___piob | 18 | 72 |
| _GS_ContextRecord | 18 | 72 |
| __nhandle | 17 | 68 |
| ___locale_changed | 16 | 64 |
| _memcpy | 15 | 60 |
| __environ | 15 | 60 |
| _NAME_ | 14 | 56 |
| __crtheap | 14 | 56 |
| _rgValidPages | 13 | 52 |
| _dstend | 13 | 52 |
| ??_7bad_exception@std@@6B@ | 12 | 48 |
| ___sbh_pHeaderDefer | 12 | 48 |
| _DoubleFormat | 12 | 48 |
| ___iob_func | 10 | 40 |
| __un_inc | 10 | 40 |
| ___globallocalestatus | 9 | 36 |
| ___getvalueindex | 9 | 36 |
