extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern void __cdecl FUN_00fdb1d0();

// @fnv 0x00fb64d0
void __cdecl FUN_00fb64d0()
{
    atexit(FUN_00fdb1d0);
}
