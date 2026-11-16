#include "h_74712c1d3c73.h"

struct FUN_00c65180_VTable
{
    virtual void FUN_00c65180_v0();
    virtual void FUN_00c65180_v1();
    virtual void FUN_00c65180_v2();
    virtual void FUN_00c65180_v3();
    virtual void FUN_00c65180_v4();
    virtual void FUN_00c65180_v5();
    virtual void FUN_00c65180_v6();
    virtual void FUN_00c65180_v7();
    virtual void FUN_00c65180_v8(void* p);
};

struct FUN_00c65180_Class
{
    unsigned char __thiscall FUN_00a7b290(FUN_00c65180_VTable* p);

    void* m_0;
    void* m_4;
    void* m_8;
    void* m_c;
    void** m_10;
    int m_14;
    unsigned short m_18;

    unsigned char __thiscall FUN_00c65180(FUN_00c65180_VTable* p);
};

unsigned char __thiscall FUN_00c65180_Class::FUN_00c65180(FUN_00c65180_VTable* p)
{
    unsigned char result = FUN_00a7b290(p);

    if (result)
    {
        unsigned int count = m_18;

        for (unsigned int i = 0; i < count; ++i)
        {
            void* item = m_10[i];

            p->FUN_00c65180_v8(item);
            p->FUN_00c65180_v8(static_cast<char*>(item) + 4);
        }
    }

    return result;
}