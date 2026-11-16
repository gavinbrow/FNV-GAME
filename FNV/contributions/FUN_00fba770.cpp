// @fnv 0x00fba770
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdd040();
void __cdecl FUN_00fba770()
{
    atexit(&FUN_00fdd040);
}
