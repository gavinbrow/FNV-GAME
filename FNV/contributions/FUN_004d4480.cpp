struct ItemExtraNode;
struct ChangeEntry {
    int FUN_0044ddc0();
    ItemExtraNode* FUN_00559450();
};
struct ItemChangeNode {
    ChangeEntry** _ref_006815c0();
    ItemChangeNode* _ref_00726070();
};
struct ItemExtraNode {
    int* _ref_006815c0();
    ItemExtraNode* _ref_00726070();
};
struct ItemChangeList {
    ItemChangeNode* first;
    int FUN_004d4480(int form, int position);
};
int ItemChangeList::FUN_004d4480(int form, int position) {
    if (form == 0 || position == -1)
        return 0;
    ItemChangeNode* node = first;
    while (node != 0) {
        ChangeEntry* entry = *node->_ref_006815c0();
        node = node->_ref_00726070();
        if (entry != 0 && entry->FUN_0044ddc0() == form) {
            int index = 0;
            ItemExtraNode* extra = entry->FUN_00559450();
            while (extra != 0) {
                int result = *extra->_ref_006815c0();
                if (index == position)
                    return result;
                ++index;
                extra = extra->_ref_00726070();
            }
            break;
        }
    }
    return 0;
}