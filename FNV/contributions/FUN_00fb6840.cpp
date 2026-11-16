extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2c54;
extern const float DAT_010a2c58;
extern const double DAT_01011598;
extern float DAT_011f6c28;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb6840
void FUN_00fb6840()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2c54;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c28 = DAT_01011598 / (DAT_010a2c54 * calculation.root) * DAT_010a2c58;
}
