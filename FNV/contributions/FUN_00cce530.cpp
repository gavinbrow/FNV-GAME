struct MemoryAllocator_CCE530 {
    virtual void Unknown00(); virtual void Unknown04();
    virtual void Unknown08(); virtual void Unknown0C();
    virtual void Free(void* allocation, unsigned int bytes);
};
extern "C" FUN_00e4ae20_Router* FUN_00c85750();
struct ArrayElement_CCE530 { int unk00, unk04, unk08, unk0C; };
struct Array_CCE530 {
    ArrayElement_CCE530* data;
    int size;
    int capacityAndFlags;
    ~Array_CCE530() {
        FUN_00e4ae20_Router* router = FUN_00c85750();
        MemoryAllocator_CCE530* heap =
            (MemoryAllocator_CCE530*)router->m_pMemoryManager;
        int capacity = capacityAndFlags;
        size = 0;
        if ((capacity & 0x80000000) == 0) {
            ArrayElement_CCE530* allocation = data;
            heap->Free(allocation, (capacity & 0x3fffffff) * sizeof(ArrayElement_CCE530));
        }
        data = 0;
        capacityAndFlags = 0x80000000;
    }
};
struct FUN_00cce530 {
    Array_CCE530 first;
    Array_CCE530 second;
    ~FUN_00cce530();
};
FUN_00cce530::~FUN_00cce530() {}