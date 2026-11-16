struct ImageSpaceEffectParam
{
    float first;
    float second;
    float third;
    float fourth;

    void FUN_00414430(float firstValue, float secondValue, float thirdValue, float fourthValue);
};

extern ImageSpaceEffectParam DAT_011ca3f8;
extern const float DAT_0101622c;

// @fnv 0x00f4bcd0
void FUN_00f4bcd0()
{
    DAT_011ca3f8.FUN_00414430(0.0f, 0.0f, 0.0f, DAT_0101622c);
}
