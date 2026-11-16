struct NiTriBasedGeom;
struct TESObjectREFR;
struct TES;
struct FUN_00559450_h { NiTriBasedGeom* __thiscall FUN_00559450(); };
struct Col_0043b4f0 { int __thiscall FUN_0043b540(); };
struct GlobalObject_008c71b0 {
    int m_value;
    GlobalObject_008c71b0(int value);
};
struct FUN_00457880_Class { unsigned int __thiscall FUN_00457880(int value); };
extern TES* g_TES;
extern unsigned int __cdecl FUN_004a3a40(TESObjectREFR* value);
extern int __cdecl FUN_004a8f20(int first, int second);
extern int __cdecl FUN_00c80020(unsigned int value);
unsigned int __cdecl FUN_0062b150(unsigned int param_1, unsigned int param_2)
{
    int iStack_8;
    unsigned int uStack_c;
    iStack_8 = FUN_004a3a40(reinterpret_cast<TESObjectREFR*>(reinterpret_cast<FUN_00559450_h*>(param_1)->FUN_00559450()));
    if (iStack_8 == 0) {
        GlobalObject_008c71b0 local(reinterpret_cast<Col_0043b4f0*>(reinterpret_cast<FUN_00624020_Class*>(param_1)->FUN_00624020())->FUN_0043b540());
        if (reinterpret_cast<H0043b4d0*>(&local)->FUN_0043b4d0() == 0x11) {
            uStack_c = reinterpret_cast<FUN_00457880_Class*>(g_TES)->FUN_00457880(param_2);
        } else {
            uStack_c = FUN_00c80020(param_1);
        }
    } else {
        uStack_c = FUN_004a8f20(reinterpret_cast<FUN_006205a0_Class*>(iStack_8)->FUN_006205a0(), 0x23);
    }
    return uStack_c;
}