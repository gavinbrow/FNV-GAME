// @fnv 0x00fbab20
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fdd280(void);

extern "C" void __cdecl FUN_00fbab20(void)
{
    atexit(FUN_00fdd280);
}
