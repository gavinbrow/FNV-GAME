struct ImageSpaceEffectParam
{
    float values[4];

    void FUN_00414430(float first, float second, float third, float fourth);
};

extern ImageSpaceEffectParam DAT_011ca2e8;
extern const float DAT_0101e2bc;

// @fnv 0x00f4bd00
void FUN_00f4bd00()
{
    DAT_011ca2e8.FUN_00414430(DAT_0101e2bc, DAT_0101e2bc, DAT_0101e2bc, 0.0f);
}
