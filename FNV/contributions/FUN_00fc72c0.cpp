extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern void __cdecl FUN_00fde320();

// @fnv 0x00fc72c0
void __cdecl FUN_00fc72c0()
{
    atexit(FUN_00fde320);
}
