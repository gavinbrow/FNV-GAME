extern "C" void* __cdecl FUN_00aa13e0(unsigned int);
struct ExtraDataOwner {
    int unk00;
    int unk04;
    int unk08;
    int m_iValue;
    void __thiscall FUN_00a7b330(NiIntegerExtraData*, unsigned int);
    NiIntegerExtraData* __thiscall FUN_00a99c80(unsigned int);
};
NiIntegerExtraData* ExtraDataOwner::FUN_00a99c80(unsigned int argument)
{
    NiIntegerExtraData* result;
    NiIntegerExtraData* allocated = (NiIntegerExtraData*)FUN_00aa13e0(16);
    if (allocated != 0) {
        ((NiExtraDataShell*)allocated)->FUN_00a7b2e0();
        *(void**)allocated = &DAT_010a0d24;
        allocated->m_iValue = 0;
        result = allocated;
    } else {
        result = 0;
    }
    FUN_00a7b330(result, argument);
    result->m_iValue = m_iValue;
    return result;
}
