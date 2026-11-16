struct StrArr {
    void* m_pVtbl;
    char** m_pBase;
    unsigned short m_usMaxSize;
    unsigned short m_usSize;
    unsigned short m_usESize;
    unsigned short m_usGrowBy;
    void SetSize(unsigned int uiMaxSize);
    void SetAt(unsigned int uiIndex, char*& pcElement);
    unsigned int Add(char* pcElement) {
        unsigned int uiIndex = m_usSize;
        if (uiIndex >= m_usMaxSize)
            SetSize(uiIndex + m_usGrowBy);
        SetAt(uiIndex, pcElement);
        return uiIndex;
    }
};
struct NiPoint3Viewer { float x, y, z; char* FUN_00a59af0(const char* pcPrefix); };
char* FUN_00a7d330(char* pcText);
struct NiCollisionModel {
    virtual void Unk_00(); virtual void Unk_01(); virtual void Unk_02(); virtual void Unk_03();
    virtual void Unk_04(); virtual void Unk_05(); virtual void Unk_06(); virtual void Unk_07();
    virtual void Unk_08(); virtual void Unk_09(); virtual void Unk_0A();
    virtual void GetViewerStrings(const char* pcPrefix, StrArr* pkStrings);
};
struct FUN_00a81160_base {
    void FUN_00a81160(StrArr* pkStrings);
};
struct FUN_00ead8d0_shell : FUN_00a81160_base {
    int unk00;
    int unk04;
    int unk08;
    NiPoint3Viewer m_kLocalVelocity;
    NiPoint3Viewer m_kWorldVelocity;
    unsigned int m_ePropagationMode;
    unsigned int m_eCollisionMode;
    NiCollisionModel* m_pkModelABV;
    char* FUN_00eacfd0(const char* pcPrefix, unsigned int eMode);
    char* FUN_00eacef0(const char* pcPrefix, unsigned int eMode);
    void FUN_00ead8d0(StrArr* pkStrings);
};

void FUN_00ead8d0_shell::FUN_00ead8d0(StrArr* pkStrings) {
    FUN_00a81160(pkStrings);
    pkStrings->Add(FUN_00a7d330((char*)g_0126fab4));
    unsigned int propagationMode = m_ePropagationMode;
    pkStrings->Add(FUN_00eacfd0("m_ePropagationMode", propagationMode));
    unsigned int collisionMode = m_eCollisionMode;
    pkStrings->Add(FUN_00eacef0("m_eCollisionMode", collisionMode));
    if (m_pkModelABV)
        m_pkModelABV->GetViewerStrings("m_pkModelABV->Type", pkStrings);
    pkStrings->Add(m_kLocalVelocity.FUN_00a59af0("m_kLocalVelocity"));
    pkStrings->Add(m_kWorldVelocity.FUN_00a59af0("m_kWorldVelocity"));
}
