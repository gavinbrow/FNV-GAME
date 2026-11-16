extern int DAT_011daf74;
struct MenuBase {
    virtual ~MenuBase();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
};
struct TraitEntries {
    ~TraitEntries();
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
};
struct SelectionState {
    ~SelectionState();
};
struct FUN_007e6910 : MenuBase {
    TraitEntries entries;
    SelectionState selection;
    virtual ~FUN_007e6910();
};
FUN_007e6910::~FUN_007e6910() {
    DAT_011daf74 = 0;
}