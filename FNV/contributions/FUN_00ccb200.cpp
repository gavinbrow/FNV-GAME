extern int DAT_01030bf4;
extern int DAT_010ca5c4;
extern int DAT_010ca4dc;
extern int DAT_012680f8;
extern int DAT_01268f8c;
extern int DAT_0126866c;

struct AllocationBase {
    static void* __cdecl operator new(unsigned int size);
};

struct S_00c87c30_Base {
    void* m_pVtable;
    unsigned int m_uiRefCount;
    unsigned int m_uiFlags;
    unsigned int m_uiData1;
    unsigned int m_uiData2;
    S_00c87c30_Base();
};

struct TargetObject : AllocationBase, S_00c87c30_Base {
    TargetObject() : S_00c87c30_Base() {
        m_pVtable = &DAT_01030bf4;
        unsigned int count = 1;
        m_uiData1 = 0;
        m_uiData2 = 0;
        DAT_012680f8 += count;
        m_pVtable = &DAT_010ca5c4;
        DAT_01268f8c += count;
        m_pVtable = &DAT_010ca4dc;
        DAT_0126866c += count;
    }
};

TargetObject* __cdecl FUN_00ccb200() {
    return new TargetObject();
}