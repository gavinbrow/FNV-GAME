struct FUN_00802a20_class
{
    int __thiscall FUN_00802a20(const char* apPage);
};

struct FUN_008029c0_class
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;

    bool __thiscall FUN_008029c0(const char* apPage, int value);
};

bool FUN_008029c0_class::FUN_008029c0(const char* apPage, int value)
{
    int result = reinterpret_cast<FUN_00802a20_class*>(this)->FUN_00802a20(apPage);

    if (result != -1)
    {
        unk18 = result;
        unk1c = value;
    }

    return result != -1;
}