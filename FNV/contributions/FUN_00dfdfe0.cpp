struct EngineHeap {
    virtual void Unknown0();
    virtual void Unknown1();
    virtual void Unknown2();
    virtual void Unknown3();
    virtual void Free(void* memory, unsigned int bytes);
};
struct EngineMemoryManager {
    void* unknown00;
    void* unknown04;
    void* unknown08;
    void* unknown0C;
    EngineHeap* heap;
};
EngineMemoryManager* __cdecl FUN_00c85750();
struct ArrayEntry {
    unsigned int index;
    unsigned int value;
};
struct ArrayBase {
    virtual void UnknownVirtual();
    unsigned int unknown04;
    ~ArrayBase() {}
};
struct ArrayStorage {
    ArrayEntry* entries;
    int length;
    int allocationFlags;
    __forceinline void Reset(EngineHeap* heap) {
        ArrayEntry* current = entries;
        if (length > 0) {
            int remaining = length;
            do {
                reinterpret_cast<FUN_00cb0c00_class*>(current)->FUN_00cb0c00();
                ++current;
            } while (--remaining != 0);
        }
        length = 0;
        if (!(allocationFlags & 0x80000000))
            heap->Free(entries, (allocationFlags & 0x3fffffff) * sizeof(ArrayEntry));
        entries = 0;
        allocationFlags = 0x80000000;
    }
};
struct ArrayContainer : ArrayBase {
    ArrayStorage contents;
    void FUN_00dfdfe0();
};
void ArrayContainer::FUN_00dfdfe0()
{
    EngineHeap* heap = FUN_00c85750()->heap;
    contents.Reset(heap);
    ArrayBase::~ArrayBase();
}
