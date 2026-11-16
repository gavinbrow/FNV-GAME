struct HashNode {
    HashNode* next;
    unsigned int key;
    unsigned int value;
};
struct HashTable {
    virtual void Reserved0() = 0;
    virtual unsigned int BucketIndex(unsigned int key) = 0;
    virtual bool EqualKey(unsigned int key, unsigned int existingKey) = 0;
    virtual void Initialize(HashNode* entry, unsigned int key, unsigned int value) = 0;
    virtual void Reserved4() = 0;
    virtual HashNode* AllocateNode() = 0;

    unsigned int tableSize;
    HashNode** buckets;
    unsigned int elementCount;
    void FUN_00b57ea0(unsigned int key, unsigned int value);
};
void HashTable::FUN_00b57ea0(unsigned int key, unsigned int value)
{
    unsigned int bucketIndex = BucketIndex(key);
    HashNode* node = buckets[bucketIndex];
    while (node) {
        if (EqualKey(key, node->key)) {
            node->value = value;
            return;
        }
        node = node->next;
    }
    HashNode* newNode = AllocateNode();
    Initialize(newNode, key, value);
    newNode->next = buckets[bucketIndex];
    buckets[bucketIndex] = newNode;
    ++elementCount;
}