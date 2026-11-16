// @fnv 0x00fb9600
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc7b0();
void __cdecl FUN_00fb9600()
{
    atexit(&FUN_00fdc7b0);
}
