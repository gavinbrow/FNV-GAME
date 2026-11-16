// @fnv 0x00fb9610
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc7e0();

void __cdecl FUN_00fb9610()
{
    atexit(&FUN_00fdc7e0);
}
