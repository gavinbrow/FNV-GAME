struct S_Cfca40_AdjustedSource {
    void* m_type;
    void* m_owner;
    void* m_data;
    void* m_context;
    signed char m_offset;
    void* GetAdjustedData() {
        return reinterpret_cast<char*>(this) + m_offset;
    }
};
struct S_Cfca40_Manager {
    virtual void Deallocate();
    virtual void* Allocate(unsigned int bytes);
};
struct S_Cfca40_Router {
    void* m_allocatorState;
    void* m_parent;
    void* m_reserved;
    void* m_context;
    S_Cfca40_Manager* m_manager;
    S_Cfca40_Manager& heap() { return *m_manager; }
};
S_Cfca40_Router* FUN_00c85750();
struct S_Cfca40_Element {
    void* m_vtable;
    unsigned short m_allocatedBytes;
    void FUN_00cfc5a0(void* context, void* first, void* second);
};
struct S_Cfca40_Factory {
    void* m_type;
    unsigned short m_reserved;
    unsigned short m_flags;
    void* m_context;
    void FUN_00cfca40(S_Cfca40_AdjustedSource* first,
                        S_Cfca40_AdjustedSource* second,
                        S_Cfca40_AdjustedSource* unused);
};
void S_Cfca40_Factory::FUN_00cfca40(
    S_Cfca40_AdjustedSource* first,
    S_Cfca40_AdjustedSource* second,
    S_Cfca40_AdjustedSource* unused) {
    void* firstData = first->GetAdjustedData();
    void* secondData = second->GetAdjustedData();
    S_Cfca40_Element* obj = static_cast<S_Cfca40_Element*>(
        FUN_00c85750()->heap().Allocate(28));
    obj->m_allocatedBytes = 28;
    obj->FUN_00cfc5a0(m_context, firstData, secondData);
}
