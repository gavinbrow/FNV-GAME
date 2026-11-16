struct FUN_00cbadb0_Dispatch {
    virtual void v0();
    virtual void v1();
    virtual void releaseItem(void* item);
};
struct FUN_00cbadb0_Obj {
    virtual void v0();
    virtual void v1();
    virtual void releaseItem(void* item);
    virtual ~FUN_00cbadb0_Obj();

    void* m_items;
    unsigned int m_count;
    unsigned int m_capacity;

    void FUN_00cba0d0(void* items, unsigned int count);
};
FUN_00cbadb0_Obj::~FUN_00cbadb0_Obj() {
    if (m_items) {
        FUN_00cba0d0(m_items, m_count);
        reinterpret_cast<FUN_00cbadb0_Dispatch*>(this)->releaseItem(m_items);
        m_items = 0;
        m_capacity = 0;
        m_count = 0;
    }
}
