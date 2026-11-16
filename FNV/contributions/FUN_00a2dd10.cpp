extern char* DAT_0109b220;
struct FNVRefObject {
    virtual void UnusedVirtual();
    virtual void DeleteThis();
    volatile long referenceCount;
};
struct FNVHolder {
    void* vtable;
    int unk04;
    int unk08;
    FNVRefObject* object;
    char* text;
    void FUN_00a2dd10();
};
void FNVHolder::FUN_00a2dd10() {
    FnInterlockedDecrement decrement = DAT_00fdf1c4;
    FNVRefObject* held = object;
    if (held) {
        if (decrement((void*)&held->referenceCount) == 0)
            held->DeleteThis();
        object = 0;
    }
    if (text != DAT_0109b220)
        decrement(text - 8);
    held = object;
    if (held && decrement((void*)&held->referenceCount) == 0)
        held->DeleteThis();
}