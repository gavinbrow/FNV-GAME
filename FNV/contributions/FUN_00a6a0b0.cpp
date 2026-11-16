extern int DAT_0109c514;
void __fastcall FUN_00a6a0b0(NiTexturingProperty* pThis) {
    *reinterpret_cast<void**>(pThis) = &DAT_0109c514;
    for (unsigned int i = 0; i < pThis->m_kMaps.m_usSize; ++i) {
        delete pThis->m_kMaps.m_pBase[i];
    }
    if (pThis->m_pkShaderMaps) {
        for (unsigned int i = 0; i < pThis->m_pkShaderMaps->m_usSize; ++i) {
            delete pThis->m_pkShaderMaps->m_pBase[i];
        }
        delete pThis->m_pkShaderMaps;
    }
    *reinterpret_cast<void**>(&pThis->m_kMaps) = &DAT_0109c394;
    _NiFreeAlias(pThis->m_kMaps.m_pBase);
    pThis->NiProperty::~NiProperty();
}