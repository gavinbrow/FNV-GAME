struct FNV_ValuePair { unsigned int data1; unsigned int data2; };
struct FNV_MapEntry {
    FNV_MapEntry* next;
    unsigned int key;
    FNV_ValuePair data;
};

class FNV_BucketMap {
public:
    virtual void OnDestroy();
    virtual unsigned int GetBucket(unsigned int key);
    virtual bool IsEqual(unsigned int key, unsigned int entryKey);
    virtual void InitializeEntry(FNV_MapEntry* entry, unsigned int key, FNV_ValuePair value);
    virtual void ReservedSlot();
    virtual FNV_MapEntry* NewEntry();

    unsigned int bucketCount;
    FNV_MapEntry** buckets;
    unsigned int entryCount;

    void FUN_00844310(unsigned int key, FNV_ValuePair value);
};

void FNV_BucketMap::FUN_00844310(unsigned int key, FNV_ValuePair value)
{
    unsigned int bucketIndex = GetBucket(key);
    FNV_MapEntry* entry = buckets[bucketIndex];
    unsigned int visited = 0;
    while (entry) {
        ++visited;
        if (IsEqual(key, entry->key)) {
            entry->data = value;
            return;
        }
        entry = entry->next;
    }
    entry = NewEntry();
    InitializeEntry(entry, key, value);
    entry->next = buckets[bucketIndex];
    buckets[bucketIndex] = entry;
    entryCount += 1;
}