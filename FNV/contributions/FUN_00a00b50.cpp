
struct TileNode;
struct TileObject {
    void* unk00;
    TileNode* unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    unsigned int uiFlags;
    bool GetFlag(unsigned int uiFlag) const { return !!(uiFlags & uiFlag); }
    void FUN_00a00b50();
};
struct TileNode {
    TileNode* pkNext;
    TileNode* pkPrev;
    TileObject* pTile;
};
void TileObject::FUN_00a00b50() {
    AutoTileLock_Local lock;
    if (!GetFlag(0x2000) && !GetFlag(0x4000)) {
        uiFlags |= 0x4000;
        TileNode* iter = unk04;
        TileNode* current = iter;
        while (current) {
            TileObject** pChild = &current->pTile;
            current = current->pkNext;
            (*pChild)->FUN_00a00b50();
        }
    }
}
