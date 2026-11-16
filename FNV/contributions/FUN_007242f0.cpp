struct ListItem {
    int key;
};
struct ListLink {
    ListItem* item;
    ListLink* next;
    ListItem** FUN_006815c0();
    ListLink* FUN_00726070();
};
struct ListOwner {
    int unknown00;
    ListLink head;
    bool FUN_007242f0(int key);
};
bool ListOwner::FUN_007242f0(int key)
{
    ListLink* current = this ? &head : 0;
    for (; current && *current->FUN_006815c0(); current = current->FUN_00726070()) {
        if ((*current->FUN_006815c0())->key == key) {
            return true;
        }
    }
    return false;
}