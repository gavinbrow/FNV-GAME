// @fnv 0x00fb8770
extern "C" char DAT_011f8bc4;
extern "C" void (__stdcall *DAT_00fdf054)(void*);
extern "C" void FUN_00fdc480();
extern "C" int __cdecl atexit(void (__cdecl *function)());

extern "C" void FUN_00fb8770()
{
    DAT_00fdf054(&DAT_011f8bc4);
    atexit(&FUN_00fdc480);
}