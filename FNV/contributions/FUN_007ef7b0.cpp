struct VATSMenu_007ef7b0 : VATSMenu {
    void __thiscall FUN_007ef7b0(int aiID, int aiArg);
};
void* __cdecl FUN_004b7210();
bool __cdecl _FUN_004b71d0();

void __thiscall VATSMenu_007ef7b0::FUN_007ef7b0(int aiID, int aiArg)
{
    FUN_004b7210();
    if (_FUN_004b71d0())
        return;

    switch (aiID) {
    case 2: case 3: case 4: case 5: case 30: case 31:
        bMouseOverButton = true;
        break;
    }
}
