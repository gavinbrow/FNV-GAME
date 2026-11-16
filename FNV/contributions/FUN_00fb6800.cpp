extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2c54;
extern const float DAT_010a2c58;
extern float DAT_011f6c2c;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb6800
void FUN_00fb6800()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2c54;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c2c = DAT_010a2c58 / calculation.root;
}
