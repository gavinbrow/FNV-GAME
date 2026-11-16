extern int DAT_010c7310;
struct ChildLayout;
typedef void (__thiscall ChildLayout::*ReleaseFunction)(void*);
extern ReleaseFunction DAT_010c7318;
struct BaseState {
    virtual ~BaseState() {}
};
struct ChildLayout {
    void* m_vptr;
    void* m_4;
    int m_8;
    int m_c;
    ~ChildLayout() {
        m_vptr = &DAT_010c7310;
        if (m_4 != 0) {
            (this->*DAT_010c7318)(m_4);
            m_4 = 0;
            m_c = 0;
            m_8 = 0;
        }
    }
};
struct FUN_00ca2140 : BaseState {
    ChildLayout child;
    ~FUN_00ca2140();
};
FUN_00ca2140::~FUN_00ca2140()
{
    ((FUN_00ca20e0_Class*)this)->FUN_00ca20e0();
}