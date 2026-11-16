// @fnv 0x00fc7190
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fde2d0(void);
extern "C" void __cdecl FUN_00fc7190(void)
{
    atexit(FUN_00fde2d0);
}
