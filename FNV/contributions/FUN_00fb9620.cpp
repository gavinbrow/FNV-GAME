// @fnv 0x00fb9620
extern "C" int __cdecl atexit(void (__cdecl *)());
extern "C" void __cdecl FUN_00fdc810();

void __cdecl FUN_00fb9620()
{
    atexit(&FUN_00fdc810);
}
