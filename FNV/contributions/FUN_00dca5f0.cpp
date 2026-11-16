struct C85750Router {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* allocator;
};
C85750Router* FUN_00c85750();
void __cdecl FUN_00c908c0(void* allocator, void* array, int newCapacity, int itemSize);
void __cdecl FUN_00cb1260(void* dst, const void* src, unsigned int bytes);
struct DCA5F0Array {
    void* volatile data;
    volatile int count;
    int capacityAndFlags;
};
struct DCA5F0Owner {
    int unk00;
    int unk04;
    int unk08;
    DCA5F0Array elements;
    void FUN_00dca5f0(const void* source, int count);
};
void DCA5F0Owner::FUN_00dca5f0(const void* source, int count)
{
    DCA5F0Array* array = &elements;
    C85750Router* router = FUN_00c85750();
    void* allocator = router->allocator;
    int capacity = array->capacityAndFlags & 0x3fffffff;
    if (capacity < count) {
        int grown = capacity * 2;
        if (count >= grown)
            grown = count;
        FUN_00c908c0(allocator, array, grown, 4);
    }
    array->count = count;
    FUN_00cb1260(array->data, source, count * 4);
}