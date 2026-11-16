struct TableValue { int first; int second; int third; };
struct TableEntry { TableEntry* next; int key; TableValue value; };
struct HashTable {
    virtual void Reserved();
    virtual unsigned int FindBucket(int key);
    unsigned int bucketCount;
    TableEntry** buckets;
    void FUN_004b9bf0(TableEntry** iterator, int* keyOut, TableValue* valueOut);
};
void HashTable::FUN_004b9bf0(TableEntry** iterator, int* keyOut, TableValue* valueOut) {
    unsigned int bucketIndex;
    TableEntry* node = *iterator;
    *keyOut = node->key;
    *valueOut = node->value;
    if (node->next != 0) {
        *iterator = node->next;
    } else {
        bucketIndex = FindBucket(node->key);
        ++bucketIndex;
        for (; bucketIndex < bucketCount; ++bucketIndex) {
            node = buckets[bucketIndex];
            if (node != 0) {
                *iterator = node;
                return;
            }
        }
        *iterator = 0;
    }
}