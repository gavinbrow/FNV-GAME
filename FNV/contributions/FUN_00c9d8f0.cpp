extern int DAT_010c6fec;
extern int DAT_01268910;

struct C9D8F0Callback {
    virtual void method0();
    virtual void method1();
    virtual void method2();
    virtual void method3(void* context, void* childShape, int flags);
};

struct C9D8F0Shape {
    void* vtable;
    int field04;
    int field08;
    int field0c;
    int field10;
    int field14;
    void* m_childShape;

    void FUN_00c90360(C9D8F0Callback* callback, void* typeInfo);
    void FUN_00c9d8f0(C9D8F0Callback* callback, int flags);
};

void C9D8F0Shape::FUN_00c9d8f0(C9D8F0Callback* callback, int flags)
{
    callback->method3(&DAT_010c6fec, m_childShape, 0);
    FUN_00c90360(callback, &DAT_01268910);
}
