extern void* DAT_011ac044;
extern void* DAT_011ac040;
extern char DAT_010a1458[];
extern "C" void __cdecl FUN_00a47600(void*);
extern "C" void __cdecl FUN_00fdb270(void)
{
    void* p = DAT_011ac044;
    DAT_011ac040 = DAT_010a1458;
    FUN_00a47600(p);
}
