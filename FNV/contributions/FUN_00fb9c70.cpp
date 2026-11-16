// @fnv 0x00fb9c70
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fdcda0(void);

extern "C" void __cdecl FUN_00fb9c70(void)
{
    atexit(FUN_00fdcda0);
}
