struct DetectionSetting {
    SETTING_VALUE* FUN_00403e20();
};
extern DetectionSetting g_011d0bb4;
extern DetectionSetting g_011d04b4;
struct DetectionActor : public MobileObject {
    virtual void Unk_C1();
    virtual void Unk_C2();
    virtual void Unk_C3();
    virtual void Unk_C4();
    virtual void Unk_C5();
    virtual void Unk_C6();
    virtual void Unk_C7();
    virtual void Unk_C8();
    virtual void Unk_C9();
    virtual void Unk_CA();
    virtual void Unk_CB();
    virtual void Unk_CC();
    virtual void Unk_CD();
    virtual void Unk_CE();
    virtual void Unk_CF();
    virtual void Unk_D0();
    virtual int FUN_D1(PlayerCharacter*, bool);
    bool FUN_00440da0();
    BaseProcess* FUN_008d8520();
    bool FUN_008bc700(PlayerCharacter*);
    bool FUN_008b06d0(PlayerCharacter*, bool, unsigned int*, bool);
};
struct DetectionProcessArray {
    unsigned int FUN_005be5c0(int);
};
struct DetectionList : public ProcessLists {
    bool FUN_009764a0(bool differentDistance);
};
bool DetectionList::FUN_009764a0(bool differentDistance) {
    float threshold3 = g_011d0bb4.FUN_00403e20()->f;
    bool found7 = false;
    if (differentDistance) {
        threshold3 = g_011d04b4.FUN_00403e20()->f;
    }
    float distance8 = 0.0f;
    DetectionActor* actor = 0;
    unsigned int index2 = 0;
    for (; !found7 && index2 < reinterpret_cast<DetectionProcessArray*>(&MobProcessArray)->FUN_005be5c0(0); ++index2) {
        actor = reinterpret_cast<DetectionActor*>(MobProcessArray.GetItem(index2));
        DetectionActor* current = 0;
        if (actor && actor->IsActor()) {
            current = actor;
        }
        if (current && current != reinterpret_cast<DetectionActor*>(pPlayer) && !current->IsDead(false) && !current->FUN_00440da0()) {
            if (current->FUN_008d8520() && current->FUN_008d8520()->GetCommandingActor()) {
                current = reinterpret_cast<DetectionActor*>(current->FUN_008d8520()->GetCommandingActor());
            }
            distance8 = reinterpret_cast<FUN_00973de0_player*>(pPlayer)->GetDistanceFromReference(current, false, false);
            if (distance8 <= threshold3) {
                int result = current->FUN_D1(pPlayer, false);
                unsigned int state2 = 0;
                if (current->FUN_008bc700(pPlayer)) {
                    found7 = true;
                } else if (current->FUN_008b06d0(pPlayer, false, &state2, false)) {
                    found7 = true;
                }
            }
        }
    }
    return found7;
}
