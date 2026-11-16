struct VATSMenu007ef830 : VATSMenu {
    void FUN_007ef830(int aiID, int aiOther);
};

void VATSMenu007ef830::FUN_007ef830(int aiID, int aiOther)
{
    _FUN_004b7210();
    if (_FUN_004b71d0()) {
        return;
    }

    switch (aiID) {
    case 2:
    case 3:
    case 4:
    case 5:
    case 30:
    case 31:
        bMouseOverButton = false;
        break;
    }
}
