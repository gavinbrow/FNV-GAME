struct C6b7f20_Node {
    C6b7f20_Node* next;
    unsigned int key;
    void* value;
};
struct C6b7f20_Map {
    virtual void unknownVirtual();
    virtual unsigned int GetBucket(unsigned int key);
    unsigned int bucketCount;
    C6b7f20_Node** buckets;
    void __thiscall FUN_006b7f20(C6b7f20_Node** position, unsigned int* outKey, void** outValue);
};
void C6b7f20_Map::FUN_006b7f20(C6b7f20_Node** position, unsigned int* outKey, void** outValue)
{
    unsigned int bucket;
    {
        C6b7f20_Node* current = *position;
        *outKey = current->key;
        *outValue = current->value;
        if (current->next != 0) {
            *position = current->next;
        } else {
            bucket = GetBucket(current->key);
            ++bucket;
            for (; bucket < bucketCount; ++bucket) {
                current = buckets[bucket];
                if (current != 0) {
                    *position = current;
                    return;
                }
            }
            *position = 0;
        }
    }
}