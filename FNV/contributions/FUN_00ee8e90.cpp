#include <windows.h>
struct RefObject {
    virtual void V0();
    virtual void Destroy();
    volatile LONG refs;
};
struct Node {
    Node* next;
    unsigned int key;
    RefObject* value;
};
struct Map {
    int unk00;
    unsigned int bucketCount;
    Node** buckets;
    bool FUN_00ee8e90(unsigned int*, RefObject**);
};
bool Map::FUN_00ee8e90(unsigned int* key, RefObject** out)
{
    unsigned int value = *key;
    Node* node = buckets[value % bucketCount];
    while (node && value != node->key)
        node = node->next;
    if (!node)
        return false;
    RefObject* oldValue = *out;
    if (oldValue != node->value) {
        if (oldValue && InterlockedDecrement(&oldValue->refs) == 0)
            oldValue->Destroy();
        RefObject* newValue = node->value;
        *out = newValue;
        if (newValue)
            InterlockedIncrement(&newValue->refs);
    }
    return true;
}

