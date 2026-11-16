
inline void* __cdecl operator new(unsigned int, void* place) { return place; }
struct Entry {
    unsigned int unk00, unk04, unk08, unk0c;
    unsigned int unk10, unk14, unk18, unk1c;
    unsigned short unk20;
    unsigned short index;
    unsigned short unk24;
    unsigned char flags;
};
struct EntryArray {
    Entry** entries;
    unsigned int count;
    unsigned int capacity;
};
struct AllocatorContext {
    unsigned int unk00, unk04, unk08, unk0c;
    unsigned int allocator;
};
extern AllocatorContext* __cdecl FUN_00c85750();
extern void __cdecl FUN_00c90940(unsigned int allocator, EntryArray* list, int entrySize);

void __cdecl FUN_00cb5500(void* owner, Entry* entry) {
    unsigned char bits = entry->flags;
    if ((bits & 0x0c) == 0 && (bits & 3) != 0) {
        entry->flags = (bits & ~0x20) | 0x10;
    }
    entry->flags = (entry->flags & ~0x08) | 0x04;
    if (entry->index == 0xffff) {
        entry->index = (unsigned short)*(unsigned int*)((unsigned char*)owner + 0x44);
        EntryArray* list = (EntryArray*)((unsigned char*)owner + 0x40);
        AllocatorContext* allocator = FUN_00c85750();
        if (list->count == (list->capacity & 0x3fffffff)) {
            FUN_00c90940(allocator->allocator, list, 4);
        }
        Entry** slot = list->entries + list->count;
        __assume(slot != 0);
        new (slot) Entry*(entry);
        ++list->count;
    }
}