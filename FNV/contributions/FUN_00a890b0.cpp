struct NiFloatsExtraData_compare : NiFloatsExtraData {
    bool __thiscall FUN_00a890b0(const NiFloatsExtraData* pOther);
};
bool __thiscall NiFloatsExtraData_compare::FUN_00a890b0(const NiFloatsExtraData* pOther)
{
    if (!pOther)
        return false;
    if (m_uiSize != pOther->m_uiSize)
        return false;

    if ((m_pfValue != 0 && pOther->m_pfValue == 0) ||
        (m_pfValue == 0 && pOther->m_pfValue != 0))
        return false;

    if (m_pfValue) {
        for (unsigned int i = 0; i < m_uiSize; ++i) {
            if (m_pfValue[i] != pOther->m_pfValue[i])
                return false;
        }
    }
    return true;
}