class ImageSpaceEffectParam
{
public:
    void FUN_00414430(float first, float second, float third, float fourth);
};

extern const float DAT_0101df44;
extern const float DAT_010177e8;
extern const float DAT_010181bc;
extern ImageSpaceEffectParam DAT_011ca33c;

// @fnv 0x00f4bc30
void FUN_00f4bc30()
{
    DAT_011ca33c.FUN_00414430(
        1.0f,
        DAT_0101df44,
        DAT_010177e8,
        DAT_010181bc);
}
