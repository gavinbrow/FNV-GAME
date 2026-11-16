// Based on checked WIP by GPT-6 Astra Pro worker C.
// Final arithmetic hypothesis and subsequent validation by worker A.

namespace fnv_00526100
{
    struct GlobalObject2_0040c150
    {
        int* Int();
    };
}

struct GlobalObject_0045cfe0
{
    void FUN_0045cfe0(const char* name, int value);
};

extern fnv_00526100::GlobalObject2_0040c150 DAT_011c63cc;
extern GlobalObject_0045cfe0 DAT_011c3c90;
extern const char DAT_01017ffc[];
extern "C" void __cdecl FUN_00fc8090();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f38300
void FUN_00f38300()
{
    DAT_011c3c90.FUN_0045cfe0(DAT_01017ffc,
        *DAT_011c63cc.Int() * *DAT_011c63cc.Int()
        + *DAT_011c63cc.Int() + *DAT_011c63cc.Int() + 1);
    atexit(FUN_00fc8090);
}
