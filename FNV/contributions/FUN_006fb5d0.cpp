struct B5D0Status { unsigned char FUN_006fb150(); };
struct B5D0Item {
    B5D0Status* FUN_00559450();
    void FUN_006fb760();
    void FUN_006fb6e0();
};
struct B5D0List {
    bool FUN_008256d0();
    B5D0Item** FUN_006815c0();
    B5D0List* FUN_00726070();
};
void __cdecl FUN_006fb5d0()
{
    B5D0List* node = reinterpret_cast<B5D0List*>(&g_011d8624);
    while (node && !node->FUN_008256d0()) {
        B5D0Item* item = *node->FUN_006815c0();
        if (item->FUN_00559450()->FUN_006fb150()) {
            item->FUN_006fb760();
        } else {
            item->FUN_006fb6e0();
        }
        node = node->FUN_00726070();
    }
}