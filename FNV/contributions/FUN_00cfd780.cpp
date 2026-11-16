struct OffsetDescriptor {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    signed char relativeOffset;
};
struct AllocatorInterface {
    virtual void unk00();
    virtual void* allocate(unsigned int size);
};
struct MemoryContext {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    AllocatorInterface* allocator;
};
MemoryContext* __cdecl FUN_00c85750();
struct ContactObject {
    int unk00;
    unsigned short memSize;
    ContactObject* FUN_00cfd670(void* a, void* b, void* c);
};
struct FUN_00cfd780_class {
    void* unk00;
    void* unk04;
    void* m_08;
    ContactObject* FUN_00cfd780(OffsetDescriptor* first, OffsetDescriptor* second, int unused);
};
ContactObject* FUN_00cfd780_class::FUN_00cfd780(OffsetDescriptor* first, OffsetDescriptor* second, int unused)
{
    void* relativeFirst = (char*)first + first->relativeOffset;
    void* relativeSecond = (char*)second + second->relativeOffset;
    MemoryContext* manager = FUN_00c85750();
    ContactObject* memory = (ContactObject*)manager->allocator->allocate(128);
    memory->memSize = 128;
    return memory->FUN_00cfd670(m_08, relativeFirst, relativeSecond);
}
