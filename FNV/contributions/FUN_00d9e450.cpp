struct Record { void* first; void* second; void* third; };
struct RecordArray { Record* data; unsigned int count; unsigned int capacity; };
struct MemoryManager { int unk00; int unk04; int unk08; int unk0C; void* allocator; };
struct FUN_00d9e450_class {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14;
    int unk18; int unk1C; int unk20; int unk24; int unk28;
    RecordArray records;
    void FUN_00d9e450(void* first, void* second, void* third);
};
MemoryManager* __cdecl FUN_00885750();
void __cdecl FUN_00890940(void* allocator, RecordArray* array, unsigned int elementSize);
void FUN_00d9e450_class::FUN_00d9e450(void* first, void* second, void* third) {
    RecordArray* array = &records;
    MemoryManager* manager = FUN_00885750();
    if (array->count == (array->capacity & 0x3fffffff))
        FUN_00890940(manager->allocator, array, sizeof(Record));
    unsigned int index = array->count;
    Record* data = array->data;
    Record* slot = data + index;
    array->count = index + 1;
    slot->first = first;
    slot->second = second;
    slot->third = third;
}
