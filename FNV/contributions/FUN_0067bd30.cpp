struct FUN_0067f030 : PackageLocation {
    int unk08;
    FUN_0067f030();
    ~FUN_0067f030();
    void FUN_0067f4d0(PackageLocation* pSource, int flags);
};

struct TESPackageData {
    void* unk00;
    FUN_0067f030* m_pLoc;
    TESForm* m_form;
};

struct FUN_0067bd30_shell : FUN_0067ad70_cls {
    TESForm* m_form;
    void FUN_0067bd30(BGSLoadFormBuffer* pBuffer);
};

extern const int DAT_0119bdec;
extern const int DAT_0119be60;
extern TESPackageData* __cdecl FUN_00ec43fb(BGSLoadFormBuffer* pBuffer, int arg2, const void* arg3, const void* arg4, int arg5);

void FUN_0067bd30_shell::FUN_0067bd30(BGSLoadFormBuffer* pBuffer)
{
    TESPackageData* pData = FUN_00ec43fb(pBuffer, 0, &DAT_0119bdec, &DAT_0119be60, 0);
    if (pData != 0) {
        if (m_pLoc != 0) {
            delete m_pLoc;
            m_pLoc = 0;
        }
        if (pData->m_pLoc != 0) {
            m_pLoc = new FUN_0067f030();
            ((FUN_0067f030*)m_pLoc)->FUN_0067f4d0(pData->m_pLoc, 0);
        }
        m_form = pData->m_form;
    }
}