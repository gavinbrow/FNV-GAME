extern void* DAT_01015914[];

struct FUN_0042c760 : FUN_0040ec80_cls {
    void** m_vtable;
    unsigned char m_type;
    void* m_next;
    int m_counter;
    int m_state;

    FUN_0042c760();
};

FUN_0042c760::FUN_0042c760() {
    init(13);
    m_vtable = DAT_01015914;
    m_counter = 0;
    m_state = 0;
}
