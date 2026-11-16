// @fnv 0x00fb95f0
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdcb10();

void __cdecl FUN_00fb95f0()
{
    atexit(&FUN_00fdcb10);
}
