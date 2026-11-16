struct FUN_00803d30 {
    virtual ~FUN_00803d30();
    int unk04; int unk08; int unk0C; int unk10; int unk14;
    int unk18; int unk1C; int unk20; int unk24; int unk28;
    int unk2C; int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44;
    FUN_00803d30(int first, int second, int third);
};
struct FUN_00633c90 {
    FUN_00633c90(int mode);
    ~FUN_00633c90();
    void FUN_0066b0d0(int mode);
};
struct FUN_0080e610 : FUN_00803d30 {
    FUN_00633c90 effect;
    FUN_0080e610(int first, int second, int third);
    virtual ~FUN_0080e610();
};
FUN_0080e610::FUN_0080e610(int first, int second, int third)
    : FUN_00803d30(first, second, third), effect(0)
{
    effect.FUN_0066b0d0(0);
}