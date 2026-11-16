struct FUN_007e8470_shell
{
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
    Tile* pTiles[18];
    int unk70;
    float m_fRatio;
    int m_CurrentlyCheckedTile;
    void __thiscall FUN_007e8470(int aiID, bool abForce);
};

struct Tile
{
    void __thiscall FUN_00700320(int, int);
    float __thiscall FUN_00a011b0(int);
};

struct FUN_004b7210_result
{
    bool __thiscall FUN_00755680();
};

bool __cdecl FUN_004b71d0();
void* __cdecl FUN_00a09030(int);
extern double const _DAT_01012060;

void __thiscall FUN_007e8470_shell::FUN_007e8470(int aiID, bool abForce)
{
    Tile* settings;
    float selectedValue;
    float settingValue;
    float initialSetting;

    if (!abForce && m_CurrentlyCheckedTile == aiID)
        return;

    if (m_CurrentlyCheckedTile != -1 &&
        pTiles[m_CurrentlyCheckedTile] != 0)
    {
        pTiles[m_CurrentlyCheckedTile]->FUN_00700320(0x1005, 0);
    }

    m_CurrentlyCheckedTile = aiID;

    if (m_CurrentlyCheckedTile != -1)
    {
        if (pTiles[m_CurrentlyCheckedTile] != 0)
        {
            pTiles[m_CurrentlyCheckedTile]->FUN_00700320(0x1005, 1);
        }

        FUN_004b7210();
        if (FUN_004b71d0() &&
            !reinterpret_cast<FUN_004b7210_result*>(FUN_004b7210())->FUN_00755680())
        {
            settings = reinterpret_cast<Tile*>(FUN_00a09030(0x434));
            if (settings != 0 && pTiles[15] != 0)
            {
                settingValue = settings->FUN_00a011b0(0x1008);
                initialSetting = pTiles[15]->FUN_00a011b0(0xfb0);
                selectedValue = pTiles[m_CurrentlyCheckedTile]->FUN_00a011b0(0xfa2);
                if (initialSetting != _DAT_01012060)
                {
                    m_fRatio = selectedValue / initialSetting;
                }
                else
                {
                    m_fRatio = 0.0f;
                }
            }
        }
    }
}