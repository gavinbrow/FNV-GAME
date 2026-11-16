struct FUN_007a6b00_item {
    Tile* displayTile;
    unsigned int metadata04;
    unsigned char inactive;
};
struct FUN_007a6b00_listNode : SL {
    FUN_007a6b00_item** FUN_006815c0();
    FUN_007a6b00_listNode* FUN_00726070();
};
struct FUN_007a6b00_shell : FUN_007a1c90 {
    void FUN_007a6b00();
    void FUN_007269d0(Tile*);
    void FUN_007a7080();
    void FUN_007a6c80();
};
void FUN_007a6b00_shell::FUN_007a6b00()
{
    f1c = 0;
    f20 = 0.0f;
    for (FUN_007a6b00_listNode* node =
        reinterpret_cast<FUN_007a6b00_listNode*>(static_cast<SL*>(this));
        node != 0 && *node->FUN_006815c0() != 0;
        node = node->FUN_00726070()) {
        if ((*node->FUN_006815c0())->inactive == 0) {
            (*node->FUN_006815c0())->displayTile->Set(0xfac, static_cast<unsigned short>(f1c++));
            FUN_007269d0((*node->FUN_006815c0())->displayTile);
        }
    }
    FUN_007a7080();
    FUN_007a6c80();
}