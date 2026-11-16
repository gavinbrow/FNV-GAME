// @fnv 0x00fb9630
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc840();
void __cdecl FUN_00fb9630()
{
    atexit(&FUN_00fdc840);
}
