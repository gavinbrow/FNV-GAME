// @fnv 0x00fbb7c0
extern "C" char DAT_01202d78;
extern "C" void (__stdcall *DAT_00fdf054)(void*);
extern "C" void FUN_00fdd430();
extern "C" int __cdecl atexit(void (__cdecl *function)());

extern "C" void FUN_00fbb7c0()
{
    DAT_00fdf054(&DAT_01202d78);
    atexit(&FUN_00fdd430);
}