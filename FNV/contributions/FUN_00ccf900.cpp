struct Link {
    void* m_type;
    unsigned int m_flags;
    void* m_object;
};
struct RefObject {
    void** m_vtable;
    unsigned int m_flags;
    Link* m_link;
};
struct LinkCollection {
    unsigned int m_type;
    unsigned int m_flags;
    unsigned int m_capacity;
    unsigned int m_generation;
    Link** m_links;
    int m_count;
};
struct Owner {
    void** m_vtable;
    void __thiscall FUN_00c84df0(void* item, void* key);
    void __thiscall FUN_00ccf900(void* item, void* key);
};
typedef LinkCollection* (__thiscall *AcquireLinks)(Owner*, unsigned char*);
typedef bool (__thiscall *CheckRef)(RefObject*, void*);
typedef RefObject* (__thiscall *FindRef)(RefObject*, void*);
void Owner::FUN_00ccf900(void* item, void* key)
{
    unsigned char unusedFlag;
    LinkCollection* list = ((AcquireLinks)m_vtable[0xb4 / 4])(this, &unusedFlag);
    for (int index = 0; index < list->m_count; ++index) {
        Link* link = list->m_links[index];
        if (link) {
            RefObject* ref = (RefObject*)link->m_object;
            if (ref && !((CheckRef)ref->m_vtable[0xd0 / 4])(ref, key)) {
                RefObject* replacement = ((FindRef)ref->m_vtable[0x48 / 4])(ref, key);
                list->m_links[index] = replacement ? replacement->m_link : 0;
            }
        }
    }
    FUN_00c84df0(item, key);
}