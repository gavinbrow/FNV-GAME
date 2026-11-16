struct GlobalObject_0045cfe0
{
    void FUN_0045cfe0(const char* name, int value);
};
extern GlobalObject_0045cfe0 DAT_011c77c0;
extern const char DAT_010226f0;
extern void __cdecl FUN_00fc9920();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f41320
void FUN_00f41320()
{
    DAT_011c77c0.FUN_0045cfe0(&DAT_010226f0, -1);
    atexit(FUN_00fc9920);
}
