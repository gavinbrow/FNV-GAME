// @fnv 0x00fbaaf0
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fdd250(void);

extern "C" void __cdecl FUN_00fbaaf0(void)
{
    atexit(FUN_00fdd250);
}
