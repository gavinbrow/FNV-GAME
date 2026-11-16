// Define the known helper from the preserved surrounding source.
unsigned int GetWFlags(hkWorldObjStub* world) {
    hkWorldObjSub* sub = world ? &world->sub : 0;
    return sub ? sub->flags : 0;
}
struct LiquidBase {
 virtual ~LiquidBase();
 unsigned int refCount, unk08, unk0c, unk10;
};
struct LiquidLink { ~LiquidLink(); };
struct FUN_00c8e9c0 : LiquidBase {
 LiquidLink link;
 void FUN_00c8da40();
 virtual ~FUN_00c8e9c0();
};
FUN_00c8e9c0::~FUN_00c8e9c0() {
 FUN_00c8da40();
 --g_iLiquidActionCount;
}