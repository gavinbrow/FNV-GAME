struct FUN_00a57050_helper {
    NiColorInterpolator* FUN_00a57050(float startTime, float endTime);
};
struct FUN_00a3d270_helper : NiColorData {
    void FUN_00a3d270(float startTime, float endTime, NiColorData** clippedData);
};
struct FUN_00a3bef0_shell : NiColorInterpolator {
    NiColorInterpolator* FUN_00a3bef0(float startTime, float endTime);
};
NiColorInterpolator* FUN_00a3bef0_shell::FUN_00a3bef0(float startTime, float endTime)
{
    NiColorInterpolator* interpolator =
        reinterpret_cast<FUN_00a57050_helper*>(this)->FUN_00a57050(startTime, endTime);
    if (m_spColorData.m_pObject) {
        NiColorData* clippedData = 0;
        reinterpret_cast<FUN_00a3d270_helper*>(m_spColorData.m_pObject)
            ->FUN_00a3d270(startTime, endTime, &clippedData);
        interpolator->m_spColorData = clippedData;
        interpolator->m_uiLastIdx = 0;
        if (clippedData) clippedData->DecRefCount();
    }
    return interpolator;
}