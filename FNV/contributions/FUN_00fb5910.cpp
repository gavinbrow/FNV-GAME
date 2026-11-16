struct RuntimeGlobal;

extern void (__stdcall* DAT_00fdf054)(RuntimeGlobal* object);
extern RuntimeGlobal DAT_011f4900;
extern "C" int __cdecl atexit(void (__cdecl* callback)());
extern void __cdecl FUN_00fdaf70();

// @fnv 0x00fb5910
void FUN_00fb5910()
{
    DAT_00fdf054(&DAT_011f4900);
    atexit(FUN_00fdaf70);
}
