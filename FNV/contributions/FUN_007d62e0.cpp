#include "h_f88eb61fd685.h"

struct FUN_007d62e0_shell : public StartMenu {
    void FUN_007d62e0();
};

void FUN_007d62e0_shell::FUN_007d62e0()
{
    this->lbSaveLoad.SetEnabled(true);
    this->lbSaveLoad.RemoveItem(this->lbSaveLoad.GetHighlightedItem());
    this->pTiles[6]->Set(0x1004, 1);
    if (!FUN_004b71d0()) {
        ((FUN_0075f6f0_shell*)this)->FUN_0075f6f0(0x40000, false);
    }
}
