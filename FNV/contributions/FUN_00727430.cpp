struct FNVVirtualTarget {
    bool (__thiscall **vtable)(FNVVirtualTarget*, int);
};
struct FNVAuxController {
    FNVVirtualTarget* FUN_008d8520();
    void FUN_00950030();
};
extern FNVAuxController* DAT_011dea3c;
extern int DAT_011d8e90;
struct FNVMenuAction {
    void FUN_00700320(int id, int value);
};
struct FNVRecipeMenu {
    int field00;
    FNVMenuAction* action;
    void FUN_00a1d910();
};
void __cdecl FUN_007640a0(int value);

void __cdecl FUN_00727430()
{
    if (DAT_011d8e90 != 0) {
        FNVVirtualTarget* target = DAT_011dea3c->FUN_008d8520();
        if (target->vtable[0x474 / 4](target, 1)) {
            DAT_011dea3c->FUN_00950030();
        }

        int value = 0;
        FUN_007640a0(value);
        ((FNVRecipeMenu*)DAT_011d8e90)->action->FUN_00700320(0x1772, 1);
        ((FNVRecipeMenu*)DAT_011d8e90)->FUN_00a1d910();
    }
}