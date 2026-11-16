class ImageSpaceEffectParam
{
public:
    void FUN_00414430(float, float, float, float);
};

extern ImageSpaceEffectParam DAT_011c3afc;
extern const float DAT_01016248;

// @fnv 0x00f37ba0
void FUN_00f37ba0()
{
    DAT_011c3afc.FUN_00414430(0.0f, 1.0f, 0.0f, DAT_01016248);
}
