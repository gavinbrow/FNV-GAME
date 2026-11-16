typedef void (__cdecl* Callback)();

extern "C" unsigned char* __cdecl FUN_00ed11de();
extern "C" void __cdecl FUN_00ed14b4();

// @fnv 0x00ed14ed
extern "C" void __cdecl FUN_00ed14ed()
{
    unsigned char* state = FUN_00ed11de();
    Callback callback = *reinterpret_cast<Callback*>(state + 0x7c);
    if (callback != 0)
    {
        callback();
    }
    FUN_00ed14b4();
}
