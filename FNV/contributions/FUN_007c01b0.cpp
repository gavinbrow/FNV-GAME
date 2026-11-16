struct BGSSaveLoadGame { bool FUN_0042ce10(); };
struct ProcessLists { void FUN_00975d10(); };
struct Interface { void FUN_007010e0(int, int); };
struct Tile { void Set(int, int); };
struct MenuState
{
    int unk00, unk04, unk08, unk0C, unk10, unk14, unk18, unk1C;
    int unk20, unk24, unk28, unk2C, unk30, unk34, unk38, unk3C;
    int unk40;
    char unk44;
    bool active;
    Tile* FUN_00726070();
    void FUN_00a1d910();
};
extern BGSSaveLoadGame* g_BGSSaveLoadGame;
extern ProcessLists DAT_011e0e80;
extern Interface* DAT_011d8804;
extern MenuState* DAT_011da920;

void FUN_007c01b0()
{
    if (DAT_011da920)
    {
        if (!g_BGSSaveLoadGame->FUN_0042ce10())
            DAT_011e0e80.FUN_00975d10();
        if (DAT_011da920->active)
            DAT_011d8804->FUN_007010e0(0, 0);
        DAT_011da920->FUN_00726070()->Set(0x1772, 1);
        DAT_011da920->FUN_00a1d910();
    }
}
