struct InventoryItem {
    bool FUN_00418750();
    short FUN_00418770();
};
struct LinkedEntry {
    InventoryItem** FUN_006815c0();
    LinkedEntry* FUN_00726070();
};
struct FUN_004bcc30_List {
    LinkedEntry* first;
    int FUN_004bcc30();
};
int FUN_004bcc30_List::FUN_004bcc30()
{
    LinkedEntry* current = first;
    int total = 0;
    while (current && *current->FUN_006815c0()) {
        InventoryItem* item = *current->FUN_006815c0();
        if (item && item->FUN_00418750()) {
            total += item->FUN_00418770();
        }
        current = current->FUN_00726070();
    }
    return total;
}