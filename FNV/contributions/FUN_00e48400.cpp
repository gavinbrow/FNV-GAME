extern int DAT_010cb76c;
extern int DAT_010cb780;
extern int DAT_010e83b4;

struct SourceData {
    void* m_vtable;
    unsigned short m_unknown04,m_flags;
    unsigned char m_state,m_unknown09,m_unknown0a,m_unknown0b;
    float m_first,m_second;
    int m_third,m_fourth,m_fifth,m_sixth,m_seventh;
};
struct FUN_00e48400 {
    int* m_vtable;
    unsigned short m_unknown04,m_flags;
    unsigned char m_state,m_unknown09,m_unknown0a,m_unknown0b;
    float m_first,m_second;
    int m_third,m_fourth,m_fifth,m_sixth,m_seventh;
    FUN_00e48400(const SourceData* source);
};
FUN_00e48400::FUN_00e48400(const SourceData* source) {
    m_vtable = &DAT_010cb76c;
    m_flags = 1;

    unsigned char state = source->m_state;
    *reinterpret_cast<int* volatile*>(&m_vtable) = &DAT_010cb780;
    m_state = state;

    m_first = source->m_first;
    m_second = source->m_second;
    m_vtable = &DAT_010e83b4;

    m_third = source->m_third;
    m_fourth = source->m_fourth;
    m_fifth = source->m_fifth;
    m_sixth = source->m_sixth;
    m_seventh = source->m_seventh;
}
