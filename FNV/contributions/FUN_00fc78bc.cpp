extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern void __cdecl FUN_00fde54f();

// @fnv 0x00fc78bc
void __cdecl FUN_00fc78bc()
{
    atexit(FUN_00fde54f);
}
