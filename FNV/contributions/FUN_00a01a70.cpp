struct MapIterator_00a0c850 {
    void** m_vtable;
    unsigned int m_uiHashSize;
    BSMapItem<unsigned long, ScrapHeap*>** m_ppkHashTable;
    void FUN_00a0c850(void** position, ScrapHeap** value, unsigned int* key) {
        typedef BSMapItem<unsigned long, ScrapHeap*> Entry;
        Entry* current = (Entry*)*position;
        *key = current->m_key;
        *value = current->m_val;
        *position = current->m_pkNext;
        if (*position != 0) return;
        unsigned int bucket = ((BSMapBase<unsigned long, ScrapHeap*>*)this)->KeyToHashIndex(*key);
        for (++bucket; bucket < m_uiHashSize; ++bucket) {
            if (m_ppkHashTable[bucket] != 0) {
                *position = m_ppkHashTable[bucket];
                break;
            }
        }
    }
};
__forceinline BSMapItem<unsigned long, ScrapHeap*>* FindFirstHeapEntry(
    BSMapBase<unsigned long, ScrapHeap*>& map)
{
    unsigned int bucketIndex = 0;
    for (; bucketIndex < map.m_uiHashSize; ++bucketIndex) {
        if (map.m_ppkHashTable[bucketIndex] != 0)
            return map.m_ppkHashTable[bucketIndex];
    }
    return 0;
}
ScrapHeap* __cdecl FUN_00a01a70(unsigned int requestedKey) {
    ScrapHeap* result;
    unsigned int key;
    void* position = FindFirstHeapEntry(DAT_011f32f4);
    while (position) {
        ((MapIterator_00a0c850*)&DAT_011f32f4)->FUN_00a0c850(&position, &result, &key);
        if (key == requestedKey) return result;
    }
    return 0;
}