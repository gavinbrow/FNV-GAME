#include <math.h>

struct Xf36 {
    unsigned int m_00, m_04, m_08, m_0c, m_10, m_14, m_18, m_1c, m_20;
};

struct Ps21Target {
    virtual void v00();
    virtual void v01();
    virtual void v02();
    virtual void v03();
    virtual void v04();
    virtual void v05();
    virtual void v06();
    virtual void v07();
    virtual void v08();
    virtual void v09();
    virtual void v0a();
    virtual void v0b();
    virtual void v0c();
    virtual void v0d();
    virtual void v0e();
    virtual void v0f();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v1a();
    virtual void v1b();
    virtual void v1c();
    virtual void v1d();
    virtual void v1e();
    virtual void v1f();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();
    virtual void v29();
    virtual void v2a();
    virtual void v2b();
    virtual void v2c();
    virtual void v2d();
    virtual void v2e(unsigned int a1);
    char _pad04[0x30];
    Xf36 m_34;
    unsigned int m_58;
    unsigned int m_5c;
    unsigned int m_60;
    float m_64;
};

struct Ps21Owner {
    char _pad00[0x7c];
    Ps21Target* m_7c;
};

struct Ps21Node {
    char _pad00[0x68];
    Xf36 m_68;
    unsigned int m_8c;
    unsigned int m_90;
    unsigned int m_94;
    float m_98;
    char _pad9c[0x1c];
    Ps21Owner* m_b8;

    void FUN_00c1add0(unsigned int a1);
    void FUN_00c21bf0(unsigned int a1);
};

void Ps21Node::FUN_00c21bf0(unsigned int a1) {
    FUN_00c1add0(a1);
    Ps21Owner* owner = m_b8;
    owner->m_7c->m_34 = m_68;
    Ps21Target* y = owner->m_7c;
    unsigned int* p = &y->m_58;
    *p = m_8c;
    p[1] = m_90;
    p[2] = m_94;
    float fTemp = (float)fabs(m_98);
    Ps21Target* z = owner->m_7c;
    z->m_64 = fTemp;
    z->v2e(a1);
}