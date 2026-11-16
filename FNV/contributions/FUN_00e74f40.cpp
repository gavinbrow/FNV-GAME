class RObj74 { public:
    virtual ~RObj74();
    virtual void DeleteThis();
    long m_uiRefCount;
    void IncRefCount() { InterlockedIncrement(&m_uiRefCount); }
    void DecRefCount() { if (InterlockedDecrement(&m_uiRefCount) == 0) DeleteThis(); }
};
class RPtr74 { public:
    RObj74* m_p;
    RPtr74(const RPtr74& o) : m_p(o.m_p) { if (m_p) m_p->IncRefCount(); }
    ~RPtr74() { if (m_p) m_p->DecRefCount(); }
};
struct Node74 { Node74* next; Node74* prev; RPtr74 elem; };
struct List74 {
    Node74* head; Node74* tail; unsigned int count;
    void FUN_00e6e830(Node74* p) throw();
    void RemoveHead() {
        Node74* n = head;
        head = n->next;
        if (head) head->prev = 0; else tail = 0;
        RPtr74 e = n->elem;
        FUN_00e6e830(n);
        count--;
    }
    bool IsEmpty() const { return count == 0; }
    unsigned int GetSize() const { return count; }
};
struct Dev74 { virtual void v0(); virtual void v1(); virtual void v2(); virtual void v3(); virtual void v4(); virtual void v5(); virtual void v6(); virtual void v7(); virtual void v8(); virtual void v9();
 virtual void v10(); virtual void v11(); virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15(); virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
 virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23(); virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27(); virtual void v28(); virtual void v29();
 virtual void v30(); virtual void v31(); virtual void v32(); virtual void v33(); virtual void v34(); virtual void v35(); virtual void v36(); virtual void v37(); virtual void v38(); virtual void v39();
 virtual void v40(); virtual long __stdcall BeginScene(); };
struct Sub74 { void FUN_00e8b560(); };
class Rend74 { public:
    char pad0[0x288]; Dev74* m_pkD3DDevice9; char pad1[0x8c8-0x28c]; Sub74* m_8c8; char pad2[0x900-0x8cc]; List74 m_kList;
    bool FUN_00e74c00(); void FUN_00e74120();
    bool FUN_00e74f40();
};
bool Rend74::FUN_00e74f40()
{
    if (FUN_00e74c00()) {
        FUN_00e74120();
        m_8c8->FUN_00e8b560();
        if (m_pkD3DDevice9->BeginScene() < 0) return false;
        unsigned int remaining = reinterpret_cast<const volatile List74&>(m_kList).count;
        while (remaining) { m_kList.RemoveHead(); remaining = m_kList.count; }
    }
    return true;
}
