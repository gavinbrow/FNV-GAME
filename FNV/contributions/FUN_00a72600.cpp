struct SceneEntry {
    virtual void Detach(unsigned int reason);
    virtual void Unknown04();
    virtual void Unknown08();
    virtual void Unknown0C();
    virtual void Prepare(unsigned int reason);
};

struct IndexedObjects {
    void* vtable;
    SceneEntry** entries;
    unsigned short capacity;
    unsigned short count;
    unsigned short elementSize;
    unsigned short growth;
    void __thiscall FUN_00ba3aa0(unsigned int index, unsigned int* removed);
};

struct LinkedRecord {
    void* owner;
    void* object;
    void* metadata;
    void* parent;
    void* child;
    unsigned int objectIndex;
    void* cachedValue;
};

struct ObjectRegistry {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0C;
    unsigned int recordCount;
    LinkedRecord* records;
    void* unk18;
    IndexedObjects indexedObjects;

    bool __thiscall FUN_00a72600(unsigned int index, bool clearReferences);
};

bool __thiscall ObjectRegistry::FUN_00a72600(unsigned int index, bool clearReferences)
{
    SceneEntry* object = index < indexedObjects.count
        ? indexedObjects.entries[index] : 0;
    if (!object)
        return false;

    object->Prepare(0);
    object->Detach(1);

    unsigned int removed = 0;
    indexedObjects.FUN_00ba3aa0(index, &removed);

    if (clearReferences) {
        for (unsigned int i = 0; i < recordCount; ++i) {
            LinkedRecord* record = &records[i];
            if (index == record->objectIndex &&
                i < recordCount && records) {
                record->object = 0;
                record->parent = 0;
                record->metadata = 0;
                record->child = 0;
                record->objectIndex = 0;
                record->cachedValue = 0;
            }
        }
    }
    return true;
}