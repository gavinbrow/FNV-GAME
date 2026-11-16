// @fnv 0x00fb6340
extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __cdecl FUN_00fdb1a0();

void __cdecl FUN_00fb6340()
{
    atexit(FUN_00fdb1a0);
}
