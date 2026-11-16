#include "h_17f0267c5f44.h"

struct FUN_00c32450_target
{
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
    virtual void v30();
    virtual void v31();
    virtual void v32();
    virtual void v33();
    virtual void v34();
    virtual unsigned int FUN_00c32450_target_call(
        float param1,
        unsigned int param2,
        unsigned int param3,
        unsigned int param4);
};

struct FUN_00c32450_shell : public NiPSysCollider
{
    unsigned int FUN_00c32450(
        float param1,
        unsigned int param2,
        unsigned int param3,
        unsigned int param4);
};

unsigned int FUN_00c32450_shell::FUN_00c32450(
    float param1,
    unsigned int param2,
    unsigned int param3,
    unsigned int param4)
{
    FUN_00c32450_target* target =
        reinterpret_cast<FUN_00c32450_target*>(m_spNext.m_pObject);

    if (target)
    {
        unsigned int result = target->FUN_00c32450_target_call(
            param1,
            param2,
            param3,
            param4);

        if (result)
            return result;
    }

    return 0;
}