struct KeyPair { unsigned int first; unsigned int second; };
struct MapEntry {
    MapEntry* next;
    int flags;
    KeyPair key;
    unsigned int value;
};

struct HashMap {
    virtual void Unknown0();
    virtual unsigned int GetBucket(unsigned int key1, unsigned int key2);
    virtual bool Equal(unsigned int key1, unsigned int key2, KeyPair other);
    virtual void InitEntry(MapEntry* entry, unsigned int key1, unsigned int key2, unsigned int value);
    virtual void Unknown4();
    virtual MapEntry* NewEntry();

    unsigned int unknown04;
    MapEntry** buckets;
    unsigned int count;

    void FUN_0084b7c0(unsigned int key1, unsigned int key2, unsigned int value);
};

void HashMap::FUN_0084b7c0(unsigned int key1, unsigned int key2, unsigned int value)
{
    unsigned int index = GetBucket(key1, key2);
    MapEntry* entry = buckets[index];
    unsigned int num = 0;
    while (entry != 0) {
        ++num;
        if (Equal(key1, key2, entry->key)) {
            entry->value = value;
            return;
        }
        entry = entry->next;
    }
    entry = NewEntry();
    InitEntry(entry, key1, key2, value);
    entry->next = buckets[index];
    buckets[index] = entry;
    ++count;
}