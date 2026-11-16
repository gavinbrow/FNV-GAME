struct WeightedEntry { void* key; float weight; };
struct EntryGroup { WeightedEntry* entries; unsigned int unk04; unsigned int count; };
struct MapNode { MapNode* next; void* key; float weight; };
struct WeightedMap {
    virtual void ReservedVirtual();
    virtual unsigned int HashKey(void* key);
    virtual bool KeysEqual(void* left, void* right);
    unsigned int unk04;
    MapNode** buckets;
    void FUN_00a82050(void* key, float weight);
};
void __stdcall FUN_00a82530(WeightedMap* map, const unsigned short* groupIndices, EntryGroup* __restrict groups)
{
    for (unsigned int groupIndex = 0; groupIndex < 3; ++groupIndex) {
        EntryGroup* group = &groups[groupIndices[groupIndex]];
        unsigned int itemCount = group->count;
        for (unsigned int itemIndex = 0; itemIndex < itemCount; ++itemIndex) {
            void* key = group->entries[itemIndex].key;
            MapNode* node = map->buckets[map->HashKey(key)];
            while (node) {
                if (map->KeysEqual(key, node->key)) {
                    volatile float previousWeight = node->weight;
                    if (!(previousWeight < group->entries[itemIndex].weight)) goto nextItem;
                    break;
                }
                node = node->next;
            }
            map->FUN_00a82050(key, group->entries[itemIndex].weight);
        nextItem:;
        }
    }
}
