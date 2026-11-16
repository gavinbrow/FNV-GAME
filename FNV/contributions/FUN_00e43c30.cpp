struct FUN_00e43c30_arg1
{
    char pad_00[0x10];
};
struct FUN_00e43c30_state
{
    char pad_00[0x0d];
    unsigned char m_reverse;
    signed char m_currentGear;
};
struct FUN_00e43c30_class
{
    char pad_00[0x10];
    float m_fPrimaryRatio;
    float m_fClutchDelay;
    float m_fReverseRatio;
    float* m_pfGearRatios;

    float FUN_00e43c30(FUN_00e43c30_arg1* pUnused, FUN_00e43c30_state* pState);
};

float FUN_00e43c30_class::FUN_00e43c30(FUN_00e43c30_arg1* pUnused, FUN_00e43c30_state* pState)
{
    if (pState->m_reverse)
    {
        float fRatio = -m_fReverseRatio;
        float fResult = m_fPrimaryRatio * *(volatile const float*)&fRatio;
        return fResult;
    }
    float fRatio = m_pfGearRatios[pState->m_currentGear];
    float fResult = m_fPrimaryRatio * *(volatile const float*)&fRatio;
    return fResult;
}
