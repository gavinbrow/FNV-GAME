struct FUN_00425fd0_shell {
    bool FUN_00425fd0();
};

bool __cdecl FUN_00527b20(TESForm* form) {
    if (form == 0)
        return true;

    switch (form->FNV_GetFormType()) {
    case 0x41:
        return true;
    case 0x39: {
        FUN_00425fd0_shell* cell = (FUN_00425fd0_shell*)form;
        if (cell->FUN_00425fd0())
            return true;
        break;
    }
    }
    return false;
}