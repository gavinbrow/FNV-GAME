struct FUN_006c7850 {
    virtual void v0();
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    FUN_006c7850();
    ~FUN_006c7850();
};
struct FUN_0042fb00 {
    int unk00;
    FUN_0042fb00();
    ~FUN_0042fb00();
};
struct FUN_006c87c0 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_006c87c0();
    ~FUN_006c87c0();
};
struct FUN_00699450 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    FUN_00699450();
    ~FUN_00699450();
};
struct FUN_006c77a0 : FUN_006c7850 {
    unsigned int unk18;
    FUN_0042fb00 m1c;
    FUN_0042fb00 m20;
    FUN_006c87c0 m24;
    FUN_00699450 m34;
    unsigned char unk54;
    FUN_006c77a0(unsigned int value);
};
FUN_006c77a0::FUN_006c77a0(unsigned int value)
{
    unk18 = value;
    unk54 = 0;
}
