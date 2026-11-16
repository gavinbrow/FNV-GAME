// @fnv 0x00fb9660
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc8d0();
void __cdecl FUN_00fb9660()
{
    atexit(&FUN_00fdc8d0);
}
