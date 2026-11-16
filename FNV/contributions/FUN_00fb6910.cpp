extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2d1c;
extern const float DAT_010a2d20;
extern const double DAT_01011598;
extern float DAT_011f6c38;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb6910
void FUN_00fb6910()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2d1c;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c38 = DAT_01011598 / (DAT_010a2d1c * calculation.root) * DAT_010a2d20;
}
