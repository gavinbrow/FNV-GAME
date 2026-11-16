extern "C" void* __cdecl FUN_00ecdf44();
extern "C" void __cdecl FUN_00fde56d();
extern "C" int __cdecl atexit(void (__cdecl*)());

struct GlobalInitObject
{
    void __thiscall FUN_00ec3a4f(void* value);
};

extern GlobalInitObject DAT_0126fbc0;

// @fnv 0x00fc78de
void __cdecl FUN_00fc78de()
{
    char* value = static_cast<char*>(FUN_00ecdf44());
    DAT_0126fbc0.FUN_00ec3a4f(value + 64);
    atexit(FUN_00fde56d);
}
