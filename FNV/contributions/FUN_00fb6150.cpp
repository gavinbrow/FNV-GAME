// @fnv 0x00fb6150
extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __cdecl FUN_00fdb0d0();

void __cdecl FUN_00fb6150()
{
    atexit(FUN_00fdb0d0);
}
