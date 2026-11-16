struct PendingObject {
    int group;
    int value;
    int flags08;
    int flags0c;
    int flags10;
    InventoryLookup resource;
    void* __thiscall FUN_00915790(unsigned int deletingFlags);
};
struct PendingListNode {
    PendingObject** FUN_006815c0();
    PendingListNode* FUN_00726070();
    void FUN_00905330(PendingObject** item);
};
struct PendingResourceManager {
    void FUN_00528870(InventoryItemLookup* item, unsigned int unused);
};
extern PendingResourceManager* DAT_01202d98;
struct PendingProcess : MiddleHighProcess {
    void __thiscall FUN_00915870(int group, int value);
};
void PendingProcess::FUN_00915870(int group, int value) {
    PendingListNode* current = reinterpret_cast<PendingListNode*>(pListItemstoEquipUnequip);
    while (current != 0 && *current->FUN_006815c0() != 0) {
        PendingObject* item = *current->FUN_006815c0();
        if (item != 0 && item->group == group && value == item->value) {
            if (item->resource.FUN_00559450() != 0) {
                DAT_01202d98->FUN_00528870(item->resource.FUN_00559450(), 0);
            }
            PendingObject* destructorOwner = item;
            PendingObject* destructorCandidate = destructorOwner;
            destructorCandidate ? destructorCandidate->FUN_00915790(1) : 0;
            reinterpret_cast<PendingListNode*>(pListItemstoEquipUnequip)->FUN_00905330(&item);
            return;
        }
        current = current->FUN_00726070();
    }
}