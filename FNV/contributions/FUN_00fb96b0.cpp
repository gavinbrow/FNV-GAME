// @fnv 0x00fb96b0
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc9c0();
void __cdecl FUN_00fb96b0()
{
    atexit(&FUN_00fdc9c0);
}
