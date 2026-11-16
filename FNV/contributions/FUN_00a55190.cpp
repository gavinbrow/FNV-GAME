struct MemoryAllocator {
    void FUN_00aa4060(void* object);
};
extern MemoryAllocator g_011f6238;
extern "C" void __cdecl FUN_00aa10f0(void* object);
extern "C" long __declspec(dllimport) __stdcall InterlockedDecrement(volatile long* addend);

struct RefCounter {
    virtual void Keep();
    virtual void Release();
    volatile long count;
};

struct FirstEntry {
    void* allocation;
};

struct NestedEntry {
    void* object;
    RefCounter* reference;
};
struct EntryGroup {
    NestedEntry** objects;
    unsigned int reserved;
    unsigned int count;
};

struct FUN_00a55190_owner {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    FirstEntry** smallEntries;
    unsigned short unk44;
    unsigned short smallCount;
    unsigned short smallCapacity;
    unsigned short unk4a;
    unsigned int unk4c;
    EntryGroup** largeEntries;
    unsigned short unk54;
    unsigned short largeCount;
    unsigned short largeCapacity;
    unsigned short unk5a;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int current;

    void FUN_00a55190();
};

void FUN_00a55190_owner::FUN_00a55190() {
    for (unsigned int i = 0; i < smallCount; ++i) {
        FirstEntry* entry = smallEntries[i];
        if (entry) {
            FUN_00aa10f0(entry->allocation);
            g_011f6238.FUN_00aa4060(entry);
        }
    }
    for (unsigned short i = 0; i < smallCount; ++i)
        smallEntries[i] = 0;
    smallCount = 0;
    smallCapacity = 0;

    for (unsigned int i = 0; i < largeCount; ++i) {
        EntryGroup* group = largeEntries[i];
        if (group) {
            for (unsigned int j = 0; j < group->count; ++j) {
                NestedEntry* object = group->objects[j];
                if (object) {
                    RefCounter* reference = object->reference;
                    if (reference && InterlockedDecrement(&reference->count) == 0)
                        reference->Release();
                    g_011f6238.FUN_00aa4060(object);
                }
            }
            FUN_00aa10f0(group->objects);
            g_011f6238.FUN_00aa4060(group);
        }
    }
    for (unsigned short i = 0; i < largeCount; ++i)
        largeEntries[i] = 0;
    largeCount = 0;
    largeCapacity = 0;
    *(volatile unsigned int*)&current = 0;
}