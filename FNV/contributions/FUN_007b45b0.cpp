struct Item {
    virtual ~Item();
};

struct NodeT {
    Item* m_item;
    ~NodeT();
};

struct FUN_007b45b0_shell {
    void* m_00;
    void* m_04;
    void* m_08;
    void* m_0c;
    void* m_10;
    void* m_14;
    void* m_18;
    void* m_1c;
    void* m_20;

    void* FUN_00559450();
    NodeT*& FUN_0057cbe0(void*& it);
    void FUN_004ed900();
    void FUN_007b45b0();
};

void FUN_007b45b0_shell::FUN_007b45b0() {
    void* it = FUN_00559450();
    while (it != 0) {
        NodeT* node = FUN_0057cbe0(it);
        delete node->m_item;
        delete node;
    }
    FUN_004ed900();
    m_20 = 0;
}
