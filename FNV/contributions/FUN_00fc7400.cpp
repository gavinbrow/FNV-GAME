extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern void __cdecl FUN_00fde340();

// @fnv 0x00fc7400
void __cdecl FUN_00fc7400()
{
    atexit(FUN_00fde340);
}
