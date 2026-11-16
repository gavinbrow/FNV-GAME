
struct FUN_00cb1930_s {
    int FUN_00cb1930(const void* key, int defaultValue);
};
struct FUN_00c85750_s {
    void* m00;
    void* m04;
    void* m08;
    void* m0c;
    void* allocator;
    static FUN_00c85750_s* __cdecl FUN_00c85750();
};
struct TrackedElement {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    int state;
    unsigned int unk14;
};
struct FUN_00dbda80_s {
    void* m00;
    void* m04;
    TrackedElement* entries;
    void* m0c;
    void* m10;
    FUN_00cb1930_s entryIndex;
    unsigned int unk18;
    unsigned int unk1c;
    DepthLimit firstDepth;
    void FUN_00dbda80(void* key, int value);
};
void FUN_00dbda80_s::FUN_00dbda80(void* key, int value)
{
    int index = entryIndex.FUN_00cb1930(key, -1);
    if (index >= 0)
        entries[index].state = -2;

    FUN_00c85750_s* router = FUN_00c85750_s::FUN_00c85750();
    ((DepthLimit*)&entryIndex)->FUN_00cb1870(router->allocator, key, -2);

    FUN_00c85750_s* router2 = FUN_00c85750_s::FUN_00c85750();
    firstDepth.FUN_00cb1870(router2->allocator, key, value);
}
