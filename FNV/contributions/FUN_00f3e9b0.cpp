extern unsigned char DAT_011c5d10;
extern void __cdecl FUN_00488f50();
extern void __cdecl FUN_00489070();
extern void __cdecl FUN_00fc9090();
extern "C" void __stdcall FUN_00ec782f(
    void* data,
    unsigned int elementSize,
    int elementCount,
    void (__cdecl* constructor)(),
    void (__cdecl* destructor)());
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f3e9b0
void FUN_00f3e9b0()
{
    FUN_00ec782f(&DAT_011c5d10, 24, 20, FUN_00488f50, FUN_00489070);
    atexit(FUN_00fc9090);
}
