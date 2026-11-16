struct NiBaseEqualityView { unsigned char FUN_00c85800(const NiObject* other); };
struct NiFloatDataEqualityView {
    virtual void ScalarDeletingDestructor(); virtual void DeleteThis();
    virtual void LoadBinary(); virtual void GetRTTI(); virtual void CreateClone();
    virtual void LinkObject(); virtual void RegisterStreamables(); virtual void SaveBinary();
    virtual void GetViewerStrings(); virtual void AsNiNode(); virtual void AsNiAVObject();
    virtual void AsNiGeometry(); virtual void AsNiTriBasedGeom(); virtual void AsNiTriShape();
    virtual void AsNiTriStrips(); virtual void AsNiProperty(); virtual void AsNiTimeController();
    virtual void AsNiTexture(); virtual void AsNiSourceTexture(); virtual void AsNiPixelData();
    virtual void IsKindOf(); virtual void IsExactKindOf(); virtual void IsDerivedKindOf();
    virtual bool IsEqual(const NiFloatData* other);
};
struct NiFloatInterpolatorEquality : NiFloatInterpolator {
    bool FUN_00a3c5e0(const NiObject* otherObject);
};
bool NiFloatInterpolatorEquality::FUN_00a3c5e0(const NiObject* otherObject) {
    if (!reinterpret_cast<NiBaseEqualityView*>(this)->FUN_00c85800(otherObject))
        return false;
    const NiFloatInterpolator* other = static_cast<const NiFloatInterpolator*>(otherObject);
    if (m_fFloatValue != other->m_fFloatValue)
        return false;
    if ((m_spFloatData.m_pObject && !other->m_spFloatData.m_pObject) ||
        (!m_spFloatData.m_pObject && other->m_spFloatData.m_pObject))
        return false;
    if (m_spFloatData.m_pObject) {
        NiFloatDataEqualityView& data = *reinterpret_cast<NiFloatDataEqualityView*>(m_spFloatData.m_pObject);
        NiFloatData* otherData = other->m_spFloatData.m_pObject;
        if (!data.IsEqual(otherData))
            return false;
    }
    return true;
}