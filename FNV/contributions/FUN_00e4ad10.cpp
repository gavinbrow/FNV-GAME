extern "C" int DAT_010ec1dc;
extern "C" int DAT_0102e388;
struct FNV_00e4ad10_Ref { void FUN_00c905b0(); };
struct FNV_00e4ad10_Array {
    FNV_00e4ad10_Ref** objects;
    int length;
    int capacity;
};
struct FNV_00e4ad10_Allocator {
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual void unused3();
    virtual void Free(void* allocation, unsigned int bytes);
};
struct FNV_00e4ad10_Layout {
    void* vtable;
    int unk04;
    FNV_00e4ad10_Array first;
    FNV_00e4ad10_Array second;
};
extern "C" FUN_00e4ae20_Router* __cdecl FUN_00c85750();
void FUN_00e4ae20_Object::FUN_00e4ad10() {
    FNV_00e4ad10_Layout* object = reinterpret_cast<FNV_00e4ad10_Layout*>(this);
    object->vtable = &DAT_010ec1dc;
    FNV_00e4ad10_Allocator* heap = reinterpret_cast<FNV_00e4ad10_Allocator*>(FUN_00c85750()->m_pMemoryManager);
    int count = object->second.length;
    FNV_00e4ad10_Ref** items = object->second.objects;
    for (int index = 0; index < count; index++) {
        FNV_00e4ad10_Ref* entry = items[index];
        if (entry)
            entry->FUN_00c905b0();
        items[index] = 0;
    }
    object->second.length = 0;
    int size = object->second.capacity;
    if ((size & 0x80000000u) == 0)
        heap->Free(object->second.objects, (size & 0x3fffffff) * 4);
    object->second.objects = 0;
    object->second.capacity = 0x80000000;
    heap = reinterpret_cast<FNV_00e4ad10_Allocator*>(FUN_00c85750()->m_pMemoryManager);
    count = object->first.length;
    items = object->first.objects;
    for (int index = 0; index < count; index++) {
        FNV_00e4ad10_Ref* entry = items[index];
        if (entry)
            entry->FUN_00c905b0();
        items[index] = 0;
    }
    object->first.length = 0;
    size = object->first.capacity;
    if ((size & 0x80000000u) == 0)
        heap->Free(object->first.objects, (size & 0x3fffffff) * 4);
    object->first.objects = 0;
    object->first.capacity = 0x80000000;
    object->vtable = &DAT_0102e388;
}