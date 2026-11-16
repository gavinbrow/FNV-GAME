extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern "C" void __cdecl FUN_00fdca50();

// @fnv 0x00fb9710
extern "C" void FUN_00fb9710()
{
    atexit(FUN_00fdca50);
}
