struct BoundReader {
    unsigned int rawValue;
    float __thiscall FUN_006a7f50();
};
struct CombatRange {
    int m_state;
    int m_owner;
    BoundReader m_lower;
    BoundReader m_upper;
    bool __thiscall FUN_009a4960(float value);
};
bool CombatRange::FUN_009a4960(float value)
{
    return m_lower.FUN_006a7f50() <= value
        && value <= m_upper.FUN_006a7f50();
}