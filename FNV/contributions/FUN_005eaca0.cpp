
struct VirtualListItem {
    virtual void v00();
    virtual void v01();
    virtual void v02();
    virtual ~VirtualListItem();
};
struct ListCleanup { void FUN_00470470(); };
struct ConditionCleanup { void FUN_00680fe0(); };
void FUN_005eabb0::FUN_005eaca0() {
    const ConditionList_t* cursor = reinterpret_cast<const ConditionList_t*>(&m_list);
    while (cursor != 0) {
        delete reinterpret_cast<VirtualListItem*>(*cursor->FUN_006815c0());
        cursor = cursor->FUN_00726070();
    }
    reinterpret_cast<ListCleanup*>(&m_list)->FUN_00470470();
    reinterpret_cast<ConditionCleanup*>(&m_condition)->FUN_00680fe0();
}
