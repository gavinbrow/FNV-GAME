struct FUN_005f8d70_runtime : FUN_00843150_shell {
    void* FUN_00600700(void*);
};
extern FUN_005f8d70_runtime* DAT_011cb6a0;
struct FUN_005f8d70_virtual {
    virtual void v0(); virtual void v1(); virtual void v2();
    virtual void v3(); virtual void v4(); virtual void* v5(unsigned int);
};
struct FUN_005f8d70_record { int* FUN_006815c0(); };
struct FUN_005f8d70_actor : FUN_0047ded0_shell { bool FUN_00461560(); };
struct FUN_005f8d70_settings { float* FUN_00403e20(); };
extern FUN_005f8d70_settings DAT_011cb58c;
struct FUN_005f8d70_shell {
    unsigned short FUN_0047ff30();
    unsigned short FUN_005f8d70();
};
unsigned short FUN_005f8d70_shell::FUN_005f8d70()
{
    unsigned short result = 0;
    if (DAT_011cb6a0->FUN_00843150() &&
        !g_dataHandler->FUN_004516b0() &&
        reinterpret_cast<signed char*>(this)[0x50] == -1) {
        FUN_005f8d70_record* record =
            static_cast<FUN_005f8d70_record*>(DAT_011cb6a0->FUN_00600700(
                reinterpret_cast<FUN_005f8d70_virtual*>(
                    reinterpret_cast<char*>(this) - 0x30)->v5(1)));
        if (record == 0 || *record->FUN_006815c0() == 0)
            reinterpret_cast<signed char*>(this)[0x50] = 0;
        else
            reinterpret_cast<signed char*>(this)[0x50] = 1;
    }
    if (reinterpret_cast<signed char*>(this)[0x50] == 0)
        return 0;
    if (reinterpret_cast<FUN_005f8d70_actor*>(
            reinterpret_cast<char*>(this) - 0xdc)->FUN_00461560()) {
        short level = reinterpret_cast<FUN_005f8d70_actor*>(
            reinterpret_cast<char*>(this) - 0xdc)->FUN_0047ded0();
        if (level < 1)
            level = 1;
        result = FUN_0047ff30();
        result += static_cast<int>(static_cast<double>(level) *
            *DAT_011cb58c.FUN_00403e20());
    } else {
        result = FUN_0047ff30();
    }
    return result;
}