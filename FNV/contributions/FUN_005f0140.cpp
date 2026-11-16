#include "h_6f17835f1bf2.h"
struct FUN_004855a0 { void M(); };
struct FUN_00485680 { void M(); };
struct B1_4fe { void ClearData(); };
bool __cdecl FUN_00401500();
void __cdecl FUN_00485990(unsigned int, void*, unsigned int);
struct FUN_005f0140_obj : TESForm {
    B1_4fe unk18;
    void FUN_005f0140();
};
void FUN_005f0140_obj::FUN_005f0140() {
    ((FUN_004855a0*)this)->M();
    if (FUN_00401500())
        unk18.ClearData();
    FUN_00485990(0x4d414e44, &unk18, 1);
    if (FUN_00401500())
        unk18.ClearData();
    ((FUN_00485680*)this)->M();
}
