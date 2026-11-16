// @fnv 0x00fb3340
extern "C" char DAT_011f3330;
extern "C" void (__stdcall *DAT_00fdf054)(void*);
extern "C" void FUN_00fda140();
extern "C" int __cdecl atexit(void (__cdecl *function)());

extern "C" void FUN_00fb3340()
{
    DAT_00fdf054(&DAT_011f3330);
    atexit(&FUN_00fda140);
}