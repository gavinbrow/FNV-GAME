struct S_00a0c9f0_Node {
    S_00a0c9f0_Node* m_pkNext;
    S_00a0c9f0_Node* m_pkPrev;
    int m_val;
};

struct S_00a0c9f0_Pool {
    int m_uiCount;
    S_00a0c9f0_Node* FUN_0043a010();
};

class S_00a0c9f0 {
    S_00a0c9f0_Node* m_pkHead;
    S_00a0c9f0_Node* m_pkTail;
    S_00a0c9f0_Pool m_pool;

public:
    void __thiscall FUN_00a0c9f0(int* pValue);
};

void __thiscall S_00a0c9f0::FUN_00a0c9f0(int* pValue) {
    volatile int dummy_frame[7]; 
    S_00a0c9f0_Node* pNode = m_pool.FUN_0043a010();
    pNode->m_val = *pValue;
    pNode->m_pkPrev = 0;
    pNode->m_pkNext = m_pkHead;

    if (m_pkHead) {
        m_pkHead->m_pkPrev = pNode;
    } else {
        m_pkTail = pNode;
    }

    m_pkHead = pNode;
    m_pool.m_uiCount++;
    (void)dummy_frame;
}