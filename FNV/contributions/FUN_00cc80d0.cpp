extern int DAT_0108febc; extern int DAT_010c9e5c; extern int DAT_010c9d7c;
extern int DAT_01268188; extern int DAT_01268f74; extern int DAT_01268624;
void FUN_00c876f0(); void FUN_00c87700() throw();
void* FUN_00aa13e0(unsigned int size);
struct ThreadHeapContext { unsigned int m_allocationTag; };
extern __declspec(thread) ThreadHeapContext g_threadHeapContext;
struct PhysicsNode {
    void* m_vtable; unsigned int m_referenceCount; unsigned int m_flags; unsigned int m_data;
    void FUN_00c87c30();
    static void* operator new(unsigned int size) { return FUN_00aa13e0(size); }
    PhysicsNode() {
        FUN_00c87c30(); m_vtable = &DAT_0108febc;
        unsigned int increment = 1; m_data = 0;
        DAT_01268188 += increment; m_vtable = &DAT_010c9e5c;
        DAT_01268f74 += increment; m_vtable = &DAT_010c9d7c; DAT_01268624 += increment;
    }
};
struct AllocationScope {
    unsigned int m_previousTag;
    AllocationScope() {
        m_previousTag = g_threadHeapContext.m_allocationTag;
        g_threadHeapContext.m_allocationTag = 16;
    }
    __forceinline ~AllocationScope() throw() {
        FUN_00c87700();
        g_threadHeapContext.m_allocationTag = m_previousTag;
    }
};
struct PhysicsWorld { void FUN_00c89730(PhysicsNode*, bool); PhysicsNode* FUN_00cc80d0(bool); };
PhysicsNode* PhysicsWorld::FUN_00cc80d0(bool argument) {
    AllocationScope scope;
    FUN_00c876f0();
    PhysicsNode* node = new PhysicsNode;
    FUN_00c89730(node, argument);
    return node;
}