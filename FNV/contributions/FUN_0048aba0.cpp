extern "C" char DAT_01183040;
extern "C" char DAT_011831c4;
void* __cdecl FUN_00ec43fb(unsigned int, int, const void*, const void*, int);
struct TextureSwapRecord {
    unsigned int formID;
    int index;
    char objectName[128];
};
struct TextureSwapNode {
    unsigned char FUN_008256d0();
    TextureSwapRecord** FUN_006815c0();
    TextureSwapNode* FUN_00726070();
};
struct TextureSwapList {
    TextureSwapNode* FUN_00500940();
};
struct FUN_0048aba0_Class {
    void FUN_00489430(unsigned int);
    void FUN_0048ade0();
    void FUN_0048ae30(const char*, int, unsigned int);
    void FUN_0048aba0(unsigned int formID);
};
void FUN_0048aba0_Class::FUN_0048aba0(unsigned int formID) {
    FUN_00489430(formID);
    TextureSwapList* list = static_cast<TextureSwapList*>(FUN_00ec43fb(formID, 0, &DAT_01183040, &DAT_011831c4, 0));
    if (!list)
        return;
    FUN_0048ade0();
    TextureSwapNode* node = list->FUN_00500940();
    while (node && !node->FUN_008256d0()) {
        TextureSwapRecord* record = *node->FUN_006815c0();
        FUN_0048ae30(record->objectName, record->index, record->formID);
        node = node->FUN_00726070();
    }
}