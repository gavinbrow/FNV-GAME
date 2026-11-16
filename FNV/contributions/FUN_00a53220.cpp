// Based on unverified previous work by another contributor (2026-10-22).
struct BoolData {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
    virtual void v20(); virtual void v21(); virtual void v22();
    virtual bool IsEqual(BoolData* other);
};
struct BoolInterpolator {
    int unk00; int unk04; int unk08;
    unsigned char m_value, unk0D, unk0E, unk0F;
    BoolData* m_data;
    bool FUN_00c85800(BoolInterpolator* other);
    bool FUN_00a53220(BoolInterpolator* other);
};
bool BoolInterpolator::FUN_00a53220(BoolInterpolator* other)
{
    if (!FUN_00c85800(other))
        return false;
    if (m_value != other->m_value)
        return false;
    BoolData* data = m_data;
    if ((m_data && !other->m_data) || (!m_data && other->m_data))
        return false;
    if (m_data)
    {
        BoolData* otherData = other->m_data;
        if (!data->IsEqual(otherData))
            return false;
    }
    return true;
}
