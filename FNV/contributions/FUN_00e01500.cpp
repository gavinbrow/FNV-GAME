struct State {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int FUN_00e01500();
};
int State::FUN_00e01500() {
    return unk2C & ~1;
}
