extern int DAT_0108febc;
extern int DAT_010c8b0c;
extern int DAT_01268188;
extern int DAT_01268648;

struct PhysicsAllocator {
    static void* __cdecl operator new(unsigned int size);
};

struct PhysicsReference {
    void* m_pVtable;
    unsigned int m_uiRefCount;
    unsigned int m_uiFlags;
    PhysicsReference();
};

struct PhysicsObject : PhysicsAllocator, PhysicsReference {
    unsigned int m_uiData;

    PhysicsObject() : PhysicsReference()
    {
        unsigned int count = 1;
        m_pVtable = &DAT_0108febc;
        m_uiData = 0;
        DAT_01268188 += count;
        m_pVtable = &DAT_010c8b0c;
        DAT_01268648 += count;
    }
};

PhysicsObject* __cdecl FUN_00cc9700()
{
    return new PhysicsObject;
}
