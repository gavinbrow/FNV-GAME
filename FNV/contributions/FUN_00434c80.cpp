
struct FNVLoadEntry {
    unsigned int first;
    unsigned int second;
    FNVLoadEntry();
};
struct FNVLoadList {
    void FUN_005ae3d0(FNVLoadEntry** item);
};
struct FNVLoadBlock {
    void* value00;
    void* value04;
    void* value08;
    ContNode firstNode;
};
struct FNVLoadHost : FUN_00434d90_standin {
    void FUN_00434c80(void* input);
};
extern unsigned char DAT_01184010;
extern FNVLoadBlock* __cdecl FUN_00ec43fb(void* input, int unused, const void* sourceA, const void* sourceB, int mode);

void FNVLoadHost::FUN_00434c80(void* input)
{
    ContNode* node;
    FNVLoadBlock* block = FUN_00ec43fb(input, 0, &DAT_01183b2c, &DAT_01184010, 0);
    if (!block) return;
    FUN_00434d90();
        node = &block->firstNode;
        while (node && !node->FUN_008256d0()) {
            void* contents = *(void**)node->FUN_006815c0();
            {
                FNVLoadEntry* entry = new FNVLoadEntry;
            memcpy(entry, contents, 8);
            ((FNVLoadList*)&m_list)->FUN_005ae3d0(&entry);
            }
            node = node->GetNext();
        }
}
