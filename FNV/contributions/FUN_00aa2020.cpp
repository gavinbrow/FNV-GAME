#include "h_74712c1d3c73.h"

struct FUN_00aa2020_Impl {
    virtual void FUN_00aa2020_00();
    virtual void FUN_00aa2020_01();
    virtual void FUN_00aa2020_02();
    virtual void FUN_00aa2020_03();
    virtual void FUN_00aa2020_04();
    virtual void FUN_00aa2020_05();
    virtual void FUN_00aa2020_06();
    virtual void FUN_00aa2020_07();
};

struct FUN_00aa2020_Holder {
    FUN_00aa2020_Impl* m_pImpl;
};

struct FUN_00aa2020_Allocator {
    FUN_00aa2020_Holder* FUN_00aa3e40(int size);
};

struct FUN_00aa2020_Source {
    FUN_00aa2020_Impl* FUN_009fd0f0();
};

extern FUN_00aa2020_Allocator DAT_011f6238;
extern FUN_00aa2020_Source* DAT_011f6118;
extern FUN_00aa2020_Holder* DAT_011f6080;

extern "C" void __cdecl FUN_00aa2020()
{
    DAT_011f6080 = DAT_011f6238.FUN_00aa3e40(4);
    DAT_011f6080->m_pImpl = DAT_011f6118->FUN_009fd0f0();
    DAT_011f6080->m_pImpl->FUN_00aa2020_07();
}