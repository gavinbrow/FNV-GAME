extern "C" void* __cdecl _alloca(unsigned int);

struct ItemChangeList : BSSimpleList<ItemChange*> {
    int ItemsInList();
    void FUN_007653f0(ItemChange**, int (__cdecl *)(ItemChange*, ItemChange*), int);
    void FUN_007a8790(int (__cdecl *)(ItemChange*, ItemChange*));
    void FUN_0083fd60(int (__cdecl *compare)(ItemChange*, ItemChange*));
};

void ItemChangeList::FUN_0083fd60(int (__cdecl *compare)(ItemChange*, ItemChange*)) {
    int iStack6 = ItemsInList();
    ItemChange** puStack_10 = (ItemChange**)_alloca(iStack6 * 4 + 4);
    if (!puStack_10) {
        FUN_007a8790(compare);
        return;
    }

    BSSimpleList<ItemChange*>* _puStack_18 = this;
    int iStack_20 = 0;
    for (; iStack_20 < iStack6; ++iStack_20, _puStack_18 = _puStack_18->m_pkNext) {
        puStack_10[iStack_20] = _puStack_18->m_item;
    }

    FUN_007653f0(puStack_10, compare, iStack6);
    RemoveAll();

    _puStack_18 = this;
    BSSimpleList<ItemChange*>* puStack_1c = 0;
    for (int iStack_24 = 0; iStack_24 < iStack6; ++iStack_24) {
        if (iStack_24 > 0) {
            _puStack_18 = new BSSimpleList<ItemChange*>(puStack_10[iStack_24]);
        } else {
            _puStack_18->m_item = puStack_10[iStack_24];
            _puStack_18->m_pkNext = 0;
        }
        if (puStack_1c) {
            puStack_1c->m_pkNext = _puStack_18;
        }
        puStack_1c = _puStack_18;
    }
}



