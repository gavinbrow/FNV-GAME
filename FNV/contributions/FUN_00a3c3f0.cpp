extern const volatile float DAT_0109a918;

struct NiFloatInterpolatorShell_00a3c3f0 : NiFloatInterpolator {
    unsigned char FUN_00a3c3f0(unsigned int unused) const;
};

unsigned char NiFloatInterpolatorShell_00a3c3f0::FUN_00a3c3f0(unsigned int unused) const
{
    if (m_spFloatData.m_pObject)
        return 0;
    if (m_fFloatValue == DAT_0109a918)
        return 0;
    return 1;
}