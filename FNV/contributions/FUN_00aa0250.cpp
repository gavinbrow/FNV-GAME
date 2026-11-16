struct HashNode { HashNode* next; unsigned int key; };
class HashTable {
public:
    virtual void unknown0();
    virtual void unknown1();
    virtual void destroy(HashNode* node);
    unsigned int bucketCount;
    HashNode** buckets;
    unsigned int count;
    bool FUN_00aa0250(const unsigned int* key);
};
bool HashTable::FUN_00aa0250(const unsigned int* key) {
    unsigned int value = *key;
    HashNode** link = &buckets[value % bucketCount];
    HashNode* node = *link;
    if (node != 0) {
        if (value == node->key) {
            *link = node->next;
            destroy(node);
            --count;
            return true;
        }
        link = &node->next;
        for (node = node->next; node != 0; node = node->next) {
            if (value == node->key) {
                *link = node->next;
                destroy(node);
                --count;
                return true;
            }
            link = &node->next;
        }
    }
    return false;
}
