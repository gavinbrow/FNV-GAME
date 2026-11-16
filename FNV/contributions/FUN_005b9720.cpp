extern unsigned char __cdecl FUN_005b9790(void);
extern void __cdecl FUN_005b97d0(bool);
extern void __cdecl FUN_00703c00(const char*, const char*);
extern const char str_010399afc[];
extern const char str_010399b8[];
extern const char str_010399bc[];

bool __cdecl FUN_005b9720(void)
{
    const char* puStack_8;

    FUN_005b97d0(FUN_005b9790() == 0);
    if (tlsData.bConsoleEcho) {
        if (FUN_005b9790()) {
            puStack_8 = str_010399bc;
        } else {
            puStack_8 = str_010399b8;
        }
        FUN_00703c00(str_010399afc, puStack_8);
    }
    return true;
}


