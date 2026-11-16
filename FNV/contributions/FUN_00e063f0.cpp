struct FnvAllocator {
    virtual void unk00();
    virtual void unk04();
    virtual void unk08();
    virtual void* blockAlloc(int* bytes);
    virtual void blockFree(void* ptr, int bytes);
};
struct FnvMemoryRouter {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    FnvAllocator* allocator;
};
extern "C" FnvMemoryRouter* __cdecl FUN_00c85750();
struct FnvEntityArray {
    void** m_data;
    int m_size;
    int m_capacityAndFlags;
};
struct hkpConstraintChainInstance {
    void* unk00; void* unk04; void* unk08; void* unk0c;
    void* unk10; void* unk14; void* unk18; void* unk1c;
    void* unk20; void* unk24; void* unk28; void* unk2c;
    void* unk30; void* unk34;
    FnvEntityArray entities;
};
void __fastcall FUN_00e063f0(hkpConstraintChainInstanceAction* self, void* unusedEdx, FnvEntityArray* output)
{
    FnvEntityArray* source = &self->m_constraintInstance->entities;
    FnvAllocator* allocator = FUN_00c85750()->allocator;
    int capacity = output->m_capacityAndFlags & 0x3fffffff;
    if (capacity < source->m_size) {
        if (!(output->m_capacityAndFlags & 0x80000000))
            allocator->blockFree(output->m_data, capacity * 4);
        int bytes = source->m_size * 4;
        output->m_data = (void**)allocator->blockAlloc(&bytes);
        output->m_capacityAndFlags = bytes / 4;
    }
    int count = source->m_size;
    output->m_size = count;
    void** dest = output->m_data;
    void** from = source->m_data;
    for (int i = 0; i < count; ++i)
        dest[i] = from[i];
}