
extern "C" char DAT_01070244;
extern "C" void* __cdecl FUN_00a00940(const char* name, int lookupMode);

struct SelectedOption {
    bool FUN_00a01230(void* item);
};

struct SelectionManager {
    void* vtable;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    SelectedOption* selectedOption;

    bool FUN_0072c7d0();
    bool FUN_007242f0(SelectedOption* option);
    void FUN_0072c880();
    bool FUN_0072b5b0(SelectedOption* option);
};

bool SelectionManager::FUN_0072b5b0(SelectedOption* option) {
    if (FUN_0072c7d0() &&
        (!option || (FUN_007242f0(option) &&
                     option->FUN_00a01230(FUN_00a00940(&DAT_01070244, -1))))) {
        selectedOption = option;
        FUN_0072c880();
        return true;
    } else {
        return false;
    }
}
