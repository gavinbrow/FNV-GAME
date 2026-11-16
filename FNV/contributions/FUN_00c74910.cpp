struct MapEntry {
    MapEntry* next;
    unsigned int key;
    unsigned short value;
};

struct MapTable {
    virtual void Destroy();
    virtual unsigned int Hash(unsigned int key);
    virtual bool Equal(unsigned int lhs, unsigned int rhs);
    virtual void Initialize(MapEntry* entry, unsigned int key, unsigned int value);
    virtual void OnResize();
    virtual MapEntry* AllocateEntry();

    unsigned int bucketCount;
    MapEntry** buckets;
    unsigned int count;

    void FUN_00c74910(unsigned int key, unsigned int value);
};

void MapTable::FUN_00c74910(unsigned int key, unsigned int value)
{
    unsigned int bucket = Hash(key);
    MapEntry* entry = buckets[bucket];
    while (entry) {
        if (Equal(key, entry->key)) {
            entry->value = (unsigned short)value;
            return;
        }
        entry = entry->next;
    }

    MapEntry* newEntry = AllocateEntry();
    Initialize(newEntry, key, value);
    newEntry->next = buckets[bucket];
    buckets[bucket] = newEntry;
    ++count;
}