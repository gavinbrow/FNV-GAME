struct FUN_00e69970_Class { void FUN_00e69970(void* owner); };
struct FUN_00e89ac0_Class {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34;
    void FUN_00e89ac0();
};
void FUN_00e89ac0_Class::FUN_00e89ac0() {
    if (unk34 != 0) {
        ((FUN_00e69970_Class*)unk24)->FUN_00e69970(this);
    }
}
