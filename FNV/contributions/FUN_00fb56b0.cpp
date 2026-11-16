extern "C" int __cdecl atexit(void (__cdecl *fn)());
extern "C" void __cdecl FUN_00fdae70();

// @fnv 0x00fb56b0
extern "C" void __cdecl FUN_00fb56b0()
{
    atexit(FUN_00fdae70);
}