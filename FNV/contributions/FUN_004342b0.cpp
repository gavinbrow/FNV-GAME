extern char DAT_01183b2c;
extern char DAT_01184ea4;
struct Item_004342b0 {
    unsigned int field00;
    unsigned int field04;
    unsigned int field08;
    unsigned int field0C;
    unsigned int field10;
    unsigned int field14;
    unsigned int field18;
    Item_004342b0();
};
struct Node_004342b0 {
    bool FUN_008256d0();
    void** FUN_006815c0();
    Node_004342b0* FUN_00726070();
};
struct Results_004342b0 {
    unsigned int signature;
    unsigned int itemCount;
    unsigned int flags;
    Node_004342b0 firstNode;
};
struct ItemList_004342b0 {
    void FUN_005ae3d0(Item_004342b0**);
};
struct FUN_004342b0_shell {
    unsigned int field00;
    unsigned int field04;
    unsigned int field08;
    ItemList_004342b0 entries;
    void FUN_004343c0();
    void FUN_004342b0(void* archive);
};
Results_004342b0* __cdecl FUN_00ec43fb(void*, int, void*, void*, int);
extern "C" void* __cdecl memcpy(void*, const void*, unsigned int);

void FUN_004342b0_shell::FUN_004342b0(void* archive)
{
    Results_004342b0* result = FUN_00ec43fb(archive, 0, &DAT_01183b2c, &DAT_01184ea4, 0);
    if (result == 0) {
        return;
    }
    FUN_004343c0();
    Node_004342b0* node = &result->firstNode;
    while (node != 0 && !node->FUN_008256d0()) {
        void* source2 = *node->FUN_006815c0();
        Item_004342b0* item = new Item_004342b0();
        memcpy(item, source2, sizeof(Item_004342b0));
        entries.FUN_005ae3d0(&item);
        node = node->FUN_00726070();
    }
}
