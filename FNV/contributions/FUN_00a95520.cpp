void* __cdecl FUN_00aa1070(unsigned int bytes);
void __cdecl FUN_00aa10f0(void* memory);

struct ScreenRectArray {
    ScreenRect* m_pBase;
    unsigned int m_uiAlloced;
    unsigned int m_uiUsed;
    void FUN_00a95520(unsigned int uiNewAlloced);
};

void ScreenRectArray::FUN_00a95520(unsigned int uiNewAlloced)
{
    if (uiNewAlloced != m_uiAlloced) {
        ScreenRect* pNew;
        if (uiNewAlloced > 0) {
            pNew = static_cast<ScreenRect*>(FUN_00aa1070(uiNewAlloced * sizeof(ScreenRect)));
            for (unsigned int i = 0; i < m_uiUsed; ++i) {
                pNew[i] = m_pBase[i];
            }
        } else {
            pNew = 0;
        }
        FUN_00aa10f0(m_pBase);
        m_pBase = pNew;
        m_uiAlloced = uiNewAlloced;
    }
}