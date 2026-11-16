extern const char DAT_0104f2ac;
struct FUN_00404eb0 {
    int state;
    FUN_00404eb0(int category, int enabled, const char* source, int line);
    ~FUN_00404eb0();
};
struct FUN_00508050 {
    float FUN_00508050_value();
};
struct FUN_00559450 {
    FUN_00508050* FUN_00559450_value();
};
struct FUN_006427c0_Class {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24;
    FUN_00559450 unk28;
    float FUN_006427c0();
};
float FUN_006427c0_Class::FUN_006427c0()
{
    FUN_00404eb0 scope(0x21, 1, &DAT_0104f2ac, 0x235);
    FUN_00508050* value = unk28.FUN_00559450_value();
    if (value)
        return value->FUN_00508050_value();
    return 0.0f;
}
