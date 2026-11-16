extern const float DAT_01016248;

struct FloatPair
{
    float x;
    float y;

    FloatPair(float first, float second)
        : x(first), y(second)
    {
    }
};

struct FloatPairState
{
    FloatPair firstPair;
    float unknown08;
    FloatPair secondPair;
    FloatPair thirdPair;

    void FUN_00a88cd0();

    void Initialize(const FloatPair& initialFirstPair,
                    const FloatPair& initialSecondPair,
                    const FloatPair& initialThirdPair)
    {
        firstPair = initialFirstPair;
        secondPair = initialSecondPair;
        thirdPair = initialThirdPair;
        FUN_00a88cd0();
    }
};

extern FloatPairState DAT_011ab598;

// @fnv 0x00fb5f40
void FUN_00fb5f40()
{
    DAT_011ab598.Initialize(FloatPair(0.0f, 0.0f),
                           FloatPair(1.0f, 1.0f),
                           FloatPair(DAT_01016248, DAT_01016248));
}
