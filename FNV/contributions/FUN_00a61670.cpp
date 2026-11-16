struct HashValue_00a61670 { unsigned int unk00; unsigned int key; };
struct HashNode_00a61670 { HashValue_00a61670* value; HashNode_00a61670* next; };
struct FUN_00a61670_Map {
    HashNode_00a61670* buckets[1001];
    unsigned int count;
    HashValue_00a61670* FUN_00a61670(unsigned int key);
};
extern struct MemoryManager g_memoryManager;
HashValue_00a61670* FUN_00a61670_Map::FUN_00a61670(unsigned int key) {
    unsigned int index = (key >> 4) % 1001;
    HashValue_00a61670* result = 0;
    HashNode_00a61670* current = buckets[index];
    HashNode_00a61670* previous = 0;
    if (current != 0) {
        do {
            if (current->value->key == key) {
                if (previous != 0) previous->next = current->next;
                else buckets[index] = current->next;
                HashValue_00a61670* value = current->value;
                --count;
                g_memoryManager.Deallocate(current);
                value->key = 0;
                result = value;
                break;
            }
            previous = current;
            current = current->next;
        } while (current != 0);
    }
    return result;
}