struct ObjectRef { void FUN_00c90510(); void FUN_00c905b0(); };
extern __declspec(thread) int g_threadFlag;
struct ThreadFlagGuard {
    int previousFlag;
    ThreadFlagGuard() : previousFlag(g_threadFlag) { g_threadFlag = 16; }
    ~ThreadFlagGuard() { g_threadFlag = previousFlag; }
};
struct FUN_00ca9b40_class {
    void** m_pVTable;
    short m_uFlags;
    short m_uCount;
    int m_extraneousState;
    ObjectRef* m_pObject;
    void FUN_00ca9b40(ObjectRef* pObject);
};
void FUN_00ca9b40_class::FUN_00ca9b40(ObjectRef* pObject) {
    ThreadFlagGuard guard;
    if (pObject) pObject->FUN_00c90510();
    if (m_pObject) m_pObject->FUN_00c905b0();
    m_pObject = pObject;
}