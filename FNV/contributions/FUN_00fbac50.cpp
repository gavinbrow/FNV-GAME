// @fnv 0x00fbac50
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fdd2b0(void);
extern "C" void __cdecl FUN_00fbac50(void)
{
    atexit(FUN_00fdd2b0);
}
