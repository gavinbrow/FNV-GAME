extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(thread) int g_memoryContext;

struct MemoryContextScope {
    int previousContext;
    MemoryContextScope() {
        previousContext = g_memoryContext;
        g_memoryContext = 16;
    }
    ~MemoryContextScope() {
        g_memoryContext = previousContext;
    }
};

struct RefCountedEntry {
    virtual void UnusedVirtual();
    virtual void Release();
    volatile long referenceCount;
};

struct Record {
    int firstField;
    int secondField;
    RefCountedEntry* referencedObject;
};

struct CollectionSlot {
    Record* record;
    int key;
    int status;
    int extra;
};

struct IndexedRecords {
    virtual void FirstVirtual();
    virtual unsigned int GetSize();
    int capacity;
    CollectionSlot* entries;
};

struct RecordCollection {
    int header0;
    int header4;
    int header8;
    int headerC;
    IndexedRecords items;
};

struct CollectionHolderLayout {
    int state;
    int reserved;
    RecordCollection* collection;
};

void H_00c8c810::FUN_00c8b310() {
    MemoryContextScope memoryContext;
    CollectionHolderLayout* holder = reinterpret_cast<CollectionHolderLayout*>(this);

    if (this != 0) {
        RecordCollection* records = holder->collection;
        if (records != 0) {
            unsigned int count = records->items.GetSize();
            if (count != 0) {
                unsigned int offset = count << 4;
                do {
                    --count;
                    offset -= 16;
                    if (holder->collection != 0) {
                        Record* record = *reinterpret_cast<Record**>(
                            reinterpret_cast<unsigned char*>(holder->collection->items.entries) + offset);
                        if (record != 0) {
                            RefCountedEntry* reference = record->referencedObject;
                            if (reference != 0 &&
                                InterlockedDecrement(&reference->referenceCount) == 0) {
                                reference->Release();
                            }
                        }
                    }
                } while (count != 0);
            }
        }
    }
}