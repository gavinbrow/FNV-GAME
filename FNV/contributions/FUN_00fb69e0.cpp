extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2d34;
extern const double DAT_01011598;
extern const float DAT_010a2d38;
extern float DAT_011f6c48;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb69e0
void FUN_00fb69e0()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2d34;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c48 = DAT_01011598 / (DAT_010a2d34 * calculation.root) * DAT_010a2d38;
}
