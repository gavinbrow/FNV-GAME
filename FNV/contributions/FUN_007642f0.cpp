struct FUN_007240c0 {
    virtual void vfn00();
    FUN_007240c0();
};
struct FUN_0096a2d0 {
    unsigned int unk00;
    unsigned int unk04;
    FUN_0096a2d0();
    ~FUN_0096a2d0();
};
struct FUN_007642f0 : FUN_007240c0, FUN_0096a2d0 {
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned short unk1c;
    unsigned short unk1e;
    float unk20;
    float unk24;
    float unk28;
    unsigned short unk2c;
    FUN_007642f0();
    void FUN_007a1950(int a, int b);
};
void __cdecl FUN_00721130(FUN_007642f0* object);
FUN_007642f0::FUN_007642f0()
{
    unk14 = 0;
    unk10 = 0;
    unk0c = 0;
    unk18 = 0;
    unk2c = 0;
    unk1c = 0;
    unk28 = 0.0f;
    unk24 = 0.0f;
    unk20 = 0.0f;
    FUN_007a1950(0, 1);
    FUN_00721130(this);
}
