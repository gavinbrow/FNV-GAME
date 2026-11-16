struct MatchData {
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
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int value84;
};
struct MatchObject {
    int unk00;
    int unk04;
    MatchData* data;
    bool __thiscall FUN_00c84dc0(MatchObject* rhs);
    bool __thiscall FUN_00ca54f0(MatchObject* rhs);
};
bool __thiscall MatchObject::FUN_00ca54f0(MatchObject* rhs) {
    bool result = FUN_00c84dc0(rhs);
    if (result) {
        MatchData* right = rhs ? rhs->data : 0;
        MatchData* left = this ? this->data : 0;
        result = left->value84 == right->value84;
    }
    return result;
}
