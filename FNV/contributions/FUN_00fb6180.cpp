// @fnv 0x00fb6180
extern "C" int __cdecl atexit(void (__cdecl *callback)());
extern "C" void __cdecl FUN_00fdb100();

void __cdecl FUN_00fb6180()
{
    atexit(FUN_00fdb100);
}
