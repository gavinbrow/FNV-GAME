// @fnv 0x00fba6d0
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdcf90();
void __cdecl FUN_00fba6d0()
{
    atexit(&FUN_00fdcf90);
}
