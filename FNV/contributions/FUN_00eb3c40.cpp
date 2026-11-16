struct FNVVectorParameter { int unk00; int unk04; int unk08; int unk0c; float extent10; };
extern "C" int FUN_00eb3c40_VTable;
extern "C" float FUN_00eb3c40_Default;
struct FNVRegion {
    void* vtable;
    int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34;
    void* owner38; FNVVectorParameter* bounds3c;
    float inverseSquare40; float axis44; float axis48; float axis4c;
    void FUN_00eae720(float x, float y, float z, void* userdata);
    FNVRegion* FUN_00eb3c40(void* owner, FNVVectorParameter* bounds,
                           float x, float y, float z, void* userdata);
};
FNVRegion* FNVRegion::FUN_00eb3c40(void* owner, FNVVectorParameter* bounds,
                                    float x, float y, float z, void* userdata) {
    FUN_00eae720(x, y, z, userdata);
    bounds3c = bounds;
    vtable = &FUN_00eb3c40_VTable;
    owner38 = owner;
    inverseSquare40 = 1.0f / (bounds->extent10 * bounds->extent10);
    FNVRegion* __restrict p = this;
    p->axis44 = FUN_00eb3c40_Default;
    p->axis48 = FUN_00eb3c40_Default;
    p->axis4c = FUN_00eb3c40_Default;
    return this;
}