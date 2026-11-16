// @fnv 0x00fba020
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdce40();
void __cdecl FUN_00fba020()
{
    atexit(&FUN_00fdce40);
}
