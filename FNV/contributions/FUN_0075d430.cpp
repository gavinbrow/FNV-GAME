struct FUN_0075d430_base
{
    virtual void vfn_0000() = 0;
    virtual void vfn_0004() = 0;
    virtual void vfn_0008() = 0;
    virtual void FUN_0075d430_call(int param1, int param2) = 0;
};

struct FUN_0075d430_shell : FUN_0075d430_base
{
    char unk04[0x20];
    int unk24;
    char unk28[0x58];
    int unk80;

    bool __thiscall FUN_0075d430(int param1, int param2);
};

extern void __cdecl FUN_0075b750();

bool __thiscall FUN_0075d430_shell::FUN_0075d430(int param1, int param2)
{
    bool result = false;

    if (param1 == 0x0b &&
        unk80 != 4 &&
        unk80 != 3 &&
        unk24 == 1)
    {
        FUN_0075d430_call(0x0a, 0);
        result = true;
    }
    else if (param1 == 0x0a)
    {
        FUN_0075b750();
        result = true;
    }

    return result;
}