struct RadiationTile {
    double FUN_00a011b0(int trait);
    void FUN_00a012d0(int trait, float value, int propagate);
    void FUN_00700320(int trait, int enabled);
};
struct RandomGenerator {
    unsigned int FUN_00825c00();
};
extern RandomGenerator g_011f6394;
extern const double DAT_01073490;
void HUDMainMenuS::FUN_007737c0(float afDrinkinRads, float afStandinRads)
{
    float totalRads = afDrinkinRads + afStandinRads;
    if (afDrinkinRads > _gModifierZero) {
        reinterpret_cast<RadiationTile*>(pme->pTiles[19])->FUN_00a012d0(
            0x100a, (float)((double)g_011f6394.FUN_00825c00() + DAT_01073490), 1);
        reinterpret_cast<RadiationTile*>(pme->pTiles[19])->FUN_00a012d0(0x1009, totalRads, 1);
        reinterpret_cast<RadiationTile*>(pme->pTiles[19])->FUN_00700320(0x100b, 1);
    } else if (afStandinRads > _gModifierZero) {
        if (reinterpret_cast<RadiationTile*>(pme->pTiles[19])->FUN_00a011b0(0x100a)
            <= (double)g_011f6394.FUN_00825c00()) {
            reinterpret_cast<RadiationTile*>(pme->pTiles[19])->FUN_00a012d0(0x1009, totalRads, 1);
        }
    }
}