struct FnvAllocator;
struct FnvMemoryRouter {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FnvAllocator* m_heap;
};
FnvMemoryRouter* __cdecl FUN_00c85750();
struct FnvNodeValue {
    int unk00;
    int unk04;
    void* m_value;
};
struct FnvNode {
    int m_id;
    FnvNodeValue* m_keySource;
    int unk08;
    int unk0c;
    void* m_context;
    int m_flags;
};
struct FnvEntry {
    int m_id;
    struct FnvRefCounted* m_object;
};
struct FnvEntries {
    FnvEntry* m_data;
    int m_size;
    int m_capacity;
};
void __cdecl FUN_00c90940(FnvAllocator*, FnvEntries*, unsigned int);
struct FnvStringMaker {
    void* FUN_00d87800(void* value, int flags);
};
struct FnvCreatorResult {
    int unk00;
    int unk04;
    FnvStringMaker* m_maker;
};
struct FnvManager {
    virtual void vf00();
    virtual FnvCreatorResult* GetCreator();
};
struct FnvRefCounted {
    int unk00;
    int unk04;
    int m_refs;
};
FnvRefCounted* __cdecl FUN_00dc7de0(void* context, void* key, int flags);
struct FnvObjectHolder {
    int unk00;
    int unk04;
    int unk08;
    FnvEntries m_entries;
    FnvManager* m_manager;
    int FUN_00dc9c20(FnvNode* node);
};
int FnvObjectHolder::FUN_00dc9c20(FnvNode* node)
{
    if (!node->m_context)
        return -1;

    FnvEntries* entries = &m_entries;
    FnvMemoryRouter* router = FUN_00c85750();
    if (entries->m_size == (entries->m_capacity & 0x3fffffff))
        FUN_00c90940(router->m_heap, entries, sizeof(FnvEntry));

    FnvEntry* entry = entries->m_data + entries->m_size;
    if (entry)
        entry->m_id = 0;
    entry = entries->m_data + entries->m_size++;
    entry->m_id = node->m_id;

    FnvManager* manager = m_manager;
    FnvNodeValue* source = node->m_keySource;
    void* original = source->m_value;
    FnvStringMaker* maker = manager->GetCreator()->m_maker;
    void* key = original ? maker->FUN_00d87800(original, 0) : 0;
    void* context = node->m_context;
    FnvRefCounted* created = FUN_00dc7de0(context, key, node->m_flags);
    entry->m_object = created;
    ++created->m_refs;
    return m_entries.m_size - 1;
}
