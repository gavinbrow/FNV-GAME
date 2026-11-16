struct NiRTTI {
    const char* m_pcName;
    const NiRTTI* m_pkBaseRTTI;
};
extern NiRTTI DAT_012024e0;
extern void* DAT_0109b220;

struct NiParticleSystemRuntime {
    virtual void DeleteThis();
    virtual void LoadBinary();
    virtual const NiRTTI* GetRTTI();
    void* FUN_00c1b0f0(const void* pkName);
};

struct NiPSysModifierCtlrRuntime : NiPSysModifierCtlr {
    bool FUN_00c31530(NiParticleSystemRuntime* pkTarget);
};

bool NiPSysModifierCtlrRuntime::FUN_00c31530(NiParticleSystemRuntime* pkTarget)
{
    if (pkTarget != 0) {
        const NiRTTI* pkRTTI = pkTarget->GetRTTI();
        while (pkRTTI != 0) {
            if (pkRTTI == &DAT_012024e0) {
                if (m_kModifierName != DAT_0109b220 && m_pkTarget != 0) {
                    if (pkTarget->FUN_00c1b0f0(&m_kModifierName)) {
                        return true;
                    }
                }
                return false;
            }
            pkRTTI = pkRTTI->m_pkBaseRTTI;
        }
    }
    return false;
}