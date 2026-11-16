extern "C" int DAT_010eb2c4;
extern "C" int DAT_0102e388;
struct FUN_00c905b0_Class {
    void FUN_00c905b0();
};
struct MemoryAllocator {
    virtual void Slot00();
    virtual void Slot04();
    virtual void Slot08();
    virtual void Slot0c();
    virtual void Free(void* address, unsigned int bytes);
};
struct MemoryRouter {
    int m_00, m_04, m_08, m_0c;
    MemoryAllocator* m_allocator;
};
void* FUN_00c85750() throw();
struct HandleState {int m_value;void FUN_00cb0c00();};
struct AnimationResource {
    int* m_vtable; int m_04; HandleState m_handle; int m_0c;
    FUN_00c905b0_Class** m_firstItems;
    int m_firstCount;
    int m_firstCapacity;
    FUN_00c905b0_Class** m_secondItems;
    int m_secondCount;
    int m_secondCapacity;
    void FUN_00e2ec00();
};
void AnimationResource::FUN_00e2ec00()
{
    m_vtable = &DAT_010eb2c4;
    MemoryRouter* router = reinterpret_cast<MemoryRouter*>(FUN_00c85750());
    int count = m_secondCount;
    MemoryAllocator* allocator = router->m_allocator;
    FUN_00c905b0_Class** items = m_secondItems;
    int i = 0;
    while (i < count) {
        FUN_00c905b0_Class* current = items[i];
        if(current)
            current->FUN_00c905b0();
        items[i] = 0;
        ++i;
    }
    m_secondCount = 0;
    int capacity = m_secondCapacity;
    if((capacity & 0x80000000) == 0)
        allocator->Free(m_secondItems, (capacity & 0x3fffffff) * sizeof(FUN_00c905b0_Class*));
    m_secondItems = 0;
    m_secondCapacity = 0x80000000;
    router = reinterpret_cast<MemoryRouter*>(FUN_00c85750());
    int count2 = m_firstCount;
    allocator = router->m_allocator;
    FUN_00c905b0_Class** items2 = m_firstItems;
    i=0;
    while(i<count2) {
        FUN_00c905b0_Class* current=items2[i];
        if(current)
            current->FUN_00c905b0();
        items2[i]=0;
        ++i;
    }
    m_firstCount=0;
    int capacity2=m_firstCapacity;
    if((capacity2 & 0x80000000) == 0)
        allocator->Free(m_firstItems, (capacity2 & 0x3fffffff)*sizeof(FUN_00c905b0_Class*));
    m_firstItems=0;
    m_firstCapacity=0x80000000;
    m_handle.FUN_00cb0c00();
    m_vtable=&DAT_0102e388;
}