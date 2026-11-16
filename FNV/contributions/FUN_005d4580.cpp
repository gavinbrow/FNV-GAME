extern bool DAT_012004fc;
void __cdecl FUN_005d45c0();
void __cdecl FUN_005d45e0();

bool __cdecl FUN_005d4580()
{
    DAT_012004fc = true;
    FUN_005d45c0();

    for (unsigned int i = 0; i < 0x19; ++i) {
        FUN_005d45e0();
    }

    DAT_012004fc = false;
    return true;
}