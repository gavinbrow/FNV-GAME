struct NiPosDataRangeHelper : NiPosData {
    void FUN_00a49140(float startTime, float endTime, NiPosData*& result);
};
NiPoint3Interpolator* __stdcall FUN_00a57050(float startTime, float endTime);

inline void AssignPosData(NiPosData*& destination, NiPosData* nextData)
{
    NiPosData* oldData = destination;
    if (oldData != nextData) {
        if (oldData)
            oldData->DecRefCount();
        destination = nextData;
        if (nextData)
            nextData->IncRefCount();
    }
}

struct NiPoint3InterpolatorRange : NiPoint3Interpolator {
    NiPoint3Interpolator* FUN_00a497b0(float startTime, float endTime);
};

NiPoint3Interpolator* NiPoint3InterpolatorRange::FUN_00a497b0(float startTime, float endTime)
{
    NiPoint3Interpolator* result = FUN_00a57050(startTime, endTime);
    if (m_spPosData) {
        NiPosData* extractedData = 0;
        static_cast<NiPosDataRangeHelper*>(m_spPosData)->FUN_00a49140(
            startTime, endTime, extractedData);
        AssignPosData(result->m_spPosData, extractedData);
        result->m_uiLastIdx = 0;
        if (extractedData)
            extractedData->DecRefCount();
    }
    return result;
}