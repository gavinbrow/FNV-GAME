
struct RefAgent { void __thiscall FUN_00c905b0(); };
struct Allocator {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0C();
    virtual void Deallocate(void* data, unsigned int size);
};
struct AllocatorManager {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0C;
    Allocator* allocator;
};
AllocatorManager* __cdecl FUN_00c85750();
struct FUN_00dcecc0 {
    virtual ~FUN_00dcecc0();
    unsigned short m_memSizeAndFlags;
    short m_referenceCount;
    hkArray<void*> m_rigidBodies;
    hkArray<hkpConstraintInstance*> m_constraints;
    hkArray<hkpAction*> m_actions;
    hkArray<hkpPhantom*> m_phantoms;
    char* m_name;
    unsigned int m_userData;
    unsigned int m_activeFlags;
    hkArray<hkpSerializedAgentNnEntry*> m_contacts;
    void __thiscall FUN_00d06640();
};
FUN_00dcecc0::~FUN_00dcecc0() {
    int count = m_contacts.m_size;
    for (int i = 0; i < count; ++i) {
        reinterpret_cast<RefAgent*>(m_contacts.m_data[i])->FUN_00c905b0();
    }
    AllocatorManager* manager = FUN_00c85750();
    Allocator* allocator = manager->allocator;
    unsigned int flags = m_contacts.m_capacityAndFlags;
    m_contacts.m_size = 0;
    if (!(flags & 0x80000000u)) {
        allocator->Deallocate(m_contacts.m_data, 4 * (flags & 0x3fffffffu));
    }
    m_contacts.m_data = 0;
    m_contacts.m_capacityAndFlags = 0x80000000;
    FUN_00d06640();
}
