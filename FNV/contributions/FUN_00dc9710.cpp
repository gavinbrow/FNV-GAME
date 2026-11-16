struct FUN_00dc8e50_Class;
extern "C" void* __cdecl FUN_00c85750();
void __cdecl FUN_00c90940(void* allocator, void* array, unsigned int stride);
void __cdecl FUN_00dc88c0(void* source, void* target, int count);
struct Entry {
    int key, flags, next, previous;
};
struct EntryArray {
    Entry* data;
    int size;
    unsigned int capacityFlags;
};
struct FindResult {
    int* node;
    int index;
};
struct FUN_00dc9710_class {
    void* owner;
    void* context;
    void* extra;
    FUN_00dc8e50_Class* finder;
    EntryArray entries;
    FindResult* __thiscall FUN_00dc9710(FindResult* result, int key, int option);
};
FindResult* FUN_00dc9710_class::FUN_00dc9710(FindResult* result, int key, int option) {
    int* node = finder->FUN_00dc8e50(key);
    if (node) {
        int count = entries.size;
        for (int i = 0; i < count; ++i) {
            if (entries.data[i].key == key) {
                FUN_00dc88c0(*(void**)((char*)node + 0x10), &entries.data[i].next, 1);
                result->index = i;
                result->node = node;
                return result;
            }
        }
        EntryArray* array = &entries;
        void* allocationContext = FUN_00c85750();
        if (array->size == (int)(array->capacityFlags & 0x3fffffff)) {
            FUN_00c90940(*(void**)((char*)allocationContext + 0x10), array, sizeof(Entry));
        }
        Entry* slot = array->data + array->size;
        if (slot) slot->key = 0;
        slot = array->data + array->size++;
        slot->key = key;
        slot->next = 0;
        slot->previous = 0;
        result->index = count;
        result->node = node;
        return result;
    }
    result->node = 0;
    result->index = -1;
    return result;
}