struct RefEntryObject {
    virtual void Unknown();
    virtual void Release();
    volatile long referenceCount;
    void IncRefCount() { InterlockedIncrement(&referenceCount); }
    void DecRefCount() {
        if (InterlockedDecrement(&referenceCount) == 0)
            Release();
    }
};
struct RecordEntry {
    NiPointer<RefEntryObject> object;
    unsigned int value;
    RecordEntry() : object(), value(0) {}
};
struct RecordArray {
    void* vtable;
    RecordEntry* records;
    unsigned int capacity;
    unsigned int count;
    unsigned int elementSize;
    void FUN_00ca4b20();
};
void RecordArray::FUN_00ca4b20() {
    for (unsigned int i = 0; i < count; ++i) {
        records[i] = RecordEntry();
    }
    count = 0;
    elementSize = 0;
}