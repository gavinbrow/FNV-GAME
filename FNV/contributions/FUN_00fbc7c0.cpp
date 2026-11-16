// @fnv 0x00fbc7c0
extern "C" char DAT_01203328;
extern "C" void (__stdcall *DAT_00fdf054)(void*);
extern "C" void FUN_00fddcd0();
extern "C" int __cdecl atexit(void (__cdecl *function)());

extern "C" void FUN_00fbc7c0()
{
    DAT_00fdf054(&DAT_01203328);
    atexit(&FUN_00fddcd0);
}