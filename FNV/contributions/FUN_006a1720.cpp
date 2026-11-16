struct FUN_006a1720_Element {
    int m_0;
    int m_4;
    int m_8;
    int m_c;
};

struct FUN_006a1720_class {
    virtual void FUN_006a1720_vf0();
    virtual FUN_006a1720_Element* Allocate(unsigned int count);

    FUN_006a1720_Element* m_data;
    unsigned int m_size;
    unsigned int m_capacity;

    void FUN_0049faf0(bool free_memory);
    void FUN_009f6540(unsigned int requested, unsigned int old_size);
    void FUN_0049fc80(FUN_006a1720_Element* first, unsigned int count);
    void FUN_006a2000(FUN_006a1720_Element* first, unsigned int count);
    void FUN_006a1720(unsigned int requested, bool shrink);
};

void FUN_006a1720_class::FUN_006a1720(unsigned int requested, bool shrink)
{
    if (requested == 0) {
        FUN_0049faf0(shrink);
    } else if (requested > m_capacity) {
        if (m_capacity == 0) {
            m_data = Allocate(requested);
            m_capacity = requested;
        } else {
            FUN_009f6540(requested, m_size);
            m_capacity = requested;
        }
        FUN_006a2000(m_data + m_size, requested - m_size);
        m_size = requested;
    } else if (requested < m_size) {
        FUN_0049fc80(m_data + requested, m_size - requested);
        m_size = requested;
        if (shrink && requested <= (m_capacity >> 2)) {
            FUN_009f6540(requested, requested);
            m_capacity = requested;
        }
    } else {
        FUN_006a2000(m_data + m_size, requested - m_size);
        m_size = requested;
    }
}