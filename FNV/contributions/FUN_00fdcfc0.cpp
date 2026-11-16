extern void* DAT_011ae5dc;
extern void* DAT_011ae5d8;
extern char DAT_010b9d24[];
extern "C" void __cdecl FUN_00aa10f0(void*);
extern "C" void __cdecl FUN_00fdcfc0(void)
{
    void* p = DAT_011ae5dc;
    DAT_011ae5d8 = DAT_010b9d24;
    FUN_00aa10f0(p);
}
