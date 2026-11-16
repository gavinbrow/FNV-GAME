extern int DAT_010e56d4;
extern int DAT_0102e388;
void* __cdecl FUN_00c85750();
struct hkReferencedObject { void removeReference(); };
struct Allocator;
typedef void (__thiscall *FreeFunction)(Allocator*, void*, unsigned int);
struct AllocatorVTable { void* slot0; void* slot1; void* slot2; void* slot3; FreeFunction free; };
struct Allocator { AllocatorVTable* vtable; };
struct HolderLayout { unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c; Allocator* allocator; };
struct Owner { int* vtable; unsigned int unk04; hkReferencedObject** items; int count; int size; void FUN_00e40fd0(); };
void Owner::FUN_00e40fd0() {
    vtable = &DAT_010e56d4;
    Allocator* allocator = ((HolderLayout*)FUN_00c85750())->allocator;
    hkReferencedObject** values = items;
    int n = count;
    for (int i = 0; i < n; ++i) {
        hkReferencedObject* item = values[i];
        if (item) item->removeReference();
        values[i] = 0;
    }
    int oldSize = size;
    count = 0;
    if (oldSize & 0x80000000) {
    } else {
        allocator->vtable->free(allocator, items, (oldSize & 0x3fffffff) * 4);
    }
    items = 0;
    size = 0x80000000;
    vtable = &DAT_0102e388;
}

