struct NiPoint3 {
    float x;
    float y;
    float z;
    void __thiscall FUN_006815c0();
};
struct NonPodPoint3 {
    float x;
    float y;
    float z;
    NonPodPoint3();
};
NiPoint3* __cdecl FUN_009a8050(NiPoint3* result, void* actor);
void __cdecl FUN_009a8600(NiPoint3* result, void* target, int mode);
NonPodPoint3 __cdecl FUN_009a8660(void* target);
unsigned char __cdecl FUN_009a7670(void* actor, void* target, unsigned int flags,
                                    NiPoint3 origin, NiPoint3 direction, NonPodPoint3 offset,
                                    unsigned int mode, unsigned int category, float scale);

unsigned char __cdecl FUN_009a7580(void* actor, void* target, unsigned int flags,
                                    NiPoint3* optionalOrigin, unsigned int mode,
                                    unsigned int category, float scale)
{
    if (!actor || !target)
        return 0;
    NiPoint3 offset;
    offset.FUN_006815c0();
    if (optionalOrigin)
        offset = *optionalOrigin;
    else {
        NiPoint3 temp;
        offset = *FUN_009a8050(&temp, actor);
    }
    NiPoint3 origin;
    FUN_009a8600(&origin, target, 2);
    NonPodPoint3 direction = FUN_009a8660(target);
    return FUN_009a7670(actor, target, flags, offset, origin, direction, mode, category, scale);
}