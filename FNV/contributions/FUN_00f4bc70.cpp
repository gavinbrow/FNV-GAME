class ImageSpaceEffectParam
{
public:
    void FUN_00414430(float first, float second, float third, float fourth);
};

extern const float DAT_0101e2bc;
extern ImageSpaceEffectParam DAT_011ca2bc;

// @fnv 0x00f4bc70
void FUN_00f4bc70()
{
    DAT_011ca2bc.FUN_00414430(1.0f, 1.0f, 1.0f, DAT_0101e2bc);
}
