#include "h_95da0502e9cd.h"
extern const double DAT_01012060;

struct FUN_0064ac30_shell : public BSFaceGenAnimationData {
    void FUN_0064ac30(float* quantities, float time);
};

struct FUN_0064ed60_shell {
    void FUN_0064ed60(NiTPointerList<BSFaceGenKeyframe*>* list);
};

void FUN_0064ac30_shell::FUN_0064ac30(float* quantities, float time)
{
    BSFaceGenKeyframeMultiple keyframe(CUSTOM, 1);
    if (dead || quantities == 0 || time < DAT_01012060) {
        return;
    }

    keyframe.SetTime(time);
    for (unsigned int i = 0; i < 1; ++i) {
        keyframe.FUN_0064a4d0(i, quantities[i]);
    }
    reinterpret_cast<FUN_0064ed60_shell*>(&keyframe)->FUN_0064ed60(
        reinterpret_cast<NiTPointerList<BSFaceGenKeyframe*>*>(
            reinterpret_cast<char*>(this) + 0xf0));
}