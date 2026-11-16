struct SolverItem {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44, unk48, unk4c, unk50, unk54, unk58, unk5c;
    int unk60, unk64;
};

void __cdecl FUN_00d6f2b0(SolverItem* item, int index, int count, int stride);

struct FUN_00d50bd0_owner {
    hkpConstraintData m_base;
    hkpBridgeAtoms m_atoms;
    hkpGenericConstraintDataScheme m_scheme;

    void FUN_00d50640(hkpGenericConstraintDataScheme* scheme, SolverItem* item, int index);
    void FUN_00d50bd0(SolverItem* item, int index);
};

void FUN_00d50bd0_owner::FUN_00d50bd0(SolverItem* item, int index) {
    FUN_00d6f2b0(item, index, item->unk64, 8);
    FUN_00d50640(&m_scheme, item, index);
}