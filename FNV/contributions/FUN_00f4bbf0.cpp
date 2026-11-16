class ImageSpaceEffectParam
{
public:
    void FUN_00414430(float first, float second, float third, float fourth);
};

extern const float DAT_01030ff0;
extern const float DAT_01017870;
extern const float DAT_0101df44;
extern const float DAT_01030ff4;
extern ImageSpaceEffectParam DAT_011ca2a0;

// @fnv 0x00f4bbf0
void FUN_00f4bbf0()
{
    DAT_011ca2a0.FUN_00414430(
        DAT_01030ff0,
        DAT_01017870,
        DAT_0101df44,
        DAT_01030ff4);
}
