// @fnv 0x00fb9670
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc900();
void __cdecl FUN_00fb9670()
{
    atexit(&FUN_00fdc900);
}
