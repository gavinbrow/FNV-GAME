
struct FnvScopedContext {
    int previousContext;
    int currentContext;
    FnvScopedContext();
    ~FnvScopedContext();
};
struct FnvModelElement {
    unsigned short __thiscall FUN_00669990();
};
struct FnvModelReference {
    FnvModelElement* __thiscall FUN_00559450();
};
struct FnvObjectSlot {
    void* m_object;
    void* __thiscall FUN_00559450();
    void __thiscall FUN_0066b0d0(int type);
};
struct FnvElementCollection : S_0066b6c0_Base {
    FnvModelReference m_model;
    FnvObjectSlot* m_slots;
    bool __thiscall FUN_0066b8b0(unsigned short index, int type);
};
typedef S_0066ba30_Node* (__thiscall *FnvNodeGetter)(FnvElementCollection*);
bool __thiscall FnvElementCollection::FUN_0066b8b0(unsigned short index, int type) {
    FnvScopedContext guard;
    if (!m_model.FUN_00559450() || !m_slots || !type) return false;
    unsigned short maxIndex = m_model.FUN_00559450()->FUN_00669990();
    if (index >= maxIndex)
        return false;
    S_0066ba30_Node* actor = reinterpret_cast<FnvNodeGetter>(reinterpret_cast<FUN_0066bf80_vftable*>(*reinterpret_cast<void**>(this))->slot104)(this);
    if (!actor)
        return false;
    if (m_slots[index].FUN_00559450()) {
        actor->ClearObj(reinterpret_cast<S_0066ba30_Obj*>(m_slots[index].FUN_00559450()));
    }
    actor->SetObj(reinterpret_cast<S_0066ba30_Obj*>(type), true);
    m_slots[index].FUN_0066b0d0(type);
    return true;
}