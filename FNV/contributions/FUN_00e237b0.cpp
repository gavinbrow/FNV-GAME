inline void* __cdecl operator new(unsigned int, void* where) { return where; }
struct FUN_00e237b0_Input {
    void* unk00; void* unk04; void* unk08; void* unk0c;
    void* unk10; void* unk14; void* unk18; void* unk1c; void* entry;
};
struct FUN_00e237b0_Allocation {
    void* unk00; void* unk04; void* unk08; void* unk0c; void* allocator;
};
struct FUN_00e237b0_List {
    void** data;
    unsigned int size;
    unsigned int capacityAndFlags;
};
extern "C" FUN_00e237b0_Allocation* __cdecl FUN_00c85750();
extern "C" void __cdecl FUN_00c90940(void*, FUN_00e237b0_List*, unsigned int);
struct FUN_00e237b0_Owner {
    void* unk00;
    FUN_00e237b0_List list;
    double FUN_00e237b0(FUN_00e237b0_Input* input);
};
double FUN_00e237b0_Owner::FUN_00e237b0(FUN_00e237b0_Input* input) {
    void* entry = input->entry;
    FUN_00e237b0_List* values = &list;
    FUN_00e237b0_Allocation* alloc = FUN_00c85750();
    if (values->size == (values->capacityAndFlags & 0x3fffffff))
        FUN_00c90940(alloc->allocator, values, 4);
    void** destination = values->data + values->size;
    __assume(destination != 0);
    new (destination) void*(entry);
    ++values->size;
    return 1.0;
}