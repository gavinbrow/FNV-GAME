extern const double DAT_01012060;
extern const double DAT_01012070;
void* __cdecl FUN_004af350();

struct DecalEffect {
    float FUN_00598040();
    void FUN_0068c9f0(float value);
};
struct DecalTarget {
    void FUN_004ee560(void* effect);
};
struct DecalState {
    DecalEffect* FUN_00a59d30(void* texture);
    DecalTarget* FUN_009611e0();
};
struct DecalRef {
    DecalState* FUN_00559450();
};
struct DecalHost {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    DecalRef decalRef;
    bool FUN_006828a0(float alpha);
    double FUN_00621b00();
    double FUN_00488d50();
    bool FUN_0068c8e0(float alpha);
};
bool DecalHost::FUN_0068c8e0(float alpha) {
    bool changed = FUN_006828a0(alpha);
    DecalTarget* pTarget;
    if (!changed && decalRef.FUN_00559450()) {
        float elapsed = (float)(FUN_00621b00() - FUN_00488d50());
        float intensity;
        if (elapsed >= DAT_01012060 && elapsed <= DAT_01012070) {
            intensity = (float)((1.0 - elapsed) / DAT_01012070);
            DecalEffect* pCandidate = decalRef.FUN_00559450()->FUN_00a59d30(FUN_004af350());
            DecalEffect* pEffect = pCandidate;
            if (pEffect && pEffect->FUN_00598040() != intensity)
                pEffect->FUN_0068c9f0(intensity);
            return true;
        }
        pTarget = decalRef.FUN_00559450()->FUN_009611e0();
        if (pTarget)
            pTarget->FUN_004ee560(this);
    }
    return changed;
}