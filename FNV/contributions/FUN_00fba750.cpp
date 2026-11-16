extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __cdecl FUN_00fdcfe0();

// @fnv 0x00fba750
void __cdecl FUN_00fba750()
{
    atexit(FUN_00fdcfe0);
}
