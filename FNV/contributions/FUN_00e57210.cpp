struct HolderView { int unk00; int unk04; int unk08; int unk0c; void* volatile m_pAllocator; };
struct FloatArrayRef {
    float* data;
    int size;
    unsigned int capacity;
};

int __cdecl FUN_00e57210(FloatArrayRef* array, int count) {
    int added = FUN_00e54840(reinterpret_cast<float**>(array), count);
    int destination = added + count;
    int newSize = destination + 1;
    HolderStub* holder = FUN_00c85750();
    E4AAA0Allocator* alloc = reinterpret_cast<E4AAA0Allocator*>(reinterpret_cast<HolderView*>(holder)->m_pAllocator);
    unsigned int capacity = array->capacity & 0x3fffffff;
    if ((int)capacity < newSize) {
        int newCapacity = (int)(capacity * 2);
        if (newSize >= newCapacity) {
            newCapacity = newSize;
        }
        FUN_00c908c0(alloc, array, newCapacity, 4);
    }
    array->size = newSize;
    int dest = destination;

    for (int n = count; n > 0; --n) {
        if (array->data[n] != array->data[n-1]) array->data[dest--] = array->data[n];
        array->data[dest--] = array->data[n];
    }
    return added - 2;
}