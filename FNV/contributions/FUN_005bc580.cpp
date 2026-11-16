extern bool DAT_011f122c;
extern const char DAT_010399b8[];
extern const char DAT_010399bc[];
extern const char DAT_0103a094[];
void __cdecl FUN_00703c00(const char* format, const char* value);

bool __cdecl FUN_005bc580()
{
    DAT_011f122c = !DAT_011f122c;

    if (tlsData.bConsoleEcho)
    {
        FUN_00703c00(DAT_0103a094,
                      DAT_011f122c ? DAT_010399bc : DAT_010399b8);
    }
    return true;
}
