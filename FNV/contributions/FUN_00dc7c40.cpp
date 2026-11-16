extern int DAT_010d6ee4;

struct Mem_dc7c {
    virtual void v00();
    virtual void* blockAlloc(int nbytes) throw();
};
struct Router_dc7c {
    int unk00, unk04, unk08, unk0C;
    Mem_dc7c* m_heap;
    Mem_dc7c& heap() { return *m_heap; }
    static Router_dc7c& __cdecl FUN_00c85750() throw();
};

struct RefCounted_dc7c {
    int* m_vtbl;
    unsigned short m_memSizeAndFlags;
    unsigned short m_flags;
    int m_referenceCount;
    void addReference() { ++m_referenceCount; }
};

struct Node_dc7c : RefCounted_dc7c {
    RefCounted_dc7c* m_parent;
    void* volatile m_data;
    int m_size;
    int m_capacityAndFlags;
    static void* operator new(unsigned int nbytes) throw()
    {
        Node_dc7c* p = (Node_dc7c*)Router_dc7c::FUN_00c85750().heap().blockAlloc(nbytes);
        p->m_memSizeAndFlags = (unsigned short)nbytes;
        return p;
    }
    Node_dc7c(RefCounted_dc7c* parent) throw()
    {
        m_flags = 0;
        m_referenceCount = 0;
        m_vtbl = &DAT_010d6ee4;
        if (parent)
            parent->addReference();
        m_parent = parent;
        m_data = 0;
        m_size = 0;
        m_capacityAndFlags = 0x80000000;
    }
    const char* getName() { return ((const char* (__thiscall*)(Node_dc7c*))((void**)m_vtbl)[2])(this); }
};

struct NameView_dc7c {
    virtual void slot0();
    virtual void slot1();
    virtual const char* getName();
};
struct NameMap_dc7c {
    void FUN_00dc9ec0(const char* name, Node_dc7c** value);
};

struct Registry_dc7c {
    int unk00, unk04, unk08, unk0C, unk10, unk14, unk18, unk1C, unk20, unk24, unk28;
    Node_dc7c* m_first;
    NameMap_dc7c m_nodes;
};

struct Builder_dc7c {
    int unk00, unk04;
    Registry_dc7c* m_registry;
    Node_dc7c* FUN_00dc7c40(RefCounted_dc7c* const& parent);
};

Node_dc7c* Builder_dc7c::FUN_00dc7c40(RefCounted_dc7c* const& parent)
{
    Node_dc7c* node = new Node_dc7c(parent);
    node->addReference();
    Registry_dc7c* registry = m_registry;
    {
        Node_dc7c* entry;
        NameView_dc7c* view = reinterpret_cast<NameView_dc7c*>(node);
        entry = node;
        const char* name = view->getName();
        registry->m_nodes.FUN_00dc9ec0(name, &entry);
    }
    if (!registry->m_first)
        registry->m_first = node;
    return node;
}
