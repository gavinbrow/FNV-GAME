
struct FNV_MapKey { int value; FNV_MapKey(const FNV_MapKey&); ~FNV_MapKey(); void FUN_006e5cc0(FNV_MapKey*); };
struct FNV_MapNode { FNV_MapNode* next; int id; FNV_MapKey key; };
struct FNV_HashMap {
    virtual void Reserved(); virtual int Hash(int id); virtual bool Equals(int id,int existing);
    virtual void Init(FNV_MapNode* node,int id,FNV_MapKey key);
    unsigned int unk04; FNV_MapNode** buckets; int count; bool keepExisting;
    FNV_MapNode* FUN_006c63e0(); void FUN_00658950(int id,FNV_MapKey key);
};
void FNV_HashMap::FUN_00658950(int id, FNV_MapKey key) {
    int bucketIndex = Hash(id);
    FNV_MapNode* node = buckets[bucketIndex];
    int probeCount = 0;
    while (node) {
        ++probeCount;
        if (Equals(id,node->id)) {
            if (!keepExisting) node->id = id;
            node->key.FUN_006e5cc0(&key);
            return;
        }
        node = node->next;
    }
    node = FUN_006c63e0();
    Init(node,id,key);
    node->next = buckets[bucketIndex];
    buckets[bucketIndex] = node;
    ++count;
}