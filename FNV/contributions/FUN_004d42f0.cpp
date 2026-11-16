
struct FUN_008c71b0 {
    int bits;
    FUN_008c71b0(int value);
};
struct InventoryStream {
    virtual void v0();
    virtual int getInitialSetting();
    void FUN_00428110(int*);
    void FUN_0042ce30(int*);
    void FUN_007037c0(int);
    void FUN_00428130(FUN_008c71b0);
    void FUN_0086cf00(FUN_008c71b0);
};
struct InventoryItem {
    void FUN_004bef60(InventoryStream*);
};
struct InventoryNode {
    InventoryItem** FUN_006815c0();
    InventoryNode* FUN_00726070();
};
struct InventoryItemManager {
    InventoryNode* entries;
    void __thiscall FUN_004d42f0(InventoryStream*);
};
void __thiscall InventoryItemManager::FUN_004d42f0(InventoryStream* stream)
{
    int savedInitial = stream->getInitialSetting();
    int savedFlags;
    {
        int savedExtra;
        stream->FUN_00428110(&savedFlags);
        stream->FUN_0042ce30(&savedExtra);
        stream->FUN_007037c0(0);
        stream->FUN_00428130(0x400);
        stream->FUN_0086cf00(0);
        InventoryNode* node = entries;
        while (node) {
            InventoryItem* item = *node->FUN_006815c0();
            if (item) item->FUN_004bef60(stream);
            node = node->FUN_00726070();
        }
        stream->FUN_007037c0(savedInitial);
        stream->FUN_00428130(*reinterpret_cast<FUN_008c71b0*>(&savedFlags));
        stream->FUN_0086cf00(*reinterpret_cast<FUN_008c71b0*>(&savedExtra));
    }
}
