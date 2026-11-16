struct FUN_00559450_Source {
    unsigned int __thiscall FUN_00559450();
};
struct FUN_007ca8e0_Params {
    unsigned int m_unknown00;
    unsigned int m_unknown04;
    unsigned int m_unknown08;
    FUN_007ca530_CallbackBase* callback;
};
void __cdecl FUN_007ca8e0(FUN_007ca8e0_Params* params) {
    if (FUN_00794d80(DAT_011daa38) < *(int*)((char*)DAT_011daa38 + 0x58)) {
        params->callback->FUN_000000f0(0, 0,
            ((FUN_00559450_Source*)((char*)DAT_011daa38 + 0x1d0))->FUN_00559450());
    } else {
        params->callback->FUN_000000f0(0, 0,
            ((FUN_00559450_Source*)((char*)DAT_011daa38 + 0x1cc))->FUN_00559450());
    }
}