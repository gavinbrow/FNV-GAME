struct SpellListHandle {
    bool FUN_005f65d0();
    void FUN_005ae3d0();
};
struct SpellListTask {
    SpellListHandle* FUN_0048d150(TESLevSpell*& spell);
    bool FUN_0048d210(TESLevSpell* spell);
};
struct PlayerBaseData {
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
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
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
};
struct PlayerProcess : PlayerBaseData, SpellListTask {};
struct PlayerProcessAccessor { PlayerProcess* FUN_004181e0(); };
bool SpellListTask::FUN_0048d210(TESLevSpell* spell) {
    if (!spell)
        return false;
    if (this == static_cast<SpellListTask*>(reinterpret_cast<PlayerProcessAccessor*>(g_thePlayer)->FUN_004181e0()))
        return false;
    if (FUN_0048d150(spell)->FUN_005f65d0())
        return false;
    FUN_0048d150(spell)->FUN_005ae3d0();
    return true;
}