struct StatsMenuItem { int FUN_007b39b0(); };
struct StatsMenuItemList { StatsMenuItem* FUN_00559450(); StatsMenuItem** FUN_0057cbe0(StatsMenuItem*& p); };
struct StatsMenuTile { void FUN_00700320(int,int); };
extern void __cdecl FUN_00a04200(int);
class StatsMenu { public:
 int unk00,unk04,unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24;
 StatsMenuItemList* m_pageLists[2];
 int unk30,unk34,unk38,unk3C,unk40,unk44,unk48,unk4C;
 int unk50,unk54,unk58,unk5C,unk60,unk64,unk68,unk6C,unk70,unk74,unk78,unk7C;
 StatsMenuTile* m_minusTile; StatsMenuTile* m_plusTile;
 int FUN_007dcc00(); void FUN_007af6b0();
};
void StatsMenu::FUN_007af6b0() {
    StatsMenuItem* pos;
    StatsMenuItemList* pOwner = m_pageLists[FUN_007dcc00()];
    pos = pOwner->FUN_00559450();
    bool foundPlus;
    {
        bool foundMinus = false;
        foundPlus = false;
        FUN_00a04200(0);
        while (pos && (!foundMinus || !foundPlus)) {
            switch ((*pOwner->FUN_0057cbe0(pos))->FUN_007b39b0()) {
                case -1: foundMinus = true; break;
                case 1: foundPlus = true; break;
            }
        }
        m_minusTile->FUN_00700320(0xFA3, foundMinus);
        m_plusTile->FUN_00700320(0xFA3, foundPlus);
    }
}