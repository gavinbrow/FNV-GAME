struct HelperAt6c { void FUN_0066b0d0(int mode); };
struct RefAt48 { void* FUN_0040f2a0(int deletionFlags); };
struct FUN_00583180_Class {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c, unk40, unk44;
    RefAt48* m_ref;
    int unk4c, unk50, unk54, unk58, unk5c, unk60, unk64, unk68;
    HelperAt6c m_container;
    void FUN_00583180();
};
void FUN_00583180_Class::FUN_00583180() {
    m_container.FUN_0066b0d0(0);
    RefAt48* node = m_ref;
    RefAt48* doomed = node;
    doomed ? doomed->FUN_0040f2a0(1) : 0;
    m_ref = 0;
}