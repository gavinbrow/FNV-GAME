// @fnv 0x00fbb130
extern "C" int __cdecl atexit(void (__cdecl *function)(void));
extern "C" void __cdecl FUN_00fdd420(void);
extern "C" void __cdecl FUN_00fbb130(void)
{
    atexit(FUN_00fdd420);
}
