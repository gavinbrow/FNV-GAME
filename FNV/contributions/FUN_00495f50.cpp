struct SequenceRef {
    signed char* FUN_0043b1b0();
};
struct TrackEntry {
    void* controller;
    void* interpolationData;
    SequenceRef* FUN_00717e50();
    float FUN_006a7f50();
};
struct SequenceInterface : BSAnimGroupSequence {
    float FUN_00598040();
    FUN_00495f30_shell* FUN_00700300();
};
unsigned int __cdecl FUN_0044a670(int actionId);
int __cdecl FUN_00ec7ec0(signed char* sequenceData, int actionId, unsigned int trackCount);
char __cdecl FUN_00ec67aa(int character);

struct AnimationInterface : Animation {
    char FUN_00495f50(int sequenceIndex, int actionId, float* outTime);
};
char AnimationInterface::FUN_00495f50(int sequenceIndex, int actionId, float* outTime)
{
    if (outTime != 0)
        *outTime = 0.0f;

    if (pCurrentSequence[sequenceIndex] == 0 || actionId == 0)
        return 0;

    int entries;
    float tracks = static_cast<SequenceInterface*>(pCurrentSequence[sequenceIndex])->FUN_00598040();
    FUN_00495f30_shell* sequenceTime = static_cast<SequenceInterface*>(pCurrentSequence[sequenceIndex])->FUN_00700300();
    TrackEntry* key = reinterpret_cast<TrackEntry*>(sequenceTime->FUN_00495f30(&entries));
    unsigned int trackCount = FUN_0044a670(actionId);
    if (!trackCount)
        return 0;

    for (unsigned int i = 0; i < static_cast<unsigned int>(entries); ++i) {
        signed char* object = key[i].FUN_00717e50()->FUN_0043b1b0();
        if (object != 0 && FUN_00ec7ec0(object, actionId, trackCount) == 0
                && tracks <= key[i].FUN_006a7f50()) {
            if (outTime != 0)
                *outTime = key[i].FUN_006a7f50();
            return FUN_00ec67aa(object[trackCount]);
        }
    }
    return 0;
}