struct VirtObj0043fb50 {
    virtual void f0();
    virtual void f1();
    virtual void f2();
    virtual void f3();
    virtual void f4();
    virtual void f5(int);
};

struct Standin0043fb50 {
    char _pad[0x18];
    VirtObj0043fb50* m_18;
    void FUN_0043fb50(int);
};

struct Host0043fb10 {
    char _pad[0x11c];
    Standin0043fb50* m_11c;
    void FUN_00c3cb70(int, int);
    void FUN_0043fb10(int a, int b);
};

extern Standin0043fb50* g_11c3b3c;

void Host0043fb10::FUN_0043fb10(int a, int b)
{
    FUN_00c3cb70(a, b);
    g_11c3b3c->FUN_0043fb50((int)m_11c);
}