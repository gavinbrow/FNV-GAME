struct FUN_006c93f0_Stage {
    void FUN_006ddbe0();
};
struct FUN_006c93f0_Node {
    FUN_006c93f0_Stage* FUN_00717e50();
    void FUN_006f5020();
};
struct FUN_006c93f0_Collection {
    unsigned int FUN_005a4320();
    FUN_006c93f0_Node* FUN_006e78b0(unsigned int index);
};
struct FUN_006c93f0_Object {
    int unk00;
    FUN_006c93f0_Collection* collection;
    bool FUN_006c9fc0(int index, int* firstIndex, int* lastIndex);
    bool FUN_006ca0e0(int flag, int index);
    int FUN_006c93f0(int index);
};
int FUN_006c93f0_Object::FUN_006c93f0(int index) {
    int firstIndex = -1;
    int lastIndex = -1;
    if (!FUN_006c9fc0(index, &firstIndex, &lastIndex))
        return 0;
    for (unsigned int i = 0; i < collection->FUN_005a4320(); ++i)
        collection->FUN_006e78b0(i)->FUN_00717e50()->FUN_006ddbe0();
    for (int j = firstIndex; j <= lastIndex; ++j)
        collection->FUN_006e78b0(j)->FUN_006f5020();
    if (!FUN_006ca0e0(0, index))
        return -1;
    return 2;
}
