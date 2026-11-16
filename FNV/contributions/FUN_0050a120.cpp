struct ResetState { unsigned char value; };
void __cdecl FUN_00407a90(void* destination, unsigned char reset);
void __cdecl FUN_00401080(void* destination, unsigned char reset);
void TESGrass__GRASS_DATA::FUN_0050a120()
{
    ResetState b0 = {};
    FUN_00407a90(&sDistanceFromWaterLevel, b0.value);
    ResetState c0 = {};
    FUN_00401080(&eUnderwater, c0.value);
    ResetState b2 = {};
    FUN_00401080(&fPositionRange, b2.value);
    ResetState b4 = {};
    FUN_00401080(&fHeightRange, b4.value);
    ResetState b3 = {};
    FUN_00401080(&fColorRange, b3.value);
    ResetState b1 = {};
    FUN_00401080(&fWavePeriod, b1.value);
}