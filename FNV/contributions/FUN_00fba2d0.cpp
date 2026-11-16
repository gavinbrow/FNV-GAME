// @fnv 0x00fba2d0
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdcf20();
void __cdecl FUN_00fba2d0()
{
    atexit(&FUN_00fdcf20);
}
