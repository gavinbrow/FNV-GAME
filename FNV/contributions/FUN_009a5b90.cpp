
struct FUN_00435de0 {
    float value;
    FUN_00435de0(float input);
};
struct FUN_00633c90 {
    int unk00;
    int unk04;
    int unk08;
    FUN_00633c90(int value);
    ~FUN_00633c90();
};
struct FUN_006815c0 {
    int unk00;
    int unk04;
    int unk08;
    FUN_006815c0();
};
struct FUN_009a5b90 {
    int unk00;
    float unk04;
    FUN_00435de0 unk08;
    FUN_00435de0 unk0c;
    float unk10;
    FUN_00633c90 unk14;
    FUN_006815c0 unk20;
    CombatTimeStamp unk2c;
    FUN_009a5b90();
};
FUN_009a5b90::FUN_009a5b90() : unk00(0), unk04(0.0f), unk08(0.0f),
    unk0c(0.0f), unk10(0.0f), unk14(0), unk20()
{
    FUN_004300a0(&unk2c);
}