// @fnv 0x00fbac60
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fdd2e0(void);
extern "C" void __cdecl FUN_00fbac60(void)
{
    atexit(FUN_00fdd2e0);
}
