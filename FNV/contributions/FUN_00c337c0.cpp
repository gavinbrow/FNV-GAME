
struct StateVec3 { unsigned int x, y, z; };
struct StateVec2 { unsigned int x, y; };
struct StateMatrix3 { unsigned int entries[9]; };

struct FUN_00c337c0_State {
    unsigned int unk00;
    unsigned int unk04;
    StateVec3 primary;
    StateVec2 secondary;
    StateMatrix3 transform;
    unsigned int scalar;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9c;
    unsigned int unka0;
    unsigned int unka4;
    unsigned int unka8;
    unsigned int unkac;
    unsigned int unkb0;
    unsigned int unkb4;
    unsigned int unkb8;
    unsigned int unkbc;
    unsigned int unkc0;
    unsigned int unkc4;
    unsigned int unkc8;
    unsigned int unkcc;
    unsigned int unkd0;
    unsigned int unkd4;
    unsigned int unkd8;
    unsigned int unkdc;
    unsigned int unke0;
    unsigned char dirtyE4;
    unsigned char dirtyE5;

    void FUN_00c337c0(FUN_00c337c0_State* destination, unsigned int unused);
};

void FUN_00c337c0_State::FUN_00c337c0(
    FUN_00c337c0_State* destination, unsigned int unused) {
    destination->primary = primary;
    destination->dirtyE4 = 1;
    destination->dirtyE5 = 1;

    destination->secondary = secondary;
    destination->dirtyE4 = 1;
    destination->dirtyE5 = 1;

    destination->transform = transform;
    destination->dirtyE4 = 1;
    destination->dirtyE5 = 1;

    unsigned int value = scalar;
    destination->scalar = value;
}
