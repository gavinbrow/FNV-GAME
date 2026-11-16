// @fnv 0x00fba100
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdcef0();
void __cdecl FUN_00fba100()
{
    atexit(&FUN_00fdcef0);
}
