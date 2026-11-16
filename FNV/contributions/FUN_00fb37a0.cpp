extern "C" double __cdecl sqrt(double value);
extern const float DAT_010950a0;
extern const double DAT_01011598;
extern const float DAT_010950a4;
extern float DAT_011f3410;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb37a0
void FUN_00fb37a0()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010950a0;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f3410 = DAT_01011598 / (DAT_010950a0 * calculation.root) * DAT_010950a4;
}
