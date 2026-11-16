// @fnv 0x00fb85c0
extern "C" char DAT_011f8170;
extern "C" void (__stdcall *DAT_00fdf054)(void*);
extern "C" void FUN_00fdc370();
extern "C" int __cdecl atexit(void (__cdecl *function)());

extern "C" void FUN_00fb85c0()
{
    DAT_00fdf054(&DAT_011f8170);
    atexit(&FUN_00fdc370);
}