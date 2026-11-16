// @fnv 0x00fb3700
extern "C" char DAT_011f33dc;
extern "C" void (__stdcall *DAT_00fdf054)(void*);
extern "C" void FUN_00fda3b0();
extern "C" int __cdecl atexit(void (__cdecl *function)());

extern "C" void FUN_00fb3700()
{
    DAT_00fdf054(&DAT_011f33dc);
    atexit(&FUN_00fda3b0);
}