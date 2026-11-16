struct FUN_00caba90_array {
    void* data;
    unsigned int count;
    unsigned int capacity;
};
struct FUN_006212c0_shell {
    void* FUN_006212c0(void* source);
};
void* __cdecl FUN_00c85750();
void __cdecl FUN_00c90940(void* manager, void* array, int itemSize);
struct FUN_00caba90_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00caba90_array array;
    void* FUN_00caba90(void* source);
};
void* FUN_00caba90_Class::FUN_00caba90(void* source) {
    FUN_00caba90_array* items = &array;
    void* manager = FUN_00c85750();
    if (items->count == (items->capacity & 0x3fffffff)) {
        void* allocator = *(void**)((char*)manager + 0x10);
        FUN_00c90940(allocator, items, 0x70);
    }
    unsigned int index = items->count;
    char* item = (char*)items->data + index * 0x70;
    items->count = index + 1;
    return ((FUN_006212c0_shell*)item)->FUN_006212c0(source);
}
