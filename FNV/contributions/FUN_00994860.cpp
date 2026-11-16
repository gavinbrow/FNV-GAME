struct ListItem {
    int FUN_0059bb30();
};
struct ListSlot {
    ListItem* item;
};
struct SearchList {
    ListSlot** entries;
    unsigned int entryCount;
    bool FUN_00994860(int searchValue);
};
bool SearchList::FUN_00994860(int searchValue)
{
    for (unsigned int index = 0; index < entryCount; ++index) {
        if (entries[index]->item->FUN_0059bb30() == searchValue) {
            return true;
        }
    }
    return false;
}