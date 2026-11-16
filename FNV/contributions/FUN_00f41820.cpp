// @fnv 0x00f41820
extern "C" unsigned char DAT_011c7860;
extern "C" void __cdecl FUN_0045cec0(void*);
extern "C" void __cdecl FUN_006694e0(void*);
extern "C" void __cdecl FUN_00fc9a60();
extern "C" void __stdcall FUN_00ec782f(void*, unsigned int, int, void*, void*);
extern "C" int __cdecl atexit(void (__cdecl*)());

// @fnv 0x00f41820
extern "C" void __cdecl FUN_00f41820()
{
    FUN_00ec782f(&DAT_011c7860, sizeof(void*), 3,
                  reinterpret_cast<void*>(&FUN_006694e0),
                  reinterpret_cast<void*>(&FUN_0045cec0));
    atexit(FUN_00fc9a60);
}
