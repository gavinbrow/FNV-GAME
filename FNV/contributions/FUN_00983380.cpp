struct FUN_009836d0_class
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    FUN_009836d0_class* __thiscall FUN_009836d0();
    FUN_009836d0_class() { FUN_009836d0(); }
    ~FUN_009836d0_class() {}
};

struct GlobalObject_00633c90
{
    int unk00;
    GlobalObject_00633c90(int);
    ~GlobalObject_00633c90() {}
};

struct FUN_00983380 : FUN_009836d0_class
{
    int unk10;
    unsigned char unk14;
    unsigned char unk15;
    unsigned char unk16;
    unsigned char unk17;
    GlobalObject_00633c90 unk18;
    FUN_00983380();
};

FUN_00983380::FUN_00983380()
    : unk10(0), unk14(0), unk15(0), unk16(0), unk18(0)
{
}

